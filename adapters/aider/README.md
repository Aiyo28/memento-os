# Memento OS — Aider Adapter

Tier 3 (Manual) integration. Loads Memento OS conventions as read-only context so Aider's AI follows the artifact format, session lifecycle, and retrieval-first protocol.

## Install

1. Copy `CONVENTIONS.md` to your project root:
   ```
   cp CONVENTIONS.md /your/project/CONVENTIONS.md
   ```
2. Copy `.aider.conf.yml` to your project root (or merge with existing):
   ```
   cp .aider.conf.yml /your/project/.aider.conf.yml
   ```
3. Aider will auto-load `CONVENTIONS.md` as read-only context on every run.

## What You Get

- Artifact format (`[D]/[I]/[E]/[S]`) enforced in all session output
- Priority matrix applied when the AI stores conclusions
- Kobe 24-artifact cap respected on writes
- Recall and end workflows encoded as explicit instructions
- `memento:check` and `memento:forget` Python scripts callable from `/run` commands

## Optional: check and forget

Add these `commands:` entries to your `.aider.conf.yml` (export `MEMENTO_PLUGIN_ROOT` to wherever you cloned memento-os):

```yaml
commands:
  - name: check
    run: python3 ${MEMENTO_PLUGIN_ROOT}/skills/check/lint.py
  - name: forget
    run: python3 ${MEMENTO_PLUGIN_ROOT}/skills/forget/decay.py --format json
```

Then `/check` and `/forget` inside the Aider session invoke the scripts. See `CONVENTIONS.md` for the full schema rules and agent flow.

## Differences from Tier 1/2

- No slash commands — workflows run by prompting the AI directly ("start session", "wrap up")
- No auto-hooks — you must prompt the end workflow manually before ending a session
- Vault sync is manual (`git pull` / `git push` in your vault repo)
