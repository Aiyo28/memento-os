# memento-os tests

Bash-driven assertions against `lint.py`, `decay.py` and `hooks/memento_hook.py`. No external test framework — matches the repo's existing pattern (bash hooks, markdown skills, no node/pip deps).

## Run

```bash
./tests/run.sh
```

Exit 0 = all pass. Exit 1 = at least one assertion failed.

## What's tested

| Suite | What it asserts |
|-------|----------------|
| `memento:lint` clean | Exit 0, "0 violations" summary, all 5 fixture artifacts checked |
| `memento:lint` violations | Exit 1, every rule (R1–R6) surfaces on its targeted row |
| `memento:lint` strict | `--strict` mode rejects `activates when` form |
| `memento:lint` JSON | `--format json` produces parseable output with rule codes |
| `memento:decay` text | Vault-overlap signal flags [D]#1 LIKELY STALE; recent [D] excluded |
| `memento:decay` JSON | `--format json` produces candidates with signal types |
| `memento:decay` age | High `--age` produces empty candidate list |
| hooks Stop | Hook input JSON in, decision out: blocks once on unsaved artifacts; silent when `stop_hook_active`, when saved in `_context.md` or `Decisions/`, when uninitialized or skipped |
| hooks lookup | `memory_path` from `.memento/config.yaml`; input `cwd` when `CLAUDE_PROJECT_DIR` is unset |
| hooks escape | A config path or symlink to a file not named `_context.md` is ignored; a vault `_context.md` outside the project works; a path with spaces is not printed |
| hooks SessionStart / PreCompact | One-line notice only when uninitialized; PreCompact instructions only when initialized |

## Why property-based assertions, not golden files

Decay scores include `age_days` which shifts with the calendar. Golden-file diffs would break every day. We assert on stable invariants — exit codes, rule codes, key evidence substrings — and let the absolute numbers flex.

`tests/expected/*.out` snapshots are kept for documentation only (they show what a typical run looks like).

## Fixtures

```
fixtures/
  clean/_context.md       — passes lint, no decay candidates
  violations/_context.md  — one row per failing rule
  decay/_context.md       — aged [D] artifacts, one with a vault-overlap supersession
  hooks/                  — projects (initialized, configured, uninitialized, skipped)
                            and Stop hook inputs (stop-*.json)
```
