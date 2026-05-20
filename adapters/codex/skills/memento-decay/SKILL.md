---
name: decay
version: 1.0.0
description: >
  Find aged [D] artifacts whose invalidation triggers may have fired. Scans
  vault _context.md tables, parses the invalidates-if clause, scores decay
  from git log keyword search + vault contradiction + age. Emits ranked
  candidates with the triggering signal. User confirms → artifact marked
  superseded.
  Triggers: "decay check", "what's stale", "memento decay", "find stale
  decisions", "audit aged artifacts".
user_invocable: true
---

# /decay

Walk every `[D]` artifact past its freshness window, look for evidence the invalidation trigger has fired, prompt the user to mark stale ones `superseded`.

## Signals

| Signal | Weight | Source |
|--------|--------|--------|
| Git commits matching N invalidator keywords | +1 (1kw) / +3 (2kw) / +5 (3+kw), cap +6 | `git log --grep` grouped per-commit |
| Newer vault artifact with ≥2 overlapping terms | +3 per match | scan all `_context.md` |
| Age past 90 days with no other signal | +1 | weak |

Tiers: score ≥3 = LIKELY STALE; 1–2 = REVIEW; 0 = skipped unless `--all`.

## How to invoke

```bash
python3 .agents/skills/decay/decay.py [VAULT_ROOT] \
  [--age 30] [--format text|json] [--no-git] [--all] [--stopwords <file>]
```

Vault root resolution: argument → `$MEMENTO_VAULT_ROOT` → CWD.

A per-vault stopword list at `<vault_root>/.memento-stopwords` is loaded automatically (one word per line, `#` comments). Use this to suppress project-specific noise words (e.g., the project's own name, dominant tech terms).

## Agent flow

1. Run with `--format json`.
2. For each LIKELY STALE candidate, prompt: "Mark `[D]#N` as superseded? (y/n/skip)".
3. On `y`: change priority cell to `superseded`. Update `Decisions/` file frontmatter if present.
4. On `n`: optionally capture an `[I]` insight explaining why the trigger hasn't fired.

## Don't

- Don't auto-supersede. Every supersession needs user confirmation.
- Don't pass `--no-git` silently when a repo IS available.
- Don't widen the vault-overlap threshold (≥2 keywords).
