#!/usr/bin/env bash
# Hook: Destructive Command Blocker
# Event: PreToolUse
# Matcher: Bash
#
# Blocks catastrophic shell commands: rm -rf on root/home, DROP TABLE,
# TRUNCATE, chmod 777, killing system processes, fork bombs, dd to raw disk.
#
# Installation:
#   1. Copy to ~/.claude/hooks/destructive-command.sh
#   2. chmod +x ~/.claude/hooks/destructive-command.sh
#   3. Add to ~/.claude/settings.json (see starter/quickstart.md)

set -euo pipefail

INPUT=$(cat)
CMD=$(echo "$INPUT" | jq -r '.tool_input.command // empty')

[[ -z "$CMD" ]] && exit 0

# Catastrophic recursive deletes
if echo "$CMD" | grep -qE 'rm[[:space:]]+-[a-zA-Z]*r[a-zA-Z]*f'; then
  target=$(echo "$CMD" | grep -oE 'rm[[:space:]]+-[a-zA-Z]*rf?[[:space:]]+[^;&|]+' | sed -E 's/rm[[:space:]]+-[a-zA-Z]*rf?[[:space:]]+//')
  if echo "$target" | grep -qE '^[[:space:]]*(\/|~|\.|\.\/)[[:space:]]*$'; then
    echo "BLOCKED: Catastrophic rm -rf targeting root/home/current directory." >&2
    echo "If you need to clean up, specify exact paths (e.g., rm -rf ./dist)." >&2
    exit 2
  fi
  if echo "$target" | grep -qE '^[[:space:]]*(\/\*|~\/\*|\.\*)'; then
    echo "BLOCKED: Wildcard rm -rf detected." >&2
    exit 2
  fi
fi

# SQL data destruction
if echo "$CMD" | grep -qiE 'DROP[[:space:]]+(TABLE|DATABASE)[[:space:]]'; then
  echo "BLOCKED: DROP TABLE/DATABASE detected." >&2
  echo "Create a backup first, or use DROP TABLE IF EXISTS in a migration with rollback." >&2
  exit 2
fi

if echo "$CMD" | grep -qiE 'TRUNCATE[[:space:]]+TABLE[[:space:]]'; then
  echo "BLOCKED: TRUNCATE TABLE detected." >&2
  echo "Safer alternative: DELETE FROM <table> WHERE <condition>" >&2
  exit 2
fi

# DELETE FROM without WHERE
if echo "$CMD" | grep -qiE 'DELETE[[:space:]]+FROM[[:space:]]+[a-zA-Z_]+[[:space:]]*;'; then
  echo "BLOCKED: DELETE FROM without WHERE clause detected." >&2
  echo "Add a WHERE clause to target specific rows." >&2
  exit 2
fi

# chmod 777
if echo "$CMD" | grep -qE 'chmod[[:space:]]+777'; then
  echo "BLOCKED: chmod 777 (world-writable) detected." >&2
  echo "Safer alternatives: chmod 755 (dirs), chmod 644 (files), chmod 600 (private)." >&2
  exit 2
fi

# Killing critical system processes
if echo "$CMD" | grep -qE 'kill[[:space:]]+-9[[:space:]]+1([[:space:]]|$)'; then
  echo "BLOCKED: Attempting to kill PID 1 (init/launchd)." >&2
  exit 2
fi

if echo "$CMD" | grep -qiE 'killall[[:space:]]+(launchd|WindowServer|loginwindow|kernel_task|systemd|init)'; then
  echo "BLOCKED: Attempting to kill critical system process." >&2
  exit 2
fi

# Fork bomb
if echo "$CMD" | grep -qE ':\(\)\{.*\|.*&\}.*:|\.%0\|\.%0'; then
  echo "BLOCKED: Fork bomb pattern detected." >&2
  exit 2
fi

# dd to raw disk devices
if echo "$CMD" | grep -qE 'dd[[:space:]]+.*of=[[:space:]]*/dev/(sd[a-z]|disk[0-9]|nvme|hd[a-z]|vd[a-z])'; then
  echo "BLOCKED: dd writing to raw disk device detected." >&2
  exit 2
fi

exit 0
