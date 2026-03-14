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
status: <draft | active | archived>
confidence: <high | medium | low>
language: <en | ru>
summary: >
  One paragraph written for LLM consumption. Describe what the document
  contains, why it exists, and what a reader would learn from it.
---
```

### Allowed `type` values

| Value | Use for |
|-------|---------|
| `research` | Source-extracted research note |
| `knowledge-extract` | Synthesized insight or pattern (cross-project) |
| `note` | Working note, scratch thinking |
| `decision` | Decision record with rationale |
| `project-context` | Project `_context.md` files |
| `session-log` | Session log files |
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
| `Projects/{name}/Notes/` | Working notes, scratch | Can be messy, not indexed |
| `Projects/{name}/sessions/` | SESSION_LOG.md, archive | Managed by `/session-complete` |
| `Knowledge/` | Cross-project insights | Must be transferable, not project-specific |
| `Knowledge/patterns/` | Reusable patterns | Must have context / pattern / why structure |
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
