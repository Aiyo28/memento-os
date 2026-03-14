# 002 — Safety Hooks

**Status:** Solved
**Score impact:** Auto-capture reliability from 3/10 → 5/10 (indirect — less time on recovery = more time for capture)
**Date:** 2026-03-10
**Core goal:** Memory loss prevention

## The Problem

Three incidents in one week:

1. **Secret leak:** The agent wrote a hardcoded API key into a source file during a rapid prototyping session. The key was committed and pushed before anyone noticed. Required key rotation and git history rewriting.

2. **Destructive delete:** During a cleanup task, the agent ran `rm -rf .` instead of `rm -rf ./dist`. The entire working directory was deleted. Recovery required cloning from remote and replaying uncommitted changes from memory (several were lost).

3. **Force push:** The agent resolved a merge conflict by force-pushing to main, overwriting a teammate's commits. Required manual reconstruction of the lost work.

Each incident cost 1-3 hours of recovery time. More importantly, each one destroyed work — the very problem a memory system is supposed to prevent.

Adding rules to CLAUDE.md ("never commit secrets", "never force push") reduced incidents but didn't eliminate them. The agent followed the rules ~80% of the time. For destructive operations, 80% reliability means you get burned roughly once a week.

## What We Tried

**Approach 1: CLAUDE.md rules.** "Never hardcode API keys. Never use rm -rf without confirmation. Never force push." The agent followed these most of the time, but LLMs are probabilistic — instructions aren't guarantees. One distracted session and the rule is forgotten.

**Approach 2: Post-commit scanning.** A git hook that scans commits for secrets after they're made. Better than nothing, but the damage is already done — the secret is in git history. Cleaning it up is expensive.

## What Worked

Three `PreToolUse` shell hooks that intercept dangerous operations *before* they execute. The agent can attempt the operation, but the hook blocks it and explains why.

### Hook 1: Secret Detection (Write/Edit)

Scans content being written for known secret patterns:

- API key prefixes (`sk-`, `AKIA`, `ghp_`, `xoxb-`, etc.) with 20+ character length
- PEM private key headers
- AWS secret access keys (40-char base64 pattern)
- Generic credential assignments (`password`/`token`/`secret` = `"value"`)

Includes false-positive prevention:

- Skips placeholders (`"your-api-key-here"`, `"changeme"`, `"xxx..."`)
- Skips environment variable references (`process.env.X`, `os.environ`)
- Skips values shorter than 8 characters

```bash
#!/usr/bin/env bash
# PreToolUse hook — matcher: Write|Edit
# Scans for hardcoded secrets in file writes

INPUT=$(cat)
TOOL_NAME=$(echo "$INPUT" | jq -r '.tool_name // empty')

if [[ "$TOOL_NAME" == "Edit" ]]; then
  TEXT=$(echo "$INPUT" | jq -r '.tool_input.new_string // empty')
elif [[ "$TOOL_NAME" == "Write" ]]; then
  TEXT=$(echo "$INPUT" | jq -r '.tool_input.content // empty')
else
  exit 0
fi

[[ -z "$TEXT" ]] && exit 0

# Check for known API key prefixes (20+ chars)
while IFS= read -r match; do
  [[ -z "$match" ]] && continue
  # Skip placeholders
  [[ ${#match} -lt 8 ]] && continue
  lower=$(echo "$match" | tr '[:upper:]' '[:lower:]')
  [[ "$lower" =~ ^(your|fake|test|example|dummy) ]] && continue
  echo "BLOCKED: Detected probable API key." >&2
  echo "Use environment variables instead of hardcoding keys." >&2
  exit 2
done < <(echo "$TEXT" | grep -oE '(sk-[a-zA-Z0-9_-]{20,}|AKIA[0-9A-Z]{16}|ghp_[a-zA-Z0-9]{36})' 2>/dev/null || true)

# Check for PEM private keys
if echo "$TEXT" | grep -qE 'BEGIN.*PRIVATE KEY'; then
  echo "BLOCKED: Detected private key." >&2
  exit 2
fi

exit 0
```

### Hook 2: Destructive Commands (Bash)

Blocks catastrophic shell operations:

- `rm -rf` targeting root, home, or current directory (allows specific targets like `./dist`)
- `DROP TABLE` / `TRUNCATE TABLE`
- `chmod 777`
- `killall` on system processes
- `dd` to raw disk devices

### Hook 3: Git Safety (Bash)

Blocks dangerous git operations:

- Force push (`--force`, `--force-with-lease`)
- Hard reset (`reset --hard`)
- Discarding all changes (`checkout -- .`)
- Force-deleting branches (`branch -D`)
- Staging sensitive files (`.env`, `*.pem`, `credentials.json`)

Each hook outputs a clear explanation of what was blocked and suggests a safer alternative.

## Why It Works

Hooks are deterministic. They don't rely on LLM judgment or attention. The check happens at the tool execution layer — below the model's reasoning, above the actual file system operation. This means:

- The agent can *try* dangerous operations (it doesn't need to know the rules)
- The hook *always* catches them (no probability, no "forgot the rule")
- The user is prompted to approve or deny (human stays in the loop for genuine needs)

This is defense in depth: CLAUDE.md rules reduce the frequency of dangerous attempts, hooks catch the ones that slip through.

## Verification

- **Zero secret leaks** since hook deployment (8+ weeks)
- **Zero destructive deletes** — agent has been blocked 12+ times from operations that would have required recovery
- **Zero accidental force pushes**
- Hook false-positive rate: ~2% (placeholder values occasionally trigger secret detection). Acceptable — a false positive costs 5 seconds of user approval, a false negative costs hours.

## Open Questions

- Should hooks log blocked attempts for audit purposes?
- Is there a way to make hooks adaptive — learning from approved overrides to reduce false positives?
- PostToolUse hooks could verify results (e.g., confirm a file was written correctly). Worth exploring for write verification.
