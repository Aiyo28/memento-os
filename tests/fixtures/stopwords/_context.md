---
title: "Stopwords Fixture"
type: project-context
---

# Stopwords Fixture

Two [D] artifacts share project-specific terms (engine, vendor, breaking).
Without stopwords: overlap ≥ 2 → #1 flagged LIKELY STALE.
With .memento-stopwords filtering those terms: overlap drops below 2 → only age signal remains.

## Active Reasoning Artifacts

| # | Artifact | Priority | Date |
|---|----------|----------|------|
| 1 | `[D] Use engine vendor alpha — invalidates if engine vendor releases breaking update` | critical | 2025-08-01 |
| 2 | `[D] Engine vendor released breaking update — invalidates if migration timeline slips` | critical | 2025-09-01 |
