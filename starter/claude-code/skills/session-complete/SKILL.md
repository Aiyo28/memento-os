---
name: session-complete
description: >
  Run at the end of a work session. Extracts decisions, updates NEXT.md,
  appends to session log, and optionally extracts reusable patterns.
  Trigger: "I'm done", "wrap up", "session complete", "end of session".
version: 1.0.0
---

# Session Complete

Update living docs to reflect what happened this session.

## Steps

### 1. Resolve vault directory

Determine which project vault to use:
1. Check the current repo's CLAUDE.md for a vault path or project name
2. Match to `~/knowledge-vault/Projects/{project-name}/`
3. If no match, ask the user which project this session belongs to

Create `{VAULT}/sessions/` if it doesn't exist.

### 2. Gather session changes

```bash
git diff --stat
git log --oneline -10
git status
```

### 3. Read current living docs

Read these files:
- `{VAULT}/sessions/SESSION_LOG.md`
- `{VAULT}/TODO.md` (if exists)
- `docs/_context/DECISIONS.md` (in repo, if exists)

### 4. Update NEXT.md

Read `NEXT.md` in the project root. Update based on this session:
- Move completed items out of "Continue"
- Add new items from work done / issues found
- Update "Decide" with pending decisions
- Update "Blocked" with new blockers
- Keep under 15 lines

### 5. Append session log entry

Add a new entry at the TOP of `{VAULT}/sessions/SESSION_LOG.md`:

```markdown
### {YYYY-MM-DD} — {one-line summary}

**Changed files:** {list of modified files}

- **What changed:** {1-2 sentences}
- **Decisions made:** {list or "None"}
- **Issues resolved:** {list or "None"}
- **New issues found:** {list or "None"}
- **Next up:** {what should happen next session}
```

### 6. Record decisions (if any)

If architectural or strategic decisions were made, append to `docs/_context/DECISIONS.md` (in repo). Newest first. Never remove old entries.

### 7. Extract patterns (if applicable)

Ask: "Did this session reveal a reusable pattern?"

If YES, write to `{VAULT}/patterns/{kebab-name}.md`:

```markdown
---
title: "{Pattern Name}"
type: knowledge-extract
tags: [{relevant-tags}]
status: active
summary: >
  {When you see X, do Y because Z}
---

## Context
{When does this apply?}

## Pattern
{The solution — concrete, actionable}

## Why
{Why this works}
```

If NO, skip. Most sessions won't produce patterns.

### 8. Enforce 200-line limit on SESSION_LOG.md

If over 200 lines, move oldest entries to `SESSION_LOG_ARCHIVE.md`.

### 9. Commit

Stage repo-level changes (NEXT.md, DECISIONS.md if updated). Ask user which branch to commit to.

### 10. Report

Tell the user what was updated and suggest `/clear` to start fresh.

## Criteria

| # | Criterion | Test |
|---|-----------|------|
| C1 | Session log entry references specific changes from this session | Does it mention actual files/features/decisions? |
| C2 | NEXT.md reflects what's actually next | Does it differ from pre-session state? |
| C3 | SESSION_LOG.md stays under 200 lines | `wc -l` check |
| C4 | Decisions recorded in DECISIONS.md, not just session log | If a decision was made, is it in both? |
| C5 | User was asked which branch to commit to | Was AskUserQuestion used? |
