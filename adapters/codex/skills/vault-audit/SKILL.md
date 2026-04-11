---
name: vault-audit
version: 1.1.0
description: >
  Vault health check. Validates structure, detects stale reasoning artifacts
  by priority level, processes inbox, and suggests cleanup.
  Triggers: "vault audit", "check vault", "clean up vault", "process inbox",
  "what's stale", "vault health".
user_invocable: true
---

# /vault-audit

Check structure. Flag staleness. Process inbox. Suggest cleanup.

## Steps

### 1. Structure Check

Verify each project under `Projects/` has:
- `_context.md` (required)
- Active Reasoning Artifacts table in `_context.md`
- Subfolders created on-demand (don't flag missing empty folders)

### 2. Staleness Scan

For each project `_context.md`, check Active Reasoning Artifacts table:

**Expiry check (first — overrides priority-based staleness):**
- Scan for `expires: YYYY-MM-DD` in artifact text
- If past expiry date → flag as **EXPIRED** regardless of priority
- Show: `"EXPIRED: #X — <artifact summary> (expired YYYY-MM-DD). Still valid?"`

**Priority-based staleness (for artifacts without expiry):**

| Priority | Age | Action |
|----------|-----|--------|
| critical | > 90 days | Flag for review — ask if invalidation trigger has fired |
| volatile | > 30 days | Flag for resolution — upgrade to critical or delete |
| settled | > 90 days | Suggest archiving to Decisions/ folder |
| noise | Any age | Flag for immediate removal |
| superseded | Any age | Should already be evicted — flag if still in L1 |

### 3. Inbox Processing

Check `_inbox/` for unprocessed items. For each:
- Identify type (research, note, decision, reference)
- Route to correct project and subfolder
- Add proper frontmatter
- Update project `_context.md` document index

### 4. Fluff Detection

Flag documents that may be stale or redundant:
- Files with `status: draft` older than 30 days
- Duplicate content across projects
- Documents with no wikilinks (orphaned)
- MOC files with no backlinks (orphaned hubs)
- `experiment-context` files past their teardown date
- `[S]` seeds dormant > 90 days (not activated, not decided)

### 5. Report

```
## Vault Audit — {date}

**Structure:** {OK or issues found}
**Stale artifacts:** {count by priority level}
**Inbox:** {count processed, count remaining}
**Suggestions:** {cleanup actions}
```
