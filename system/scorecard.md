# Memory System Scorecard

A self-evaluation methodology for grading any AI agent memory system. Score each dimension 1-10, identify your weakest areas, and use the evolution log to find solutions.

## How to Use

1. Score your system on each dimension using the rubrics below
2. Write a one-line justification for each score
3. Calculate your overall average
4. Identify dimensions scoring below 5 — these are your highest-impact improvement areas
5. Check the evolution log for entries that address those dimensions

## Scoring Rubric

| Level | Score | Meaning |
|-------|-------|---------|
| Weak | 1-3 | Dimension is absent or barely functional |
| Partial | 4-6 | Works but has known gaps or requires manual effort |
| Strong | 7-9 | Works reliably with minimal manual intervention |
| Complete | 10 | Fully automated, battle-tested, no known gaps |

## Dimensions

### 1. Persistence Durability
**Question:** Does memory survive restarts, crashes, and system changes?
**Core goal:** Memory loss prevention

| Score | Description |
|-------|-------------|
| 1-3 | Memory exists only in conversation context. Lost on restart. |
| 4-6 | Some memory persisted to disk, but inconsistently. Some types survive, others don't. |
| 7-9 | All memory types persisted to disk. Git-backed or equivalent. Survives restarts reliably. |
| 10 | All memory persisted, versioned, backed up, and recoverable from any point in history. |

### 2. Semantic Retrieval
**Question:** Can the agent find related context by meaning, not just exact match?
**Core goal:** Token efficiency

| Score | Description |
|-------|-------------|
| 1-3 | No search beyond exact filename/path. Agent must be told which file to read. |
| 4-6 | Keyword/grep search available. Finds exact matches but misses semantic relatives. |
| 7-9 | Hybrid search (keyword + embeddings). Finds related content even with different wording. |
| 10 | Full semantic search with MMR diversity, temporal decay, and configurable relevance tuning. |

### 3. Recency Awareness
**Question:** Does fresh context rank higher than stale context?
**Core goal:** Token efficiency

| Score | Description |
|-------|-------------|
| 1-3 | No recency signal. Month-old notes compete equally with today's decisions. |
| 4-6 | Manual recency (NEXT.md updated by hand). Some files dated but no automatic ranking. |
| 7-9 | Automatic recency signals (modification timestamps, session dates). Recent context loaded first. |
| 10 | Configurable temporal decay with half-life. Stale notes automatically deprioritized in retrieval. |

### 4. Compaction Handling
**Question:** Is knowledge preserved before the context window fills?
**Core goal:** Memory loss prevention

| Score | Description |
|-------|-------------|
| 1-3 | No compaction awareness. Context is silently truncated when window fills. Decisions lost. |
| 4-6 | Manual compaction skill exists but must be invoked by the user. Often forgotten. |
| 7-9 | Automatic pre-compaction extraction triggered near threshold. Key decisions saved to disk. |
| 10 | Silent, agentic pre-compaction flush. Decisions, task state, and open questions automatically persisted. |

### 5. Auto-Capture Reliability
**Question:** Does the agent write memory without being explicitly told?
**Core goal:** Memory loss prevention

| Score | Description |
|-------|-------------|
| 1-3 | Agent never writes memory unless user says "remember this." |
| 4-6 | Agent sometimes writes memory (e.g., when corrected). Inconsistent — misses most decisions. |
| 7-9 | Agent writes memory at session boundaries and after decisions. Triggered by hooks or skills. |
| 10 | Fully automated capture: pre-compaction, post-decision, session-end. No manual invocation needed. |

### 6. Cross-File Linking
**Question:** Can knowledge from Project A inform Project B?
**Core goal:** Both (token efficiency + memory loss prevention)

| Score | Description |
|-------|-------------|
| 1-3 | Each project is an island. No cross-project awareness. |
| 4-6 | Some cross-references exist but are manual. Agent doesn't discover them automatically. |
| 7-9 | Hub documents (MOCs) or tags connect projects semantically. Agent navigates cross-project knowledge. |
| 10 | Automatic cross-project pattern detection. Agent proactively surfaces relevant findings from other projects. |

### 7. Storage Scalability
**Question:** Does the system degrade as memory accumulates?
**Core goal:** Token efficiency

| Score | Description |
|-------|-------------|
| 1-3 | All memory loaded every session. Token cost grows linearly with memory size. |
| 4-6 | Tiered loading exists but no archival. Old files accumulate, indexes grow unwieldy. |
| 7-9 | Tiered loading + archival strategy. Session logs capped. Old content archived. Indexes maintained. |
| 10 | Automatic archival, index maintenance, and storage budget enforcement. System stays lean indefinitely. |

### 8. Knowledge OS Fit
**Question:** How well does the agent integrate with your knowledge base?
**Core goal:** Both

| Score | Description |
|-------|-------------|
| 1-3 | No knowledge base integration. Agent memory and your notes are separate worlds. |
| 4-6 | Basic integration (agent can read some knowledge base files). No write-back or sync. |
| 7-9 | Bidirectional: agent reads from and writes to the knowledge base. Sync hooks in place. |
| 10 | Deep integration: agent maintains knowledge base structure, enforces conventions, routes captures automatically. |

### 9. Portability / Ownership
**Question:** Can you move the system? Is there vendor lock-in?
**Core goal:** Meta

| Score | Description |
|-------|-------------|
| 1-3 | Proprietary format. Locked to one vendor. Migration would lose structure. |
| 4-6 | Mostly portable (Markdown) but some components are vendor-specific. |
| 7-9 | Plain Markdown everywhere. Git-backed. Could switch tools with minimal effort. |
| 10 | Fully portable, documented, and tested with multiple tools. Migration guide exists. |

### 10. Setup Complexity (Inverse)
**Question:** How hard is it to get running?
**Core goal:** Meta

| Score | Description |
|-------|-------------|
| 1-3 | Requires extensive configuration, multiple tools, custom scripts, and deep understanding. |
| 4-6 | Moderate setup. Starter configs help but still require significant customization. |
| 7-9 | Quick setup with sensible defaults. Starter kit gets you running with minimal changes. |
| 10 | One-command setup. Works out of the box with no customization needed. |

## Current Scores (Agentic Total Recall System)

| # | Dimension | Score | Justification | Evolution Entry |
|---|-----------|-------|---------------|-----------------|
| 1 | Persistence durability | 9/10 | Git-backed Markdown on disk. Survives everything. | — |
| 2 | Semantic retrieval | 4/10 | Grep/glob only. No vector search in agent loop. | — |
| 3 | Recency awareness | 6/10 | NEXT.md is manual. File timestamps exist but no ranking. | — |
| 4 | Compaction handling | 3/10 | Manual strategic-compact skill. Often forgotten. | [007](../evolution/007-compaction-loss.md) |
| 5 | Auto-capture reliability | 5.5/10 | session-complete exists but is manual. Criteria framework helps track quality. | [008](../evolution/008-write-discipline.md) |
| 6 | Cross-file linking | 7/10 | 4 MOC hubs, pattern extraction, wikilinks. | [004](../evolution/004-cross-project-linking.md) |
| 7 | Storage scalability | 6/10 | L0/L1/L2 tiered loading. 200-line session log cap. No auto-archival. | [001](../evolution/001-tiered-context.md) |
| 8 | Knowledge OS fit | 9/10 | Deep vault integration. Sync hook, conventions, MOCs. | [003](../evolution/003-vault-bridge.md) |
| 9 | Portability / ownership | 9/10 | Plain Markdown, git-backed. Slight skill/plugin coupling. | — |
| 10 | Setup complexity | 3/10 | Extensive: 4 hooks, 4 skills, vault setup, CLAUDE.md routing. | — |

**Overall: 6.15 / 10** (rounded to 6.5 for communication)
