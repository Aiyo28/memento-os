---
name: memento:init
description: "Initialize Memento OS for a project. Creates memory structure, captures first artifact, shows memory score. Run once per project."
argument-hint: "[path]"
allowed-tools:
  - Read
  - Write
  - Bash
  - Glob
  - Grep
  - AskUserQuestion
---

# /memento init

Set up persistent memory for this project. 3 questions, 30 seconds, your first artifact captured.

## Flow

### Step 0: Detect Environment

```bash
PROJECT_ROOT=$(pwd)
PROJECT_NAME=$(basename "$PROJECT_ROOT")
```

Check for existing memento setup:
- If `_context.md` already exists → "Memento OS is already initialized here. Run `/session-start` instead."
- If `.memento/config.yaml` exists → same

Check for existing project context:
- If `CLAUDE.md` exists → read it for project name and context
- If `package.json` / `Cargo.toml` / `pyproject.toml` exists → extract project name and tech stack

### Step 1: Where to Store Memory

Auto-detect and confirm:

```
MEMENTO OS — Store conclusions, not notes.

Memory location: ./{project-name}/memento/
> Is this correct? (Y to confirm, or enter a different path)
```

If `$ARGUMENTS` was provided, use that path instead of asking.

Default: `./memento/` in the project root. Add to `.gitignore` if the user wants private memory (ask).

### Step 2: What Are You Building?

```
What are you building? (1-2 sentences)
>
```

Use AskUserQuestion. This becomes the `summary` field in `_context.md` frontmatter.

If CLAUDE.md or project config was found in Step 0, pre-fill and ask to confirm:
```
I found this in your CLAUDE.md: "{extracted description}"
Is this accurate, or would you describe it differently?
```

### Step 3: First Artifact — The Hardest Decision

```
What's the hardest decision you've already made on this project?
(tech stack choice, architecture direction, what NOT to build — anything)
>
```

Use AskUserQuestion. This becomes the first `[D]` artifact.

After the user answers:
1. Extract a conclusion from their answer
2. Generate an invalidation trigger ("invalidates if...")
3. Assign priority: default `settled` unless it's clearly architectural (then `critical`)
4. Present: "I'll capture this as: `[D] {conclusion} — invalidates if {trigger} [{priority}] [{today}]`"
5. Confirm or adjust

### Step 4: Create Structure

Create the memory folder:

```
{memory_path}/
├── _context.md          # Project context with first artifact
└── NEXT.md              # Session continuity
```

**`_context.md`** — use this template:

```markdown
---
title: "{Project Name} Memory"
type: project-context
project: {project-slug}
created: {today}
updated: {today}
status: active
confidence: medium
repo_path: "{absolute path to project root, or empty for vault-only}"
repo_docs_path: "{relative path to docs/ if found, or empty}"
summary: >
  {user's answer from Step 2}
---

# {Project Name} Memory

## Key Numbers

| Metric | Value | Confidence |
|--------|-------|------------|
| Status | Active | high |

## Active Reasoning Artifacts

<!-- Kobe cap: 24 artifacts. Evict: noise → settled → volatile. Never evict critical. -->

| # | Artifact | Priority | Date |
|---|----------|----------|------|
| 1 | `{first artifact from Step 3}` | {priority} | {today} |

## Document Index

| Document | Location | Description | Status |
|----------|----------|-------------|--------|

## Open Questions

- [ ] {any obvious unknowns from the project description}

## Related
- [[MOC — relevant hub]]
```

**`NEXT.md`** — use this template:

```markdown
## Continue
- Start building — memory system is active

## Decide
- Nothing pending

## Blocked
- Nothing pending

Updated: {today}
```

### Step 5: Configure

Create `.memento/config.yaml` in the project root:

```yaml
memory_path: {relative path to memory folder}
auto_log: true
created: {today}
```

Add to `.gitignore` if it exists:
```
# Memento OS (optional — remove if you want memory in version control)
.memento/
```

Ask: "Should I add the memory folder to .gitignore too? (Y = private memory, N = version-controlled)"

### Step 6: Report

```
✓ Memento OS initialized

  "We all need mirrors to remind ourselves who we are."

  Memory:  {memory_path}/
  Score:   █░░░░░░░░░ 1.0 / 10
  Artifacts: 1 ([D]: 1)

  Your first artifact:
  [D] {conclusion} — invalidates if {trigger} [{priority}] [{today}]

  Next session, run /memento:session-start — you'll see this decision
  in your briefing. That's the system working.

  Commands:
  /memento:session-start   — recall what matters
  /memento:session-complete — capture what happened
  /memento:decide          — make choices with OODA
  /memento:grill-me        — stress-test any plan
  /memento:stats           — check your memory score

  Tip: This is a plain markdown folder. Obsidian users get graph view for free.
```

## Edge Cases

- **Monorepo**: ask which sub-project this is for
- **Existing _context.md**: offer to merge or skip (don't overwrite)
- **No decisions yet**: "That's fine — your first decision will be captured next time you run /decide or /session-complete. Memory score starts at 0.5/10."
- **User provides path as argument**: skip Step 1, use provided path

## Criteria

| # | Criterion | Test |
|---|-----------|------|
| C1 | First artifact created | _context.md has at least 1 entry in Active Reasoning Artifacts table? |
| C2 | Memory score displayed | User sees their starting score? |
| C3 | 3 questions or fewer | Init completed with max 3 user prompts? |
| C4 | Next steps shown | User knows what to do in session 2? |
