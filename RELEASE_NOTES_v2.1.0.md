# Memento OS v2.1.0

Decision-centric memory system for AI coding agents. **Store conclusions, not notes** — every artifact is a pre-computed reasoning output with an invalidation trigger, not a raw note that needs re-reasoning each session.

This is the first GitHub Release for Memento OS. It consolidates everything since the initial public `v0.1.0` tag (2026-03-14) into a single discoverable artifact.

---

## What's new in 2.1.0

### Area-level artifact routing
DIES artifacts (`[D]` decisions, `[I]` insights, `[E]` errors, `[S]` seeds) now land in the correct `_context.md` based on the file's area, instead of dumping everything into a single root file. Large vaults stay navigable.

### `fix:` field on error artifacts
`[E]` entries now require a `fix:` line — the explicit "what unblocks this" — across all 8 adapters. Errors without fixes are unfinished thoughts; this enforces the discipline at capture time.

### Knowledge OS gaps port
Three patterns ported from the upstream Knowledge OS vault:
- **L0.5 context directory** — optional intermediate layer for stable domain knowledge
- **Confidence gate** — self-assess "do I have full context?" before mid-task decisions
- **Embedded / resolved artifact states** — beyond just `active`/`superseded`

### PayPal donation link
Coffee CTA in README. If Memento OS saves you re-deciding the same thing five times, consider buying me one.

---

## What was already in 2.0 (highlights, for new users)

If you missed the 2.0 line, here's what landed between v0.1.0 → 2.0.0:

- **Multi-AI adapters** — 8 coding tools supported (Claude Code, Codex, Cursor, Windsurf, Cline, Gemini Code Assist, Aider, Continue)
- **Artifact Tier System (L0/L1/L2)** — formal promotion, eviction, and lifecycle rules
- **Mid-Task Retrieval Protocol** — protected domains + confidence gate before decisions
- **People/Self.md peer card** — communication calibration loaded at session-start
- **`memento:init` command** — 3-question onboarding that seeds your first artifact
- **`memento:stats` command** — memory score, artifact breakdown, session streak
- **`memento:grill-me` skill** — stress-test plans, produce artifacts (credit: Matt Pocock)
- **All skills namespaced as `memento:*`** — no collision with personal skills

Full history: see [CHANGELOG.md](./CHANGELOG.md).

---

## Install

```bash
# Claude Code plugin
/plugin install memento-os
```

For other tools (Codex, Cursor, Windsurf, Cline, Gemini, Aider, Continue), see the per-tool install guides in `adapters/`.

---

## Background

Memento OS started as the memory layer of a personal Knowledge OS vault. It was extracted because the same problem — *AI sessions forget what we already decided* — turned out to be everyone's problem, not just one solo founder's.

The core mental model: **OODA loops produce reasoning artifacts (`[D]`/`[I]`/`[E]`/`[S]`), every artifact has an invalidation or activation trigger, and sessions re-load only the still-load-bearing ones.** That's it. The rest is plumbing.

Named after the Nolan film. Unlike the guy in Memento, your AI actually remembers correctly — and knows when to forget.

---

## Thanks

- Matt Pocock — `grill-me` skill lineage
- Everyone who opened an issue, sent a Reddit DM, or quietly forked

If this saved you time, [☕ buy me a coffee](https://paypal.me/aiyo28).
