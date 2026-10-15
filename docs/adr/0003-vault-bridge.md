# Bridge the knowledge vault to the agent with a sync hook, a routing table and `_context.md` as vault L1

Agent memory (per-project, always loaded) and the knowledge vault (cross-project, invisible to the agent) were disconnected. Reading named files by hand does not support discovery; loading the whole vault (~50K tokens for 135 files) destroyed the context budget; grep-on-demand misses semantic matches and depends on the agent knowing to search. The agent lacked a map of what exists, so we added three parts built on the tiers in ADR 0001:

- **Sync hook** — a `SessionStart` hook copies only the current project's TODO and `_context.md` from the vault into a local `.vault-cache/` (under one second), so the agent reads local files and still works if the vault path is unreachable.
- **Routing table** — a project registry in the global `CLAUDE.md` maps each project to its vault context path, so the agent navigates instead of searching.
- **`_context.md` as vault L1** — a document index with one-sentence summaries, open questions and related hubs (~300 tokens); the agent loads a full vault document only when the index points to it.

Write-back goes through the `process-inbox` and `session-complete` skills, which closes the read/write loop.

Status: design record. This plugin's `SessionStart` hook only checks whether the project is initialized; it does not sync a vault cache. Open: a summary-only sync for very large `_context.md` files, an explicit warning when the vault is unreachable, and automatic write-back prompts.
