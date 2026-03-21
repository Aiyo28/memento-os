---
name: process-inbox
description: >
  Process raw captures from the knowledge vault _inbox/ into proper locations.
  Triggers: "process inbox", "process captures", "clean inbox", "sort inbox".
version: 1.0.0
---

# Process Inbox

Route raw captures from `~/knowledge-vault/_inbox/` to proper vault locations with correct frontmatter.

## Step 1 — Scan Inbox

List all files in `~/knowledge-vault/_inbox/` (excluding `.gitkeep`).
If empty, report "Inbox is empty." and stop.

## Step 2 — Classify Each File

Read content and determine destination:

| Content type | Type field | Destination |
|---|---|---|
| Transferable insight, not tied to one project | knowledge-extract | Knowledge/ |
| Reusable pattern (cross-project) | knowledge-extract | Knowledge/patterns/ |
| Research for a specific project | research | Projects/{name}/Research/ |
| Working note for a project | note | Projects/{name}/Notes/ |
| Decision record | decision | Projects/{name}/Decisions/ |

If destination is ambiguous, ask the user — don't guess.

## Step 3 — Process Each File

1. Generate proper filename (sentence case with spaces)
2. Add frontmatter:

```yaml
---
title: "<descriptive title>"
type: <classified type>
project: "<project-slug>"
tags: [<3-7 tags, nested domain/subtopic format>]
created: <date>
updated: <today>
status: draft
confidence: low
language: en
summary: >
  <One paragraph for LLM consumption>
---
```

3. Preserve original content
4. Write to destination
5. Delete from `_inbox/`

## Step 4 — Update Indexes

If a file was placed in a project folder, update that project's `_context.md` document index.

## Step 5 — Handle Duplicates

If a capture overlaps with an existing doc on the same topic, append insights to the existing doc rather than creating a duplicate.

## Step 6 — Report

```markdown
## Inbox Processing Complete

| File | Destination | Type | Project |
|------|-------------|------|---------|
| ... | ... | ... | ... |

### Skipped
- {files too raw to classify}
```

## Criteria

| # | Criterion | Test |
|---|-----------|------|
| C1 | Files landed in correct destination per routing table | Path matches type/project? |
| C2 | All 10 frontmatter fields present and non-empty | Check each output file |
| C3 | Original deleted from _inbox/ after processing | Source file absent? |
| C4 | Ambiguous files were not silently routed | User asked or file left with comment? |
| C5 | No duplicate files created on same topic | Checked for existing docs? |
