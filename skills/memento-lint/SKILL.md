---
name: memento:lint
version: 1.0.0
description: >
  Validate every reasoning artifact in vault _context.md tables against
  schema rules. [D]/[I] need an invalidates clause, [S] needs an activation
  clause, [E] needs a fix: line, every artifact needs # number + priority +
  YYYY-MM-DD date. Exit non-zero on violation so it runs as a hook or in CI.
  Triggers: "lint vault", "validate artifacts", "check artifact schema",
  "memento lint", "are my decisions valid".
user_invocable: true
---

# /memento:lint

Enforce the reasoning-artifact schema across every `_context.md` in a vault. Prose templates can't do this — that's the point.

## What gets checked

| Rule | Applies to | Required text (case-insensitive) |
|------|-----------|----------------------------------|
| R1 | `[D]`, `[I]` | `invalidates if` / `invalidates when` / `dies if` |
| R2 | `[S]` | `Activation:` / `activates when` (use `--strict` to require literal `Activation:`) |
| R3 | `[E]` | `fix:` |
| R4 | all | `#` column non-empty |
| R5 | all | priority column non-empty |
| R6 | all | row contains a `YYYY-MM-DD` date |

`[I]` shares R1 with `[D]` because the inline grammar documented in `session-complete` is identical (`[I] insight — invalidates if condition`).

## How to invoke

### Default — lint the current vault

```bash
python3 ${MEMENTO_PLUGIN_ROOT:-skills/memento-lint}/lint.py
```

The script discovers the vault root via:
1. The path argument if provided
2. The `$MEMENTO_VAULT_ROOT` env var
3. The current working directory

### Common flags

```bash
# Lint a specific vault
python3 lint.py ~/Documents/Developer/knowledge-os

# Strict mode — require literal "Activation:" for all [S]
python3 lint.py --strict

# Machine-readable output for hooks / CI
python3 lint.py --format json

# Show only violations
python3 lint.py --quiet
```

### Exit codes

| Code | Meaning |
|------|---------|
| 0 | No violations |
| 1 | Violations found |
| 2 | Usage error / vault root missing |

## When the agent invokes this

1. User says "lint", "validate", "check artifacts", or wires lint into a hook.
2. Agent runs `python3 <plugin>/skills/memento-lint/lint.py <vault_root>` via Bash.
3. Agent reads stdout, presents the violation list to the user.
4. For each violation, offer to fix in-place:
   - **R1 missing** — ask user for the invalidation trigger, then `Edit` the artifact row to append `— invalidates if <trigger>`.
   - **R2 missing** — ask user for the activation condition, then append `Activation: <condition>` (or `— activates when <condition>` in lax mode).
   - **R3 missing** — ask user what unblocked the error, then append `— fix: <what solved it>`.
   - **R4/R5/R6** — fix by inspection: assign a `#`, infer priority from the matrix, add today's date.
5. Re-run lint after fixes to confirm green.

## Hook / CI wiring

### pre-commit

```yaml
- repo: local
  hooks:
    - id: memento-lint
      name: memento:lint
      entry: python3 .claude/plugins/memento-os/skills/memento-lint/lint.py
      language: system
      pass_filenames: false
      files: '_context\.md$'
```

### GitHub Actions

```yaml
- name: Validate reasoning artifacts
  run: python3 .claude/plugins/memento-os/skills/memento-lint/lint.py ${{ github.workspace }}/vault
```

## Sample report

```
memento:lint — vault validation report (vault: /Users/me/vault)

Projects/memento-os/_context.md
  L47   [D]#1      OK
  L48   [D]#2      R1: missing 'invalidates if|invalidates when|dies if' clause
  L67   [S]#27     OK

Knowledge/_context.md
  L23   [D]#5      R6: no YYYY-MM-DD date in row

Summary: 2 violations across 2 files (5 artifacts checked)
```

## Done condition

- Lint exits 0 against the vault, OR
- All violations have been triaged (fixed, accepted with override, or artifact removed).

## Don't

- Don't auto-fix without user confirmation. The schema is load-bearing; silently rewriting artifacts erodes trust.
- Don't widen the rules to accommodate sloppy artifacts. Adding `"maybe invalidates if"` etc. defeats the purpose.
- Don't run lint with `--strict` on legacy vaults without warning the user — many existing `[S]` entries use `activates when`.
