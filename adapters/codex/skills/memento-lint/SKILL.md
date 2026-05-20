---
name: lint
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

# /lint

Enforce the reasoning-artifact schema across every `_context.md` in a vault. Prose templates can't do this — that's the point.

## What gets checked

| Rule | Applies to | Required text (case-insensitive) |
|------|-----------|----------------------------------|
| R1 | `[D]`, `[I]` | `invalidates if` / `invalidates when` / `dies if` |
| R2 | `[S]` | `Activation:` / `activates when` (use `--strict` for literal `Activation:`) |
| R3 | `[E]` | `fix:` |
| R4 | all | `#` column non-empty |
| R5 | all | priority column non-empty |
| R6 | all | row contains `YYYY-MM-DD` date |
| R7 | warning | malformed table row (unbalanced backticks, <4 cells); promoted to violation under `--strict` |

## How to invoke

```bash
python3 .agents/skills/lint/lint.py [VAULT_ROOT] [--strict] [--ci] [--format json] [--quiet]
```

Vault root resolution: argument → `$MEMENTO_VAULT_ROOT` → CWD.

| Flag | Effect |
|------|--------|
| `--strict` | Requires literal `Activation:` for `[S]`; promotes R7 warnings to violations |
| `--ci` | Sugar for `--strict --quiet` |
| `--format json` | Machine-readable for hooks/CI |
| `--quiet` | Suppress per-file OK lines |

| Exit | Meaning |
|------|---------|
| 0 | clean |
| 1 | violations found |
| 2 | usage / IO error |

## When the agent invokes this

1. User says "lint", "validate", "check artifacts".
2. Run the script via shell.
3. For each violation, ask the user the missing field, then edit the artifact row in place. Re-run lint to confirm clean.

## Don't

- Don't auto-fix without user confirmation.
- Don't widen the rules. Adding `"maybe invalidates if"` defeats the purpose.
- Don't run `--strict` on legacy vaults without warning the user — many existing `[S]` entries use `activates when`.
