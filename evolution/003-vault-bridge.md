# 003 — Vault Bridge

**Status:** Solved
**Score impact:** Knowledge OS fit from 6/10 → 9/10
**Date:** 2026-03-13
**Core goal:** Both (token efficiency + memory loss prevention)

## The Problem

Two memory systems existed in parallel with no connection:

1. **Agent memory** (`.claude/projects/*/memory/`) — per-project typed Markdown files. Fast, always loaded, but siloed per project.
2. **Knowledge vault** (Obsidian) — cross-project knowledge base with research, patterns, competitive intelligence. Rich but invisible to the agent.

The agent working on a Chrome extension had no idea that the vault contained competitive analysis of 8 similar products, a pricing pattern extracted from a SaaS project, or a debugging guide written during a previous session. The knowledge existed but was unreachable.

Worse, when the agent discovered something worth keeping — a reusable pattern, a market insight — it had nowhere to put it except project-scoped memory. Cross-project knowledge died in project silos.

Two concrete losses:

- **Lost research:** A competitive analysis covering 8 Chrome extension competitors sat in the vault. The agent working on the extension spent 40 minutes doing redundant competitor research in a later session because it didn't know the analysis existed.
- **Lost patterns:** A pricing tier approach validated on a web app was never surfaced when a mobile app needed the same decision. Both projects converged on the same approach independently — two sessions, same conclusion, zero knowledge transfer.

The gap wasn't a missing file. It was a missing bridge.

## What We Tried

**Approach 1: Manual file reading.** Instructions in CLAUDE.md like "read `~/knowledge-vault/Projects/my-project/Research/competitive-analysis.md` at session start." This worked when the user knew exactly which file existed and where. Failed completely for discovery — the agent couldn't find documents it didn't already know about.

**Approach 2: Loading the entire vault at session start.** 135 Markdown files, ~50K tokens. Destroyed the context budget before any work began, diluted attention across dozens of irrelevant files, and slowed every session regardless of whether vault knowledge was needed. Abandoned after three sessions.

**Approach 3: Grep-on-demand.** Agent searched the vault filesystem when it needed something. Worked for keyword-exact matches. Missed semantic connections — "competitor pricing" wouldn't surface a doc titled "Monetization Strategy." Also required the agent to know to search, which it often didn't.

None of these solved the real problem: the agent didn't have a map of what knowledge existed. Without a map, it couldn't navigate. Without navigation, it reverted to doing work from scratch.

## What Worked

A three-part bridge connecting vault and agent memory, designed around the L0/L1/L2 loading protocol from entry 001.

### Part 1: Vault Sync Hook

A `SessionStart` hook that copies lightweight vault summary files into a local `.vault-cache/` directory before the agent's context loads. It copies only the TODO and summary files for the current project — not the full vault.

```bash
#!/bin/bash
# SessionStart hook — copies L1 from vault to local cache
VAULT="$HOME/knowledge-vault"
REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || echo "$PWD")"
PROJECT="$VAULT/Projects/$(basename "$REPO_ROOT")"

[ -d "$PROJECT" ] || exit 0

CACHE="$REPO_ROOT/.vault-cache"
mkdir -p "$CACHE"
[ -f "$PROJECT/TODO.md" ] && cp -f "$PROJECT/TODO.md" "$CACHE/TODO.md"
[ -f "$PROJECT/_context.md" ] && cp -f "$PROJECT/_context.md" "$CACHE/_context.md"
echo "$(basename "$PROJECT") | $(date -u +%Y-%m-%dT%H:%M:%SZ)" > "$CACHE/.last-sync"
```

Sync cost: under 1 second at session start. The copied files are available locally, so the agent reads them at near-zero overhead during context load.

### Part 2: Global Routing Table

A project registry in the global `~/.claude/CLAUDE.md` that maps each project to its vault context path. The agent doesn't search — it navigates.

```markdown
## Project Registry

| Project | Repo | Vault Context | Session Start |
|---------|------|---------------|---------------|
| Web App | ~/projects/web-app/ | Projects/web-app/_context.md | NEXT.md → BRIEF.md |
| Extension | ~/projects/extension/ | Projects/extension/_context.md | NEXT.md → BRIEF.md |
| Mobile | ~/projects/mobile/ | Projects/mobile/_context.md | NEXT.md → BRIEF.md |
```

When the agent starts a session on any project, it knows exactly where to find vault context and exactly where to write new knowledge back. No search overhead, no guessing.

### Part 3: `_context.md` as Vault L1

Each project in the vault has a `_context.md` file — a document index with one-sentence summaries, open questions, and links to related knowledge hubs. This is the vault's L1: enough to know what's available without loading anything.

```markdown
## Document Index

| Document | Summary | Status |
|----------|---------|--------|
| [[Competitive Analysis]] | 8 competitors profiled, moat analysis complete | active |
| [[Pricing Research]] | Depth-gating pattern, validated on 3 tiers | active |
| [[Tech Stack Decision]] | Why vanilla JS over React for this use case | archived |

## Open Questions
- Should the extension support real-time sync or batch-on-close?

## Related Hubs
- [[MOC — AI & Agents]]
- [[MOC — Competitive Intelligence]]
```

The document index is the key artifact. The agent reads it, sees that "Pricing Research" contains a validated pattern, and loads that document — not because it was told to, but because the index made the document discoverable.

## Why It Works

The vault is the knowledge store. The agent is the knowledge worker. The bridge makes the store accessible without requiring the user to manually route the agent to every file.

L0/L1/L2 applies to vault access the same way it applies to project docs:

- **L0:** Sync hook brings vault summary to local cache automatically. Zero tokens consumed until the agent decides to read it.
- **L1:** `_context.md` provides a document index and open questions. ~300 tokens. Enough for the agent to decide whether any vault document is relevant to the current task.
- **L2:** Full vault documents — competitive analyses, research reports, decision logs — loaded only when the `_context.md` index indicates relevance.

The routing table eliminates discovery cost. The agent doesn't need to know the vault's folder structure or search for project-specific content. It follows a direct path defined in global config.

The sync hook eliminates availability risk. Vault documents are cached locally at session start, so even if the vault path is temporarily unreachable (permissions change, drive unmounted), the agent works from the cached copy without degrading silently.

## Verification

After implementing the vault bridge:

- Agent referenced vault research during coding sessions without being told it existed. It navigated via the `_context.md` document index — saw "Competitive Analysis: 8 competitors profiled" in the index, loaded the doc, and used the findings to inform a UX decision. No user prompt required.
- Pricing pattern from a web app project was surfaced and applied to a mobile app subscription model. Agent found it by reading the Competitive Intelligence MOC, which linked to the pattern file. Saved an estimated 2-hour research and design session.
- Vault sync adds under 1 second to session start and costs ~0 tokens at load time (files are local, read on demand only when the index indicates relevance).
- Agent writes back to vault via `process-inbox` and session-complete skills, closing the read/write loop. Knowledge discovered during a session doesn't vanish — it enters the vault for future sessions.

## Open Questions

- The sync hook copies `_context.md` along with `TODO.md`. For projects with dense context files (500+ lines), this may be wasteful. Worth exploring a "summary-only" sync mode that copies only the Document Index section.
- When the vault is unreachable (drive unmounted, wrong permissions), the agent falls back to project-local memory silently. Should there be an explicit warning so the user knows vault knowledge isn't available?
- Bidirectional sync currently requires the user to run specific skills at session end. Could the `SessionStop` hook detect when new knowledge was created and prompt for vault write-back automatically?
