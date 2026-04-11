---
title: "Example Project Context"
type: project-context
project: example-project
tags: []
created: YYYY-MM-DD
updated: YYYY-MM-DD
status: active
confidence: high
language: en
repo_path: ""
repo_docs_path: ""
summary: >
  Replace with a one-paragraph project summary for LLM consumption. Describe
  what the project does, its current state, and the key technical decisions
  made so far. An agent reading only this field should understand whether to
  load more context from this project.
---

# Example Project

> One-sentence description of what this project does.

## Key Numbers

| Metric | Value | Confidence |
|--------|-------|------------|
| Status | Planning / Active / Maintenance | high |
| Tech stack | [list key technologies] | high |
| Target | [who is this for] | high |

## Active Reasoning Artifacts

<!-- Kobe cap: 24 artifacts. Evict: noise → settled → volatile. Never evict critical. -->

| # | Artifact | Priority | Date |
|---|----------|----------|------|
| 1 | `[D] example decision — invalidates if conditions change [settled] [YYYY-MM-DD]` | settled | YYYY-MM-DD |

## Repo Knowledge Map
<!-- Delete this section for vault-only projects (no code repo) -->

| Layer | Path | What's there |
|-------|------|-------------|
| L0 | `NEXT.md` | Session continuity |
| L1 | `docs/_context/BRIEF.md` | Project overview |
| L2 | `docs/ARCHITECTURE.md` | System design |
| L2 | `docs/DECISIONS.md` | Decision log |

## Document Index

| Document | Location | Description | Status |
|----------|----------|-------------|--------|
| *(add research docs as they're created)* | | | |

## Open Questions
- [List unanswered questions that need research or decisions]

## Related
- [[MOC — relevant hub]]
