# Memento OS — Cursor Adapter

Port of the Memento OS memory system for Cursor using MDC rules.

## Install

Copy `rules/` to `.cursor/rules/` in your project root:

```bash
cp -r rules/ /your/project/.cursor/rules/
```

Cursor auto-applies rules with `alwaysApply: true`. Workflow rules are triggered contextually.

## Files

| File | Purpose | Applied |
|------|---------|---------|
| `memento-conventions.mdc` | Artifact format, priority matrix, vault rules | Always |
| `memento-workflows.mdc` | Session lifecycle, decide workflow | On demand |

## Differences from Claude Code version

- No slash commands — Cursor uses natural language triggers instead
- Rules replace CLAUDE.md system prompts
- Auto-log path is `~/.memento/auto-log` instead of `~/.claude/memento-auto-log`
- No hooks — session-start/complete must be invoked manually
