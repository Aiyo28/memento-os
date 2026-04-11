# Memento OS — Cline Adapter

Port of the Memento OS memory system for Cline using `.clinerules/` directory.

## Install

Copy `.clinerules/` to your project root:

```bash
cp -r .clinerules/ /your/project/.clinerules/
```

Cline reads all `.md` files in `.clinerules/` as persistent instructions for every conversation.

## Files

| File | Purpose |
|------|---------|
| `.clinerules/memento-conventions.md` | Artifact format, priority matrix, vault rules |
| `.clinerules/memento-workflows.md` | Session lifecycle, decide workflow |

## Differences from Claude Code version

- No slash commands — invoke workflows by describing what you want
- Rules replace CLAUDE.md system prompts
- Auto-log path is `~/.memento/auto-log` instead of `~/.claude/memento-auto-log`
- No hooks — session-start/complete must be invoked manually
