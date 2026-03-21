---
name: memento:session-complete
version: 4.0.0
description: >
  Run at end of session OR before compaction. Extracts reasoning artifacts
  with priority matrix, updates NEXT.md, appends to session log.
  Two modes: end-of-session (default) and pre-compaction (--compact).
  Triggers: "done", "wrap up", "session complete", "end of session",
  "about to compact", "context getting long".
user_invocable: true
---

# /session-complete

Extract what matters. Discard the rest. Update continuity docs.

## Mode Detection

| Signal | Mode | Behavior |
|--------|------|----------|
| End of session | `default` | Full extraction + NEXT.md + session log |
| Before compaction | `--compact` | Quick extraction + NEXT.md only (speed matters) |

## Steps

### 1. Scan Conversation for Reasoning Artifacts

Extract:
- **Decisions made** → `[D]` artifacts
- **Insights learned** → `[I]` artifacts
- **Errors resolved** → `[E]` artifacts with root cause
- **Ideas deferred with conditions** → `[S]` seeds (forward-looking ideas that surface when a condition is met)

For each, draft the inline format:
```
`[D] <conclusion> — invalidates if <trigger> [priority] [YYYY-MM-DD]`
`[I] <insight> — invalidates if <condition> [priority] [YYYY-MM-DD]`
`[E] <what went wrong> — root cause: <why> [settled] [YYYY-MM-DD]`
`[S] <idea> — activates when <condition> [priority] [YYYY-MM-DD]`
```

Seeds are ideas that came up but weren't actionable yet. Look for "maybe later", "when we have X", "not now but eventually".

Where `[priority]` is derived from:
- Claude proposes **confidence** (high/medium/low)
- Ask user: **"High or low impact?"**
- Matrix: high confidence + high impact = critical, low + low = noise, etc.
- `[E]` errors default to **settled**; once resolved → **noise**
- In `--compact` mode: skip impact prompt — default all to `settled`

### 2. Confirm with User

Present extracted artifacts: "I found these reasoning artifacts: [list]. Anything to add or correct?"

For each artifact, confirm impact: **"High or low impact?"**

In `--compact` mode: skip impact confirmation, present briefly.

### 3. Write Artifacts

**Inline artifacts** → add to `_context.md` Active Reasoning Artifacts table
**Full artifact files** → create in `Decisions/` for critical/volatile artifacts
**Error entries** → inline to `_context.md` (settled priority)

### 4. Update NEXT.md

- Move completed items out of "Continue"
- Add new items from this session
- Update "Decide" with pending decisions
- Update "Blocked" with new blockers
- Update date
- Keep under 15 lines

### 5. Append Session Log (default mode only)

Skip in `--compact` mode.

Add at the TOP of `Sessions/SESSION_LOG.md`:

```markdown
### {YYYY-MM-DD} — {most important decision or outcome}

**Artifacts produced:** {count} ([D]: {count}, [I]: {count}, [E]: {count}, [S]: {count})
**Changed:** {1-2 sentences on what changed}
**Next:** {what should happen next session}
```

### 6. Enforce Limits

- SESSION_LOG.md: move entries beyond 200 lines to SESSION_LOG_ARCHIVE.md
- _context.md Active Reasoning Artifacts table: cap at 24 entries (Kobe). When over cap, evict by priority: noise first → settled → volatile. **Never auto-evict critical artifacts.** Archive evicted artifacts to `Decisions/` folder.

### 7. Show Progress

After writing artifacts, display the delta:

```
Session captured: {n} artifacts ([D]: {d}, [I]: {i}, [E]: {e}, [S]: {s})
Memory: {old_score} → {new_score}/10 ({delta})
```

Milestone messages (show once, when threshold first crossed):
- 5 total artifacts: "Your memory is taking shape."
- First critical artifact: "A foundational decision. This one sticks."
- 10 total artifacts: "Pattern recognition unlocked — your agent learns from the past."
- First seed activated: "A seed you planted just sprouted. The vault remembered for you."
- 20 total artifacts: "Approaching Kobe cap. Quality over quantity now."
