# Agent Instructions — Memento OS

## What This Repo Is

A Claude Code plugin for persistent AI memory. Core unit: reasoning artifacts (`[D]`, `[I]`, `[E]`, `[S]`) with invalidation/activation triggers.

## If You're Working On This Repo

- Skills are in `skills/*/SKILL.md` — each namespaced as `memento:*`
- Commands are in `commands/memento/*.md`
- Hooks are in `hooks/hooks.json` (prompt-type hooks for Stop and PreCompact)
- Plugin manifest is `.claude-plugin/plugin.json` (currently v0.4.0)

## Conventions

- Artifact format: `[D] conclusion — invalidates if trigger [priority] [date]`
- Seed format: `[S] idea — activates when condition [priority] [date]`
- Priority: confidence x impact → critical/volatile/settled/noise
- Cap: 24 artifacts per project (Kobe rule). Evict noise first.
- Skills produce artifacts as byproduct — grill-me surfaces `[D]`/`[I]`, decide captures `[D]` or plants `[S]`

## Do Not

- Hardcode vault paths — users configure via `/memento:init`
- Reference "Knowledge OS" or "Agentic Total Recall" — this is "Memento OS"
- Add skills outside the memory mission (no dev workflow, no project management)
- Store raw notes or conversation fragments — store conclusions only
