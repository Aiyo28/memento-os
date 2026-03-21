---
name: memento:decide
version: 2.0.0
description: >
  Composable decision skill. Core OODA loop: present options, assess confidence,
  record reasoning artifact with priority matrix. Modes: default (decide from
  current context), --research (ingest source first, then decide), --reframe
  (force perspective shift before options).
  Triggers: "decide", "should we", "which option", "evaluate", "compare",
  "research this" (with decision intent), "let's think about".
user_invocable: true
---

# /decide

One skill. Three modes. Every decision produces a reasoning artifact with a priority level.

## Setup

The vault path is configured during `memento init`. If not set, ask the user where their vault lives.

## Mode Detection

| Signal | Mode | What happens |
|--------|------|-------------|
| Decision needed from current context | `default` | Jump to OODA loop |
| URL, file, or "research this" provided | `--research` | Ingest source → extract → then OODA loop |
| "reframe", "different angle", "what am I missing" | `--reframe` | Force perspective shift → then OODA loop |

## Mode: --research (Ingest First)

Extract knowledge from the source before deciding.

### Extraction Engine (5 Fields)

1. **Core argument** — what it argues, not what it's about (1-2 sentences)
2. **Why it holds** — evidence, reasoning, mechanism (3 bullets max)
3. **Technical specifics** — numbers, code patterns, tools. "None" if none
4. **Execution pattern** — the craft move worth stealing. Omit if N/A
5. **Open questions** — what connects to existing work? What assumption might break?

After extraction, ask: "Does this inform a decision, or is it reference material?"
- Decision → continue to OODA loop
- Reference only → save to project Research/ folder, stop

## Mode: --reframe

Force a perspective shift before presenting options:

1. **Invert the question** — "What if we did the opposite?"
2. **Change the timeframe** — "What matters in 6 months vs today?"
3. **Change the stakeholder** — "What would the end user prioritize?"
4. **Expose assumptions** — "What are we assuming that might not be true?"

Then enter the OODA loop with the expanded frame.

## OODA Decision Loop (All Modes)

### Observe
- Read current project `_context.md` and `NEXT.md`
- Check existing decisions and Active Reasoning Artifacts table (avoid re-deciding settled questions)

### Orient
Present the decision landscape:
- **Options** (2-5): each with concrete pros, cons, and effort estimate
- **Recommendation**: which option and why
- **Confidence**: High (>85%) / Medium (60-85%) / Low (<60%) — show reasoning

### Decide
Ask the user to choose. Accept their decision even if it differs from recommendation.

### Act — Record the Reasoning Artifact

#### Step 1: Assess Priority

Claude proposes confidence: High / Medium / Low

Then ask the user: **"High or low impact?"**

Derive priority from the matrix:

|  | High Impact | Low Impact |
|---|---|---|
| **High Confidence** | **critical** | **settled** |
| **Medium Confidence** | **volatile** | **settled** |
| **Low Confidence** | **volatile** | **noise** |

If priority is **noise**: ask "Store it anyway or discard?" Default: discard.

#### Step 2: Record

**Inline format:**
```
`[D] <conclusion> — invalidates if <trigger> [priority] [YYYY-MM-DD]`
```

**If the decision is "not now, but later when X"** → plant a seed instead:
```
`[S] <idea> — activates when <condition> [priority] [YYYY-MM-DD]`
```
Seeds are checked at session-start. When the activation condition is met, the seed surfaces and becomes a `/decide` candidate.

**Inline only** (settled or noise): Add to `_context.md` Active Reasoning Artifacts table.
**Full artifact file** (critical or volatile): Create in `Decisions/` folder + inline entry.

### Significance Heuristic

| Signal | Likely Priority | Storage |
|--------|----------------|---------|
| Affects architecture or tech stack | critical | Full file + inline |
| Affects only current task | settled | Inline only |
| Affects multiple projects | critical | Full file + inline |
| Easily reversible | settled | Inline only |
| Uncertain but foundational | volatile | Inline (review next session) |
