# Spec: `memento:lint` + `memento:decay` (v2.2)

**Date:** 2026-05-20
**Status:** Approved for Tier 1 implementation
**Driver:** `[S]#27` — Jeff Su / HubSpot mainstreamed the CLAUDE.md/memory.md/archive.md ontology 2026-05-19. Structural pattern is mass-market commodity within 2–3 months. Memento OS's durable differentiator collapses to the **judgment layer** — schema enforcement and drift detection — neither of which a prose template can replicate.

## Goal

Ship two new verbs in v2.2 that no prose template can replicate:

1. **`memento:lint`** — validate every reasoning artifact against schema rules. Exit non-zero on violation so it runs as a hook or in CI.
2. **`memento:decay`** — find aged `[D]` artifacts whose invalidation triggers may have fired. Rank by signal strength. User confirms supersession.

## Non-Goals

- **No reformatting / "memento:format" / "memento:reorganize" verb.** Prose templates do that. We only ADD value where prose can't reach.
- **No line-count ceilings.** That's Jeff Su's commodity layer.
- **No schema changes to `[D]`/`[I]`/`[E]`/`[S]` grammar.** Load-bearing across the vault.
- **No hard dependency on `git`.** Vault projects don't always live in a repo. `git log` is one signal among many for decay.
- **No Tier 2/3 adapter ports in this release.** Tier 1 (Claude Code) only. Adapter parity is deferred.

## Distribution Surface

| Tier | Tool                                    | This release | Follow-up |
|------|-----------------------------------------|--------------|-----------|
| 1    | Claude Code, Codex                      | Claude Code  | Codex port |
| 2    | Cursor, Windsurf, Cline, Gemini         | —            | Rule snippet |
| 3    | Aider, Continue                         | —            | Manual instructions |

Rationale: both verbs invoke a Python script (`lint.py`, `decay.py`) that is stack-neutral. Tier 1 ports map 1:1 to the Claude Code skill (same script, different SKILL.md frontmatter). Tier 2/3 just point users at the script.

---

## `memento:lint`

### What it does

1. Walks every `_context.md` under a vault root (arg or auto-detect via `$MEMENTO_VAULT_ROOT` → CWD).
2. Locates the `## Active Reasoning Artifacts` section in each file.
3. Parses every row of the markdown table beneath that header.
4. Validates each row against the schema rules below.
5. Emits a report grouped by file with line numbers and violation types.
6. Exits **1** if any violation found, **0** otherwise (**2** on usage/IO error).

### Schema rules

| Rule | Applies to | Required text (case-insensitive) | Why |
|------|-----------|----------------------------------|-----|
| R1 | `[D]`, `[I]` | `invalidates if` OR `invalidates when` OR `dies if` | Decisions/insights without invalidation triggers can't decay. |
| R2 | `[S]` | `Activation:` OR `activates when` | Seeds without activation conditions never surface. |
| R3 | `[E]` | `fix:` | Errors without a fix are unresolved noise. |
| R4 | All | `#` column non-empty | Artifacts must be addressable. |
| R5 | All | priority column non-empty | Priority drives eviction order. |
| R6 | All | row contains `YYYY-MM-DD` date | Required for decay scans + staleness. |

`[I]` (insight) shares R1 with `[D]` because the inline format documented in `session-complete` is `[I] insight — invalidates if condition`. Same grammar, same rule.

### Why "Activation:" OR "activates when"

User spec listed only `Activation:`. The existing vault uses both forms — e.g., `.vault-cache/_context.md` artifacts `#23`/`#24` use `activates when` inline, `#27` uses the `**Activation:**` block. Lint accepts both, mirroring how `[D]` accepts three synonyms. Strict-`Activation:`-only mode is available via `--strict`.

### Invocation

```bash
python3 skills/memento-lint/lint.py [VAULT_ROOT] [--strict] [--format text|json] [--quiet]
```

- `VAULT_ROOT` — defaults to `$MEMENTO_VAULT_ROOT` or current working directory
- `--strict` — disallow `activates when` for `[S]`; require literal `Activation:`
- `--format json` — machine-readable output for hooks/CI consumers
- `--quiet` — suppress per-file OK lines; show only violations + summary

### Exit codes

| Code | Meaning |
|------|---------|
| 0 | No violations |
| 1 | Violations found |
| 2 | Usage error / vault root missing / IO error |

### Sample output

```
memento:lint — vault validation report (vault: ~/Documents/Developer/knowledge-os)

Projects/memento-os/_context.md
  L47  [D]#1  OK
  L48  [D]#2  R1: missing invalidates clause
  L67  [S]#27 OK

Knowledge/_context.md
  L23  [D]#5  R6: no YYYY-MM-DD date in row

Summary: 2 violations across 2 files (5 artifacts checked)
```

### Hook integration

A repo can wire lint as a pre-commit hook:

```yaml
# .pre-commit-config.yaml
- repo: local
  hooks:
    - id: memento-lint
      name: memento:lint
      entry: python3 .claude/plugins/memento-os/skills/memento-lint/lint.py
      language: system
      pass_filenames: false
      files: '_context\.md$'
```

---

## `memento:decay`

### What it does

1. Walks every `_context.md`, collects every `[D]` artifact with a date older than 30 days (threshold configurable via `--age`).
2. For each, extracts the invalidator phrase (text after `invalidates if|when|dies if`).
3. Assesses likelihood that the trigger has fired using **three signals**:
   - **(a) Git keyword search** — when a git repo is reachable, run `git log --all --grep <keyword>` for noun-phrase tokens extracted from the invalidator. Each match is a signal point.
   - **(b) Vault state contradiction** — scan all `_context.md` files for newer artifacts whose conclusion contradicts the candidate. Heuristic: same key terms appear in a `[D]`/`[I]` dated AFTER the candidate.
   - **(c) Interactive confirmation** — if (a) and (b) are both null/inconclusive, defer to the agent which asks the user one yes/no question.
4. Emits a ranked list of candidates with their triggering signal(s).
5. The Claude Code agent reads the JSON output, runs the user-facing y/n prompts, and on confirmation marks the artifact `superseded` (per existing session-complete eviction protocol).

### Signal weights

| Signal | Weight | Notes |
|--------|--------|-------|
| (a) git log match for invalidator keyword | +2 per matching commit, cap at +6 | Most direct: the trigger phrase appears in commit history |
| (b) newer artifact with overlapping terms | +3 per overlapping artifact | Strong: the vault itself documents the supersession |
| (c) age past threshold only | +1 | Weak: just old |

Candidates with score ≥ 3 are flagged "likely stale". Score 1–2 are "review". Score 0 are skipped unless `--all` is set.

### Invocation

```bash
python3 skills/memento-decay/decay.py [VAULT_ROOT] [--age 30] [--format text|json] [--no-git]
```

- `--age N` — minimum age in days (default 30)
- `--no-git` — skip git signal even if repo is present (offline / privacy)
- `--format json` — agent consumes JSON to drive user-facing prompts

### Why git is optional, not required

User spec: "vault projects don't always live in git." If `git status` fails or no `repo_path` field in `_context.md` frontmatter, decay falls back to signals (b) and (c) only. The script never errors on missing git.

### Sample JSON output (consumed by the agent)

```json
{
  "vault_root": "/home/user/vault",
  "candidates": [
    {
      "file": "Projects/memento-os/_context.md",
      "line": 51,
      "number": "6",
      "artifact": "[D] Phase 1 assumes clean install, Phase 2 handles merge...",
      "invalidator": "if most users have existing setups (test during beta)",
      "age_days": 64,
      "score": 5,
      "signals": [
        {"type": "git", "weight": 2, "evidence": "commit 9e43abc mentions 'merge'"},
        {"type": "vault", "weight": 3, "evidence": "Projects/memento-os/_context.md #25 (2026-04-14) supersedes"}
      ]
    }
  ]
}
```

### Agent flow (SKILL.md)

1. Run `decay.py --format json` against the user's vault.
2. Present ranked candidates to the user.
3. For each high-confidence candidate, ask: "Mark `[D]#N` as superseded? (y/n)"
4. On `y`, edit the artifact's row: change priority to `superseded`. Per `session-complete` rules, full file moves to `Decisions/` with `status: superseded` if it has one.
5. Report: X superseded, Y kept, Z deferred.

---

## Multi-adapter strategy (deferred)

8-adapter parity is the long-term promise. For v2.2 we ship Claude Code only. Adapter ports planned for v2.2.x:

| Tier | Adapter | Port form |
|------|---------|-----------|
| 1 | Codex | Copy `skills/memento-lint/` + `skills/memento-decay/` to `adapters/codex/skills/`. Update `adapters/codex/AGENTS.md` skill table. |
| 2 | Cursor, Windsurf, Cline | Append "Memento Lint" + "Memento Decay" sections to `adapters/{tool}/rules/memento-workflows.mdc`. Tells the AI when to invoke the Python script. |
| 2 | Gemini | Append to `adapters/gemini/GEMINI.md`. |
| 3 | Aider, Continue | Document manual invocation in `adapters/{tool}/README.md`. |

All tiers invoke the same `lint.py`/`decay.py` scripts. No per-adapter reimplementation.

## Testing

The repo has no pre-existing test framework. Lightest-weight pattern that matches the repo's style (markdown-first, bash hooks):

```
tests/
  fixtures/
    clean/_context.md           — passes lint, no decay candidates
    violations/_context.md      — one [D]/[I]/[E]/[S] each failing its rule
    decay/_context.md           — aged [D] artifacts for decay
  expected/
    clean.out, violations.out
  run.sh                        — bash driver: invoke scripts, diff against expected
  README.md
```

`tests/run.sh` exits non-zero on any test failure. CI-ready, no external test runner needed.

Additionally, lint is dogfooded against `.vault-cache/_context.md` (real-world vault) and `starter/obsidian-vault/Projects/_example-project/_context.md` (template).

## Open questions

- None blocking implementation. Adapter ports tracked as v2.2.x follow-up.

## Decision artifacts produced by this spec

```
[D] memento:lint + memento:decay are the v2.2 differentiator verbs — invalidates if mainstream templates start shipping equivalent schema enforcement (unlikely without the [D]/[I]/[E]/[S] grammar) [critical] [2026-05-20]
[D] Both verbs implemented as Python 3 stdlib scripts invoked from SKILL.md — invalidates if vault scale demands a compiled binary or daemon [settled] [2026-05-20]
[D] Tier 2/3 adapter ports deferred to v2.2.x — invalidates if user feedback in first week demands cross-tool parity at launch [settled] [2026-05-20]
[D] Lint accepts both `Activation:` and `activates when` for [S] — invalidates if dogfood reveals the laxer form lets bad seeds through [volatile] [2026-05-20]
```
