# Memento OS Conventions

You are an AI assistant operating with persistent memory. Follow these conventions exactly.

---

## Artifact Format

All conclusions extracted from a session MUST use one of these four artifact types:

```
[D] conclusion text — invalidates if: trigger condition [priority] [YYYY-MM-DD]
[I] insight text — invalidates if: condition [priority] [YYYY-MM-DD]
[E] what went wrong — root cause: why it happened [settled] [YYYY-MM-DD]
[S] seed idea — activates when: condition [priority] [YYYY-MM-DD]
```

- `[D]` Decision — a resolved choice with a stated trigger for reconsideration
- `[I]` Insight — a pattern or learning that may change under stated conditions
- `[E]` Error — a mistake with root cause + fix; defaults to `settled` priority
- `[S]` Seed — a deferred idea to revisit when a specific condition is met

---

## Priority Matrix

Assign priority using confidence × impact:

|                     | High Impact  | Low Impact  |
|---------------------|--------------|-------------|
| **High Confidence** | `critical`   | `settled`   |
| **Medium Confidence** | `volatile` | `settled`   |
| **Low Confidence**  | `volatile`   | `noise`     |

- `[E]` errors always default to `settled`
- `noise` artifacts: ask "store anyway or discard?" — default is discard

---

## Kobe Cap — 24 Artifacts Maximum

Each project's Active Reasoning Artifacts table holds at most **24 artifacts**.

When over cap, evict in this order:
1. `noise` first
2. `settled` next
3. `volatile` last
4. Never auto-evict `critical` — ask the user

Archive evicted artifacts to the project's `Decisions/` folder.

---

## Vault File Frontmatter Schema

Every vault note you create or update must include this YAML frontmatter:

```yaml
---
title: Note Title
type: decision | insight | research | log | reference
project: ProjectName
tags: [tag1, tag2]
created: YYYY-MM-DD
updated: YYYY-MM-DD
status: active | archived | draft
---
```

---

## Session Lifecycle

### Session Start (do this when beginning work)

1. Read `NEXT.md` in the project root — note blockers and next actions
2. Read the top 3 sections of `_context.md` (Summary, Key Numbers, Active Artifacts)
3. Check for seed artifacts (`[S]`) with conditions now met
4. Check artifact staleness — flag any `[D]` or `[I]` past their invalidation trigger
5. Display a short briefing: current focus, active artifacts count, any blockers

### Session Complete (do this before ending work)

1. Scan the conversation — identify conclusions, insights, errors, and seeds
2. For each candidate artifact: assign type, priority, and invalidation trigger
3. Check for contradictions with existing `[D]` artifacts in the vault
4. Confirm the artifact list with the user before writing
5. Write confirmed artifacts to the project's `_context.md` Active Artifacts table
6. Update `NEXT.md` — remove completed items, add new blockers or next actions
7. Append a one-line entry to the session log: `YYYY-MM-DD — what changed`

---

## Retrieval-First Protocol

Before making any decision or generating any plan, search the vault first:

- Before deciding → search for prior `[D]` artifacts on the same topic
- Before designing → check `Knowledge/` for existing research
- Before recommending → surface any `[E]` errors from similar past work
- Before brainstorming → check if a `[S]` seed already captures the idea

The vault is a retrieval source, not just a write destination. Search first, fill gaps second.

---

## Do Not

- Hardcode vault paths — users configure their vault location
- Store raw conversation fragments — store conclusions only
- Auto-evict `critical` artifacts — always confirm with the user
- Reference "Knowledge OS" or "Agentic Total Recall" — this system is called "Memento OS"
- Skip session-complete — every session that produces conclusions must end with a write

---

## Schema Validation: `memento:lint`

When the user asks to "lint", "validate artifacts", or "check the schema", run:

```bash
python3 ${MEMENTO_PLUGIN_ROOT}/skills/memento-lint/lint.py [vault_root] [--strict] [--ci] [--format json] [--quiet]
```

Rules enforced (case-insensitive):
- `[D]` / `[I]` MUST contain `invalidates if` / `invalidates when` / `dies if`
- `[S]` MUST contain `Activation:` (or `activates when` without `--strict`)
- `[E]` MUST contain `fix:`
- Every artifact MUST have a `#` number, a priority, and a `YYYY-MM-DD` date
- R7 (warning): malformed table rows surface as warnings; `--strict` promotes them to violations

`--ci` = `--strict --quiet`. Exit codes: 0 clean, 1 violations, 2 usage error.

For each violation, ask the user the missing field, then edit the artifact row in place. Re-run lint to confirm clean. Never auto-fix without confirmation.

---

## Decay Audit: `memento:decay`

When the user asks for "decay check", "what's stale", or "audit aged decisions", run:

```bash
python3 ${MEMENTO_PLUGIN_ROOT}/skills/memento-decay/decay.py [vault_root] [--age 30] [--format json] [--no-git] [--all] [--stopwords <file>]
```

Finds aged `[D]` artifacts (default >30 days) whose invalidation triggers may have fired. Scores from three signals: git-log keyword grep (multi-keyword AND in same commit weighted higher), vault-state contradiction (newer artifact with ≥2 overlapping terms), and age past 90 days.

A per-vault stopword list at `<vault_root>/.memento-stopwords` is loaded automatically.

Agent flow:
1. Run with `--format json`.
2. For each LIKELY STALE candidate, prompt user: "Mark `[D]#N` as superseded? (y/n/skip)".
3. On `y`, change the priority cell in `_context.md` to `superseded`.
4. On `n` / `skip`, optionally capture an `[I]` insight explaining why the trigger hasn't fired.

Never auto-supersede. Every supersession requires user confirmation.
