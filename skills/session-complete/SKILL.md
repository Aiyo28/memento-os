---
name: memento:session-complete
version: 4.3.0
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
- **Errors resolved** → `[E]` artifacts with root cause + fix
- **Ideas deferred with conditions** → `[S]` seeds (forward-looking ideas that surface when a condition is met)

For each, draft the inline format:
```
`[D] <conclusion> — invalidates if <trigger> [priority] [YYYY-MM-DD]`
`[I] <insight> — invalidates if <condition> [priority] [YYYY-MM-DD]`
`[E] <what went wrong> — root cause: <why> — fix: <what solved it> [settled] [YYYY-MM-DD]`
`[S] <idea> — activates when <condition> [priority] [YYYY-MM-DD]`
```

**Optional expiry**: If the conclusion is time-bound (free tier, trial, beta, seasonal, "for now"), add `— expires: YYYY-MM-DD` before priority. Do NOT add expiry to foundational architecture decisions.

Seeds are ideas that came up but weren't actionable yet. Look for "maybe later", "when we have X", "not now but eventually".

Where `[priority]` is derived from:
- Claude proposes **confidence** (high/medium/low)
- Ask user: **"High or low impact?"**
- Matrix: high confidence + high impact = critical, low + low = noise, etc.
- `[E]` errors default to **settled**; once resolved → **noise**
- In `--compact` mode: skip impact prompt — default all to `settled`

### 2. Contradiction Check

Before confirming, scan existing artifacts in `_context.md` for contradictions with new ones:

1. For each new `[D]` or `[I]`, grep the Active Reasoning Artifacts table for overlapping topics
2. If a new artifact **supersedes** an existing one (same domain, updated conclusion):
   - Mark the old artifact for eviction to `Decisions/` with `status: superseded`
   - Show: `"#X superseded: <old> → <new>"`
3. If a new artifact **contradicts** an existing one (conflicting conclusions, both may be valid):
   - Flag: `"Conflict: new <artifact> vs existing #X — keep both, or resolve?"`
4. If no overlap → proceed normally

In `--compact` mode: auto-supersede without prompting. Flag conflicts only.

### 3. Confirm with User

Present extracted artifacts: "I found these reasoning artifacts: [list]. Anything to add or correct?"

Show supersessions and conflicts from Step 2.

For each artifact, confirm impact: **"High or low impact?"**

In `--compact` mode: skip impact confirmation, present briefly.

### 4. Write Artifacts

Route each artifact to the correct `_context.md` Active Reasoning Artifacts table:

| Condition | Target |
|-----------|--------|
| Project-specific | `Projects/{name}/_context.md` |
| Cross-project engineering | `Projects/_context.md` |
| Personal (hobby, health, learning) | `Personal/_context.md` |
| Business-specific | `Business/{name}/_context.md` |
| Cross-business | `Business/_context.md` |
| General cross-domain | `Knowledge/_context.md` |
| Ambiguous | Ask user |

**Full artifact files** → create in `Decisions/` for critical/volatile artifacts
**Kobe cap** (24) applies per `_context.md` — check each target independently

### 5. Update NEXT.md

- Move completed items out of "Continue"
- Add new items from this session
- Update "Decide" with pending decisions
- Update "Blocked" with new blockers
- Update date
- Keep under 15 lines

### 6. Append Session Log (default mode only)

Skip in `--compact` mode.

Add at the TOP of `Sessions/SESSION_LOG.md`:

```markdown
### {YYYY-MM-DD} — {most important decision or outcome}

**Artifacts produced:** {count} ([D]: {count}, [I]: {count}, [E]: {count}, [S]: {count})
**Changed:** {1-2 sentences on what changed}
**Next:** {what should happen next session}
```

### 7. Enforce Limits

- SESSION_LOG.md: move entries beyond 200 lines to SESSION_LOG_ARCHIVE.md
- _context.md Active Reasoning Artifacts table: cap at 24 entries (Kobe). When over cap, evict by priority: noise first → settled → volatile. **Never auto-evict critical artifacts.** Archive evicted artifacts to `Decisions/` folder with appropriate status: `superseded` (replaced by newer decision), `archived` (no longer relevant), or keep `active` if the full file is for reference depth only.
- Eviction also triggers for: `embedded` artifacts (decision is in code, not referenced in 30+ days), `resolved` errors (learning extracted into a `[D]`), dormant `[S]` seeds (not activated after 90 days).

### 8. Peer Card Update (optional, default mode only)

If this session revealed a new communication preference, decision pattern, or context-dependent trait that isn't already in the Peer Card (`People/Self.md`):
- Propose the update: `"Peer Card update: add <trait> to <section>?"`
- Only update if user confirms
- Add evidence and date to the Reflection Log table

Skip if: no new behavioral patterns observed, or in `--compact` mode.

### 9. Show Progress

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
