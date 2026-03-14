#!/usr/bin/env bash
# Hook: Git Safety
# Event: PreToolUse
# Matcher: Bash
#
# Blocks dangerous git operations: force push, reset --hard, checkout --,
# clean -f, branch -D, and staging sensitive files (.env, *.pem, credentials).
#
# Installation:
#   1. Copy to ~/.claude/hooks/git-safety.sh
#   2. chmod +x ~/.claude/hooks/git-safety.sh
#   3. Add to ~/.claude/settings.json (see starter/quickstart.md)

set -euo pipefail

INPUT=$(cat)
CMD=$(echo "$INPUT" | jq -r '.tool_input.command // empty')

[[ -z "$CMD" ]] && exit 0
[[ ! "$CMD" =~ git[[:space:]] ]] && exit 0

# Force push
if echo "$CMD" | grep -qE 'git[[:space:]]+push[[:space:]]+.*(-f|--force|--force-with-lease)'; then
  echo "BLOCKED: Force push detected." >&2
  echo "Force pushing rewrites remote history and can destroy teammates' work." >&2
  echo "Safer: git push (without --force) and resolve conflicts." >&2
  exit 2
fi

# Hard reset
if echo "$CMD" | grep -qE 'git[[:space:]]+reset[[:space:]]+--hard'; then
  echo "BLOCKED: git reset --hard detected." >&2
  echo "This irreversibly destroys uncommitted changes." >&2
  echo "Safer: git stash (preserves changes, recoverable)." >&2
  exit 2
fi

# Discard all working tree changes
if echo "$CMD" | grep -qE 'git[[:space:]]+checkout[[:space:]]+(--[[:space:]]+\.|--)$|git[[:space:]]+checkout[[:space:]]+\.$'; then
  echo "BLOCKED: Discarding all working tree changes." >&2
  echo "Safer: git stash or git checkout -- <specific-file>." >&2
  exit 2
fi

# Clean untracked files
if echo "$CMD" | grep -qE 'git[[:space:]]+clean[[:space:]]+-[a-zA-Z]*f'; then
  echo "BLOCKED: git clean -f detected." >&2
  echo "This permanently deletes untracked files." >&2
  echo "Safer: git clean -n (dry run) or git stash --include-untracked." >&2
  exit 2
fi

# Force delete branch
if echo "$CMD" | grep -qE 'git[[:space:]]+branch[[:space:]]+-D[[:space:]]'; then
  echo "BLOCKED: git branch -D (force delete) detected." >&2
  echo "Safer: git branch -d (only deletes if fully merged)." >&2
  exit 2
fi

# Staging sensitive files
if echo "$CMD" | grep -qE 'git[[:space:]]+add[[:space:]]+(.*/)?(\.env(\.[a-zA-Z]+)?|credentials\.json|[^[:space:]]*\.pem|[^[:space:]]*\.key)([[:space:]]|$)'; then
  echo "BLOCKED: Attempting to stage sensitive files." >&2
  echo "Add them to .gitignore instead. Use .env.example with placeholders." >&2
  exit 2
fi

exit 0
