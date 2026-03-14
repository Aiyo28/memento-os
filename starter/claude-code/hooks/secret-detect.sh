#!/usr/bin/env bash
# Hook: Secret Detection
# Event: PreToolUse
# Matcher: Write|Edit
#
# Blocks hardcoded secrets in file writes. Detects API key patterns,
# PEM private keys, AWS secrets, and generic credential assignments.
# Includes false-positive prevention for placeholders and env references.
#
# Installation:
#   1. Copy to ~/.claude/hooks/secret-detect.sh
#   2. chmod +x ~/.claude/hooks/secret-detect.sh
#   3. Add to ~/.claude/settings.json (see starter/quickstart.md)

set -euo pipefail

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

is_placeholder() {
  local val="$1"
  [[ ${#val} -lt 8 ]] && return 0
  local lower
  lower=$(echo "$val" | tr '[:upper:]' '[:lower:]')
  [[ "$lower" =~ ^your[-_] ]] && return 0
  [[ "$lower" =~ [-_]here$ ]] && return 0
  [[ "$lower" == "changeme" ]] && return 0
  [[ "$lower" == "replace_me" ]] && return 0
  [[ "$lower" =~ ^x{3,}$ ]] && return 0
  [[ "$lower" =~ ^todo ]] && return 0
  [[ "$lower" =~ ^example ]] && return 0
  [[ "$lower" =~ ^fake ]] && return 0
  [[ "$lower" =~ ^dummy ]] && return 0
  [[ "$lower" =~ ^test[-_]? ]] && return 0
  [[ "$lower" =~ ^\.\.\. ]] && return 0
  [[ "$lower" =~ ^\<.*\>$ ]] && return 0
  return 1
}

is_env_reference() {
  local line="$1"
  [[ "$line" =~ process\.env\. ]] && return 0
  [[ "$line" =~ os\.environ ]] && return 0
  [[ "$line" =~ \$\{[A-Z_]+\} ]] && return 0
  [[ "$line" =~ \{\{[A-Z_]+\}\} ]] && return 0
  [[ "$line" =~ getenv\( ]] && return 0
  [[ "$line" =~ ENV\[\" ]] && return 0
  return 1
}

# Known API key prefixes (20+ chars)
while IFS= read -r match; do
  [[ -z "$match" ]] && continue
  is_placeholder "$match" && continue
  truncated="${match:0:12}..."
  echo "BLOCKED: Detected probable API key: '${truncated}'" >&2
  echo "Use environment variables or a secrets manager instead of hardcoding keys." >&2
  exit 2
done < <(echo "$TEXT" | grep -oE '(sk-[a-zA-Z0-9_-]{20,}|sk_live_[a-zA-Z0-9]{20,}|sk_test_[a-zA-Z0-9]{20,}|AKIA[0-9A-Z]{16}|ghp_[a-zA-Z0-9]{36}|gho_[a-zA-Z0-9]{36}|ghs_[a-zA-Z0-9]{36}|github_pat_[a-zA-Z0-9_]{20,}|xoxb-[a-zA-Z0-9-]+|xoxp-[a-zA-Z0-9-]+|glpat-[a-zA-Z0-9_-]{20,}|pypi-[a-zA-Z0-9_-]{20,})' 2>/dev/null || true)

# Private keys (PEM headers)
if echo "$TEXT" | grep -qE 'BEGIN[[:space:]]+(RSA|DSA|EC|OPENSSH|PGP)?[[:space:]]*PRIVATE KEY' 2>/dev/null; then
  echo "BLOCKED: Detected private key (PEM format)." >&2
  echo "Never commit private keys. Use file references or secret managers." >&2
  exit 2
fi

# AWS secret access keys
if echo "$TEXT" | grep -qiE 'aws_secret_access_key[[:space:]]*[=:][[:space:]]*["\x27]?[A-Za-z0-9/+=]{40}' 2>/dev/null; then
  echo "BLOCKED: Detected AWS Secret Access Key." >&2
  echo "Use AWS credentials file, IAM roles, or environment variables instead." >&2
  exit 2
fi

# Generic credential assignments (8+ chars, not placeholder or env ref)
while IFS= read -r line; do
  [[ -z "$line" ]] && continue
  is_env_reference "$line" && continue
  value=$(echo "$line" | sed -E 's/^.*(password|token|secret|api_key|apikey|api_secret|auth_token|access_token|private_key)[[:space:]]*[=:][[:space:]]*["\x27]?//i' | sed -E 's/["\x27;,[:space:]]*$//')
  [[ -z "$value" ]] && continue
  is_placeholder "$value" && continue
  echo "BLOCKED: Detected hardcoded credential near '${line:0:40}...'." >&2
  echo "Use environment variables or a secrets manager instead." >&2
  exit 2
done < <(echo "$TEXT" | grep -iE '(password|token|secret|api_key|apikey|api_secret|auth_token|access_token|private_key)[[:space:]]*[=:][[:space:]]*["\x27][a-zA-Z0-9/+=_.@$!#%^&*-]{8,}' 2>/dev/null || true)

exit 0
