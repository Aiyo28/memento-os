#!/usr/bin/env bash
# Sync the v2.2+ verbs (lint.py / decay.py) from the root skills/
# directory into every adapter that hosts its own copy of the script.
#
# Run before tagging a release.

set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"

TIER1_ADAPTERS=(codex)
VERBS=(memento-lint memento-decay)

copied=0
skipped=0

for tool in "${TIER1_ADAPTERS[@]}"; do
    for verb in "${VERBS[@]}"; do
        SRC_DIR="$ROOT/skills/$verb"
        DST_DIR="$ROOT/adapters/$tool/skills/$verb"
        script_name="${verb#memento-}.py"
        if [ ! -d "$DST_DIR" ]; then
            echo "skip: $tool/$verb (target directory missing — run after Block A scaffold)"
            skipped=$((skipped + 1))
            continue
        fi
        if [ ! -f "$SRC_DIR/$script_name" ]; then
            echo "skip: $tool/$verb ($script_name not found in source)"
            skipped=$((skipped + 1))
            continue
        fi
        cp "$SRC_DIR/$script_name" "$DST_DIR/$script_name"
        chmod +x "$DST_DIR/$script_name"
        echo "synced: $verb → adapters/$tool/skills/$verb/$script_name"
        copied=$((copied + 1))
    done
done

echo
echo "done — $copied copied, $skipped skipped"
