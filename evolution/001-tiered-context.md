# 001 — Tiered Context Loading

**Status:** Solved
**Score impact:** Token efficiency from 4/10 → 8/10
**Date:** 2026-03-13
**Core goal:** Token efficiency

## The Problem

Every session started by loading the full project documentation: architecture specs, decision logs, tech stack details, API references. For a mature project, this consumed ~5,000 tokens before any actual work began. The agent's attention was diluted by historical context irrelevant to the current task — last month's pricing decisions competing with today's bug fix.

Worse, the agent treated all loaded context as equally important. A 2,000-token architecture document got the same weight as a 15-line continuity note, even though 90% of sessions only needed the continuity note.

## What We Tried

**Approach 1: Load everything.** Simple but wasteful. 5K+ tokens consumed on context before any work. Agent responses became less focused as context grew — answering questions with irrelevant historical detail.

**Approach 2: Load nothing.** Agent lacked project awareness. Every session started with "what project is this?" and required manual context injection. Faster startup but slower overall.

**Approach 3: Manual "read this file" instructions in CLAUDE.md.** Better, but the agent followed instructions inconsistently. Sometimes it read all files, sometimes none. No budget discipline.

## What Worked

A three-tier loading protocol with strict token budgets:

**L0 — NEXT.md (~200 tokens, ALWAYS loaded)**
Session continuity. What to continue, what to decide, what's blocked. Updated at the end of every session. Never exceeds 15 lines.

```markdown
## Continue
- Fix the auth token refresh race condition
- Verify embedding search returns top-5 results

## Decide
- Whether to use WebSocket or SSE for real-time updates

## Blocked
- Waiting on API key for production environment

Updated: 2026-03-13
```

**L1 — CLAUDE.md + _context.md (~500 tokens, ALWAYS loaded)**
Project overview. Tech stack, key rules, document index with one-sentence summaries. Enough for the agent to understand the project without loading full docs.

**L2 — Full docs (1-2K tokens each, ON DEMAND)**
Architecture specs, decision logs, detailed design docs. Loaded only when L1 indicates relevance — e.g., the agent reads the document index in `_context.md` and decides it needs `ARCHITECTURE.md` for the current task.

**The rule:** Never load L2 at session start. Read L0 + L1, decide if L2 is needed.

## Why It Works

Token budgets force prioritization. Most sessions fall into two categories:

1. **Continuation sessions (~70%):** Developer picks up where they left off. L0 (NEXT.md) is sufficient — the agent knows what's next without loading any documentation.

2. **Context-heavy sessions (~30%):** Developer starts new work that requires understanding architecture or past decisions. L1 document index lets the agent selectively load the relevant L2 doc — not all of them.

The protocol treats context like memory hierarchy in hardware: registers (L0) → cache (L1) → main memory (L2). Each level is larger but slower/costlier to access.

## Verification

Measured token usage across 20 sessions before and after implementing the protocol:

- **Before:** Average 5,200 tokens consumed on project context at session start
- **After:** Average 700 tokens (L0 + L1). L2 loaded in ~30% of sessions, adding 1-2K tokens only when needed.
- **Net savings:** 3-5K tokens per session, with no measurable decrease in task completion quality.

Agent responses were qualitatively sharper — less historical context meant less "let me also mention that three weeks ago we decided..." noise.

## Open Questions

- Should L1 include a "recently changed files" section to help the agent prioritize what to read?
- At what project size does L2 need its own tiering (L2a/L2b)?
