# Memory System Architecture

A 3-layer model connecting agent memory, a knowledge vault, and project repositories through a tiered loading protocol.

## The Three Layers

### Layer 1 — Agent Memory

**Location:** `.claude/projects/*/memory/` (or equivalent per tool)

Per-project typed Markdown files. Each file has frontmatter with `name`, `description`, and `type` (user, feedback, project, reference). An index file (`MEMORY.md`) is loaded every session.

**Write triggers:**
- Session-complete skill (end of session)
- Manual capture ("remember this")
- Feedback hooks (user corrections)

**Strengths:** Fast access, always loaded, project-scoped.
**Weakness:** Siloed per project. No cross-project visibility without explicit routing.

### Layer 2 — Knowledge Vault

**Location:** `~/knowledge-vault/` (Obsidian, Notion, or any Markdown-based system)

Cross-project knowledge base. Each project has a `_context.md` file (L1 summary), a `Research/` folder, and optional `patterns/` for reusable insights. MOC (Map of Content) files serve as hub nodes linking projects semantically.

**Key components:**
- `_context.md` — project summary, document index, open questions (the L1 entry point)
- `Knowledge/patterns/` — reusable solutions extracted from specific project experiences
- MOC files — semantic hubs (e.g., "AI & Agents", "Business Patterns") that connect project silos
- `_meta/conventions.md` — frontmatter schema, naming rules, tag taxonomy

**Strengths:** Cross-project visibility, durable, human-readable in Obsidian.
**Weakness:** Requires sync mechanism to be visible to the agent.

### Layer 3 — Project Repos

**Location:** Each project's git repository

- `NEXT.md` — L0 continuity (~15 lines). What to continue, what to decide, what's blocked.
- `CLAUDE.md` — Project-specific agent instructions, gotchas, effort calibration.
- `docs/` — Full specs, architecture docs, decision logs (L2 detail).

**Strengths:** Version-controlled, co-located with code, always accessible.
**Weakness:** Project-scoped. Cross-project knowledge stays in the vault.

## Routing Protocol (L0 → L1 → L2)

The core token-saving mechanism. Load context in tiers, not all at once.

```
Session Start
    │
    ▼
┌─────────────────────┐
│  L0: NEXT.md        │  ~200 tokens, ALWAYS loaded
│  "What's next?"     │  Session continuity, blockers, pending decisions
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│  L1: CLAUDE.md +    │  ~500 tokens, ALWAYS loaded
│  _context.md        │  Project overview, key rules, document index
└─────────┬───────────┘
          │
          ▼ (only if L1 indicates relevance)
┌─────────────────────┐
│  L2: Full docs      │  ~1-2K tokens each, ON DEMAND
│  ARCHITECTURE.md    │  Only when the task requires deep context
│  DECISIONS.md       │
│  TECH_STACK.md      │
└─────────────────────┘
```

**The rule:** Never load L2 at session start. Read L0 + L1, then decide if L2 is needed.

**Token savings:** 3-5K tokens per session vs. loading everything upfront.

## Connective Tissue

The layers don't work in isolation. These mechanisms connect them:

### Vault Sync Hook

A `SessionStart` hook copies L1 files from the vault into a local `.vault-cache/` directory before the agent's sandbox locks. This makes vault context available even when the vault path is restricted.

```bash
#!/bin/bash
# Copies L1 files from vault to local cache at session start
VAULT="$HOME/knowledge-vault"
REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || echo "$PWD")"
PROJECT="$VAULT/Projects/$(basename "$REPO_ROOT")"

[ -d "$PROJECT" ] || exit 0

CACHE="$REPO_ROOT/.vault-cache"
mkdir -p "$CACHE"
[ -f "$PROJECT/TODO.md" ] && cp -f "$PROJECT/TODO.md" "$CACHE/TODO.md"
echo "$(basename "$PROJECT") | $(date -u +%Y-%m-%dT%H:%M:%SZ)" > "$CACHE/.last-sync"
```

### Global Router (CLAUDE.md)

A global `~/.claude/CLAUDE.md` routes the agent to the correct project + vault paths. Contains a project registry table mapping each project to its repo path, vault context path, and session start files.

### MOC Hub Linking

MOC files in the vault link projects semantically. When the agent reads a MOC, it discovers related work across projects without loading all of them.

### Safety Hooks

Three `PreToolUse` hooks prevent destructive operations:
1. **Secret detection** — blocks API keys, credentials in Write/Edit operations
2. **Destructive commands** — blocks rm -rf, DROP TABLE, chmod 777 in Bash
3. **Git safety** — blocks force push, reset --hard, staging .env files

See [evolution/002-safety-hooks.md](../evolution/002-safety-hooks.md) for the full story.

## Data Flow

```
┌──────────────┐     sync hook      ┌──────────────┐
│  Knowledge   │ ──────────────────► │  .vault-     │
│  Vault       │                     │  cache/      │
│  (Obsidian)  │ ◄────────────────── │  (local)     │
│              │   session-complete  │              │
└──────┬───────┘   process-inbox     └──────────────┘
       │                                    │
       │  _context.md (L1)                  │  L1 files
       │  patterns/ (extracted)             │
       │                                    │
       ▼                                    ▼
┌──────────────┐                    ┌──────────────┐
│  Global      │ ──── routes ─────► │  Agent       │
│  CLAUDE.md   │                    │  Memory      │
│  (router)    │                    │  (.claude/)  │
└──────────────┘                    └──────┬───────┘
                                           │
                                           │  typed memory files
                                           │  MEMORY.md index
                                           │
                                           ▼
                                    ┌──────────────┐
                                    │  Project     │
                                    │  Repo        │
                                    │  NEXT.md     │
                                    │  CLAUDE.md   │
                                    │  docs/       │
                                    └──────────────┘
```
