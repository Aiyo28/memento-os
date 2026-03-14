# Quickstart: Set Up Agent Memory in 15 Minutes

A practical setup guide for Claude Code. No theory — for the reasoning behind each piece, see the evolution entries.

**Time to complete:** 10–15 minutes
**Result:** Claude Code with persistent memory, safety hooks, and 4 skills

---

## Prerequisites

- **Claude Code** installed and working (`claude --version`)
- **git** installed
- **Obsidian** (optional — needed for Step 4 only)

---

## Step 1: Set Up Claude Code Memory

Claude Code loads `~/.claude/CLAUDE.md` at the start of every conversation. This file is your agent's standing instructions.

**Copy the example CLAUDE.md:**

```bash
# If you don't have a CLAUDE.md yet:
cp starter/claude-code/CLAUDE.md.example ~/.claude/CLAUDE.md

# If you already have one, merge manually — open both files and add the sections you want
```

**Create the memory directory for your first project:**

```bash
mkdir -p ~/.claude/projects/my-project/memory/
cp starter/claude-code/memory/MEMORY.md.example ~/.claude/projects/my-project/memory/MEMORY.md
```

Replace `my-project` with your actual project name (use the same slug throughout).

**Edit `~/.claude/CLAUDE.md`** and update the vault path and project registry to match your setup. At minimum, update:

```
Developer vault at ~/your-path/knowledge-vault/
```

---

## Step 2: Install Safety Hooks

Three hooks prevent the most common agent mistakes: leaking secrets, running destructive commands, and force-pushing.

**Copy hook files:**

```bash
mkdir -p ~/.claude/hooks/
cp starter/claude-code/hooks/secret-detect.sh ~/.claude/hooks/
cp starter/claude-code/hooks/destructive-command.sh ~/.claude/hooks/
cp starter/claude-code/hooks/git-safety.sh ~/.claude/hooks/
chmod +x ~/.claude/hooks/secret-detect.sh
chmod +x ~/.claude/hooks/destructive-command.sh
chmod +x ~/.claude/hooks/git-safety.sh
```

**Register hooks in Claude Code settings:**

Open `~/.claude/settings.json` (create it if it doesn't exist) and add or merge:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [{ "type": "command", "command": "~/.claude/hooks/secret-detect.sh" }]
      },
      {
        "matcher": "Bash",
        "hooks": [
          { "type": "command", "command": "~/.claude/hooks/destructive-command.sh" },
          { "type": "command", "command": "~/.claude/hooks/git-safety.sh" }
        ]
      }
    ]
  }
}
```

If `settings.json` already exists, merge the `hooks` key — don't overwrite other settings.

---

## Step 3: Install Skills

Skills are slash commands that give the agent specialized workflows. Each one is a folder with a `SKILL.md` file.

**Copy skill folders:**

```bash
mkdir -p ~/.claude/skills/
cp -r starter/claude-code/skills/knowledge ~/.claude/skills/
cp -r starter/claude-code/skills/session-complete ~/.claude/skills/
cp -r starter/claude-code/skills/process-inbox ~/.claude/skills/
cp -r starter/claude-code/skills/strategic-compact ~/.claude/skills/
```

**The 4 skills and their triggers:**

| Skill | Trigger phrases | What it does |
|-------|----------------|--------------|
| `/knowledge` | "research this", "extract from", given a URL/file | Extracts structured knowledge. `--quick` for inline context (4 lines), `--deep` to save to vault. |
| `/session-complete` | "I'm done", "wrap up", "end of session" | Updates NEXT.md, appends to session log, records decisions, optionally extracts patterns. |
| `/process-inbox` | "process inbox", "clean inbox", "sort inbox" | Routes raw captures from `_inbox/` to proper vault locations with correct frontmatter. |
| `/strategic-compact` | "compact context", "context is getting long" | Guides `/compact` timing — suggests when to compact based on phase transitions, not context size. |

---

## Step 4: Set Up Knowledge Vault (Optional)

Skip this step if you don't use Obsidian. The memory system works without it.

**Copy the vault starter files into your Obsidian vault:**

```bash
# Adjust the path to your actual Obsidian vault location
VAULT=~/Documents/my-obsidian-vault

cp -r starter/obsidian-vault/_inbox $VAULT/
cp -r starter/obsidian-vault/_meta $VAULT/
cp -r starter/obsidian-vault/Knowledge $VAULT/
cp -r starter/obsidian-vault/Projects $VAULT/
cp starter/obsidian-vault/CLAUDE.md.example $VAULT/CLAUDE.md
```

**Create your first project context:**

```bash
mkdir -p "$VAULT/Projects/my-project"
cp "starter/obsidian-vault/Projects/_example-project/_context.md" \
   "$VAULT/Projects/my-project/_context.md"
```

Edit `$VAULT/Projects/my-project/_context.md` and fill in your project details.

**Update `~/.claude/CLAUDE.md`** with the correct vault path:

```
Developer vault at ~/Documents/my-obsidian-vault/
```

---

## Step 5: Create Your First NEXT.md

NEXT.md is the L0 file — the first thing the agent reads every session. It answers: what is this project and what happens next?

**In your project root:**

```bash
cp starter/obsidian-vault/NEXT.md.example NEXT.md
```

Edit it to reflect your actual project. Keep it under 15 lines. Example structure:

```markdown
# My Project — NEXT

## Continue
- [ ] Implement user auth (branch: feature/auth)

## Decide
- Which session store: Redis vs in-memory?

## Blocked
- None

## Last session
2026-03-14 — Set up database schema, created User model
```

The agent reads this file at the start of every session. It tells the agent where you left off without loading the full codebase.

---

## Verify It Works

Run through this checklist after setup:

- [ ] **Start a Claude Code session in your project** — does it read NEXT.md and summarize where you left off?
- [ ] **Try writing a fake API key in a file** — paste `SECRET_KEY=sk-abc123fake` in a file and ask the agent to save it. Does the secret-detect hook block it?
- [ ] **Run `/session-complete`** — does it update NEXT.md with what happened this session?
- [ ] **Run `/knowledge --quick` with a URL** — give the agent a URL and say "research this --quick". Does it return exactly 4 lines?

If any check fails, see the relevant evolution entry for troubleshooting:
- NEXT.md not read → [evolution/001-tiered-context.md](../evolution/001-tiered-context.md)
- Hook not triggering → [evolution/002-safety-hooks.md](../evolution/002-safety-hooks.md)
- Session log not updating → [evolution/008-write-discipline.md](../evolution/008-write-discipline.md)

---

## What's Next

Once the basics work:

1. **Add more projects** — repeat Step 1 (memory dir) and Step 5 (NEXT.md) for each project
2. **Score your system** — run through [system/scorecard.md](../system/scorecard.md) to find your weakest dimension
3. **Read the evolution log** — start with [001](../evolution/001-tiered-context.md) if you want to understand the design, or jump to the entry for your lowest-scored dimension
