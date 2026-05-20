---
title: "Clean Fixture"
type: project-context
---

# Clean Fixture

## Active Reasoning Artifacts

| # | Artifact | Priority | Date |
|---|----------|----------|------|
| 1 | `[D] Use Postgres for primary store — invalidates if write volume exceeds 10k/sec` | critical | 2026-05-01 |
| 2 | `[I] Schema migrations are the dominant deploy risk — invalidates when zero-downtime migration tooling lands` | volatile | 2026-05-02 |
| 3 | `[E] OAuth refresh failed under load — root cause: token cache thundering herd — fix: per-key mutex around refresh` | settled | 2026-05-03 |
| 4 | `[S] Add a read-replica layer — Activation: when p95 read latency exceeds 200ms for one week` | volatile | 2026-05-04 |
| 5 | `[S] Move analytics to ClickHouse — activates when daily ingest crosses 1B rows` | settled | 2026-05-05 |
