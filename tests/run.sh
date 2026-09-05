#!/usr/bin/env bash
# memento-os test driver.
# Runs lint + decay against fixtures. Asserts on exit codes and key
# substrings (not full golden output — decay scores depend on today's date).

set -u

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
LINT="${ROOT}/skills/memento-lint/lint.py"
DECAY="${ROOT}/skills/memento-decay/decay.py"
FIX="${ROOT}/tests/fixtures"

# The decay fixture is GENERATED, never checked in. decay.py scores against
# today's date, so any absolute date in a fixture silently rots into a false
# result — this suite went red on 2026-06-14 for exactly that reason and nobody
# noticed for three months because nothing ran it. Row 4 is the discriminator:
# it must be recent enough for `--age 30` to exclude it.
DECAY_FIX="$(mktemp -d)"
trap 'rm -rf "$DECAY_FIX"' EXIT

days_ago() {
    python3 -c "import datetime,sys;print((datetime.date.today()-datetime.timedelta(days=int(sys.argv[1]))).isoformat())" "$1"
}

make_decay_fixture() {
    local dir="$1" row4_days_ago="$2"
    mkdir -p "$dir"
    cat > "$dir/_context.md" <<EOF
---
title: "Decay Fixture"
type: project-context
---

# Decay Fixture

## Active Reasoning Artifacts

| # | Artifact | Priority | Date |
|---|----------|----------|------|
| 1 | \`[D] Ship the auth refactor before Q3 — invalidates if scope creeps past two epics\` | critical | $(days_ago 400) |
| 2 | \`[D] Use SendGrid for transactional email — invalidates if pricing changes\` | settled | $(days_ago 250) |
| 3 | \`[D] Auth refactor scope expanded to four epics — invalidates if engineering capacity drops\` | critical | $(days_ago 200) |
| 4 | \`[D] Recently picked TanStack Query — invalidates if SWR adds suspense first\` | volatile | $(days_ago "$row4_days_ago") |
EOF
}

make_decay_fixture "$DECAY_FIX" 5

PASS=0
FAIL=0

red()   { printf '\033[31m%s\033[0m\n' "$*"; }
green() { printf '\033[32m%s\033[0m\n' "$*"; }

assert_eq() {
    local label="$1" expected="$2" actual="$3"
    if [ "$expected" = "$actual" ]; then
        green "  PASS: $label"
        PASS=$((PASS + 1))
    else
        red "  FAIL: $label (expected=$expected, actual=$actual)"
        FAIL=$((FAIL + 1))
    fi
}

assert_contains() {
    local label="$1" needle="$2" haystack="$3"
    if printf '%s' "$haystack" | grep -qF "$needle"; then
        green "  PASS: $label"
        PASS=$((PASS + 1))
    else
        red "  FAIL: $label (missing: $needle)"
        FAIL=$((FAIL + 1))
    fi
}

assert_not_contains() {
    local label="$1" needle="$2" haystack="$3"
    if printf '%s' "$haystack" | grep -qF "$needle"; then
        red "  FAIL: $label (unexpected: $needle)"
        FAIL=$((FAIL + 1))
    else
        green "  PASS: $label"
        PASS=$((PASS + 1))
    fi
}

echo "=== memento:lint — clean fixture ==="
OUT="$(python3 "$LINT" "$FIX/clean" 2>&1)"
RC=$?
assert_eq "exit code is 0" 0 $RC
assert_contains "no violations summary" "0 violations" "$OUT"
assert_contains "5 artifacts checked" "5 artifacts checked" "$OUT"

echo "=== memento:lint — violations fixture ==="
OUT="$(python3 "$LINT" "$FIX/violations" 2>&1)"
RC=$?
assert_eq "exit code is 1" 1 $RC
assert_contains "R1 [D] missing invalidates" "R1: missing 'invalidates" "$OUT"
assert_contains "R2 [S] missing activation" "R2: missing 'Activation" "$OUT"
assert_contains "R3 [E] missing fix" "R3: missing 'fix:'" "$OUT"
assert_contains "R4 missing # number" "R4: missing # number" "$OUT"
assert_contains "R5 missing priority" "R5: missing priority" "$OUT"
assert_contains "R6 missing date" "R6: no YYYY-MM-DD date" "$OUT"

echo "=== memento:lint — strict mode (rejects 'activates when') ==="
OUT="$(python3 "$LINT" --strict "$FIX/clean" 2>&1)"
RC=$?
assert_eq "exit code is 1 in strict mode" 1 $RC
assert_contains "rejects 'activates when' [S]#5" "[S]#5      R2" "$OUT"

echo "=== memento:lint — JSON output ==="
OUT="$(python3 "$LINT" --format json "$FIX/violations" 2>&1)"
RC=$?
assert_eq "exit code is 1" 1 $RC
assert_contains "JSON has violations key" '"violations"' "$OUT"
assert_contains "JSON rule R1 surfaced" '"rule": "R1"' "$OUT"

echo "=== memento:decay — fixture (no-git) ==="
OUT="$(python3 "$DECAY" --no-git --age 30 "$DECAY_FIX" 2>&1)"
RC=$?
assert_eq "exit code is 0" 0 $RC
assert_contains "[D]#1 surfaced as LIKELY STALE (vault overlap signal)" "[LIKELY STALE]" "$OUT"
assert_contains "[D]#1 invalidator parsed" "scope creeps past two epics" "$OUT"
assert_contains "vault overlap evidence cites #3" "[D]#3" "$OUT"
assert_not_contains "recent [D]#4 (5 days old) excluded" "[D]#4" "$OUT"

echo "=== memento:decay — the age filter actually discriminates ==="
# Same fixture, row 4 aged past the threshold. If [D]#4 is still absent here the
# assertion above is passing vacuously and proves nothing.
make_decay_fixture "$DECAY_FIX" 400
OUT="$(python3 "$DECAY" --no-git --age 30 "$DECAY_FIX" 2>&1)"
assert_contains "aged [D]#4 (400 days old) now surfaces" "[D]#4" "$OUT"
make_decay_fixture "$DECAY_FIX" 5

echo "=== memento:decay — JSON output ==="
OUT="$(python3 "$DECAY" --no-git --age 30 --format json "$DECAY_FIX" 2>&1)"
RC=$?
assert_eq "exit code is 0" 0 $RC
assert_contains "JSON has candidates key" '"candidates"' "$OUT"
assert_contains "JSON signal type vault" '"type": "vault"' "$OUT"

echo "=== memento:decay — age threshold respected ==="
OUT="$(python3 "$DECAY" --no-git --age 99999 "$DECAY_FIX" 2>&1)"
RC=$?
assert_eq "exit code is 0" 0 $RC
assert_contains "no candidates when age threshold absurdly high" "No aged" "$OUT"

echo "=== memento:lint — R7 malformed rows (warn-only by default) ==="
OUT="$(python3 "$LINT" "$FIX/malformed" 2>&1)"
RC=$?
assert_eq "exit code is 0 (warnings don't fail default)" 0 $RC
assert_contains "WARN tag on malformed row" "WARN: malformed row" "$OUT"
assert_contains "unbalanced backticks detected" "unbalanced backticks" "$OUT"
assert_contains "clean row #1 still validates" "[D]#1      OK" "$OUT"

echo "=== memento:lint — R7 promoted to violation under --strict ==="
OUT="$(python3 "$LINT" --strict "$FIX/malformed" 2>&1)"
RC=$?
assert_eq "exit code is 1 (strict promotes R7)" 1 $RC
assert_contains "R7 rule code shown in strict" "R7: malformed row" "$OUT"

echo "=== memento:lint — --ci flag (= --strict --quiet) ==="
OUT="$(python3 "$LINT" --ci "$FIX/violations" 2>&1)"
RC=$?
assert_eq "exit code is 1" 1 $RC
assert_not_contains "no OK lines in --ci output" "      OK" "$OUT"

echo "=== memento:decay — .memento-stopwords blocks vault overlap ==="
OUT="$(python3 "$DECAY" --no-git --age 30 "$FIX/stopwords" 2>&1)"
assert_not_contains "no LIKELY STALE when stopwords filter the overlap" "LIKELY STALE" "$OUT"
assert_contains "still surfaces as REVIEW (age signal)" "REVIEW" "$OUT"

echo "=== memento:decay — without stopwords, vault overlap fires ==="
OUT="$(python3 "$DECAY" --no-git --age 30 --stopwords /dev/null "$FIX/stopwords" 2>&1)"
assert_contains "LIKELY STALE without project stopwords" "LIKELY STALE" "$OUT"
assert_contains "vault overlap evidence shown" "overlap: breaking,engine,update,vendor" "$OUT"

echo ""
echo "=========================================="
if [ $FAIL -eq 0 ]; then
    green "All $PASS assertions passed."
    exit 0
else
    red "$FAIL failed, $PASS passed."
    exit 1
fi
