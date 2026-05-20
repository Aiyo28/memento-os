---
name: memento:decay
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

# /memento:decay

Walk every `[D]` artifact past its freshness window, look for evidence the invalidation trigger has fired, and prompt the user to mark stale ones `superseded`.

## What signals drive scoring

| Signal | Weight | Source |
|--------|--------|--------|
| (a) git log keyword match | +2 per match, cap +6 | `git log --grep` on noun-phrase tokens from the invalidator |
| (b) newer artifact with overlapping terms | +3 per match | scan all `_context.md` for later `[D]`/`[I]` whose conclusion overlaps |
| (c) age past 90 days with no other signal | +1 | weak; surfaces only when (a)/(b) are silent |

Tiers:
- **LIKELY STALE** — score ≥ 3 — strong evidence; prompt user to supersede
- **REVIEW** — score 1–2 — possible drift; ask user to confirm or extend
- **AGE-ONLY** — score 0 with `--all` — surface only when explicitly requested

## How to invoke

```bash
python3 ${MEMENTO_PLUGIN_ROOT:-skills/memento-decay}/decay.py [VAULT_ROOT] \
  [--age 30] [--format text|json] [--no-git] [--all]
```

- `--age N` — minimum age in days (default 30)
- `--no-git` — skip git signal (use when offline or when vault is outside any repo)
- `--all` — include candidates with score 0 (pure age)
- `--format json` — recommended when the agent drives interactive supersession

Vault root resolution: arg → `$MEMENTO_VAULT_ROOT` → CWD.

The script never errors on missing git — if `find_git_root` returns nothing, git signal is silently skipped. Vault-only projects work the same.

## Agent flow

1. Run `decay.py --format json <vault_root>`.
2. Parse the JSON candidate list (already sorted by score, highest first).
3. For each **LIKELY STALE** candidate, prompt the user:
   ```
   [D]#<n> ({file}, {age_days}d old)
   Conclusion: {artifact}
   Invalidator: {invalidator}
   Evidence the trigger fired:
     - {signal 1}
     - {signal 2}
   Mark as superseded? (y/n/skip)
   ```
4. On `y`:
   - `Edit` the row in `_context.md` — change the priority cell from `critical`/`volatile`/etc. to `superseded`.
   - If a full file exists in `Decisions/`, update its frontmatter `status: superseded` and add a `superseded_by:` reference if known.
   - Per `vault-audit` rules, `superseded` artifacts should be evicted on next cap check.
5. On `n` — leave artifact in place. If user explains why the invalidator hasn't fired, capture it as an `[I]` insight via `session-complete`.
6. On `skip` — defer to next decay run.
7. For **REVIEW** tier: same prompt, but framed as "uncertain — your call."
8. Final report: `X superseded, Y kept, Z deferred. Re-run anytime.`

## When to run

- **Monthly cadence** — vault-audit can call decay as a sub-step.
- **Before a release** — confirm load-bearing `[D]`s still hold.
- **After a domain pivot** — when the project's direction changes, every old decision in that domain is suspect.
- **On user request** — "audit aged decisions", "what's gone stale".

## What it does NOT do

- **Does not auto-supersede.** Every supersession requires user confirmation.
- **Does not require git.** Git is one signal among three. Vault-only projects are first-class.
- **Does not score `[I]`/`[E]`/`[S]`.** Only `[D]` artifacts have invalidation triggers worth tracking on this cadence. `[S]` activation is checked at `session-start`; `[E]` errors evict per `session-complete` rules.
- **Does not modify any file.** The script is read-only; only the agent's `Edit` calls write back.

## Sample text output

```
memento:decay — aged decisions (vault: /Users/me/vault)

[LIKELY STALE] Projects/memento-os/_context.md [D]#6 (age 64d, score 5)
  artifact: [D] Phase 1 assumes clean install, Phase 2 handles merge with existing CLAUDE.md ...
  invalidator: most users have existing setups (test during beta)
  + vault (+3): Projects/memento-os/_context.md [D]#25 (2026-04-14) overlap: install,merge,setups
  + git (+2): keyword 'merge' matched: 9e43abc docs: update README — area-level vault structure

[REVIEW] Knowledge/_context.md [D]#12 (age 41d, score 2)
  ...

Summary: 2 candidates (1 likely stale)
```

## Done condition

- All LIKELY STALE candidates triaged (superseded, kept-with-rationale, or deferred).
- REVIEW candidates surfaced to the user — disposition optional.
- Vault contains zero `[D]` artifacts older than the freshness threshold with active invalidation evidence.

## Don't

- Don't pass `--no-git` silently when a git repo IS available — the user gets weaker signal without knowing.
- Don't widen vault overlap scoring (lower the 2-keyword threshold). False positives are worse than missed decay; the user loses trust faster.
- Don't decay `[D]`s younger than `--age`. New decisions earn their settling time.
