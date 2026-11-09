# Examples

Copy-paste configs for wiring Memento OS into automated workflows.

| File | Purpose |
|------|---------|
| `pre-commit/.pre-commit-config.yaml` | Run `memento:check` as a pre-commit hook. Fails the commit if any artifact violates the schema. |
| `github-actions/memento-check.yml` | Run `memento:check` in CI on every push/PR that touches a `_context.md`. |

## Pre-commit

```bash
cp examples/pre-commit/.pre-commit-config.yaml /path/to/your/project/
cd /path/to/your/project
pip install pre-commit
pre-commit install
```

Adjust the `entry:` path if your Memento OS plugin lives somewhere other than `.claude/plugins/memento-os/`.

## GitHub Actions

```bash
mkdir -p /path/to/your/project/.github/workflows
cp examples/github-actions/memento-check.yml /path/to/your/project/.github/workflows/
```

Adjust the vault path in the `Run memento:check` step (defaults to `${GITHUB_WORKSPACE}/vault`).

## Flag reference

| Flag | What it does |
|------|--------------|
| `--ci` | Sugar for `--strict --quiet`. Strictest schema check, output limited to violations. Recommended for hooks/CI. |
| `--strict` | Promotes R7 warnings (malformed table rows) to violations. Also disallows `activates when` for `[S]` artifacts (requires literal `Activation:`). |
| `--quiet` | Suppresses per-file "OK" lines. |
| `--format json` | Machine-readable output for downstream tools. |
