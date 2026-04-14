<p align="center">
  <img src="assets/decisions.gif" alt="Memento OS — your AI's tattoo memory" width="480">
</p>

<h3 align="center">Store conclusions, not notes.</h3>

<p align="center">
  <em>Unlike the guy in Memento, your AI actually remembers correctly — and knows when to forget.</em>
</p>

<p align="center">
  <a href="#install">Install</a> · <a href="#how-it-works">How It Works</a> · <a href="#reasoning-artifacts">Artifacts</a> · <a href="#works-with">Multi-AI</a> · <a href="#obsidian">Obsidian</a>
</p>

---

**Memento OS** is a persistent memory plugin for AI coding tools. Every conclusion is stored as a reasoning artifact with an invalidation trigger — your agent remembers what matters and knows when to re-evaluate.

## The Problem

AI agents are stateless. Every session starts from zero.

- Decisions discussed → **gone when the session ends**
- Context compressed → **compaction kills memory**
- Research done once → **invisible next session**
- "We chose Supabase" → **nobody remembers why, or when that stops being true**

## Install

```bash
/plugin install memento-os
```

Then:

```bash
/memento:init
```

Three questions. Thirty seconds. Your first decision captured.

## How It Works

Five skills. One loop.

| Skill | Phase | What it does |
|-------|-------|-------------|
| `/memento:grill-me` | **Think** | Stress-test your plan across 6 dimensions |
| `/memento:decide` | **Decide** | OODA loop → `[D]` artifacts or `[S]` seeds |
| `/memento:session-complete` | **Capture** | Extract all artifacts from the conversation |
| `/memento:session-start` | **Recall** | Load context, surface decisions, check seeds |
| `/memento:vault-audit` | **Maintain** | Health check, staleness scan, inbox processing |

**Hooks** run automatically — Stop captures artifacts on session end, PreCompact saves before compression.

**Commands:** `/memento:init` (setup) · `/memento:stats` (memory score + streaks)

## Reasoning Artifacts

The atomic unit. Not a note — a pre-computed conclusion with an expiration condition.

```
[D] Use Supabase over Firebase — invalidates if Firebase adds RLS            [critical]
[I] MV3 service workers die after 30s — invalidates if Chrome changes policy [settled]
[E] Deployed without testing webhooks — root cause: no staging env — fix: added pre-deploy checklist [settled]
[S] Consider caching layer — activates when: API p95 > 200ms                [volatile]
```

| Prefix | Type | Purpose |
|--------|------|---------|
| `[D]` | Decision | Choice between alternatives — has invalidation trigger |
| `[I]` | Insight | Reusable conclusion — survives the session that produced it |
| `[E]` | Error | Mistake with root cause + fix — drops to noise once learning extracted |
| `[S]` | Seed | Forward-looking idea — activates when conditions are met |

### Priority Matrix

Confidence (Claude proposes) × Impact (you confirm):

|  | High Impact | Low Impact |
|---|---|---|
| **High Confidence** | **critical** — pinned | **settled** — evict first |
| **Medium** | **volatile** — needs resolution | **settled** |
| **Low Confidence** | **volatile** | **noise** — discard |

Cap: 24 artifacts per context. Eviction: noise → settled → volatile → critical (never).

## Works With

Same vault, same artifacts, different integration depth.

| Tool | Tier | Install |
|------|------|---------|
| **Claude Code** | Full Plugin — 5 skills, 2 hooks, 2 commands | `/plugin install memento-os` |
| **Codex** (OpenAI) | Full Skills — AGENTS.md + 5 skills | [adapters/codex/](adapters/codex/) |
| **Cursor** | Rules — conventions + workflow | [adapters/cursor/](adapters/cursor/) |
| **Windsurf** | Rules | [adapters/windsurf/](adapters/windsurf/) |
| **Cline** | Rules | [adapters/cline/](adapters/cline/) |
| **Gemini** | Rules — GEMINI.md | [adapters/gemini/](adapters/gemini/) |
| **Aider** | Manual — CONVENTIONS.md | [adapters/aider/](adapters/aider/) |
| **Continue** | Manual — config snippet | [adapters/continue/](adapters/continue/) |

## Obsidian

Memory is plain markdown. Point [Obsidian](https://obsidian.md) at your vault for graph view, backlinks, and search.

```
knowledge-vault/
├── Projects/
│   ├── _context.md          # Cross-project decisions
│   └── my-app/
│       ├── _context.md      # Project artifacts (the brain)
│       ├── NEXT.md          # Session continuity
│       ├── Decisions/       # Full decision records
│       └── Sessions/        # Session log
├── Personal/
│   └── _context.md          # Hobbies, health, learning artifacts
├── Business/
│   └── _context.md          # Cross-business decisions
├── Knowledge/
│   ├── _context.md          # General cross-domain insights
│   └── MOC — Patterns.md    # Map of Content hubs
├── People/
│   └── Self.md              # Your peer card
└── _meta/
    └── conventions.md       # Vault rules
```

Every area has its own `_context.md` with an artifacts table. Artifacts route automatically to the right context based on domain. Tags: `tech/`, `business/`, `product/`, `ai/`, `personal/` — nested as `domain/subtopic`. Folders created on demand.

## Before / After

**Without** (session 5):
```
> What auth approach did we decide on?
I don't have context on previous decisions. Could you remind me?
```

**With** (session 5):
```
## Session Briefing — My Project
Memory: 6.8/10 | 14 artifacts | 2 seeds | streak: 5

### Active Decisions
[D] OAuth via Supabase Auth — invalidates if rate limits hit [critical]
[D] Mobile-first, no desktop v1 — invalidates if desktop demand >30% [critical]

### Seeds Ready
[S] Consider Redis caching — activates when: API p95 > 200ms ← CONDITION MET
```

## Why I Built This

I kept reaching the same conclusions across sessions — same reasoning, same answer, different day. The vault was full of notes, but the actual decisions were buried in noise.

So I flipped it: capture *only* conclusions. Each one with a condition that makes it invalid — so the system knows when to question itself instead of blindly trusting old decisions.

That shift — from "save everything" to "save only conclusions" — turned out to be the entire product.

<details>
<summary><strong>Evolution Log</strong> — how we got here, failure by failure</summary>

| # | Problem | Status |
|---|---------|--------|
| [001](evolution/001-tiered-context.md) | Tiered Context Loading | Solved |
| [002](evolution/002-safety-hooks.md) | Safety Hooks | Solved |
| [003](evolution/003-vault-bridge.md) | Vault Bridge | Solved |
| [004](evolution/004-cross-project-linking.md) | Cross-Project Linking | Solved |
| [005](evolution/005-scattered-captures.md) | Scattered Captures | In Progress |
| [006](evolution/006-decision-rot.md) | Decision Rot | Upcoming |
| [007](evolution/007-compaction-loss.md) | Compaction Loss | Upcoming |
| [008](evolution/008-write-discipline.md) | Write Discipline | Upcoming |

</details>

## Acknowledgments

The `/memento:grill-me` skill is based on [Matt Pocock](https://github.com/mattpocock)'s grill-me prompt, adapted for the Memento OS artifact system. If you like what it does, check out his repos — there's more where that came from.

## Contributing

Welcome: evolution entries, adapter improvements, scorecard improvements, translations.

Not accepted: vendor plugins, paid integrations, AI-generated filler.

## License

[MIT](LICENSE)
