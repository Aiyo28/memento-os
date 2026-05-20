# Spec: v2.2.x follow-ups — adapter ports + heuristic refinements

**Date:** 2026-05-20
**Status:** Drafted (not implemented)
**Predecessor:** `docs/specs/2026-05-20-lint-and-decay-verbs.md` (v2.2 Tier 1 ship)

## Scope

Everything deferred from the v2.2 release. Three groups:

1. **Adapter ports** — bring `memento:lint` + `memento:decay` to the remaining 7 AI tools (Codex Tier 1, Cursor/Windsurf/Cline/Gemini Tier 2, Aider/Continue Tier 3).
2. **Heuristic refinements** — observations from dogfooding v2.2 lint + decay on `.vault-cache/`.
3. **Hook + CI scaffolding** — concrete `.pre-commit-config.yaml` and GitHub Actions YAML so users don't have to translate the SKILL.md prose.

Each block is independently shippable. Recommended release cadence below.

## Constraints reaffirmed (carry over from v2.2 spec)

- **No reimplementation** — all adapters invoke the same `lint.py` / `decay.py`. Adapters are discovery layers, not logic layers.
- **No artifact schema changes.** `[D]`/`[I]`/`[E]`/`[S]` grammar stays load-bearing.
- **Git remains optional** for decay.
- **No new package dependencies.** Python 3 stdlib only.
- **No `memento:format` / `memento:reorganize` verb.** That's commodity.

## Release plan

| Version | Scope | Effort | Risk |
|---------|-------|--------|------|
| v2.2.1 | Codex adapter (Tier 1 mirror) | ~30 min | low — pattern is mechanical |
| v2.2.2 | Cursor + Windsurf + Cline rules (Tier 2) | ~45 min | low — append-only edits |
| v2.2.3 | Gemini single-file rules (Tier 2) | ~20 min | low |
| v2.2.4 | Aider CONVENTIONS + Continue config snippet + prompts (Tier 3) | ~45 min | low |
| v2.2.5 | Heuristic refinements (decay stopwords, multi-keyword AND, lint R7 malformed-row) | ~60 min | medium — touches scoring logic; needs new fixtures |
| v2.2.6 | Hook + CI scaffolding (`examples/` directory with copy-paste configs) | ~30 min | low |

Alternative: bundle all six into a single **v2.3.0** release. Choose bundle if Reddit/Discord traction motivates a louder version bump; choose patch cadence if shipping continuously is preferred. **Recommend bundle** — single CHANGELOG block reads cleaner for an OSS announcement.

---

## Block A — Codex adapter (Tier 1)

**File layout** (mirror of `skills/`):

```
adapters/codex/skills/
  memento-lint/
    SKILL.md            ← copy of skills/memento-lint/SKILL.md with name field rewritten
    lint.py             ← symlink or copy of skills/memento-lint/lint.py
  memento-decay/
    SKILL.md
    decay.py
```

**Frontmatter changes** vs Claude Code version:

| Field | Claude Code | Codex |
|-------|-------------|-------|
| `name:` | `memento:lint` | `lint` (Codex doesn't use the `memento:` namespace prefix per existing convention — see `adapters/codex/skills/vault-audit/SKILL.md`) |
| Everything else | identical | identical |

Same for `memento:decay` → `decay`.

**Decision: copy or symlink?**

| Option | Pros | Cons |
|--------|------|------|
| Symlink `.py` to root `skills/` | Single source of truth, no drift | Symlinks ship poorly in some `git archive`/tarball flows; Codex install instructions copy files (`cp -r adapters/codex/skills/ ~/.codex/skills/`) — symlinks would break that step |
| Copy `.py` | Self-contained adapter directory | Manual sync on every script change |
| Generator script (`scripts/sync-adapters.sh`) that copies on demand | No drift, explicit sync step | One more file, one more bash script |

**Recommended: option 3 — generator script.** Add `scripts/sync-adapters.sh` that copies `skills/memento-{lint,decay}/{lint,decay}.py` into every adapter directory that hosts the script. Run it manually before tagging a release. Document the step in `RELEASE.md` (new file, see Block F).

**Update needed in `adapters/codex/AGENTS.md`:** add two rows to the Skills table:

```
| `lint`   | Schema validator for reasoning artifacts — exit non-zero on violation |
| `decay`  | Find aged [D] artifacts whose invalidation triggers may have fired |
```

**Update needed in `adapters/README.md`:** bump the "What You Get" cell for Codex to include the two new skills.

**Tests:** none new. The Codex skill is the same Python script; the existing `tests/run.sh` already covers correctness. Spot-check after the sync: `python3 adapters/codex/skills/memento-lint/lint.py tests/fixtures/clean` exits 0.

---

## Block B — Cursor + Windsurf + Cline (Tier 2 rules)

All three adapters use the same shape: append a workflow section to the existing rules file.

### B.1 Cursor

**File:** `adapters/cursor/rules/memento-workflows.mdc`

**Append section:**

```mdc
## Memento Lint Workflow

Triggers: "lint vault", "validate artifacts", "check artifact schema", "memento lint"

### What it does
Walks every `_context.md` under the vault root and validates each reasoning artifact against the schema. Exits non-zero on any violation — runnable as a pre-commit hook or in CI.

### How to invoke
Run the script directly:
```bash
python3 <path-to-memento-os>/skills/memento-lint/lint.py [vault_root] [--strict] [--format json] [--quiet]
```

Vault root resolution: argument → `$MEMENTO_VAULT_ROOT` → CWD.

### Schema rules (case-insensitive)
- `[D]`/`[I]` must contain `invalidates if` / `invalidates when` / `dies if`
- `[S]` must contain `Activation:` (or `activates when` without `--strict`)
- `[E]` must contain `fix:`
- Every artifact must have a `#` number, a priority, and a `YYYY-MM-DD` date

### After lint surfaces violations
For each violation, ask the user the missing field, then edit the artifact row in place. Re-run lint to confirm clean.

## Memento Decay Workflow

Triggers: "decay check", "what's stale", "memento decay", "audit aged decisions"

### What it does
Finds aged `[D]` artifacts whose invalidation triggers may have fired. Scores from three signals (git keyword grep, vault-state contradiction, age). Surfaces ranked candidates.

### How to invoke
```bash
python3 <path-to-memento-os>/skills/memento-decay/decay.py [vault_root] [--age 30] [--format json] [--no-git]
```

Run with `--format json` when driving an interactive confirmation flow.

### Agent flow
1. Run decay with `--format json`.
2. For each `LIKELY STALE` candidate, prompt user: "Mark `[D]#N` as superseded? (y/n/skip)"
3. On `y`: change priority cell in `_context.md` to `superseded`. Update `Decisions/` file frontmatter if it exists.
4. On `n` / `skip`: leave artifact, optionally capture an `[I]` insight explaining why the trigger hasn't fired.
```

### B.2 Windsurf

**File:** `adapters/windsurf/rules/memento-workflows.md`

Same content as Cursor section above. Windsurf rules use plain Markdown (no `.mdc` frontmatter), so just drop the `---` block at the top.

### B.3 Cline

**File:** `adapters/cline/README.md` currently has no rule file. Decide which:

**Option α** — Create `adapters/cline/.clinerules/memento-workflows.md` containing the same workflow text. Install instructions: copy to `.clinerules/` in user's project.

**Option β** — Append to the existing single rules file if Cline now supports one. Check the install instructions in `adapters/cline/README.md` first.

**Recommended: option α.** Cline's `.clinerules` convention is the documented pattern. Mirror the Windsurf layout.

### Tests for Tier 2
Manual: install each rule file in a sample project, invoke each trigger phrase, confirm the AI runs the correct script and parses output. No automated tests — rules are prompt-only, not code.

---

## Block C — Gemini (Tier 2, single-file)

**File:** `adapters/gemini/GEMINI.md`

Append the same workflow content as the Cursor section to the end of the file. Gemini reads the whole file each session, so prepend a brief table-of-contents entry:

```markdown
- [Memento Lint](#memento-lint-workflow)
- [Memento Decay](#memento-decay-workflow)
```

No structural change. Single file.

---

## Block D — Aider + Continue (Tier 3, manual)

### D.1 Aider

**File:** `adapters/aider/CONVENTIONS.md`

Append two sections (same content as Cursor B.1 above, but rewritten in the imperative voice the rest of CONVENTIONS.md uses — "You MUST run...", "When the user asks 'lint vault', invoke...").

**File:** `adapters/aider/README.md`

Add an "Optional: schema validation" section explaining how to wire `python3 lint.py` as a `/run` command in `.aider.conf.yml`:

```yaml
read:
  - CONVENTIONS.md

commands:
  - name: lint
    run: python3 ${MEMENTO_PLUGIN_ROOT}/skills/memento-lint/lint.py
  - name: decay
    run: python3 ${MEMENTO_PLUGIN_ROOT}/skills/memento-decay/decay.py --format json
```

### D.2 Continue

**File:** `adapters/continue/config-snippet.yaml`

Append two rules entries (use the same compressed prose form as the existing rules):

```yaml
  - >
    Memento OS — Schema Lint (memento:lint):
    Validate every _context.md against the artifact schema.
    [D]/[I] need invalidates clause; [S] needs Activation/activates when;
    [E] needs fix:. Every artifact needs # number + priority + date.
    Invoke: python3 <plugin>/skills/memento-lint/lint.py [vault_root].
    Exit 0 = clean, 1 = violations, 2 = usage error.

  - >
    Memento OS — Decay Audit (memento:decay):
    Find aged [D] artifacts past 30 days whose invalidation triggers
    may have fired. Scores from git log + vault contradictions + age.
    Invoke: python3 <plugin>/skills/memento-decay/decay.py --format json.
    Agent prompts user y/n on each LIKELY STALE candidate; on y,
    change priority cell to `superseded`.
```

**Files:** `adapters/continue/prompts/memento-lint.prompt`, `adapters/continue/prompts/memento-decay.prompt`

Two new slash-command prompts, mirroring the existing `session-start.prompt` shape:

```
name: memento-lint
description: Validate every reasoning artifact in the vault against the schema

---
Run python3 <path>/skills/memento-lint/lint.py on the current vault.
For each violation, ask the user the missing field, then edit the artifact row in place. Re-run lint to confirm clean.
```

```
name: memento-decay
description: Find aged [D] artifacts whose invalidation triggers may have fired

---
Run python3 <path>/skills/memento-decay/decay.py --format json on the current vault.
Parse the JSON candidate list. For each LIKELY STALE entry, prompt the user "Mark [D]#N as superseded? (y/n/skip)".
On y, edit the _context.md row to change the priority cell to `superseded`. Report final tally.
```

### Tests for Tier 3
None automated. Manual install + smoke test against fixtures.

---

## Block E — Heuristic refinements (informed by dogfooding)

### E.1 Decay — project-noise stopwords

**Observation from `python3 skills/memento-decay/decay.py .vault-cache/`:** keywords like `claude`, `code`, `plugin`, `name`, `test`, `rate` are too generic — they match nearly every commit in the memento-os repo, inflating scores. Concrete false positives in the dogfood run:

- `[D]#1 (name "memento-os")` scored +2 from a commit that just mentioned the word "name"
- `[D]#17 (namespace skills as memento:*)` got `claude` and `code` matches on a totally unrelated commit

**Proposal:** per-vault stopword extension. Add `--stopwords <file>` flag pointing at a project-specific stopword list. Default lookup: `<vault_root>/.memento-stopwords` (one word per line). If missing, fall back to current behavior.

For the memento-os dogfood vault, the project-specific stopword file would contain:

```
claude
code
plugin
memento
adapter
skill
vault
```

**Edge case:** the keyword extractor is already case-insensitive and applies STOPWORDS, so this is additive. Test fixture: `tests/fixtures/decay-noisy/` with a project where generic keywords are over-represented; assert score drops after adding the stopword file.

### E.2 Decay — multi-keyword AND in git grep

**Observation:** the current git signal counts each keyword-match commit separately and sums weights. A commit that happens to mention ONE keyword from the invalidator triggers +2. A commit that mentions THREE keywords from the invalidator is far stronger evidence — but only counts +2 once per keyword if all three keywords are in the SAME commit (which they often are).

**Proposal:** change scoring so a single commit matching ≥2 invalidator keywords scores +4 (one strong signal), vs the current behavior where it would score +6 (three weak signals). Avoid double-counting the same commit.

Implementation: collect commits per keyword, group by commit hash, score based on per-commit keyword-overlap count:

| Keywords matched in same commit | Weight |
|---|---|
| 1 | +1 |
| 2 | +3 |
| 3+ | +5 (cap) |

Cap total git score at +6 as before. Test fixture: contrived git history with a "noisy match" (1 keyword in 5 commits = score +5 capped at +6) vs a "strong match" (3 keywords in 1 commit = +5) — verify the strong match outranks.

### E.3 Lint — new rule R7 (malformed table rows)

**Observation from `.vault-cache/_context.md`:** artifacts `#26` and `#27` are silently skipped because the row contains unterminated backtick spans (the artifact text opens with `` ` `` but doesn't close before the priority column). The current parser correctly skips ambiguous rows, but the user has no idea those artifacts are unvalidated.

**Proposal:** add R7 — emit a warning (not a violation) when a row inside the Active Reasoning Artifacts table starts with `|` but fails to parse into 4+ cells OR contains an unterminated backtick span. Use exit code 1 if `--strict` is set; otherwise warn-only (still exit 0 if R1–R6 pass).

**Output line:**

```
  L67   ???        R7: malformed row (unterminated backtick span) — artifact not validated
```

Test fixture: `tests/fixtures/malformed/_context.md` with one unterminated-backtick row. Assert R7 surfaces under default mode (warn, exit 0 if no other violations) and under `--strict` (violation, exit 1).

### E.4 Decay — invalidator extraction polish

**Observation:** when an invalidator phrase ends with `[priority]` markers on the same line, the regex stop-at-`[` cuts cleanly. But when the artifact uses multi-line markdown (rare but real — see `.vault-cache` #26/#27), the regex captures excess text. Already handled by table-row parsing skipping multi-line rows, but worth noting.

No code change recommended — depends on R7 landing first. Once R7 surfaces malformed rows, the user can choose to reformat them onto one line and decay then works correctly.

---

## Block F — Hook + CI scaffolding (`examples/`)

**New files:**

```
examples/
  pre-commit/.pre-commit-config.yaml      ← copy-paste pre-commit config invoking lint
  github-actions/memento-lint.yml         ← GitHub Actions workflow file
  README.md                               ← installation walkthrough
RELEASE.md                                 ← release process (includes sync-adapters.sh step)
scripts/
  sync-adapters.sh                         ← copies lint.py/decay.py into each adapter dir
```

**`examples/pre-commit/.pre-commit-config.yaml`:**

```yaml
repos:
  - repo: local
    hooks:
      - id: memento-lint
        name: memento:lint
        entry: python3 .claude/plugins/memento-os/skills/memento-lint/lint.py
        language: system
        pass_filenames: false
        files: '_context\.md$'
        args: [--quiet]
```

**`examples/github-actions/memento-lint.yml`:**

```yaml
name: memento:lint
on: [pull_request, push]
jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - name: Run memento:lint
        run: |
          python3 .claude/plugins/memento-os/skills/memento-lint/lint.py vault/
```

**`scripts/sync-adapters.sh`:**

```bash
#!/usr/bin/env bash
# Copy lint.py / decay.py into every adapter directory that hosts the script.
# Run before tagging a release.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
for tool in codex; do
  for verb in memento-lint memento-decay; do
    SRC="$ROOT/skills/$verb"
    DST="$ROOT/adapters/$tool/skills/${verb#memento-}"
    if [ -d "$DST" ]; then
      cp "$SRC/${verb#memento-}.py" "$DST/"
      echo "synced $verb → $tool"
    fi
  done
done
```

Tests: `examples/` is documentation; no automated tests. `sync-adapters.sh` gets a sanity check in `tests/run.sh` once Block A lands — assert that after running the script, the copied scripts match the source byte-for-byte.

---

## Open questions

| # | Question | Default if not answered |
|---|----------|-------------------------|
| Q1 | Bundle as v2.3.0 or ship patches v2.2.1–v2.2.6? | Bundle as v2.3.0 |
| Q2 | Symlink or copy adapter scripts? | Copy via `scripts/sync-adapters.sh` |
| Q3 | Should Block E.1 stopword file default location be `.memento-stopwords` or `.memento/stopwords`? | `.memento-stopwords` (matches the existing `.memento/config.yaml` pattern only loosely; the dotfile form is simpler) |
| Q4 | Should R7 default to warn-only or violation? | Warn-only by default, violation under `--strict` |
| Q5 | Add a separate `--ci` flag that combines `--strict --quiet`? | Yes, sugar flag — implement in Block A or skip |

## Decision artifacts this spec would produce

```
[D] Adapter ports bundle as v2.3.0, not patch cadence — invalidates if traction signals appear mid-port that warrant a hotter release window [settled] [2026-05-20]
[D] Adapter scripts are copies maintained by scripts/sync-adapters.sh, not symlinks — invalidates if a packaging tool can't handle the copy step (e.g., HuggingFace/PyPI distribution lands) [settled] [2026-05-20]
[D] R7 (malformed row) ships warn-only; --strict promotes to violation — invalidates if users routinely produce malformed rows and don't notice the warning [volatile] [2026-05-20]
[S] Add project-specific stopword file support to decay — Activation: first time a user complains about noisy git-keyword matches OR memento-os dogfood decay run produces >50% false positives [high] [2026-05-20]
```
