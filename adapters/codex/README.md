# Memento OS — Codex Adapter

Port of the Memento OS Claude Code plugin for OpenAI Codex (AGENTS.md + `.agents/skills/`).

## Install

1. Copy `AGENTS.md` to your project root
2. Copy the `skills/` directory to `.agents/skills/` in your project:
   ```
   cp -r skills/ /your/project/.agents/skills/
   ```
3. Run Codex — skills are auto-discovered from `.agents/skills/*/SKILL.md`

## Skills

| Skill | Trigger phrases |
|-------|----------------|
| `session-start` | "start session", "what's the context", "catch me up" |
| `session-complete` | "done", "wrap up", "session complete", "about to compact" |
| `decide` | "decide", "should we", "which option", "evaluate", "compare" |
| `grill-me` | "grill me", "stress test", "poke holes", "what am I missing" |
| `vault-audit` | "vault audit", "check vault", "what's stale", "vault health" |

## Differences from Claude Code version

- Skills use no namespace prefix (`session-start` not `memento:session-start`)
- Auto-log path is `~/.memento/auto-log` instead of `~/.claude/memento-auto-log`
- Project instructions file is `AGENTS.md` instead of `CLAUDE.md`
