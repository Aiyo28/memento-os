# Agent Instructions — Memento OS

## What This Is

A Codex plugin for persistent AI memory. Core unit: reasoning artifacts (`[D]`, `[I]`, `[E]`, `[S]`) with invalidation/activation triggers.

## Artifact Format

```
[D] conclusion — invalidates if trigger [priority] [YYYY-MM-DD]
[I] insight — invalidates if condition [priority] [YYYY-MM-DD]
[E] what went wrong — root cause: why [settled] [YYYY-MM-DD]
[S] idea — activates when condition [priority] [YYYY-MM-DD]
```

## Priority Matrix

Derived from confidence × impact:

|  | High Impact | Low Impact |
|---|---|---|
| **High Confidence** | **critical** | **settled** |
| **Medium Confidence** | **volatile** | **settled** |
| **Low Confidence** | **volatile** | **noise** |

- `[E]` errors default to **settled**
- **noise** artifacts: ask "store anyway or discard?" — default discard

## Cap: 24 Artifacts (Kobe Rule)

Maximum 24 artifacts per project in the Active Reasoning Artifacts table. When over cap, evict by priority: noise first → settled → volatile. Never auto-evict critical artifacts. Archive evicted artifacts to `Decisions/` folder.

## Retrieval-First Protocol

Skills that make decisions MUST search the vault before acting:

- `decide` → search for prior `[D]` artifacts before presenting options
- `grill-me` → load domain-relevant vault notes as grilling context
- `brainstorming` → check existing research before exploring designs
- `research` → vault-first: glob `Knowledge/` before web search

The vault is a retrieval source, not just a write destination. Search first, then fill gaps.

## Skills (auto-discovered from `.agents/skills/`)

| Skill | Description |
|-------|-------------|
| `session-start` | Session opening ritual — loads L0/L1 context, displays briefing |
| `session-complete` | End-of-session artifact extraction and NEXT.md update |
| `decide` | OODA decision loop with retrieval gate and priority matrix |
| `grill-me` | Relentless structured interviewing to stress-test a plan |
| `vault-audit` | Vault health check — staleness, structure, inbox processing |

## Auto-Log

Auto-logging state is stored at `~/.memento/auto-log`. Write `on` to enable, `off` to disable. Session-start enables it automatically.

## Do Not

- Hardcode vault paths — users configure their vault location
- Reference "Knowledge OS" or "Agentic Total Recall" — this is "Memento OS"
- Add skills outside the memory mission (no dev workflow, no project management)
- Store raw notes or conversation fragments — store conclusions only
