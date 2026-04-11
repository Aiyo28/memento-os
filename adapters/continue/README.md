# Memento OS — Continue Adapter

Tier 3 (Manual) integration. Encodes Memento OS conventions as Continue config rules and provides `/session-start` and `/session-complete` as Continue slash commands.

## Install

1. Paste the rules block from `config-snippet.yaml` into your `~/.continue/config.yaml` under the `rules:` key
2. Copy the `prompts/` directory to `~/.continue/prompts/`:
   ```
   cp -r prompts/ ~/.continue/prompts/
   ```
3. Restart Continue — slash commands appear as `/session-start` and `/session-complete`

## What You Get

- Artifact format and priority matrix enforced via config rules
- `/session-start` slash command runs the session-opening briefing workflow
- `/session-complete` slash command runs the artifact-extraction and NEXT.md update workflow

## Differences from Tier 1/2

- No auto-hooks — slash commands must be invoked manually
- Rules are loaded as static text; the AI cannot execute tool calls from prompts
- Vault sync (git pull/push) must be done manually in your vault repo
- Slash commands are prompts, not skill scripts — output quality depends on the underlying model
