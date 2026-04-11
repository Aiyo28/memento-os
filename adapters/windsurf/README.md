# Memento OS — Windsurf Adapter

Port of the Memento OS memory system for Windsurf using plain markdown rules.

## Install

Copy `rules/` to `.windsurf/rules/` in your project root:

```bash
cp -r rules/ /your/project/.windsurf/rules/
```

Windsurf reads `.md` files in `.windsurf/rules/` as project-level instructions.

## Files

| File | Purpose |
|------|---------|
| `memento-conventions.md` | Artifact format, priority matrix, vault rules |
| `memento-workflows.md` | Session lifecycle, decide workflow |

## Differences from Claude Code version

- No slash commands — invoke workflows by describing what you want
- Rules replace CLAUDE.md system prompts
- Auto-log path is `~/.memento/auto-log` instead of `~/.claude/memento-auto-log`
- No hooks — session-start/complete must be invoked manually
