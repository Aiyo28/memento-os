# Vault Conventions

Standards for all files in this knowledge vault. Agents and humans follow these
rules when creating or editing documents.

---

## Frontmatter Schema

Every document requires all 10 fields. No exceptions.

```yaml
---
title: "Descriptive Title in Sentence Case"
type: <see allowed values below>
project: "<project-slug or empty string>"
tags: [domain/subtopic, domain/subtopic]
created: YYYY-MM-DD
updated: YYYY-MM-DD
status: <draft | active | archived | superseded>
confidence: <high | medium | low>
language: <en | ru>
summary: >
  One paragraph written for LLM consumption. Describe what the document
  contains, why it exists, and what a reader would learn from it.
---
```

### Optional Fields (by type)

For `project-context` type:
```yaml
repo_path: ""              # Absolute path to code repo. Empty for vault-only projects.
repo_docs_path: ""         # Relative path from repo root to docs directory.
```

For `experiment-context` type:
```yaml
hypothesis: ""             # What you're testing
success_criteria: ""       # How you'll know it worked
```

### Allowed `type` values

| Value | Use for |
|-------|---------|
| `research` | Source-extracted research note |
| `knowledge-extract` | Synthesized insight or pattern (cross-project) |
| `note` | Working note, scratch thinking |
| `decision` | Decision record with rationale |
| `project-context` | Project `_context.md` files |
| `experiment-context` | Hypothesis-driven exploration, time-boxed |
| `session-log` | Session log files |
| `reference` | Peer cards, glossaries, stable reference material |
| `guide` | MOCs, how-to guides, pattern collections |
| `index` | Index or registry files |

---

## Naming Conventions

| Rule | Example |
|------|---------|
| Use sentence case with spaces | `Rate limiting strategies.md` |
| Never use camelCase or kebab-case for filenames | Not `rate-limiting.md` |
| Dates in filenames use ISO format | `2024-03-14 Session log.md` |
| Session logs do not use dates in filename | `SESSION_LOG.md` (single rolling file) |
| Pattern files use sentence case | `Retry with exponential backoff.md` |

---

## Folder Rules

| Folder | Content type | Notes |
|--------|-------------|-------|
| `Projects/{name}/` | All project-specific content | One subfolder per project |
| `Projects/{name}/Research/` | Source extracts and research | Output of `/knowledge --deep` |
| `Projects/{name}/Decisions/` | Full artifact files | L2 archive for critical/volatile artifacts |
| `Projects/{name}/Notes/` | Working notes, scratch | Can be messy, not indexed |
| `Projects/{name}/Sessions/` | SESSION_LOG.md, archive | Managed by `/session-complete` |
| `Projects/{name}/Experiments/` | Time-boxed explorations | `experiment-context` type, has teardown date |
| `Knowledge/` | Cross-project insights | Must be transferable, not project-specific |
| `Knowledge/patterns/` | Reusable patterns | Must have context / pattern / why structure |
| `People/` | Peer cards for collaborators and self | Loaded partially by `/session-start` |
| `_inbox/` | Raw captures only | Never write final docs here |
| `_meta/` | Vault infrastructure | Conventions, indexes, this file |

---

## Tag Guidelines

- Use nested `domain/subtopic` format: `auth/jwt`, `infra/caching`, `ai/prompting`
- Use 3-7 tags per document — fewer is better if precise
- Tags describe what the document is about, not what it mentions in passing
- Avoid single-word generic tags: `code`, `notes`, `misc`

### Common tag domains

`auth/` · `infra/` · `frontend/` · `backend/` · `ai/` · `data/` ·
`product/` · `business/` · `research/` · `pattern/` · `decision/`

---

## Wikilink Conventions

- Use a `## Related` section at the bottom of documents with links to MOCs or
  parent indexes
- Link to MOCs (Maps of Content), not to individual documents
- Format: `[[MOC — Domain Name]]`
- Keep Related sections short — 2-4 links maximum

Example:
```markdown
## Related
- [[MOC — Authentication]]
- [[MOC — Infrastructure Patterns]]
```

---

## Bilingual Support (optional)

The vault supports English and Russian documents. Set the `language` field
accordingly (`en` or `ru`). Documents in different languages on the same topic
are separate files — do not mix languages within a single document.

---

## Summary Field Guidelines

The `summary` field is the primary LLM retrieval surface. Write it as if
explaining the document to an agent that cannot open the file:

- State what the document contains (not just the topic)
- Include the key conclusion or recommendation if there is one
- 2-5 sentences, no bullet points inside the summary
- Write in the same language as the document

---

## Artifact Tier System

Reasoning artifacts live at three tiers based on access frequency and authority:

| Tier | Location | Cap | Purpose |
|------|----------|-----|---------|
| L0 — Constraints | CLAUDE.md "Critical Gotchas" section | ~20 items | Hard rules. Violating one wastes >1 hour of work. |
| L1 — Active | `_context.md` Active Reasoning Artifacts table | 24 (Kobe cap) | Active reasoning, loaded every session via `/session-start`. |
| L2 — Archive | `Decisions/` folder (per-project) | Unlimited | Full artifact files with context, rationale, evidence. |

### Promotion Rules

- **L1 → L0**: when violating an artifact would waste >1 hour. Copy the rule to CLAUDE.md Critical Gotchas AND keep in L1.
- **L1 → L2**: critical and volatile artifacts automatically get a full file in `Decisions/` alongside the inline L1 entry.

### Eviction Rules (L1 → L2)

When at Kobe cap (24 artifacts), evict by priority: **noise → settled → volatile**. Never auto-evict critical.

Eviction triggers:
- `embedded` — decision is in code/config, self-documenting (has file/line reference, not referenced in 30+ days)
- `superseded` — replaced by a newer `[D]` on the same topic
- `resolved` — error artifact that produced a decision (the `[D]` persists, the `[E]` evicts)
- `dormant` — `[S]` seed not activated after 90 days

Evicted artifacts move to `Decisions/` before removal from the L1 table.

### Artifact Lifecycle

```
active → embedded → archived    (decision is in code now)
active → superseded → archived  (replaced by newer decision)
active → resolved → archived    (errors only — learning extracted)
```

---

## Mid-Task Retrieval Protocol

Before making decisions or generating new reasoning, check the vault for prior
conclusions on the same domain. The vault is a retrieval source, not just a
write destination.

### Confidence Gate

Self-assess: "Do I have full context for this domain?" If confidence < 96%,
pause and retrieve before acting.

### Protected Domains (always retrieve, regardless of confidence)

- Authentication / authorization patterns
- Database schema / migration decisions
- API contract decisions
- Deployment / infrastructure choices

### Retrieval Sequence

1. Scan `_context.md` Active Reasoning Artifacts table for `[D]` entries matching the domain
2. Glob `Decisions/*{topic}*` for full artifact files
3. If prior decision found → surface it: "Existing decision: `[D] {statement}` — {date}"
4. Ask: "Reaffirm, revise, or override?"
5. If no prior decision → proceed with fresh analysis

---

## MOC Pattern (Map of Content)

MOCs are hub documents that link related notes across domains.

| Rule | Example |
|------|---------|
| Naming | `MOC — {Scope}.md` (em-dash, not hyphen) |
| Placement | `Knowledge/MOC — {name}.md` |
| Type | `guide` |
| Creation trigger | 3+ documents share a domain that has no MOC |

Every Knowledge/ note should link to at least one MOC via `## Related`.

MOC content: brief scope description, linked list of related notes with one-line
summaries, `## Related MOCs` section at bottom linking peer hubs.

---

## Scaled Vault Pattern (INDEX.md)

When a project or Knowledge/ folder exceeds ~30 notes, create an `INDEX.md` as
a machine-readable registry. Agents read INDEX.md first for topic-scoped
retrieval — cheaper than globbing every file.

Format:
```markdown
| Path | Type | Summary | Status |
|------|------|---------|--------|
| Research/auth-patterns.md | research | JWT vs session comparison | active |
```

Maintained by the AI on every note create/rename/delete. Not a manual task.

---

## Experiment Structure

For hypothesis-driven work (spikes, prototypes, time-boxed explorations):

```
Projects/{name}/Experiments/{experiment-name}/
├── _context.md      # type: experiment-context, hypothesis, success criteria
├── Notes/           # Working notes (create on demand)
└── Results/         # Outcome documentation (create on demand)
```

Frontmatter includes `hypothesis` and `success_criteria` fields.

Lifecycle: experiments graduate to projects when proven viable, get archived
when hypothesis fails. Target duration: weeks, not months. `vault-audit` flags
experiments past their teardown date.

---

## Context Directory (L0.5) — Optional

For projects with significant business context (client constraints, stakeholder
profiles, domain vocabulary), create a `context/` directory at the project root:

```
context/
├── domain-terms.md      # Domain vocabulary and constraints
├── stakeholder-profiles.md  # Key people and their priorities
└── constraints.md       # Non-negotiable requirements
```

L0.5 sits between CLAUDE.md (L0) and `_context.md` (L1). `/session-start` loads
it after L0 if present. Keep each file under 300 tokens. Total budget: ~800
tokens per session.

---

## Retrieval Patterns

Two complementary retrieval modes:

**Telescope (L0 → L3)** — sequential depth-first. Project-scoped drill-down.
Read gotchas → active artifacts → full decisions → deep vault. Used for:
"What do we know about X in this project?"

**Radar (fan-out)** — simultaneous breadth across all projects. Glob
`Projects/*/Decisions/*{topic}*` and cross-project `_context.md` files. Used
for: "Has this problem been solved before anywhere in the vault?"

Radar is expensive (many file reads). Use it for cross-project research only,
not routine session-start loading
