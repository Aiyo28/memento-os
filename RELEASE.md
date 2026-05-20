# Release process

Memento OS is a content-first repo — no build, no dependencies. Releases are git tags + GitHub Releases.

## Before tagging

1. **Sync adapter scripts** — copies `skills/memento-{lint,decay}/*.py` into every adapter directory that ships its own copy:
   ```bash
   ./scripts/sync-adapters.sh
   ```
   Run this any time `lint.py` or `decay.py` change. Forgetting this leaves the adapters running stale logic.

2. **Run the test suite**:
   ```bash
   ./tests/run.sh
   ```
   All assertions must pass.

3. **Lint the repo's own vault cache** (informational — does not block release):
   ```bash
   python3 skills/memento-lint/lint.py .vault-cache
   ```

4. **Bump version** in `.claude-plugin/plugin.json` and add a `[N.N.N] — YYYY-MM-DD` section to `CHANGELOG.md`.

5. **Review NEXT.md** — clear any "Continue" items that this release closes; archive the rest.

## Tagging

```bash
git add -A
git commit -m "chore: release vN.N.N"
git push
git tag vN.N.N
git push origin vN.N.N
```

## GitHub Release

```bash
gh release create vN.N.N \
  --title "vN.N.N" \
  --notes-file RELEASE_NOTES_vN.N.N.md  # optional
```

If no separate release notes file, paste the CHANGELOG section into the release body.

## Post-release

- Delete any `RELEASE_NOTES_vN.N.N.md` draft files.
- Update vault `_context.md` Status field with the release URL.
- If the release adds user-visible features, draft a Reddit/Discord post (Path B reputation cadence).
