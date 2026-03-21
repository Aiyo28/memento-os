---
name: memento:stats
description: "Show memory score, artifact breakdown, and session streak. Your memory system's vital signs."
allowed-tools:
  - Read
  - Bash
  - Glob
  - Grep
---

# /memento stats

Show how your memory system is doing — not a report, a pulse check.

## Flow

### 1. Gather Data

Read `_context.md` Active Reasoning Artifacts table. Count:
- Total artifacts
- By type: `[D]`, `[I]`, `[E]`, `[S]`
- By priority: critical, volatile, settled, noise
- Stale count (settled > 90 days, volatile > 30 days)
- Seeds with met activation conditions

Read `Sessions/SESSION_LOG.md` if it exists:
- Total sessions logged
- Last session date
- Session streak (consecutive days with sessions)

Read `NEXT.md`:
- Pending items count
- Last updated date

### 2. Calculate Memory Score

Score out of 10, weighted:

| Dimension | Weight | How to score |
|-----------|--------|-------------|
| Has artifacts | 2 | 0 artifacts = 0, 1-5 = 1, 6-15 = 1.5, 16-24 = 2 |
| Has critical decisions | 2 | 0 critical = 0, 1-3 = 1, 4+ = 2 |
| Recency | 2 | NEXT.md updated today = 2, this week = 1.5, this month = 1, older = 0.5 |
| No stale artifacts | 1.5 | 0 stale = 1.5, 1-3 stale = 1, 4+ stale = 0 |
| Seeds planted | 1 | 0 seeds = 0, 1-3 = 0.5, 4+ = 1 |
| Session streak | 1.5 | 0 sessions = 0, 1-2 = 0.5, 3-5 = 1, 6+ = 1.5 |

### 3. Display

```
## Memento — {Project Name}

  Score:     {X.X} / 10  {bar: ████░░░░░░}
  Artifacts: {total} ([D]: {n}  [I]: {n}  [E]: {n}  [S]: {n})
  Priority:  {critical} critical  {volatile} volatile  {settled} settled
  Sessions:  {total} logged  |  streak: {n} days
  Stale:     {n} artifacts need review
  Seeds:     {n} planted  |  {n} ready to activate

  Last session: {date}
  NEXT.md:      {date}
```

If score increased since last check, show: `Score: 7.2 / 10 (↑ 0.8 from last check)`

### 4. Suggestions (if score < 7)

Based on lowest-scoring dimension, suggest ONE action:
- No artifacts → "Run /decide on your next choice to start building memory"
- No critical decisions → "Your foundational decisions should be marked critical"
- Stale artifacts → "Run /vault-audit to review stale items"
- No seeds → "When you defer an idea, capture it as [S] with an activation condition"
- No recent sessions → "Run /session-start to reconnect with your project"
