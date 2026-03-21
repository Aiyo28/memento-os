---
name: knowledge
version: 1.0.0
description: >
  Unified research extraction. Use when asked to "research this", "extract from",
  "analyze this article/repo/video/PDF", or given a URL/file with intent to learn.
  Two modes: --deep (vault save) / --quick (inline, no save).
---

# Knowledge

One skill. Two modes. One extraction engine. Any source type.

## Mode Detection

- Standalone research request → `--deep` (saves to vault)
- Active task in progress → `--quick` (inline context block)
- User can override with explicit `--deep` or `--quick`

## Source Detection

| Input | Type | Method |
|---|---|---|
| github.com/* | repo | Fetch README, deps, tree, 2-3 key files |
| youtube.com/watch* | video | Transcript, description, chapters |
| *.pdf file | pdf | Parse, then extraction engine |
| Other URL | article | Fetch, strip nav/ads, keep body |
| Multiple inputs | batch | Process each, synthesize if related |

## Extraction Engine (5 Fields)

### Core argument
One or two sentences. What it *argues*, not what it's *about*.

### Why it holds
Three bullet points max. Evidence, reasoning, or mechanism.

### Technical specifics
Concrete detail: numbers, code patterns, methods, tools. If none, write "none."

### Execution pattern
How they built or presented this. The craft move worth stealing. Omit if not applicable.

### Open questions / reaction
What connects to existing work? What's wrong? What assumption might not hold?

## Value Gate (--deep only)

Before saving, evaluate honestly:
1. Does this introduce a novel technique or insight?
2. Would a future session benefit from having this doc?

If both "no" → present in conversation only. No vault save.

## Output

### --deep (vault save)

```markdown
---
title: [Concept name]
source: [URL or filepath]
type: research
date: YYYY-MM-DD
tags: [2-4 tags]
project: [slug or empty]
status: active
confidence: [high|medium|low]
summary: >
  [2-4 sentences for vault index]
---

## Core argument
## Why it holds
## Technical specifics
## Execution pattern
## Open questions / my reaction

## One-line retrieval hook
[15-word summary for search and cold recall]
```

Save to:
- Project-linked: `~/knowledge-vault/Projects/{name}/Research/{kebab-title}.md`
- General: `~/knowledge-vault/Knowledge/{kebab-title}.md`

### --quick (inline)

```
[SOURCE: url or filename]
Relevant to current task: [what applies now]
Key technical detail: [the one thing worth knowing]
Watch out for: [anything outdated or misleading]
```

Four lines. No saving.

## Criteria

| # | Criterion | Test |
|---|-----------|------|
| C1 | Actionable value extracted | Produced ≥1 actionable item? |
| C2 | Core argument reconstructable from note alone | Without source, can you answer "what + why"? |
| C3 | Technical specifics are specific | Contains ≥1 number, method, or tool name? |
| C4 | Field boundaries respected | Core argument free of evidence? --quick has 4 lines? |
| C5 | Cold retrieval works | One-line hook uniquely identifies the note? |
