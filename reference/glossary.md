# Glossary

Terms used throughout this project, defined for clarity.

**Auto-capture** — The agent writing memory to disk without explicit user instruction. The reliability of auto-capture is the single biggest differentiator between memory systems that work and ones that don't.

**Compaction** — When a conversation exceeds the context window limit, the system summarizes older content to make room. Valuable detail is lost unless explicitly saved before compaction occurs.

**Context window** — The agent's working memory, measured in tokens. Everything the agent can "see" at once: system prompt, conversation history, file contents, tool results. Typically 128K-1M tokens depending on model.

**Decision graduation** — The process of promoting decisions from ephemeral locations (session logs, conversation) to durable storage (DECISIONS.md, typed memory files). Decisions that aren't graduated are eventually lost.

**Decision rot** — Decisions made during a session that are never recorded durably. They exist in conversation context, maybe in a session log, but never reach a structured, retrievable location. Over time, they're forgotten and re-made (often differently).

**Evolution entry** — A documented case study in this repo. Each entry describes a problem encountered, approaches tried, what actually worked, and how it was verified. The core content format of Agentic Total Recall.

**Knowledge vault** — An external knowledge base (Obsidian, Notion, or any Markdown-based system) connected to the AI agent. Stores cross-project knowledge, research, patterns, and context that persists beyond any single conversation.

**L0 / L1 / L2** — Tiered context loading protocol. L0 (~200 tokens) is always loaded (NEXT.md — session continuity). L1 (~500 tokens) is always loaded (CLAUDE.md + _context.md — project overview). L2 (~1-2K tokens each) is loaded on demand (full docs — only when L1 indicates relevance). The rule: never load L2 at session start.

**Memory loss** — Information that existed in the agent's context window but was never persisted to disk. When the session ends or context compacts, it's gone. The primary failure mode this project addresses.

**MOC (Map of Content)** — A hub document in the knowledge vault that links related notes across projects. MOCs don't hold content — they hold connections. Reading a MOC lets the agent discover related work without loading every project.

**Pattern extraction** — Identifying reusable solutions from specific project experiences and saving them in a standard format (Context / Pattern / Why). Extracted patterns are stored in `Knowledge/patterns/` for cross-project reuse.

**Scorecard** — The 10-dimension self-evaluation methodology defined in this project. Each dimension is scored 1-10 with specific rubrics. Used to identify the weakest aspects of any memory system and prioritize improvements.

**Session boundary** — The gap between two agent conversations. Any information not persisted to disk before the session ends is lost at this boundary. Session-complete skills and hooks exist to capture knowledge at this critical moment.

**Token efficiency** — Minimizing the number of tokens spent on irrelevant, stale, or redundant context. Every token loaded into the context window competes for the agent's attention. Efficient systems load only what's needed for the current task.

**Write discipline** — The practice of proactively writing memory to disk at critical moments: before compaction, after decisions, at session end. The core insight of this project: architecture without write discipline is a well-organized graveyard of stale docs.

**Write trigger** — An event that causes memory to be saved. Can be manual (user says "remember this"), hook-based (PreToolUse/PostToolUse), skill-based (session-complete, strategic-compact), or automatic (pre-compaction flush). The progression from manual to automatic write triggers is the maturity curve of a memory system.
