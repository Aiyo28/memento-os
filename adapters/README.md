# Memento OS — Adapters

Adapters bring Memento OS to AI tools beyond Claude Code. All tiers use the same vault structure — the `starter/obsidian-vault/` template works with every tool.

## Tier Overview

| Tool | Tier | What You Get | Install |
|------|------|-------------|---------|
| Claude Code | 1 — Full Plugin | 5 skills, 2 hooks, 2 commands | `claude plugin install memento-os` |
| Codex | 1 — Full Skills | AGENTS.md + 5 skills | Copy `adapters/codex/` files |
| Cursor | 2 — Rules | Convention + workflow rules | Copy to `.cursor/rules/` |
| Windsurf | 2 — Rules | Convention + workflow rules | Copy to `.windsurf/rules/` |
| Cline | 2 — Rules | Convention + workflow rules | Copy to project root |
| Gemini | 2 — Single File | GEMINI.md with all workflows | Copy to project root |
| Aider | 3 — Manual | CONVENTIONS.md + config | Copy + merge config |
| Continue | 3 — Manual | Config snippet + prompts | Paste into config.yaml |

## Tiers Explained

**Tier 1 — Full skill parity.** The AI tool has a native skill system that can auto-discover and execute structured workflows. Session lifecycle, artifact extraction, and vault writes run as skills with tool-call access. Closest to the full Claude Code experience.

**Tier 2 — Workflow rules.** The tool has a convention/rules system but no skill runner. Memento OS conventions and session workflows are encoded as persistent instructions the AI reads on every run. The AI follows the protocol through prompting, not execution.

**Tier 3 — Manual integration.** No native skill or rules system. Conventions are loaded as read-only context files. Workflows are slash commands (prompts) the user must invoke explicitly. Vault sync is manual. Requires more discipline from the user to maintain the session lifecycle.

## Adapter Directories

```
adapters/
  codex/          — Tier 1: AGENTS.md + skills/ for OpenAI Codex
  aider/          — Tier 3: CONVENTIONS.md + .aider.conf.yml
  continue/       — Tier 3: config-snippet.yaml + prompts/
```

## Vault Compatibility

All adapters target the same vault structure. Set your vault root once — every adapter reads from and writes to the same `_context.md`, `NEXT.md`, `Knowledge/`, and `Decisions/` layout. See `starter/obsidian-vault/` for the canonical vault template.
