# Agentic Total Recall — Design Spec

**Date:** 2026-03-14
**Status:** Draft
**Author:** Ayal Nogovitsyn + Claude
**Repo:** `agentic-total-recall`

---

## 1. Purpose

A public GitHub repo documenting a living memory system for AI coding agents. Two core goals:

1. **Token efficiency** — load only what's needed, when it's needed
2. **Memory loss prevention** — decisions, research, and context survive session boundaries, compaction, and project switches

The repo is structured as an **evolution log** — each improvement documented as a case study (problem → what we tried → what worked → verification). The system is incomplete by design; upcoming/unsolved entries are marked transparently.

## 2. Audience

**Primary:** AI-assisted developers across any tool (Claude Code, Cursor, Windsurf, Copilot) who are frustrated by agent amnesia. They want methodology and principles, not a vendor-specific plugin.

**Secondary:** Claude Code power users who want a plug-and-play memory setup they can fork and customize immediately.

## 3. What It Is / What It Is Not

**IS:**
- An evolution log of real failures and fixes, with sanitized examples
- A self-evaluation scorecard methodology (10 dimensions)
- A starter kit with working configs, hooks, and 4 baseline skills

**IS NOT:**
- A framework or library (no install command)
- A finished product (upcoming entries are unsolved)
- Vendor-locked (Claude Code is reference implementation, methodology is universal)

## 4. Content Sanitization Rules

- Real system structure is preserved
- Business-sensitive projects (Meken, SCADA, MCADS) are omitted or genericized
- Some projects may use fabricated names for examples
- No credentials, API keys, or personal paths in published content
- Session logs sanitized to show the failure/fix pattern, not private context

## 5. Repo Structure

```
agentic-total-recall/
├── README.md                        # Manifesto + scorecard + evolution index
├── LICENSE                          # MIT
├── CHANGELOG.md                     # System version history
│
├── evolution/                       # Core content — problem → solution case studies
│   ├── _template.md                 # Template for new entries
│   ├── 001-tiered-context.md        # L0/L1/L2 protocol (solved)
│   ├── 002-safety-hooks.md          # Secret/destructive/git protection (solved)
│   ├── 003-vault-bridge.md          # Syncing vault <-> agent memory (solved)
│   ├── 004-cross-project-linking.md # MOCs + pattern extraction (solved)
│   ├── 005-scattered-captures.md    # Knowledge stuck in wrong locations (in progress)
│   ├── 006-decision-rot.md          # Decisions never graduating from logs (upcoming)
│   ├── 007-compaction-loss.md       # Context destroyed on compaction (upcoming)
│   └── 008-write-discipline.md      # Agent won't write unless forced (upcoming)
│
├── system/                          # Living snapshot of current state
│   ├── current-state.md             # What the system looks like today + overall score
│   ├── architecture.md              # 3-layer model: agent memory, knowledge vault, project repos
│   └── scorecard.md                 # 10 dimensions with 4-level rubrics per dimension
│
├── reference/                       # Benchmarks + research
│   ├── openclaw-comparison.md       # Side-by-side analysis
│   ├── glossary.md                  # Terms: compaction, graduation, write trigger, etc.
│   └── tools-tested.md              # What we tried, what worked, what didn't
│
└── starter/                         # Plug-and-play baseline
    ├── quickstart.md                # Setup guide
    ├── claude-code/
    │   ├── CLAUDE.md.example        # L0/L1/L2 protocol, project registry template
    │   ├── hooks/
    │   │   ├── secret-detect.sh
    │   │   ├── destructive-command.sh
    │   │   └── git-safety.sh
    │   ├── memory/
    │   │   └── MEMORY.md.example    # Index template with category headers
    │   └── skills/
    │       ├── session-complete/
    │       │   └── SKILL.md         # Auto-extract decisions + update NEXT.md
    │       ├── process-inbox/
    │       │   └── SKILL.md         # Route captures from _inbox/ to vault
    │       ├── strategic-compact/
    │       │   └── SKILL.md         # Save context before compaction
    │       └── knowledge/
    │           └── SKILL.md         # Unified research extraction (--deep/--quick)
    └── obsidian-vault/
        ├── CLAUDE.md.example        # Vault operational instructions
        ├── NEXT.md.example          # L0 continuity template
        ├── _meta/
        │   └── conventions.md       # Frontmatter schema, naming rules
        ├── _inbox/
        │   └── .gitkeep
        ├── Knowledge/
        │   └── patterns/
        │       └── _index.md        # Pattern registry template
        └── Projects/
            └── _example-project/
                ├── _context.md      # L1 template
                └── sessions/
                    └── .gitkeep
```

## 6. Architecture Overview (for `system/architecture.md`)

The memory system has 3 layers that connect through a routing protocol:

**Layer 1 — Agent Memory** (`.claude/projects/*/memory/`): Per-project typed markdown files (user, feedback, project, reference). MEMORY.md index loaded every session. Write triggers: session-complete skill, manual capture, feedback hooks.

**Layer 2 — Knowledge Vault** (Obsidian): Cross-project knowledge base. `_context.md` per project (L1 summaries), `Knowledge/patterns/` (reusable solutions), MOC hub files (semantic linking across projects). Synced via git + Obsidian Git plugin.

**Layer 3 — Project Repos**: `NEXT.md` (L0, ~15 lines, loaded every session), `CLAUDE.md` (project-specific agent instructions), `docs/` (full specs, architecture — L2, loaded on demand).

**Routing protocol (L0 → L1 → L2):**
- L0: Always load NEXT.md (~200 tokens)
- L1: Always load CLAUDE.md + _context.md (~500 tokens)
- L2: Load full docs only when L1 indicates relevance (~1-2K tokens each)
- Rule: never load L2 at session start

**Connective tissue:**
- `sync-vault-context.sh` hook copies vault L1 files into `.vault-cache/` at session start
- Global `~/.claude/CLAUDE.md` routes agent to correct project + vault paths
- MOC files in vault link projects semantically (4 hubs: AI, Business, Kazakhstan, Competitive Intelligence)
- Safety hooks (3) prevent destructive writes, secret leaks, dangerous git operations

## 7. Evolution Entry Format

Each entry in `evolution/` follows this structure:

```markdown
# [Number] — [Problem Name]

**Status:** Solved | In Progress | Upcoming
**Score impact:** [dimension] from X/10 -> Y/10
**Date:** YYYY-MM-DD
**Core goal:** Token efficiency | Memory loss prevention | Both

## The Problem

What broke, what was lost, or what kept failing.
Real example (sanitized) showing the pain.

## What We Tried

Approaches attempted, including dead ends.
Why obvious solutions didn't work.

## What Worked

The actual fix — config, hook, workflow change, or architectural decision.
Code/config snippets where relevant.

## Why It Works

The principle behind the solution.
When this pattern applies beyond our specific setup.

## Verification

How we confirmed it actually solved the problem.
Before/after metrics if available.

## Open Questions

What's still unresolved or could be improved.
```

Each entry ties back to the two core goals (token efficiency / memory loss prevention). Each entry is self-contained — someone landing from search gets full value.

## 8. Scorecard Methodology

10 dimensions, each scored 1-10. Scoring uses a 3-level rubric per dimension:

- **1-3 (Weak):** Dimension is absent or barely functional
- **4-6 (Partial):** Dimension works but has known gaps or requires manual effort
- **7-9 (Strong):** Dimension works reliably with minimal manual intervention
- **10 (Complete):** Fully automated, battle-tested, no known gaps

Detailed rubrics for each dimension are defined in `system/scorecard.md`. Scores are self-reported by the system author with justification notes. Readers are encouraged to score their own systems using the same rubrics.

| Dimension | What it measures | Core goal |
|-----------|-----------------|-----------|
| Persistence durability | Does memory survive restarts? | Memory loss |
| Semantic retrieval | Can the agent find related context by meaning? | Token efficiency |
| Recency awareness | Does fresh context rank higher? | Token efficiency |
| Compaction handling | Is knowledge preserved before context window fills? | Memory loss |
| Auto-capture reliability | Does the agent write memory without being told? | Memory loss |
| Cross-file linking | Can knowledge from project A inform project B? | Both |
| Storage scalability | Does the system degrade as memory grows? | Token efficiency |
| Knowledge OS fit | How well does it integrate with your knowledge base? | Both |
| Portability / ownership | Can you move the system? Vendor lock-in? | Neither (meta) |
| Setup complexity | How hard is it to get running? (inverse — lower = more complex) | Neither (meta) |

The README shows our current score with links to the evolution entry that moved each dimension. Score deltas in evolution entries are assigned by the author after verifying the fix works, with justification in the Verification section.

## 9. Starter Kit — Included Skills

Four baseline skills ship in `starter/claude-code/skills/`:

### session-complete
- Triggers: manual invocation at session end (goal: automatic Stop hook)
- Extracts: decisions made, feedback received, continuation context
- Writes: typed memory files + NEXT.md update
- Serves: memory loss prevention

### process-inbox
- Triggers: manual invocation or `/process-inbox`
- Routes: raw captures from `_inbox/` to proper vault locations
- Applies: frontmatter, naming conventions, MOC linking
- Serves: memory loss prevention (scattered captures)

### strategic-compact
- Triggers: manual invocation when context is getting long
- Extracts: critical decisions, current task state, unresolved questions
- Writes: memory files before compaction destroys context
- Serves: memory loss prevention (compaction)

### knowledge
- Triggers: manual invocation with URL/source
- Modes: `--deep` (vault save) / `--quick` (inline summary, no save)
- Extracts: core argument, why it holds, technical specifics, execution pattern, open questions
- Value gate: no vault save unless genuinely novel
- Serves: both (efficient extraction + durable storage)

Skills are included as working examples. The evolution log documents how and why each was built.

## 10. Parallel Workstream — Private System Cleanup

Before publishing, the author's private system needs sanitization. Details are tracked in a separate cleanup checklist (not part of this public spec). The cleanup experience becomes the basis for evolution entry 005 (Scattered Captures) — documenting the problem pattern and solution generically, without exposing private paths.

## 11. Graduation Path (Standalone → Auto-Export)

**Phase 1 (now):** Standalone repo. Write evolution entries manually from real system experience. Starter kit is a static snapshot.

**Phase 2 (when system is more complete):** Build `/export-playbook` skill that:
- Reads real system state (vault + .claude/ memory)
- Sanitizes per rules in Section 4
- Generates/updates `system/current-state.md`
- Proposes new evolution entries from recent session logs
- This graduation itself becomes an evolution entry

## 12. Implementation Phases

### Phase 1: Repo scaffold + first 4 evolution entries (solved problems)
- Create repo structure
- Write evolution entries 001-004 from existing system knowledge
- Write scorecard methodology
- Populate starter kit with sanitized configs + hooks + 4 skills
- Write quickstart guide
- Initial README with evolution index and current score

### Phase 2: .claude/ cleanup + entry 005
- Execute cleanup plan (Section 9)
- Document as evolution entry 005 (Scattered Captures)
- Update current-state.md and scorecard

### Phase 3: Solve upcoming problems + entries 006-008
- Implement pre-compaction flush (entry 007)
- Implement decision graduation pipeline (entry 006)
- Implement automatic session-complete hook (entry 008)
- Each implementation = evolution entry + score update

### Phase 4: Graduation to Auto-Export
- Build /export-playbook skill
- Automate current-state.md generation
- Document as evolution entry 009+

## 13. Success Criteria

- Someone can clone the repo, follow quickstart.md, and have a working memory system in under 30 minutes
- Each evolution entry is self-contained and valuable without reading the rest
- The scorecard is usable by anyone, regardless of their tool stack
- The system's incompleteness is visible and honest (upcoming entries clearly marked)
- No private/business-sensitive information leaks into public repo

## 14. Contribution Policy

Contributions welcome via issues and PRs. Focus areas:
- New evolution entries from other developers' memory system experiences
- Starter kit configs for non-Claude-Code tools (Cursor, Windsurf, Copilot)
- Scorecard rubric improvements
- Translations

Not accepted: vendor-specific plugins, paid tool integrations, AI-generated filler content.
