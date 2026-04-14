---
name: memento:session-start
version: 2.1.0
description: >
  Session opening ritual. Loads context via L0→L1 protocol, displays briefing
  with active decisions and pending items, checks for stale artifacts by priority.
  Triggers: "start session", "what's the context", "where were we", "catch me up".
user_invocable: true
---

# /session-start

Load context. Display briefing. Flag staleness. Get to work.

## Steps

### 1. Load L0 — Session Continuity

Read `NEXT.md` in the project root.

### 2. Load L0.5 — Context Directory (~800 tokens, optional)

If `context/` exists at project root, load all files (domain-terms, stakeholder-profiles, constraints). Skip if missing — not all projects need this.

### 3. Load L1 — Project Context (~600 tokens)

Read (skip if missing):
- Project `CLAUDE.md`
- Vault `_context.md` — **top 3 sections only**: Summary + Key Numbers + Active Reasoning Artifacts table. STOP before Doc Index / Decision Log / Open Questions / Related sections. This is the L1 partial read rule.
- Peer Card (`People/Self.md` in vault or memory folder) — structured user profile with communication style, decision patterns, strengths, growth areas. Load the **Communication Style** and **Decision Patterns** tables only (~20 lines). Template provided in starter vault. Skip if missing — suggest creating one on first session.

### 4. Seed Activation Check

Scan `[S]` entries in the Active Reasoning Artifacts table:
- If activation condition appears met → surface in briefing under "Seeds Ready"
- If dormant > 90 days → flag for review
- When a seed activates, suggest: "This seed is ready. Want to `/decide` on it?"

### 5. Staleness Check

Scan `[D]`, `[I]`, `[E]` entries in the Active Reasoning Artifacts table:

**First: check for expired artifacts** (those with `expires: YYYY-MM-DD` past today's date). Flag as **EXPIRED** in briefing regardless of priority.

**Then: priority-based staleness** (for artifacts without expiry):

| Priority | Age | Status |
|----------|-----|--------|
| critical | > 90 days | STALE — review invalidation trigger (may still be valid) |
| volatile | > 30 days | NEEDS RESOLUTION — decide, upgrade to critical, or delete |
| settled | > 90 days | STALE — likely safe to archive |
| noise | Any | Should not be in table — flag for removal |

### 6. Display Briefing

```
## Session Briefing — {Project Name}
**Date:** {today}
**Memory:** {score}/10 | {total} artifacts | {seeds} seeds | streak: {n}

### Continue
{from NEXT.md}

### Active Decisions
{from _context.md — show critical and volatile only, up to 7}

### Seeds Ready (if any)
{[S] artifacts where activation condition appears met}

### Stale Artifacts (if any)
{list with age and invalidation trigger}

### Pending
{from NEXT.md "Decide" section}
```

Memory score calculation: count artifacts (0-2pts), critical decisions (0-2pts), recency (0-2pts), no stale (0-1.5pts), seeds (0-1pt), session streak (0-1.5pts). See `/memento stats` for full breakdown.

### 7. Enable Auto-Logging

Write `on` to `~/.claude/memento-auto-log`. This activates the Stop hook for journal entries.

To disable: user says "turn off auto-logging" → write `off` to the same file.

### 8. Do NOT Load L2/L3

Never auto-load full docs or research files at session start.
- **L2** (full `_context.md` + referenced docs, ~2000 tok): load when L1 indicates relevance or task touches a listed doc.
- **L3** (deep vault grep — `Knowledge/`, cross-project `_context.md`, MOCs, ~4000 tok): load only for cross-project research or unfamiliar domain.

### 9. Memento Tip (optional, once per session)

If memory score < 5, append one tip to the briefing (rotate through these):

- "We all need mirrors to remind ourselves who we are." — Run `/memento:decide` to capture your next choice.
- "Remember Sammy Jankis." — Your artifacts remember so you don't have to.
- "I have to believe in a world outside my own mind." — Plant a `[S]` seed for ideas that aren't ready yet.
- "The world doesn't just disappear when you close your eyes." — Run `/memento:session-complete` before you leave.

If score >= 5, skip the tip. The system is working — don't nag.
