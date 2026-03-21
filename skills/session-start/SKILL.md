---
name: memento:session-start
version: 2.0.0
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

### 2. Load L1 — Project Context

Read (skip if missing):
- Project `CLAUDE.md`
- Vault `_context.md` (project context with reasoning artifacts)

### 3. Seed Activation Check

Scan `[S]` entries in the Active Reasoning Artifacts table:
- If activation condition appears met → surface in briefing under "Seeds Ready"
- If dormant > 90 days → flag for review
- When a seed activates, suggest: "This seed is ready. Want to `/decide` on it?"

### 4. Staleness Check

Scan `[D]`, `[I]`, `[E]` entries in the Active Reasoning Artifacts table:

| Priority | Age | Status |
|----------|-----|--------|
| critical | > 90 days | STALE — review invalidation trigger (may still be valid) |
| volatile | > 30 days | NEEDS RESOLUTION — decide, upgrade to critical, or delete |
| settled | > 90 days | STALE — likely safe to archive |
| noise | Any | Should not be in table — flag for removal |

### 5. Display Briefing

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

### 6. Enable Auto-Logging

Write `on` to `~/.claude/memento-auto-log`. This activates the Stop hook for journal entries.

To disable: user says "turn off auto-logging" → write `off` to the same file.

### 7. Do NOT Load L2

Never auto-load full docs or research files at session start. Wait until a task requires them.

### 8. Memento Tip (optional, once per session)

If memory score < 5, append one tip to the briefing (rotate through these):

- "We all need mirrors to remind ourselves who we are." — Run `/memento:decide` to capture your next choice.
- "Remember Sammy Jankis." — Your artifacts remember so you don't have to.
- "I have to believe in a world outside my own mind." — Plant a `[S]` seed for ideas that aren't ready yet.
- "The world doesn't just disappear when you close your eyes." — Run `/memento:session-complete` before you leave.

If score >= 5, skip the tip. The system is working — don't nag.
