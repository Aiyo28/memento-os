# Memento OS — Pivot Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Pivot agentic-total-recall into memento-os — a decision-centric memory operating system for AI coding agents that stores pre-computed reasoning artifacts instead of raw notes.

**Architecture:** The system has one atomic unit: the **reasoning artifact** (a decision with conclusion, tradeoff, invalidation trigger, and confidence level). Everything flows through a single composable `/decide` skill with modes. The vault uses 2 tiers (full projects vs experiments) with `_context.md` as demand-paged table of contents. The public repo documents the private system's evolution.

**Tech Stack:** Markdown files, shell hooks (bash), Claude Code skills (SKILL.md), Obsidian vault, git

**Core Insight Driving This Pivot:** "The systems that work best load the least context with the highest information density." Store reasoning outputs, not inputs. Log decisions and errors, not everything.

---

## File Structure

### Files to Rename/Move
- Repo directory: `agentic-total-recall/` → `memento-os/` (GitHub rename)
- All internal references to "Agentic Total Recall" → "Memento OS"

### Files to Rewrite (major changes)
- `README.md` — new framing: decisions as atomic unit, not memory files
- `system/architecture.md` — new 4-level demand-paging model + reasoning artifacts
- `system/scorecard.md` — add 2 new dimensions, update rubrics
- `system/current-state.md` — rescore with new dimensions
- `starter/claude-code/CLAUDE.md.example` — restructure around reasoning artifacts
- `starter/claude-code/memory/MEMORY.md.example` — new format
- `starter/obsidian-vault/CLAUDE.md.example` — align with new vault structure
- `starter/obsidian-vault/_meta/conventions.md` — new type values, artifact format
- `starter/obsidian-vault/Projects/_example-project/_context.md` — new template
- `CHANGELOG.md` — add v0.2.0

### Files to Create (new)
- `starter/claude-code/skills/decide/SKILL.md` — composable decision skill
- `starter/claude-code/skills/session-start/SKILL.md` — session opening ritual
- `starter/claude-code/skills/audit/SKILL.md` — structure + staleness check
- `starter/obsidian-vault/Experiments/_experiment-template/_context.md` — lightweight tier
- `starter/obsidian-vault/Projects/_full-project-template/_context.md` — full tier template
- `starter/obsidian-vault/Projects/_full-project-template/decisions/.gitkeep`
- `starter/obsidian-vault/Projects/_full-project-template/research/.gitkeep`
- `starter/obsidian-vault/Projects/_full-project-template/sessions/.gitkeep`
- `starter/obsidian-vault/Projects/_full-project-template/references/.gitkeep`
- `evolution/009-reasoning-artifacts.md` — the pivot itself as an evolution entry
- `reference/reasoning-artifact-format.md` — canonical format reference

### Files to Update (minor changes)
- `evolution/_template.md` — no change needed
- `evolution/001-008` — update header references from "Agentic Total Recall" to "Memento OS"
- `reference/glossary.md` — add new terms (reasoning artifact, demand paging, invalidation trigger, engram)
- `reference/openclaw-comparison.md` — update project name
- `reference/tools-tested.md` — update project name
- `starter/quickstart.md` — rewrite for new skill set + vault structure

### Files to Remove
- `starter/claude-code/skills/knowledge/SKILL.md` — merged into `/decide --research`
- `starter/claude-code/skills/process-inbox/SKILL.md` — merged into `/audit`
- `starter/claude-code/skills/strategic-compact/SKILL.md` — merged into `/session-complete` pre-compaction mode
- `starter/obsidian-vault/Projects/_example-project/` — replaced by 2-tier templates

---

## Chunk 1: Foundation — Formats, Rename, Core Definitions

The atomic unit of the entire system. Everything else builds on these formats.

### Task 1: Define the Reasoning Artifact Format

The core data structure. Every decision, conclusion, and stored reasoning in the system uses this format.

**Files:**
- Create: `reference/reasoning-artifact-format.md`

- [ ] **Step 1: Create the canonical format reference**

```markdown
# Reasoning Artifact Format

The atomic unit of Memento OS. Every piece of stored knowledge follows this structure.

## Why This Format

Traditional memory systems store facts ("Project uses React 18"). This forces the agent
to re-derive the reasoning behind the fact every session. A reasoning artifact stores
the *output* of thinking — the conclusion, the tradeoff, and the condition that would
invalidate it.

Research basis: Sleep-time compute (Letta, 2025) achieved same accuracy with 5× fewer
tokens by storing pre-reasoned conclusions. Agentic plan caching (Zhang et al., 2025)
achieved 50% cost reduction by storing reusable reasoning templates.

## The Format

### Inline (in CLAUDE.md, _context.md, NEXT.md)

For reasoning artifacts embedded in always-loaded files. Keep each to 3-5 lines.

\`\`\`markdown
## [D]: React 18 over Svelte [2026-03]
**Conclusion**: React 18 strict mode + TypeScript. Ecosystem depth over bundle size.
**Invalidation**: Bundle > 250KB gzipped OR team gains Svelte experience.
**Confidence**: High
\`\`\`

Prefix key:
- `[D]` — Decision (chose X over Y)
- `[I]` — Insight (learned something that changes approach)
- `[E]` — Error resolved (what broke + one-line fix)

### Full (standalone file in vault)

For decisions that need full context. Stored in `Projects/{name}/decisions/` or `Knowledge/`.

\`\`\`markdown
---
title: "React 18 over Svelte for AIYO frontend"
type: decision
project: aiyo
tags: [frontend/framework, decision/architecture]
created: 2026-03-10
updated: 2026-03-10
status: active
confidence: high
summary: >
  Chose React 18 with TypeScript strict mode over Svelte after evaluating
  ecosystem maturity, team familiarity, and bundle size tradeoffs. Revisit
  if bundle exceeds 250KB gzipped.
---

# React 18 over Svelte

## Conclusion
React 18 with TypeScript strict mode. Server components for data-heavy pages.

## Alternatives Considered
| Option | Pros | Cons | Why rejected |
|--------|------|------|--------------|
| Svelte | Smaller bundle, less boilerplate | Smaller ecosystem, team unfamiliar | Learning curve + ecosystem risk |
| Next.js App Router | Full-stack, RSC built-in | Vendor coupling, complex caching | Over-engineered for current needs |

## Key Tradeoff
Larger bundle size accepted in exchange for ecosystem depth and hiring pool.

## Invalidation Triggers
- Bundle exceeds 250KB gzipped
- Team gains Svelte experience on side projects
- React ecosystem fragments (unlikely in 2026)

## Context
[Optional: what prompted this decision, relevant research links]
\`\`\`

### Error Log Entry

For resolved errors. One-line solution + context. Stored in session logs or `_context.md`.

\`\`\`markdown
## [E]: CORS preflight failing on /api/upload [2026-03-14]
**Fix**: Header order matters — `Access-Control-Allow-Origin` must come before `Allow-Methods`.
**Root cause**: Express middleware ordering. Moved cors() before route handlers.
**Confidence**: High (verified in prod)
\`\`\`

## What NOT to Store

- Raw facts without reasoning ("uses React 18" — why?)
- Research notes that haven't produced a conclusion (keep in _inbox until they do)
- Session transcripts or conversation history
- Code snippets (they live in the codebase)
- Anything derivable from `git log` or `git blame`
```

- [ ] **Step 2: Verify the format is self-contained**

Read the file back. Can someone with zero context understand:
1. What a reasoning artifact is?
2. How to write one (inline vs full)?
3. What the three prefixes mean ([D], [I], [E])?
4. What NOT to store?

If any answer is "no", revise before proceeding.

- [ ] **Step 3: Commit**

```bash
git add reference/reasoning-artifact-format.md
git commit -m "docs: define reasoning artifact format — the atomic unit of Memento OS"
```

---

### Task 2: Rename Project Throughout Repo

Mechanical find-and-replace. No content changes — just naming.

**Files:**
- Modify: every `.md` file in the repo

- [ ] **Step 1: List all files containing "Agentic Total Recall" or "agentic-total-recall"**

```bash
grep -rl "Agentic Total Recall\|agentic-total-recall" --include="*.md" .
```

- [ ] **Step 2: Replace project name in all files**

Replace these strings throughout:
- `Agentic Total Recall` → `Memento OS`
- `agentic-total-recall` → `memento-os`

Do NOT rename the repo directory yet (that happens when pushing to GitHub).

- [ ] **Step 3: Update CHANGELOG.md — add v0.2.0 section**

Add at the top of CHANGELOG.md:

```markdown
## [0.2.0] — 2026-03-16

### Changed
- **Project renamed** from "Agentic Total Recall" to "Memento OS"
- **Atomic unit** changed from memory files to reasoning artifacts (decisions with conclusions, tradeoffs, and invalidation triggers)
- **Skills consolidated**: 4 skills → 4 skills (knowledge + process-inbox + strategic-compact merged into /decide and /audit)
- **Vault restructured**: single project template → 2 tiers (full projects + experiments)
- **Logging policy**: "store everything" → decisions and errors only
- **Scorecard**: added 2 new dimensions (Decision Retrieval Speed, Reasoning Artifact Density)

### Added
- Reasoning artifact format specification (`reference/reasoning-artifact-format.md`)
- `/decide` skill with modes (--research, --reframe)
- `/session-start` skill
- `/audit` skill (structure check + staleness detection + inbox processing)
- Experiment tier vault template
- Evolution entry 009: The Reasoning Artifact Pivot

### Removed
- `/knowledge` skill (merged into `/decide --research`)
- `/process-inbox` skill (merged into `/audit`)
- `/strategic-compact` skill (merged into `/session-complete` pre-compaction mode)
```

- [ ] **Step 4: Commit**

```bash
git add -A
git commit -m "chore: rename project to Memento OS, add v0.2.0 changelog"
```

---

## Chunk 2: Vault Architecture — Two Tiers + Reasoning Artifacts

### Task 3: Create Full Project Template

The heavy-duty template for real projects with active development.

**Files:**
- Create: `starter/obsidian-vault/Projects/_full-project-template/_context.md`
- Create: `starter/obsidian-vault/Projects/_full-project-template/decisions/.gitkeep`
- Create: `starter/obsidian-vault/Projects/_full-project-template/research/.gitkeep`
- Create: `starter/obsidian-vault/Projects/_full-project-template/sessions/.gitkeep`
- Create: `starter/obsidian-vault/Projects/_full-project-template/references/.gitkeep`
- Remove: `starter/obsidian-vault/Projects/_example-project/` (replaced by this)

- [ ] **Step 1: Create the full project _context.md template**

```markdown
---
title: "{Project Name} Context"
type: project-context
project: {project-slug}
tags: []
created: YYYY-MM-DD
updated: YYYY-MM-DD
status: active
confidence: high
language: en
summary: >
  Replace: one paragraph describing what the project does, current state,
  and key decisions made. An agent reading only this field should know
  whether to load more context.
---

# {Project Name}

> One-sentence description.

## Key Metrics
- **Status:** Planning | Active | Maintenance
- **Tech stack:** [list]
- **Target:** [who is this for]

## Active Reasoning Artifacts

The most important decisions currently shaping this project. Keep to 5-7 max.
Each follows the [D]/[I]/[E] inline format.

| Artifact | Date | Confidence | Invalidation Trigger |
|----------|------|------------|---------------------|
| *(add as decisions are made)* | | | |

## Repo Knowledge Map

| Layer | Path | What's there |
|-------|------|-------------|
| L0 | `NEXT.md` | Session continuity (~15 lines) |
| L1 | `CLAUDE.md` | Project agent instructions |
| L2 | `docs/` | Full specs, architecture (on demand) |

## Folder Index

| Folder | Contents | Count |
|--------|----------|-------|
| `decisions/` | Full reasoning artifact files | 0 |
| `research/` | Source extracts and analysis | 0 |
| `sessions/` | Session logs (rolling, 200-line cap) | 0 |
| `references/` | Architecture docs, brand guides, tech stack refs | 0 |

## Master Plan
<!-- Link to or embed the project's master plan. Keep the header short (3-5 lines),
     full breakdown lives in its own file in references/ -->

**Goal:** [one sentence]
**Current phase:** [phase name]
**Completion:** [X/Y milestones done]

## TODO
<!-- Active tasks. Kanban-style: Blocked → In Progress → Done.
     Move done items to session log, don't accumulate here. -->

### In Progress
- [ ] ...

### Blocked
- [ ] ... — blocked by: [reason]

## Open Questions
- [Unanswered questions needing research or decisions]

## Related
- [[MOC — relevant hub]]
```

- [ ] **Step 2: Create .gitkeep files in subfolders**

```bash
mkdir -p starter/obsidian-vault/Projects/_full-project-template/{decisions,research,sessions,references}
touch starter/obsidian-vault/Projects/_full-project-template/{decisions,research,sessions,references}/.gitkeep
```

- [ ] **Step 3: Remove old example project template**

```bash
rm -rf starter/obsidian-vault/Projects/_example-project/
```

- [ ] **Step 4: Verify folder structure**

```
starter/obsidian-vault/Projects/_full-project-template/
├── _context.md
├── decisions/.gitkeep
├── research/.gitkeep
├── sessions/.gitkeep
└── references/.gitkeep
```

- [ ] **Step 5: Commit**

```bash
git add -A
git commit -m "feat: add full project template with reasoning artifact table and folder structure"
```

---

### Task 4: Create Experiment Template

Lightweight tier for side projects, learning experiments, and ideas that haven't earned full project status yet.

**Files:**
- Create: `starter/obsidian-vault/Experiments/_experiment-template/_context.md`

- [ ] **Step 1: Create the experiment _context.md template**

```markdown
---
title: "{Experiment Name}"
type: project-context
project: {experiment-slug}
tags: [experiment]
created: YYYY-MM-DD
updated: YYYY-MM-DD
status: active
confidence: low
language: en
summary: >
  Replace: what you're exploring, why, and what you hope to learn.
---

# {Experiment Name}

> One-sentence description of what you're trying.

## Purpose
Why this experiment exists. What question are you answering?

## Decisions Log

Inline reasoning artifacts only. No separate files until this graduates.

*(empty — add [D]/[I]/[E] entries as you go)*

## Sessions

| Date | Key outcome |
|------|-------------|
| *(add rows per session)* | |

## Graduation Criteria

When does this become a full project?
- [ ] [Condition 1 — e.g., "validated that X works"]
- [ ] [Condition 2 — e.g., "decided to invest > 1 week"]

When ALL checked → move to `Projects/` and apply full template.

## Related
- [[MOC — relevant hub]]
```

- [ ] **Step 2: Create the Experiments directory**

```bash
mkdir -p starter/obsidian-vault/Experiments/_experiment-template
```

- [ ] **Step 3: Commit**

```bash
git add starter/obsidian-vault/Experiments/
git commit -m "feat: add experiment template — lightweight tier for trials and explorations"
```

---

### Task 5: Update Vault Conventions

Align naming, types, and format rules with the new reasoning artifact system.

**Files:**
- Modify: `starter/obsidian-vault/_meta/conventions.md`

- [ ] **Step 1: Update allowed type values**

Replace the current type values table with:

```markdown
### Allowed `type` values

| Value | Use for |
|-------|---------|
| `decision` | Reasoning artifact — a conclusion with tradeoff and invalidation trigger |
| `insight` | Learned something that changes approach (no alternatives to compare) |
| `error` | Resolved error with one-line fix and root cause |
| `research` | Source-extracted research note (input to future decisions) |
| `project-context` | Project or experiment `_context.md` files |
| `session-log` | Session log entries |
| `index` | Index, registry, or MOC files |

Removed: `knowledge-extract` (merged into `decision` or `insight`), `note` (too vague — decide what it is or leave in `_inbox/`).
```

- [ ] **Step 2: Add reasoning artifact inline format to conventions**

Add new section after "Frontmatter Schema":

```markdown
## Reasoning Artifact Inline Format

For artifacts embedded in _context.md, CLAUDE.md, or NEXT.md files:

\`\`\`markdown
## [D]: Title of decision [YYYY-MM]
**Conclusion**: What was decided and why, in one sentence.
**Invalidation**: What would make this wrong.
**Confidence**: High | Medium | Low
\`\`\`

Prefix key:
- `[D]` — Decision (chose X over Y)
- `[I]` — Insight (learned something that changes approach)
- `[E]` — Error resolved (what broke + one-line fix)

See `reference/reasoning-artifact-format.md` for full standalone format.
```

- [ ] **Step 3: Update folder rules table**

Add the Experiments tier:

```markdown
| `Experiments/{name}/` | Lightweight exploration | Only `_context.md`, no subfolders until graduation |
```

- [ ] **Step 4: Add session log format rule**

Add to naming conventions:

```markdown
| Session logs use date + decision format | `### 2026-03-14 — Chose React over Svelte` |
```

- [ ] **Step 5: Commit**

```bash
git add starter/obsidian-vault/_meta/conventions.md
git commit -m "docs: update vault conventions for reasoning artifacts, 2-tier structure, and new types"
```

---

## Chunk 3: Skills — One Decision Skill + Session Bookends + Audit

### Task 6: Build the Composable /decide Skill

The core skill. Replaces `/knowledge`, absorbs decision-making from `/session-complete`, and adds OODA-inspired modes.

**Files:**
- Create: `starter/claude-code/skills/decide/SKILL.md`
- Remove: `starter/claude-code/skills/knowledge/SKILL.md`

- [ ] **Step 1: Write the /decide skill**

```markdown
---
name: decide
version: 1.0.0
description: >
  Composable decision skill. Core OODA loop: present options, assess confidence,
  record reasoning artifact. Modes: default (decide from current context),
  --research (ingest source first, then decide), --reframe (force perspective
  shift before options). Replaces /knowledge for research-driven decisions.
  Triggers: "decide", "should we", "which option", "evaluate", "compare",
  "research this" (with decision intent), "let's think about".
---

# /decide

One skill. Three modes. Every decision produces a reasoning artifact.

## Mode Detection

| Signal | Mode | What happens |
|--------|------|-------------|
| Decision needed from current context | `default` | Jump to OODA loop |
| URL, file, or "research this" provided | `--research` | Ingest source → extract → then OODA loop |
| "reframe", "different angle", "what am I missing" | `--reframe` | Force perspective shift → then OODA loop |
| User explicitly passes `--research` or `--reframe` | explicit | Override auto-detection |

## Mode: --research (Ingest First)

Before entering the decision loop, extract knowledge from the source.

### Source Detection

| Input | Type | Method |
|-------|------|--------|
| github.com/* | repo | Fetch README, deps, tree, 2-3 key files |
| youtube.com/watch* | video | Transcript, description, chapters |
| *.pdf file | pdf | Parse, then extraction engine |
| Other URL | article | Fetch, strip nav/ads, keep body |
| Multiple inputs | batch | Process each, synthesize connections |

### Extraction Engine (5 Fields)

1. **Core argument** — what it argues, not what it's about (1-2 sentences)
2. **Why it holds** — evidence, reasoning, mechanism (3 bullets max)
3. **Technical specifics** — numbers, code patterns, tools. "None" if none
4. **Execution pattern** — the craft move worth stealing. Omit if N/A
5. **Open questions** — what connects to existing work? What assumption might break?

### After Extraction

Ask: "Does this source inform a decision, or is it reference material?"
- If decision → continue to OODA loop with extracted context
- If reference only → save extraction to `research/` folder using full artifact format with type `research`, report to user, stop

## Mode: --reframe

Before presenting options, force a perspective shift:

1. **Invert the question** — "What if we did the opposite?"
2. **Change the timeframe** — "What matters in 6 months vs today?"
3. **Change the stakeholder** — "What would the end user prioritize vs what we're prioritizing?"
4. **Expose assumptions** — "What are we assuming that might not be true?"

Present the reframe to the user. Then enter the OODA loop with the expanded frame.

## OODA Decision Loop (All Modes)

### Observe
Gather relevant context:
- Read current project `_context.md` and `NEXT.md`
- Check existing decisions in `decisions/` folder (avoid re-deciding settled questions)
- Surface any related reasoning artifacts from other projects via MOCs

### Orient
Present the decision landscape to the user:
- **Options** (2-5): each with concrete pros, cons, and effort estimate
- **Recommendation**: which option and why (or "insufficient data — need X")
- **Confidence**: High (>85%) / Medium (60-85%) / Low (<60%) — show your reasoning

### Decide
Ask the user to choose. Accept their decision even if it differs from recommendation.
If confidence is Low, suggest what additional information would raise it.

### Act — Record the Reasoning Artifact

Based on decision significance:

**Inline only** (small, tactical decisions):
Add to project `_context.md` under "Active Reasoning Artifacts":

\`\`\`markdown
## [D]: {Title} [{YYYY-MM}]
**Conclusion**: {What was decided and why}
**Invalidation**: {What would make this wrong}
**Confidence**: {High|Medium|Low}
\`\`\`

**Full artifact file** (architectural, strategic, or cross-project decisions):
Create in `Projects/{name}/decisions/{Kebab title}.md` using the full format
from `reference/reasoning-artifact-format.md`.

### Significance Heuristic
| Signal | Significance | Storage |
|--------|-------------|---------|
| Affects architecture or tech stack | High | Full file + inline |
| Affects only current task | Low | Inline only |
| Affects multiple projects | High | Full file + inline + update MOC |
| Easily reversible | Low | Inline only |
| Cost > $100 or > 1 week of work | High | Full file + inline |

## Value Gate (--research mode only)

Before saving research extraction to vault:
1. Does this introduce a novel technique or insight?
2. Would a future session benefit from having this doc?

If both "no" → present in conversation only. No vault save. Tell user why.

## Criteria

| # | Criterion | Test |
|---|-----------|------|
| C1 | Options presented with concrete tradeoffs | Each option has pros + cons + effort? |
| C2 | Confidence level stated with reasoning | Not just "Medium" but why? |
| C3 | Existing decisions checked first | Didn't re-open a settled question? |
| C4 | Reasoning artifact produced | Inline and/or full file created? |
| C5 | Invalidation trigger is specific and testable | Could you check if it's been triggered? |
| C6 | Research extraction has all 5 fields (--research mode) | Core argument ≠ topic description? |
```

- [ ] **Step 2: Remove the old /knowledge skill**

```bash
rm -rf starter/claude-code/skills/knowledge/
```

- [ ] **Step 3: Verify skill file renders correctly**

Read back `starter/claude-code/skills/decide/SKILL.md` and verify:
- Mode detection table is clear
- OODA loop steps are actionable
- Artifact format matches `reference/reasoning-artifact-format.md`
- All criteria are testable

- [ ] **Step 4: Commit**

```bash
git add -A
git commit -m "feat: add /decide skill — composable OODA decision loop replacing /knowledge"
```

---

### Task 7: Build /session-start Skill

Opens every work session with a structured briefing. Absorbs context loading that used to happen implicitly.

**Files:**
- Create: `starter/claude-code/skills/session-start/SKILL.md`

- [ ] **Step 1: Write the /session-start skill**

```markdown
---
name: session-start
version: 1.0.0
description: >
  Session opening ritual. Loads context via L0→L1→L2 protocol, displays
  briefing with active decisions and pending items, checks for stale
  artifacts. Run at the start of every work session.
  Triggers: "start session", "what's the context", "where were we",
  "catch me up", beginning of a new conversation.
---

# /session-start

Load context. Display briefing. Flag staleness. Get to work.

## Steps

### 1. Load L0 — Session Continuity

Read `NEXT.md` in the project root.

If it doesn't exist, create one from template:
\`\`\`markdown
## Continue
- [ ] (first task)

## Decide
- (pending decisions)

## Blocked
- (blockers)

*Updated: {today}*
\`\`\`

### 2. Load L1 — Project Context

Read these files (skip if missing):
- Project `CLAUDE.md` (agent instructions)
- Vault `Projects/{name}/_context.md` (project context with reasoning artifacts)
- `.claude/projects/*/memory/MEMORY.md` (agent memory index)

### 3. Staleness Check

Scan all `[D]`, `[I]`, `[E]` entries in `_context.md`:
- Flag any older than 90 days as ⚠️ STALE
- Flag any with `Confidence: Low` older than 30 days as ⚠️ NEEDS RESOLUTION
- Report flagged items to user

### 4. Display Briefing

Format:
\`\`\`
## Session Briefing — {Project Name}
**Date:** {today}
**Last session:** {date from NEXT.md or session log}

### Continue
{from NEXT.md}

### Active Decisions
{from _context.md reasoning artifacts table — show last 5}

### ⚠️ Stale Artifacts (if any)
{list with age and invalidation trigger}

### Pending
{from NEXT.md "Decide" section}
\`\`\`

### 5. Do NOT Load L2

Never auto-load full docs, research files, or reference material at session start.
Wait until a specific task requires them.

## Criteria

| # | Criterion | Test |
|---|-----------|------|
| C1 | Only L0 + L1 loaded at start | No full docs or research files read? |
| C2 | Briefing displayed to user | User can see what's next without asking? |
| C3 | Stale artifacts flagged | Items older than 90 days marked? |
| C4 | Total pre-loaded tokens under 1500 | L0 (~200) + L1 (~500) + briefing (~300) |
```

- [ ] **Step 2: Commit**

```bash
git add starter/claude-code/skills/session-start/
git commit -m "feat: add /session-start skill — structured briefing with staleness detection"
```

---

### Task 8: Rebuild /session-complete Skill

Evolve from "log what happened" to "extract reasoning artifacts + handle pre-compaction."

**Files:**
- Modify: `starter/claude-code/skills/session-complete/SKILL.md`

- [ ] **Step 1: Rewrite session-complete to focus on reasoning artifacts**

Replace the entire content of `starter/claude-code/skills/session-complete/SKILL.md`:

```markdown
---
name: session-complete
version: 2.0.0
description: >
  Run at end of session OR before compaction. Extracts reasoning artifacts
  (decisions, insights, errors) from the conversation, updates NEXT.md,
  appends to session log. Two modes: end-of-session (default) and
  pre-compaction (--compact).
  Triggers: "done", "wrap up", "session complete", "end of session",
  "about to compact", "context getting long", "save before compact".
---

# /session-complete

Extract what matters. Discard the rest. Update continuity docs.

## Mode Detection

| Signal | Mode | Behavior |
|--------|------|----------|
| End of session | `default` | Full extraction + NEXT.md + session log |
| Before compaction | `--compact` | Quick extraction + NEXT.md only (speed matters) |
| User says "compact" or "context long" | `--compact` | Auto-detect |

## Steps

### 1. Scan Conversation for Reasoning Artifacts

Review the full conversation. Extract:
- **Decisions made** → `[D]` artifacts
- **Insights learned** → `[I]` artifacts
- **Errors resolved** → `[E]` artifacts with one-line fix

For each, draft the inline format:
\`\`\`markdown
## [D]: {Title} [{YYYY-MM}]
**Conclusion**: {what and why}
**Invalidation**: {what would make this wrong}
**Confidence**: {High|Medium|Low}
\`\`\`

### 2. Confirm with User

Present extracted artifacts to the user:
"I found these reasoning artifacts from this session: [list]. Anything to add or correct?"

In `--compact` mode: present but don't wait long — time pressure.

### 3. Write Artifacts

**Inline artifacts** → add to project `_context.md` under "Active Reasoning Artifacts"
**Full artifact files** → create in `decisions/` per significance heuristic from /decide skill
**Error entries** → add to session log as `[E]` entries

### 4. Update NEXT.md

Read current `NEXT.md`. Update:
- Move completed items out of "Continue"
- Add new items from this session
- Update "Decide" with pending decisions
- Update "Blocked" with new blockers
- Update date
- Keep under 15 lines

### 5. Append Session Log (default mode only)

Add at the TOP of `{VAULT}/sessions/SESSION_LOG.md`:

\`\`\`markdown
### {YYYY-MM-DD} — {most important decision or outcome}

**Artifacts produced:** {count} ([D]: {count}, [I]: {count}, [E]: {count})
**Changed:** {1-2 sentences on what changed}
**Next:** {what should happen next session}
\`\`\`

Skip in `--compact` mode — session isn't ending, just freeing context.

### 6. Enforce Limits

- SESSION_LOG.md: move entries beyond 200 lines to SESSION_LOG_ARCHIVE.md
- _context.md "Active Reasoning Artifacts" table: cap at 7 entries. Archive older artifacts to `decisions/` folder as full files.

### 7. Pre-Compaction Guidance (--compact mode only)

After saving artifacts, advise the user:
\`\`\`
Ready to compact. Your reasoning artifacts are saved.

Suggested compact message:
/compact Focus on [current task]. Key decisions saved to _context.md.
\`\`\`

### 8. Report

| default mode | --compact mode |
|-------------|----------------|
| List all artifacts written | List artifacts saved |
| Show updated NEXT.md | Show updated NEXT.md |
| Session log entry added | "Ready to /compact" |
| Suggest `/clear` | Suggest `/compact [message]` |

## Criteria

| # | Criterion | Test |
|---|-----------|------|
| C1 | All decisions from session captured as artifacts | Review conversation — any decisions missed? |
| C2 | Artifacts follow [D]/[I]/[E] format exactly | Each has conclusion + invalidation + confidence? |
| C3 | NEXT.md reflects actual next steps | Differs from pre-session state? Under 15 lines? |
| C4 | Session log entry leads with the most important decision | Title is a decision, not "worked on stuff"? |
| C5 | No raw notes or conversation fragments stored | Only reasoning outputs, no inputs? |
```

- [ ] **Step 2: Remove old skills merged into session-complete**

```bash
rm -rf starter/claude-code/skills/strategic-compact/
```

- [ ] **Step 3: Commit**

```bash
git add -A
git commit -m "feat: rebuild /session-complete v2 — reasoning artifact extraction + pre-compaction mode"
```

---

### Task 9: Build /audit Skill

Structure checking, staleness detection, and inbox processing in one skill.

**Files:**
- Create: `starter/claude-code/skills/audit/SKILL.md`
- Remove: `starter/claude-code/skills/process-inbox/SKILL.md`

- [ ] **Step 1: Write the /audit skill**

```markdown
---
name: audit
version: 1.0.0
description: >
  System health check. Validates vault structure, detects stale reasoning
  artifacts, processes inbox, and suggests cleanup. Absorbs /process-inbox.
  Triggers: "audit", "check system", "clean up", "process inbox",
  "what's stale", "system health".
---

# /audit

Check structure. Flag staleness. Process inbox. Remove fluff.

## Steps

### 1. Structure Check

Verify vault structure matches conventions:
- [ ] Every project in `Projects/` has `_context.md`
- [ ] Every experiment in `Experiments/` has `_context.md`
- [ ] All `_context.md` files have complete frontmatter (10 fields)
- [ ] No files outside designated folders (orphans)
- [ ] `Knowledge/patterns/_index.md` exists and is current
- [ ] MOC hub files reference all active projects

Report: ✅ pass / ❌ {issue} for each check.

### 2. Staleness Scan

Scan all reasoning artifacts (both inline in `_context.md` and standalone in `decisions/`):

| Age | Confidence | Status |
|-----|-----------|--------|
| > 90 days | Any | ⚠️ STALE — review invalidation trigger |
| > 30 days | Low | ⚠️ UNRESOLVED — decide or delete |
| Any | Any | Check: has invalidation trigger been met? |

For each stale item, suggest:
- **Reconfirm**: still valid → update date
- **Revise**: partially wrong → update conclusion
- **Archive**: no longer relevant → move to archive or delete

### 3. Process Inbox

If `_inbox/` has files (excluding `.gitkeep`):

For each file:
1. Read content
2. Classify: does it contain a decision/conclusion? Or is it raw input?
   - **Has conclusion** → Create reasoning artifact (route to correct project's `decisions/` or `Knowledge/`)
   - **Raw input only** → Route to `research/` folder of relevant project
   - **Ambiguous** → Ask user. Don't guess.
3. Apply frontmatter per conventions
4. Delete from `_inbox/`
5. Update project `_context.md` folder index

### 4. Fluff Detection

Flag files that might be noise:
- Research files with no `[D]` artifacts produced (extracted but never decided on)
- Session log entries with no artifacts (sessions where nothing was decided)
- Duplicate reasoning artifacts (same decision recorded in multiple places)

Suggest: "These {N} items have no reasoning output. Archive or delete?"

### 5. Report

\`\`\`markdown
## Audit Report — {date}

### Structure: {✅ Clean | ⚠️ {N} issues}
{list issues}

### Staleness: {N} stale artifacts
{list with suggested action}

### Inbox: {N} items processed
| File | Destination | Type |
|------|-------------|------|
| ... | ... | ... |

### Fluff: {N} items flagged
{list with suggested action}
\`\`\`

## Criteria

| # | Criterion | Test |
|---|-----------|------|
| C1 | Every _context.md validated | All projects/experiments checked? |
| C2 | Stale artifacts have specific suggested actions | Not just "stale" but reconfirm/revise/archive? |
| C3 | Inbox items routed correctly | Destinations match type classification? |
| C4 | No ambiguous files silently routed | User asked when unsure? |
| C5 | Report is actionable | Every issue has a suggested fix? |
```

- [ ] **Step 2: Remove old /process-inbox skill**

```bash
rm -rf starter/claude-code/skills/process-inbox/
```

- [ ] **Step 3: Commit**

```bash
git add -A
git commit -m "feat: add /audit skill — structure validation, staleness detection, inbox processing"
```

---

## Chunk 4: System Docs — Architecture, Scorecard, README

### Task 10: Rewrite Architecture Document

New 4-level demand-paging model with reasoning artifacts as the core data structure.

**Files:**
- Modify: `system/architecture.md`

- [ ] **Step 1: Rewrite architecture.md**

Replace the entire content with:

```markdown
# Memento OS Architecture

A demand-paging memory system for AI coding agents. The atomic unit is the **reasoning artifact** — a pre-computed conclusion with tradeoff analysis and invalidation trigger.

## Core Principle

> Your context window is not memory. It is L1 cache.
> — Pichay (Mason, 2026)

Load less. Load precisely. Store reasoning outputs, not inputs.

## The Atomic Unit: Reasoning Artifact

Every piece of stored knowledge follows one format:

\`\`\`markdown
## [D]: Title [YYYY-MM]
**Conclusion**: What was decided and why.
**Invalidation**: What would make this wrong.
**Confidence**: High | Medium | Low
\`\`\`

Three prefixes: `[D]` Decision, `[I]` Insight, `[E]` Error resolved.
Full format spec: [reference/reasoning-artifact-format.md](../reference/reasoning-artifact-format.md)

**Why not raw notes?** Sleep-time compute research (Letta, 2025) achieved same accuracy with 5× fewer tokens by storing pre-reasoned conclusions. Every raw note forces the agent to re-derive reasoning from scratch each session.

## Four-Level Memory Hierarchy

\`\`\`
┌─────────────────────────────────────────────────┐
│  L0: NEXT.md                    ~200 tokens     │
│  Session continuity. What to continue/decide.   │
│  ALWAYS loaded. Updated every session.          │
├─────────────────────────────────────────────────┤
│  L1: CLAUDE.md + _context.md    ~500 tokens     │
│  Project rules + active reasoning artifacts.    │
│  ALWAYS loaded. Contains demand-page index.     │
├─────────────────────────────────────────────────┤
│  L2: decisions/ + research/     ~1-2K each      │
│  Full artifact files + research extracts.       │
│  ON DEMAND — loaded only when task requires.    │
├─────────────────────────────────────────────────┤
│  L3: Archive + Knowledge/       variable        │
│  Archived artifacts, cross-project patterns,    │
│  MOC hubs. RARELY loaded — for deep context.    │
└─────────────────────────────────────────────────┘
\`\`\`

**Budget rule:** Pre-loaded context (L0 + L1) stays under 1500 tokens — roughly 15% of a typical working context budget.

**Demand paging:** When the agent needs L2 content, it reads the L1 index (`_context.md` folder index) and loads only the specific file needed. This is the Pichay "page fault" pattern — load on demand, not on start.

## Three Storage Layers

### Layer 1 — Agent Memory (`.claude/projects/*/memory/`)

Per-project typed Markdown files. MEMORY.md index loaded every session (200-line hard limit).

**Contains:** User preferences, project feedback, reference pointers.
**Does NOT contain:** Decisions (those go in the vault) or raw notes.

### Layer 2 — Knowledge Vault (Obsidian)

Cross-project knowledge base. Two tiers:

**Full Projects** (`Projects/{name}/`):
- `_context.md` — L1 entry point with active reasoning artifacts table
- `decisions/` — full reasoning artifact files
- `research/` — source extracts and analysis
- `sessions/` — rolling session log (200-line cap)
- `references/` — architecture docs, brand guides, tech stack specs

**Experiments** (`Experiments/{name}/`):
- `_context.md` only — inline decisions log, session table, graduation criteria
- No subfolders until graduation to full project

**Cross-cutting:**
- `Knowledge/patterns/` — reusable patterns extracted from project experience
- MOC hub files — semantic links across projects
- `_inbox/` — raw captures awaiting classification (processed by /audit)

### Layer 3 — Project Repos

- `NEXT.md` — L0 (~15 lines). Continue / Decide / Blocked.
- `CLAUDE.md` — project-specific agent instructions
- `docs/` — full specs, architecture (L2, on demand)

## Data Flow

\`\`\`
Session Start ──► /session-start
                    │
                    ├── Read L0 (NEXT.md)
                    ├── Read L1 (CLAUDE.md + _context.md)
                    ├── Staleness check on artifacts
                    └── Display briefing
                           │
                           ▼
                  Work happens (L2 loaded on demand)
                           │
                    ┌──────┴──────┐
                    │             │
              Need to decide?    Error resolved?
                    │             │
                    ▼             ▼
               /decide        Record [E] artifact
                    │
                    ▼
              Reasoning artifact produced
              (inline + optional full file)
                           │
                           ▼
              Context getting long? ──► /session-complete --compact
                           │
                           ▼
              Done for the day? ──► /session-complete
                    │
                    ├── Extract all [D]/[I]/[E] from session
                    ├── Update _context.md + NEXT.md
                    └── Append session log
\`\`\`

## Connective Tissue

### Vault Sync Hook (SessionStart)
Copies L1 files from vault to `.vault-cache/` at session start.

### Global Router (~/.claude/CLAUDE.md)
Maps projects to vault paths. Contains cross-cutting reasoning patterns.

### MOC Hub Linking
Semantic hubs connect projects. Agent discovers related work without loading all projects.

### Safety Hooks (3)
1. **Secret detection** — blocks API keys in Write/Edit
2. **Destructive commands** — blocks rm -rf, DROP TABLE in Bash
3. **Git safety** — blocks force push, reset --hard

## What Gets Logged vs. What Doesn't

| Log | Don't Log |
|-----|-----------|
| Decisions with rationale `[D]` | Raw conversation transcripts |
| Insights that change approach `[I]` | Research that produced no conclusion |
| Errors with one-line fixes `[E]` | Inputs, outputs, intermediate reasoning |
| Session outcomes (1-3 lines) | Full git diffs or file contents |

> Log decisions and errors. Delete everything else.
```

- [ ] **Step 2: Verify all cross-references are valid**

Check that links to `reference/reasoning-artifact-format.md` and evolution entries resolve correctly.

- [ ] **Step 3: Commit**

```bash
git add system/architecture.md
git commit -m "docs: rewrite architecture for demand-paging model and reasoning artifacts"
```

---

### Task 11: Update Scorecard with New Dimensions

Add two new dimensions that measure what actually matters for a decision-centric system.

**Files:**
- Modify: `system/scorecard.md`

- [ ] **Step 1: Add two new dimensions after dimension 10**

Append these sections:

```markdown
### 11. Decision Retrieval Speed
**Question:** How fast can the agent find a relevant past decision?
**Core goal:** Token efficiency

| Score | Description |
|-------|-------------|
| 1-3 | Agent cannot find past decisions. Must re-derive or ask user. |
| 4-6 | Agent can find decisions in current project with manual guidance. Cross-project requires explicit direction. |
| 7-9 | Agent finds relevant decisions via _context.md index and MOC traversal. Cross-project works. |
| 10 | Instant retrieval of any past decision via semantic search. Cross-project, cross-temporal. |

### 12. Reasoning Artifact Density
**Question:** What percentage of stored knowledge is pre-computed reasoning vs raw notes?
**Core goal:** Both (token efficiency + memory loss prevention)

| Score | Description |
|-------|-------------|
| 1-3 | Mostly raw notes and facts. Agent re-derives reasoning every session. |
| 4-6 | Some decisions recorded but without invalidation triggers or confidence levels. Mixed with raw notes. |
| 7-9 | Majority of stored knowledge follows the reasoning artifact format. Raw notes exist only in _inbox/. |
| 10 | All stored knowledge is pre-computed reasoning artifacts. Zero raw notes in the system. |
```

- [ ] **Step 2: Add scores for new dimensions in the current scores table**

Add rows:

```markdown
| 11 | Decision retrieval speed | 5/10 | _context.md provides index; no semantic search yet. Cross-project via MOCs works but manual. | [009](../evolution/009-reasoning-artifacts.md) |
| 12 | Reasoning artifact density | 3/10 | System just pivoted. Most existing content is raw notes. Conversion ongoing. | [009](../evolution/009-reasoning-artifacts.md) |
```

- [ ] **Step 3: Update overall score calculation**

Recalculate with 12 dimensions. Update the "Overall" line.

- [ ] **Step 4: Update the README scorecard table**

In `README.md`, add rows 11 and 12 to the scorecard table with the new scores.

- [ ] **Step 5: Commit**

```bash
git add system/scorecard.md README.md
git commit -m "docs: add Decision Retrieval Speed and Reasoning Artifact Density to scorecard"
```

---

### Task 12: Write Evolution Entry 009 — The Reasoning Artifact Pivot

Document the pivot itself as an evolution entry. This IS the public narrative.

**Files:**
- Create: `evolution/009-reasoning-artifacts.md`

- [ ] **Step 1: Write the evolution entry**

```markdown
# 009 — The Reasoning Artifact Pivot

**Status:** In Progress
**Score impact:** Reasoning artifact density 0→3 (new dimension), Decision retrieval speed 0→5 (new dimension)
**Date:** 2026-03-16
**Core goal:** Both (token efficiency + memory loss prevention)

## The Problem

The memory system stored facts and notes — "Project uses React 18", "researched caching strategies", "discussed auth options." Every session, the agent re-derived the reasoning behind these facts from scratch. After 50+ sessions across 7 projects, we noticed:

1. **Reasoning duplication** — the agent reconstructed the same decision rationale 3-4 times across sessions because only the conclusion was stored, not the logic
2. **Decision amnesia** — 14 architectural decisions found in session logs that never made it to DECISIONS.md (see [006](006-decision-rot.md))
3. **Context waste** — raw research notes loaded into context without producing any actionable conclusion, consuming tokens that could serve active reasoning

The core realization: **we were storing the inputs to reasoning instead of the outputs.** Every fact stored was a future reasoning burden. Every note without a conclusion was a token tax.

## What We Tried

### Approach 1: More structured notes
Added frontmatter, tags, summaries. Still raw notes underneath — the structure didn't change what was stored, just how it was organized. The agent still re-derived reasoning from structured notes.

### Approach 2: Decision logs (DECISIONS.md)
A flat file of decisions made. Better — but no invalidation triggers, no confidence levels, and no connection to the alternatives considered. Decisions without context are assertions without reasoning.

### Approach 3: Reasoning artifacts (what worked)
Defined a new atomic unit: the **reasoning artifact**. Three types:
- `[D]` Decision — chose X over Y, with conclusion, tradeoff, and invalidation trigger
- `[I]` Insight — learned something that changes approach
- `[E]` Error — what broke + one-line fix

Each artifact stores the *output* of thinking, not the input. Each includes an invalidation trigger — the specific condition that would make this artifact wrong.

## What Worked

The reasoning artifact format, applied at three levels:

1. **Inline** (in _context.md and NEXT.md) — 3-5 lines per artifact for always-loaded context
2. **Full file** (in decisions/ folder) — complete artifact with alternatives table for significant decisions
3. **Error log** (in session log) — `[E]` entries with one-line fix for resolved errors

Combined with:
- **One composable skill** (`/decide`) replacing 3 separate skills
- **Two-tier vault** (full projects + experiments) instead of one-size-fits-all
- **Strict logging policy** — decisions and errors only, no raw notes in durable storage

## Why It Works

The principle: **store conclusions, not notes.** This is validated by:

- **Sleep-time compute** (Letta, 2025): same accuracy with 5× fewer tokens by storing pre-reasoned conclusions
- **Agentic plan caching** (Zhang et al., 2025): 50% cost reduction by storing reusable reasoning templates
- **"Distilling System 2 into System 1"** (Meta, 2024): compiled reasoning outputs actually produce *better* answers than re-reasoning, because they skip exploratory dead-ends

The invalidation trigger is the non-obvious key. Without it, artifacts become stale assertions. With it, they're self-expiring — the `/audit` skill can automatically flag artifacts whose triggers have been met.

## Verification

**In progress.** Metrics to track:
- Reasoning artifact density (% of stored knowledge in artifact format): target >70%
- Session start token load (L0 + L1): target <1500 tokens
- Decision re-derivation frequency: target zero (never re-derive a stored decision)
- Stale artifact detection rate: target >90% caught by /audit

## Open Questions

- What's the right cap for inline artifacts in _context.md? Started with 7, may need adjustment.
- Should invalidation triggers be machine-checkable? (e.g., "bundle > 250KB" could be automated)
- How to handle decisions that span multiple projects? Currently: full file + inline in each project's _context.md + MOC update. Might be too much duplication.
```

- [ ] **Step 2: Update the evolution index in README.md**

Add row for entry 009 in the evolution log table.

- [ ] **Step 3: Commit**

```bash
git add evolution/009-reasoning-artifacts.md README.md
git commit -m "docs: evolution 009 — the reasoning artifact pivot (in progress)"
```

---

### Task 13: Rewrite README.md

New framing: decisions as atomic unit, reasoning artifacts, the Nolan reference.

**Files:**
- Modify: `README.md`

- [ ] **Step 1: Rewrite README with new framing**

Key changes to the README:
- Title: `# Memento OS`
- Tagline: reference the film — "Like Nolan's protagonist, AI agents can't form new memories. This is the system of tattoos."
- Core insight: "Store conclusions, not notes"
- Two core goals remain (token efficiency + memory loss prevention) but add: "measured through reasoning artifact density and decision retrieval speed"
- Update scorecard table with 12 dimensions
- Update evolution log table with entry 009
- Update skill list: `/decide`, `/session-start`, `/session-complete`, `/audit`
- Update "How This Repo Works" section to describe 2-tier vault
- Keep contribution policy and license

- [ ] **Step 2: Verify all internal links resolve**

Check every `[link](path)` in README.md points to an existing file.

- [ ] **Step 3: Commit**

```bash
git add README.md
git commit -m "docs: rewrite README for Memento OS — decisions as atomic unit"
```

---

### Task 14: Update Remaining Files

Catch-all for files that need minor updates to align with the pivot.

**Files:**
- Modify: `reference/glossary.md`
- Modify: `system/current-state.md`
- Modify: `starter/quickstart.md`
- Modify: `starter/claude-code/CLAUDE.md.example`
- Modify: `starter/claude-code/memory/MEMORY.md.example`
- Modify: `starter/obsidian-vault/CLAUDE.md.example`
- Modify: `starter/obsidian-vault/NEXT.md.example`

- [ ] **Step 1: Add new terms to glossary**

Add these entries to `reference/glossary.md`:

- **Reasoning artifact** — the atomic unit of Memento OS. A pre-computed conclusion with tradeoff analysis, invalidation trigger, and confidence level. Three types: [D] Decision, [I] Insight, [E] Error.
- **Invalidation trigger** — a specific, testable condition attached to a reasoning artifact that defines when the artifact is no longer valid. Enables automated staleness detection.
- **Demand paging** — loading context into the agent's working memory only when needed, analogous to virtual memory page faults in operating systems. The L0→L1→L2→L3 hierarchy implements this.
- **Engram** — (synonym for reasoning artifact) the physical trace a memory leaves in brain tissue. Used informally for the stored form of a decision.
- **OODA loop** — Observe-Orient-Decide-Act. The decision framework implemented by the /decide skill.
- **Graduation** — when an experiment proves valuable enough to become a full project, gaining the complete folder structure.

Update existing entries:
- **Decision rot** — update definition to reference reasoning artifacts instead of DECISIONS.md
- **Write discipline** — update to reference artifact extraction instead of memory file writing

- [ ] **Step 2: Update current-state.md**

Rescore with 12 dimensions. Update the narrative to reflect the pivot. Note which dimensions are newly added and why.

- [ ] **Step 3: Rewrite quickstart.md**

Update the setup guide for the new skill set:
- 4 skills: `/decide`, `/session-start`, `/session-complete`, `/audit`
- 3 hooks: unchanged (secret detection, destructive commands, git safety)
- Vault setup: mention both tiers (full project + experiment)
- Verification: test `/session-start` produces a briefing, test `/decide` produces an artifact

- [ ] **Step 4: Update CLAUDE.md.example**

Restructure around reasoning artifacts:
- Replace memory file type references with artifact types ([D], [I], [E])
- Update skill references
- Keep L0→L1→L2 protocol (now L0→L1→L2→L3)
- Keep project registry

- [ ] **Step 5: Update MEMORY.md.example**

New category headers reflecting artifact types instead of memory types:
- Active Decisions (inline [D] artifacts pointing to full files)
- User Preferences
- Project References
- Feedback

- [ ] **Step 6: Update obsidian-vault CLAUDE.md.example**

Align with new vault structure:
- Reference 2-tier system (Projects + Experiments)
- Reference reasoning artifact format
- Update skill references
- Update folder rules

- [ ] **Step 7: Update NEXT.md.example**

No structural changes needed — the Continue/Decide/Blocked format works. Add a comment noting that "Decide" items should become `/decide` invocations.

- [ ] **Step 8: Commit**

```bash
git add -A
git commit -m "docs: align all reference files, templates, and guides with Memento OS pivot"
```

---

## Execution Order

Tasks are designed to be executed sequentially (each builds on the previous):

1. **Task 1** — Define reasoning artifact format (everything references this)
2. **Task 2** — Rename project (clean slate for new content)
3. **Task 3** — Full project template
4. **Task 4** — Experiment template
5. **Task 5** — Update vault conventions
6. **Task 6** — /decide skill (core skill, references format from Task 1)
7. **Task 7** — /session-start skill
8. **Task 8** — /session-complete v2
9. **Task 9** — /audit skill
10. **Task 10** — Architecture rewrite (references all skills and templates)
11. **Task 11** — Scorecard update
12. **Task 12** — Evolution entry 009
13. **Task 13** — README rewrite (references everything)
14. **Task 14** — Remaining files alignment

**Parallelizable groups** (if using subagents):
- Group A: Tasks 3 + 4 (vault templates — independent of each other)
- Group B: Tasks 6 + 7 + 9 (new skills — independent of each other)
- Group C: Tasks 11 + 12 (scorecard + evolution entry — independent)

Tasks 1, 2, 5, 8, 10, 13, 14 must be sequential (dependencies on prior tasks).

---

## Post-Pivot Checklist

After all tasks complete:

- [ ] All files reference "Memento OS" (no remaining "Agentic Total Recall")
- [ ] `/decide` skill produces artifacts in the canonical format
- [ ] `/session-start` loads only L0 + L1 (<1500 tokens)
- [ ] `/session-complete` extracts [D]/[I]/[E] artifacts, not raw notes
- [ ] `/audit` detects stale artifacts and processes inbox
- [ ] Vault has both tiers: `Projects/` (full) and `Experiments/` (lightweight)
- [ ] Scorecard has 12 dimensions
- [ ] README tells the Memento story
- [ ] Quickstart gets a new user running in under 30 minutes
- [ ] Evolution entry 009 documents the pivot honestly

## GitHub Migration

After all content changes are committed:

```bash
# Rename local directory
cd .. && mv agentic-total-recall memento-os && cd memento-os

# Create GitHub repo (if not exists)
gh repo create memento-os --public --description "Decision-centric memory OS for AI coding agents. Store conclusions, not notes."

# Push
git remote set-url origin git@github.com:{username}/memento-os.git
git push -u origin main
```
