# Agentic Total Recall

A living field guide to building memory systems for AI coding agents — documented through real failures and fixes.

## The Problem

AI coding agents are stateless by default. Every conversation starts from zero. The solutions people share are architecture diagrams — clean, symmetrical, and useless when your agent forgets a critical decision made 20 minutes ago.

What actually breaks:
- Decisions discussed but never written down — lost when the session ends
- Context destroyed when the conversation gets too long (compaction)
- Research done in one project, invisible to every other project
- Knowledge scattered across inboxes, plans, and memory files — never found again

This repo documents one developer's journey building a memory system that solves these problems — failure by failure, fix by fix.

## Two Core Goals

Everything in this system serves one or both:

1. **Token efficiency** — load only what's needed, when it's needed. Every irrelevant token competes for the agent's attention.
2. **Memory loss prevention** — decisions, research, and context that survive session boundaries, compaction, and project switches.

## Current Score: 6.5 / 10

| # | Dimension | Score | Evolution Entry |
|---|-----------|-------|-----------------|
| 1 | Persistence durability | 9/10 | — |
| 2 | Semantic retrieval | 4/10 | — |
| 3 | Recency awareness | 6/10 | — |
| 4 | Compaction handling | 3/10 | [007](evolution/007-compaction-loss.md) |
| 5 | Auto-capture reliability | 5.5/10 | [008](evolution/008-write-discipline.md) |
| 6 | Cross-file linking | 7/10 | [004](evolution/004-cross-project-linking.md) |
| 7 | Storage scalability | 6/10 | [001](evolution/001-tiered-context.md) |
| 8 | Knowledge OS fit | 9/10 | [003](evolution/003-vault-bridge.md) |
| 9 | Portability / ownership | 9/10 | — |
| 10 | Setup complexity | 3/10 | — |

Score your own system: [system/scorecard.md](system/scorecard.md)

## Evolution Log

The core content. Each entry is a case study: problem encountered, approaches tried, what actually worked, and how it was verified.

| # | Problem | Status | Score Impact | Core Goal |
|---|---------|--------|-------------|-----------|
| [001](evolution/001-tiered-context.md) | Tiered Context Loading | Solved | Token efficiency 4→8 | Token efficiency |
| [002](evolution/002-safety-hooks.md) | Safety Hooks | Solved | Auto-capture 3→5 | Memory loss |
| [003](evolution/003-vault-bridge.md) | Vault Bridge | Solved | Knowledge OS fit 6→9 | Both |
| [004](evolution/004-cross-project-linking.md) | Cross-Project Linking | Solved | Cross-file linking 3→7 | Both |
| [005](evolution/005-scattered-captures.md) | Scattered Captures | In Progress | TBD | Memory loss |
| [006](evolution/006-decision-rot.md) | Decision Rot | Upcoming | Target 7 | Memory loss |
| [007](evolution/007-compaction-loss.md) | Compaction Loss | Upcoming | Target 7 | Memory loss |
| [008](evolution/008-write-discipline.md) | Write Discipline | Upcoming | Target 8 | Memory loss |

## How This Repo Works

**[evolution/](evolution/)** — The core. Each entry is a problem we hit, what we tried, and what worked. Numbered, chronological. Solved entries have verified results. Upcoming entries are unsolved — we're building in public.

**[system/](system/)** — A living snapshot of the current system. Updated after each evolution entry. Includes a [self-evaluation scorecard](system/scorecard.md) so you can grade your own setup.

**[starter/](starter/)** — Drop-in configs for Claude Code + Obsidian. Includes 3 safety hooks and 4 skills. See the [quickstart guide](starter/quickstart.md).

**[reference/](reference/)** — Benchmarks ([OpenClaw comparison](reference/openclaw-comparison.md)), [glossary](reference/glossary.md), and tools evaluated.

## Who This Is For

- **AI-assisted developers** frustrated by agent amnesia — any tool (Claude Code, Cursor, Windsurf, Copilot)
- **Claude Code users** who want a plug-and-play memory setup with hooks and skills
- **Anyone building agentic workflows** who wants to learn from real failure modes, not theory

## Quick Start

[starter/quickstart.md](starter/quickstart.md) — set up a working memory system with safety hooks and 4 skills.

## The Core Insight

> Architecture without write discipline is a well-organized graveyard of stale docs.

The hardest part of agent memory isn't the file structure, the retrieval algorithm, or the knowledge base integration. It's getting the agent to *write things down* at the moments that matter — before compaction, after decisions, at session end. Everything in this repo is ultimately about solving that problem.

## Contributing

Contributions welcome via issues and PRs:
- Evolution entries from your own memory system experiences
- Starter kit configs for non-Claude-Code tools (Cursor, Windsurf, Copilot)
- Scorecard rubric improvements
- Translations

Not accepted: vendor-specific plugins, paid tool integrations, AI-generated filler content.

## License

[MIT](LICENSE)
