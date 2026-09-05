# Agentic Total Recall — Phase 1 Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Scaffold the repo, write 4 solved evolution entries, populate the starter kit with sanitized configs/hooks/skills, and publish the initial README.

**Architecture:** Content-first repo. No build system, no dependencies. All files are Markdown or shell scripts. The repo structure mirrors the design spec (Section 5). Starter kit files use `.example` suffix where users must customize.

**Tech Stack:** Markdown, Bash (hooks), Git

**Spec:** `docs/2026-03-14-agentic-total-recall-design.md`

---

## Chunk 1: Repo Scaffold + Templates

### Task 1: Create directory structure and boilerplate

**Files:**
- Create: `README.md`
- Create: `LICENSE`
- Create: `CHANGELOG.md`
- Create: `evolution/_template.md`
- Create: `system/current-state.md`
- Create: `system/architecture.md`
- Create: `system/scorecard.md`
- Create: `reference/glossary.md`
- Create: `reference/openclaw-comparison.md`
- Create: `reference/tools-tested.md`

- [ ] **Step 1: Create all directories**

```bash
cd ~/Documents/Developer/agentic-total-recall
mkdir -p evolution system reference starter/claude-code/{hooks,memory,skills/{session-complete,process-inbox,strategic-compact,knowledge}} starter/obsidian-vault/{_meta,_inbox,Knowledge/patterns,Projects/_example-project/sessions}
```

Note: `.gitignore` already exists in repo root (created during repo init).

- [ ] **Step 2: Create LICENSE (MIT)**

```bash
cat > LICENSE << 'EOF'
MIT License

Copyright (c) 2026 Ayal Nogovitsyn

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
EOF
```

- [ ] **Step 3: Create CHANGELOG.md**

Write `CHANGELOG.md` with initial entry:

```markdown
# Changelog

## [0.1.0] — 2026-03-14

### Added
- Repo scaffold with evolution/, system/, reference/, starter/ structure
- Evolution entries 001-004 (solved problems)
- Scorecard methodology (10 dimensions, 4-level rubrics)
- Starter kit: Claude Code configs, 3 safety hooks, 4 skills
- Starter kit: Obsidian vault skeleton with L0/L1/L2 templates
- OpenClaw comparison reference
- Initial README with manifesto and evolution index
```

- [ ] **Step 4: Create evolution/_template.md**

Write `evolution/_template.md` using the entry format from spec Section 7:

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

- [ ] **Step 5: Create placeholder files for system/ and reference/**

Create these files with section headers only (content comes in later tasks):
- `system/current-state.md` — "# Current State" + "Last updated: 2026-03-14" + "Overall score: 6.5/10"
- `system/architecture.md` — header only, populated in Task 2
- `system/scorecard.md` — header only, populated in Task 3
- `reference/glossary.md` — header only, populated in Task 4
- `reference/openclaw-comparison.md` — header only, populated in Task 5
- `reference/tools-tested.md` — header only, deferred to Phase 2 (populated as tools are evaluated)

- [ ] **Step 6: Create .gitkeep files**

```bash
touch starter/obsidian-vault/_inbox/.gitkeep
touch starter/obsidian-vault/Projects/_example-project/sessions/.gitkeep
```

- [ ] **Step 7: Commit scaffold**

```bash
git add LICENSE CHANGELOG.md evolution/ system/ reference/ starter/
git commit -m "chore: initial repo scaffold with directory structure and templates"
```

---

### Task 2: Write system/architecture.md

**Files:**
- Modify: `system/architecture.md`

Content source: Spec Section 6 (Architecture Overview). Sanitize all personal paths.

- [ ] **Step 1: Write the 3-layer architecture description**

Replace generic paths. Use `~/.claude/` (standard) and `~/knowledge-vault/` (generic example). Include:
- Layer 1: Agent Memory (`.claude/projects/*/memory/`)
- Layer 2: Knowledge Vault (Obsidian — generic)
- Layer 3: Project Repos (NEXT.md, CLAUDE.md, docs/)
- Routing protocol (L0 → L1 → L2) with token budgets
- Connective tissue (sync hook, global CLAUDE.md, MOCs, safety hooks)
- ASCII diagram showing data flow between layers

- [ ] **Step 2: Commit**

```bash
git add system/architecture.md
git commit -m "docs: add 3-layer memory architecture with routing protocol"
```

---

### Task 3: Write system/scorecard.md

**Files:**
- Modify: `system/scorecard.md`

Content source: Spec Section 8 (Scorecard Methodology).

- [ ] **Step 1: Write scorecard with rubrics**

Include:
- Purpose statement (evaluate any memory system, not just this one)
- 4-level rubric (1-3 Weak, 4-6 Partial, 7-9 Strong, 10 Complete)
- 10-dimension table with: dimension name, what it measures, core goal, rubric descriptions for each level
- "How to use this" section: score your system, identify weakest dimensions, read relevant evolution entries
- Current system scores with one-line justification per dimension

Dimensions (from spec):
1. Persistence durability — 9/10
2. Semantic retrieval — 4/10
3. Recency awareness — 6/10
4. Compaction handling — 3/10
5. Auto-capture reliability — 5.5/10
6. Cross-file linking — 7/10
7. Storage scalability — 6/10
8. Knowledge OS fit — 9/10
9. Portability / ownership — 9/10
10. Setup complexity — 3/10

- [ ] **Step 2: Update current-state.md with scorecard summary table**

Add the score table to `system/current-state.md` so the README can link to it.

- [ ] **Step 3: Commit**

```bash
git add system/scorecard.md system/current-state.md
git commit -m "docs: add 10-dimension scorecard methodology with rubrics and current scores"
```

---

### Task 4: Write reference/glossary.md

**Files:**
- Modify: `reference/glossary.md`

- [ ] **Step 1: Write glossary of memory system terms**

Terms to define (alphabetical):
- Auto-capture — agent writing memory without explicit instruction
- Compaction — context window summarization that discards detail
- Context window — the agent's working memory (tokens)
- Decision graduation — promoting decisions from session logs to durable storage
- Decision rot — decisions made but never recorded durably
- Evolution entry — a documented problem/solution case study
- Knowledge vault — external knowledge base (e.g., Obsidian) connected to agent
- L0/L1/L2 — tiered context loading protocol
- Memory loss — information that existed in context but was never persisted
- MOC (Map of Content) — hub document linking related notes
- Pattern extraction — identifying reusable solutions from specific experiences
- Scorecard — self-evaluation methodology for memory systems
- Session boundary — the gap between two agent conversations
- Token efficiency — minimizing tokens spent on irrelevant context
- Write discipline — the practice of proactively writing memory at critical moments
- Write trigger — an event that causes memory to be saved (manual, hook, or automatic)

- [ ] **Step 2: Commit**

```bash
git add reference/glossary.md
git commit -m "docs: add glossary of memory system terminology"
```

---

### Task 5: Write reference/openclaw-comparison.md

**Files:**
- Modify: `reference/openclaw-comparison.md`

Content source: Audit from this session. Sanitize all personal details.

- [ ] **Step 1: Write comparison document**

Include:
- What is OpenClaw (brief, neutral description of their 4-layer memory system)
- Side-by-side dimension comparison (our system vs OpenClaw)
- Where we're ahead (cross-file linking, L0/L1/L2 protocol, safety hooks)
- Where OpenClaw is ahead (semantic retrieval, compaction handling, write discipline)
- Key insight: "Architecture vs discipline — structure without write discipline is a well-organized graveyard"
- Lessons we took from the comparison (forward references to evolution entries 006-008 — these stub files are created in Task 10)

- [ ] **Step 2: Commit**

```bash
git add reference/openclaw-comparison.md
git commit -m "docs: add OpenClaw memory system comparison with dimension analysis"
```

---

## Chunk 2: Evolution Entries 001-004

### Task 6: Write evolution/001-tiered-context.md

**Files:**
- Create: `evolution/001-tiered-context.md`

Content source: Real L0/L1/L2 protocol from CLAUDE.md and arch_tiered_context.md memory file.

- [ ] **Step 1: Write the evolution entry**

Follow `_template.md` format. Key content:
- **Problem:** Every session loaded full architecture docs, tech stack specs, and decision logs. ~5K tokens wasted before any work started. Agent attention diluted by irrelevant historical context.
- **What We Tried:** Loading everything upfront (wasteful). Loading nothing (agent lacked context). Manual "read this file" instructions (inconsistent).
- **What Worked:** Three-tier protocol:
  - L0: `NEXT.md` (~15 lines, ~200 tokens) — always loaded, session continuity
  - L1: `CLAUDE.md` + `_context.md` (~500 tokens) — always loaded, project overview
  - L2: Full docs (ARCHITECTURE.md, DECISIONS.md, etc.) — loaded only when L1 indicates relevance
  - Rule: never load L2 at session start
- **Why It Works:** Token budgets force prioritization. Most sessions need continuation context (L0) and project awareness (L1), not full architecture (L2). Agent reads L0+L1, decides if L2 is needed.
- **Verification:** Measured 3-5K tokens saved per session vs. loading everything. Agent responses were equally accurate for routine tasks.
- **Score impact:** Token efficiency from 4/10 → 8/10
- **Core goal:** Token efficiency

- [ ] **Step 2: Commit**

```bash
git add evolution/001-tiered-context.md
git commit -m "docs: evolution 001 — tiered context loading (L0/L1/L2)"
```

---

### Task 7: Write evolution/002-safety-hooks.md

**Files:**
- Create: `evolution/002-safety-hooks.md`

Content source: Real hooks from ~/.claude/hooks/ (sanitized).

- [ ] **Step 1: Write the evolution entry**

Key content:
- **Problem:** Agent occasionally wrote hardcoded API keys into source files, ran `rm -rf .` during cleanup attempts, and force-pushed to main. Each incident required manual recovery.
- **What We Tried:** Adding rules to CLAUDE.md ("never commit secrets"). Agent followed them ~80% of the time — not enough for production safety.
- **What Worked:** Three PreToolUse hooks that intercept tool calls before execution:
  1. `secret-detect.sh` — scans Write/Edit content for API key patterns, PEM headers, AWS secrets, credential assignments. Includes false-positive prevention (placeholders, env references).
  2. `destructive-command.sh` — blocks rm -rf on root/home, DROP TABLE, TRUNCATE, chmod 777, fork bombs, dd to raw disk.
  3. `git-safety.sh` — blocks force push, reset --hard, checkout --, clean -f, branch -D, staging .env files.
  - Include sanitized hook code snippets.
- **Why It Works:** Hooks are deterministic — they don't rely on LLM judgment. The agent can still request dangerous operations, but the user is prompted. Defense in depth: CLAUDE.md rules + hook enforcement.
- **Verification:** Zero secret leaks since hook deployment. Agent has been blocked 12+ times from destructive operations that would have required recovery.
- **Score impact:** Auto-capture reliability from 3/10 → 5/10 (indirect — reduced time spent on recovery = more time for actual work)
- **Core goal:** Memory loss prevention (preventing destruction of existing work)

- [ ] **Step 2: Commit**

```bash
git add evolution/002-safety-hooks.md
git commit -m "docs: evolution 002 — safety hooks for secrets, destructive commands, and git"
```

---

### Task 8: Write evolution/003-vault-bridge.md

**Files:**
- Create: `evolution/003-vault-bridge.md`

Content source: sync-vault-context.sh hook and vault ↔ .claude/ memory relationship.

- [ ] **Step 1: Write the evolution entry**

Key content:
- **Problem:** Knowledge vault (Obsidian) and agent memory (`.claude/projects/*/memory/`) were disconnected silos. Research captured in vault was invisible to the agent. Agent memory was invisible to the vault. Cross-project insights stayed trapped in one context.
- **What We Tried:** Manually copying vault files into conversations ("read this file"). Worked but tedious and inconsistent.
- **What Worked:**
  1. `sync-vault-context.sh` SessionStart hook — copies L1 vault files into `.vault-cache/` at session start, before the agent's sandbox locks.
  2. Global `CLAUDE.md` routing table — maps each project to its vault path + repo path, so the agent knows where to find and store knowledge.
  3. `_context.md` as the vault L1 — each project has a context file with summary, document index, and open questions. Agent reads this instead of browsing the vault.
  - Include sanitized hook code and CLAUDE.md routing example.
- **Why It Works:** The vault is the knowledge store; the agent is the knowledge worker. The bridge makes the store accessible without loading everything. L0/L1/L2 applies to vault access too — agent reads _context.md (L1), only opens full vault docs when needed (L2).
- **Verification:** Agent can now reference vault research during coding sessions. Cross-project insights (e.g., competitive intelligence from one project informing another) happen naturally.
- **Score impact:** Knowledge OS fit from 6/10 → 9/10
- **Core goal:** Both (token efficiency via selective loading + memory loss prevention via vault persistence)

- [ ] **Step 2: Commit**

```bash
git add evolution/003-vault-bridge.md
git commit -m "docs: evolution 003 — vault bridge connecting Obsidian to agent memory"
```

---

### Task 9: Write evolution/004-cross-project-linking.md

**Files:**
- Create: `evolution/004-cross-project-linking.md`

Content source: MOC system and pattern extraction from Knowledge OS.

- [ ] **Step 1: Write the evolution entry**

Key content:
- **Problem:** 7 projects, each with their own research, decisions, and patterns. Agent working on Project A had no awareness of relevant findings from Project B. Competitive intelligence gathered for one product was invisible to others. Patterns discovered in one codebase were re-discovered (slowly) in another.
- **What We Tried:** Putting everything in one flat folder (unnavigable). Tagging (tags proliferate, nobody searches by tag).
- **What Worked:**
  1. **MOC (Map of Content) hub files** — 4 semantic hubs in `Knowledge/`: AI & Agents, Business Patterns, Competitive Intelligence, Kazakhstan Market. Each project's `_context.md` links to relevant MOCs in a `## Related` section.
  2. **Pattern extraction discipline** — when a session reveals a reusable insight, it's extracted to `Knowledge/patterns/` with a standard format (Context / Pattern / Why). Example patterns: "SaaS pricing tiers gated by cognitive depth, not feature count" (from a Chrome extension project, applicable to any SaaS).
  3. **Canonical tag taxonomy** — nested `domain/subtopic` tags (e.g., `tech/security`, `business/strategy`) with a single source of truth. Project identifiers go in frontmatter `project:` field, not tags.
  - Include example of how a pattern extracted from one project was used in another.
- **Why It Works:** MOCs are hub nodes in a knowledge graph. They don't hold content — they hold connections. When the agent reads a MOC, it discovers related work across projects without loading all of them. Pattern extraction captures the transferable insight, not the project-specific implementation.
- **Verification:** Agent successfully applied a competitive intelligence pattern (extracted from an AI summarization project) to a wedding planning platform's market analysis — without being told the pattern existed. It found it via the MOC.
- **Score impact:** Cross-file linking from 3/10 → 7/10
- **Core goal:** Both (token efficiency via selective discovery + memory loss prevention via durable patterns)

- [ ] **Step 2: Commit**

```bash
git add evolution/004-cross-project-linking.md
git commit -m "docs: evolution 004 — cross-project linking via MOCs and pattern extraction"
```

---

## Chunk 3: Evolution Entry Stubs (scope note: added beyond spec Phase 1 because README evolution index references these entries — stubs only, no solutions)

### Task 10: Create stub entries for 005-008

**Files:**
- Create: `evolution/005-scattered-captures.md`
- Create: `evolution/006-decision-rot.md`
- Create: `evolution/007-compaction-loss.md`
- Create: `evolution/008-write-discipline.md`

- [ ] **Step 1: Write stub for 005 (In Progress)**

```markdown
# 005 — Scattered Captures

**Status:** In Progress
**Score impact:** TBD
**Date:** 2026-03-14
**Core goal:** Memory loss prevention

## The Problem

Knowledge captures end up in the wrong location — session logs in skill inboxes, research in project memory instead of the vault, implementation plans in `~/.claude/plans/` instead of project docs. Each misplaced file is a future retrieval failure.

## What We Tried

(In progress — documenting the cleanup of our own system as the case study)

## What Worked

(In progress)

## Why It Works

(In progress)

## Verification

(In progress)

## Open Questions

- What's the right granularity for routing rules?
- Can routing be automated, or does it always need human judgment?
```

- [ ] **Step 2: Write stubs for 006, 007, 008 (Upcoming)**

Each with Status: Upcoming, a clear problem statement, and empty solution sections. Key problems:
- 006: Decisions made in conversation never graduate to durable storage. Session logs accumulate decisions that are never promoted to DECISIONS.md or typed memory files.
- 007: When context window fills, auto-compaction destroys undocumented decisions, unfinished reasoning, and task state. No pre-compaction extraction exists.
- 008: Agent won't write memory unless explicitly told. Manual invocation of session-complete and strategic-compact means knowledge is lost when the user forgets.

- [ ] **Step 3: Commit**

```bash
git add evolution/005-scattered-captures.md evolution/006-decision-rot.md evolution/007-compaction-loss.md evolution/008-write-discipline.md
git commit -m "docs: evolution stubs 005-008 (in progress and upcoming problems)"
```

---

## Chunk 4: Starter Kit

### Task 11: Create Claude Code starter configs

**Files:**
- Create: `starter/claude-code/CLAUDE.md.example`
- Create: `starter/claude-code/memory/MEMORY.md.example`

- [ ] **Step 1: Write CLAUDE.md.example**

Sanitized version of the L0/L1/L2 protocol and project registry template. Replace all personal paths with generic examples. Include:
- L0/L1/L2 loading protocol with instructions
- Project registry table (empty, with example row)
- Pattern library index (empty, with example row)
- Knowledge vault routing section (generic paths)
- Keep it under 80 lines — this is a starting point, not a finished config

- [ ] **Step 2: Write MEMORY.md.example**

```markdown
# Memory Index

## User
<!-- Memories about the user's role, preferences, expertise -->

## Feedback
<!-- Guidance or corrections from the user -->

## Project
<!-- Ongoing work, goals, decisions -->

## Reference
<!-- Pointers to external resources -->
```

- [ ] **Step 3: Commit**

```bash
git add starter/claude-code/CLAUDE.md.example starter/claude-code/memory/MEMORY.md.example
git commit -m "docs: add Claude Code starter configs (CLAUDE.md + MEMORY.md templates)"
```

---

### Task 12: Create safety hooks (sanitized)

**Files:**
- Create: `starter/claude-code/hooks/secret-detect.sh`
- Create: `starter/claude-code/hooks/destructive-command.sh`
- Create: `starter/claude-code/hooks/git-safety.sh`

- [ ] **Step 1: Copy and sanitize hooks**

Use the real hooks as source. They're already generic (no personal paths). Copy them directly:
- `secret-detect.sh` — PreToolUse matcher: Write|Edit
- `destructive-command.sh` — PreToolUse matcher: Bash
- `git-safety.sh` — PreToolUse matcher: Bash

Add a comment header to each explaining how to install:
```bash
# Installation: Add to ~/.claude/hooks/ and configure in ~/.claude/settings.json
# Event: PreToolUse
# Matcher: [Write|Edit / Bash]
# See starter/quickstart.md for full setup instructions
```

Make executable: `chmod +x starter/claude-code/hooks/*.sh`

- [ ] **Step 2: Commit**

```bash
git add starter/claude-code/hooks/
git commit -m "feat: add 3 safety hooks (secret detection, destructive commands, git safety)"
```

---

### Task 13: Create starter skills (sanitized)

**Files:**
- Create: `starter/claude-code/skills/session-complete/SKILL.md`
- Create: `starter/claude-code/skills/process-inbox/SKILL.md`
- Create: `starter/claude-code/skills/strategic-compact/SKILL.md`
- Create: `starter/claude-code/skills/knowledge/SKILL.md`

- [ ] **Step 1: Sanitize session-complete skill**

From real skill, replace:
- All `~/Documents/Developer/knowledge-os` → `~/knowledge-vault` (generic)
- Remove specific project names
- Keep the full workflow (resolve vault dir, gather changes, update docs, append session log, update NEXT.md, extract patterns, enforce 200-line limit, commit)
- Keep criteria section

- [ ] **Step 2: Sanitize process-inbox skill**

From real skill, replace:
- Vault path → generic
- Remove specific project names (SCADA, AIYO, Meken, MCADS) and their domain keywords
- Replace with generic examples ("Project Alpha", "Project Beta")
- Keep the full classification table, frontmatter schema, merge candidate logic, and reporting format
- Keep criteria section

- [ ] **Step 3: Sanitize strategic-compact skill**

From real skill:
- Already mostly generic — minimal changes needed
- Remove reference to continuous-learning-v2 (not in starter kit)
- Keep the compaction decision guide, what-survives table, and complementary strategies
- Keep criteria section

- [ ] **Step 4: Sanitize knowledge skill**

From real skill, replace:
- Vault path → generic
- Remove `~/.claude/skills/knowledge/inbox/` EPERM fallback (keep concept, genericize path)
- Keep the full extraction engine (5 fields), mode detection, source detection, value gate
- Keep criteria section

- [ ] **Step 5: Commit**

```bash
git add starter/claude-code/skills/
git commit -m "feat: add 4 starter skills (session-complete, process-inbox, strategic-compact, knowledge)"
```

---

### Task 14: Create Obsidian vault starter

**Files:**
- Create: `starter/obsidian-vault/CLAUDE.md.example`
- Create: `starter/obsidian-vault/NEXT.md.example`
- Create: `starter/obsidian-vault/_meta/conventions.md`
- Create: `starter/obsidian-vault/Knowledge/patterns/_index.md`
- Create: `starter/obsidian-vault/Projects/_example-project/_context.md`

- [ ] **Step 1: Write vault CLAUDE.md.example**

Sanitized vault operational instructions. Include:
- Vault structure overview
- L0/L1/L2 protocol (vault perspective)
- Project registry template
- Knowledge location rules (what goes in repo vs vault)
- Frontmatter requirements (reference conventions.md)
- Keep under 60 lines

- [ ] **Step 2: Write NEXT.md.example**

```markdown
## Continue
- [What to work on next — 1-3 items]

## Decide
- [Pending decisions, or "Nothing pending"]

## Blocked
- [Blockers, or "Nothing blocked"]

Updated: YYYY-MM-DD
```

- [ ] **Step 3: Write conventions.md**

Sanitize the real `_meta/conventions.md`:
- Remove Russian language references (keep as optional mention)
- Remove specific project examples
- Keep: frontmatter schema, naming conventions, folder rules, tag guidelines, wikilink conventions
- This is the most valuable standalone reference in the starter kit

- [ ] **Step 4: Write patterns/_index.md**

```markdown
# Pattern Registry

Reusable patterns extracted from project sessions. Each pattern follows the format:
Context (when it applies) / Pattern (what to do) / Why (the reasoning).

| Pattern | Source Project | When to Use |
|---------|--------------|-------------|
| *(add patterns as they're extracted)* | | |
```

- [ ] **Step 5: Write _example-project/_context.md**

Template showing what a project context file should contain:
- One-paragraph summary placeholder
- Key metrics section
- Strategic status
- Repo Knowledge Map (for code projects)
- Document index table (with example rows)
- Open questions
- Related MOCs (wikilinks)

- [ ] **Step 6: Commit**

```bash
git add starter/obsidian-vault/
git commit -m "feat: add Obsidian vault starter (CLAUDE.md, NEXT.md, conventions, templates)"
```

---

## Chunk 5: Quickstart + README

### Task 15: Write starter/quickstart.md

**Files:**
- Create: `starter/quickstart.md`

- [ ] **Step 1: Write the setup guide**

Sections:
1. **Prerequisites** — Claude Code installed, Obsidian installed (optional), git
2. **Step 1: Claude Code memory structure** — copy CLAUDE.md.example, create memory/ dir, copy MEMORY.md.example. Customize project registry.
3. **Step 2: Install safety hooks** — copy hooks to ~/.claude/hooks/, add to settings.json (show exact JSON). Verify with test commands.
4. **Step 3: Install skills** — copy skill folders to ~/.claude/skills/. Verify with `/session-complete` dry run.
5. **Step 4: Knowledge vault (optional)** — copy obsidian-vault/ to your vault location. Customize CLAUDE.md paths. Create first project _context.md.
6. **Step 5: Connect vault to agent** — add vault path to CLAUDE.md project registry. Create sync hook if desired.
7. **Verify it works** — checklist of things to test

Keep practical, no theory. Theory is in evolution entries.

- [ ] **Step 2: Commit**

```bash
git add starter/quickstart.md
git commit -m "docs: add quickstart setup guide"
```

---

### Task 16: Write README.md

**Files:**
- Modify: `README.md`

- [ ] **Step 1: Write the README**

Structure (from spec, adapted):
1. **Title + tagline** — "Agentic Total Recall" + one-line description
2. **The problem** — 3-4 sentences on agent amnesia and why existing solutions fail. Focus on token waste and memory loss.
3. **How this repo works** — 3 sections: evolution/ (core), system/ (snapshot), starter/ (plug and play)
4. **Current score** — 6.5/10 overall, table with 10 dimensions, links to relevant evolution entries
5. **Evolution log** — table with all 8 entries, status, score impact
6. **Who this is for** — 3 bullet points
7. **Quick start** — link to starter/quickstart.md
8. **Contributing** — brief policy from spec Section 14
9. **License** — MIT

No badges, no logo, no emoji. Clean, direct, problem-first.

- [ ] **Step 2: Commit**

```bash
git add README.md
git commit -m "docs: add README with manifesto, scorecard, and evolution index"
```

---

### Task 17: Final review and tag

- [ ] **Step 1: Review all files for sanitization**

Grep the entire repo for personal paths, project names that should be genericized, and any leaked credentials:

```bash
cd ~/Documents/Developer/agentic-total-recall
grep -r "ayalnogovitsyn\|Meken\|SCADA KZ\|MCADS\|weddings-kz\|portfolio_2\|youtube-ai-summary\|grow-pet\|aiyo" --include="*.md" --include="*.sh"
```

Fix any leaks found.

- [ ] **Step 2: Review file structure matches spec**

```bash
find . -not -path './.git/*' -type f | sort
```

Compare against spec Section 5 tree.

- [ ] **Step 3: Commit any fixes and tag**

```bash
git add -A
git commit -m "chore: sanitization review and cleanup"
git tag v0.1.0
```

- [ ] **Step 4: Report completion**

Tell the user: "Phase 1 complete. Repo is at `~/Documents/Developer/agentic-total-recall/` with tag v0.1.0. Ready to create GitHub remote and push?"
