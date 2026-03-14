# OpenClaw Memory System Comparison

A side-by-side analysis of our memory system against OpenClaw's 4-layer architecture. This comparison drove several evolution entries (006-008) and shaped our improvement roadmap.

## What Is OpenClaw?

OpenClaw is an open-source agentic memory system built on four layers:

1. **Live session context** — JSONL transcript in the context window (volatile)
2. **Daily logs** — append-only `memory/YYYY-MM-DD.md` files (durable)
3. **MEMORY.md** — curated long-term store for decisions, preferences, facts (core)
4. **Semantic vector search** — SQLite + embeddings with hybrid BM25 fallback (intelligent)

Its key innovation is a **silent pre-compaction flush**: when the session approaches the context window limit, a hidden agentic turn saves durable facts to disk before compaction destroys them.

## Dimension Comparison

| Dimension | Our System | OpenClaw | Who's Ahead |
|-----------|-----------|----------|-------------|
| Persistence durability | 9/10 — Git-backed Markdown | 9/10 — Markdown files | Tie |
| Semantic retrieval | 4/10 — Grep/glob only | 7/10 — SQLite + embeddings + BM25 | OpenClaw |
| Recency awareness | 6/10 — Manual NEXT.md | 7.5/10 — Configurable temporal decay | OpenClaw |
| Compaction handling | 3/10 — Manual skill | 7/10 — Silent pre-compaction flush | OpenClaw |
| Auto-capture reliability | 5.5/10 — Manual session-complete | 5/10 — LLM-dependent | Ours (slightly) |
| Cross-file linking | 7/10 — 4 MOC hubs + patterns | 3.5/10 — Isolated chunks | Ours |
| Storage scalability | 6/10 — Tiered loading, 200-line cap | 5.5/10 — Daily files accumulate | Ours |
| Knowledge OS fit | 9/10 — Deep vault integration | 8/10 — Obsidian/Notion sync | Ours |
| Portability / ownership | 9/10 — Plain Markdown | 9.5/10 — No vendor coupling | OpenClaw (slightly) |
| Setup complexity | 3/10 — Extensive config needed | 4/10 — Needs tuning | OpenClaw (slightly) |

**Overall: Ours 6.15/10 vs. OpenClaw 6.6/10**

## Where We're Ahead

### Cross-Project Linking (7 vs 3.5)
Our MOC (Map of Content) system creates semantic hubs that connect project silos. OpenClaw treats each memory chunk as isolated — no native graph, no hub nodes, no cross-project discovery. See [evolution/004](../evolution/004-cross-project-linking.md).

### Knowledge OS Fit (9 vs 8)
Our vault bridge — sync hooks, _context.md L1 files, routing table in global CLAUDE.md — creates deep integration between agent memory and the knowledge base. OpenClaw supports Obsidian/Notion sync but doesn't prescribe a loading protocol. See [evolution/003](../evolution/003-vault-bridge.md).

### Token Efficiency via Tiered Loading
Our L0/L1/L2 protocol saves 3-5K tokens per session by loading context in tiers. OpenClaw loads context more aggressively, relying on retrieval quality rather than loading discipline. See [evolution/001](../evolution/001-tiered-context.md).

## Where OpenClaw Is Ahead

### Compaction Handling (7 vs 3)
OpenClaw's silent pre-compaction flush is its strongest feature. When context approaches the limit, a hidden agentic turn writes durable facts to disk before compaction destroys them. Our system relies on manual invocation of the strategic-compact skill — which means knowledge is lost whenever the user forgets. See [evolution/007](../evolution/007-compaction-loss.md) (upcoming).

### Semantic Retrieval (7 vs 4)
OpenClaw uses SQLite + embeddings with hybrid BM25 fallback and configurable MMR diversity (`lambda` parameter). Our system uses grep/glob — finds exact matches but misses semantically related content with different wording.

### Recency Awareness (7.5 vs 6)
OpenClaw has configurable temporal decay with a half-life parameter, so stale notes don't outrank recent context. Our system has NEXT.md (manual) and file timestamps, but no automatic recency ranking in retrieval.

## The Core Insight

**Architecture vs. discipline.** Our system has better *structure* (MOCs, tiered loading, vault bridge, safety hooks). OpenClaw has better *write discipline* (automatic pre-compaction flush, session-end capture).

Structure without write discipline is a well-organized graveyard of stale docs. The best architecture in the world doesn't help if the agent never writes to it.

This insight drives our improvement roadmap:
- [006 — Decision Rot](../evolution/006-decision-rot.md): Graduate decisions from logs to durable storage
- [007 — Compaction Loss](../evolution/007-compaction-loss.md): Build pre-compaction extraction
- [008 — Write Discipline](../evolution/008-write-discipline.md): Make session-complete automatic

## Lessons Taken

1. **Pre-compaction flush is non-negotiable.** If your system doesn't save knowledge before compaction, you will lose decisions. Build this first.
2. **Semantic search is nice-to-have, not critical.** Our grep-based system works because tiered loading means we rarely need to search — we load the right context by protocol. Vector search helps at scale but isn't the bottleneck.
3. **Cross-project linking is underrated.** OpenClaw's weakest dimension is our strongest. Patterns extracted from one project and applied to another are among the highest-value knowledge artifacts.
4. **Simple beats clever.** OpenClaw's SQLite + embeddings pipeline is technically impressive but adds setup complexity. Our plain-Markdown approach with MOC hubs achieves 80% of the cross-linking benefit with 20% of the complexity.
