# Block dangerous tool calls with deterministic PreToolUse hooks, not prompt rules

Three incidents in one week (a hardcoded API key committed, `rm -rf .` instead of `rm -rf ./dist`, a force push over a teammate's commits) showed that CLAUDE.md rules were followed only ~80% of the time, and post-commit scanning catches a secret after it is already in history. We intercept the operation before it runs with shell hooks at the tool layer, below the model's reasoning:

- **Secrets (`Write`/`Edit`)** — block known key prefixes with 20+ characters, PEM private key headers and generic credential assignments; skip placeholders, env-var references and values under 8 characters.
- **Destructive commands (`Bash`)** — block `rm -rf` on root/home/cwd, `DROP`/`TRUNCATE TABLE`, `chmod 777`, raw `dd` to disk devices.
- **Git safety (`Bash`)** — block force push, `reset --hard`, `checkout -- .`, `branch -D`, staging `.env`/`*.pem`/`credentials.json`.

Each hook prints what it blocked and a safer alternative. CLAUDE.md rules still reduce how often the hooks fire; the hooks cover what slips through. Observed over 8+ weeks: no secret leaks, no destructive deletes, no accidental force pushes, ~2% false positives (placeholders), which cost seconds against hours for a miss.

Status: design record. The `hooks/hooks.json` shipped in this plugin contains `SessionStart`, `Stop` and `PreCompact` prompt hooks only; no `PreToolUse` hooks. Open: whether to log blocked attempts, and whether `PostToolUse` hooks should verify writes.
