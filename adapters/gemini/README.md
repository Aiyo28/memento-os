# Memento OS — Gemini Adapter

Port of the Memento OS memory system for Gemini CLI using a single `GEMINI.md` file.

## Install

Copy `GEMINI.md` to your project root:

```bash
cp GEMINI.md /your/project/GEMINI.md
```

Gemini CLI reads `GEMINI.md` as project-level instructions, equivalent to Claude Code's `CLAUDE.md`.

## Differences from Claude Code version

- No slash commands — invoke workflows by describing what you want
- Single file combines conventions + all workflows
- Auto-log path is `~/.memento/auto-log` instead of `~/.claude/memento-auto-log`
- No hooks — session-start/complete must be invoked manually
