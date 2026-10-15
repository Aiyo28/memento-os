# Load project context in three tiers with token budgets

Loading all project documentation at session start cost ~5,200 tokens and diluted the agent's attention; loading nothing forced a "what is this project?" round-trip every session; CLAUDE.md "read this file" instructions were followed inconsistently. We load context in tiers and never load L2 at session start:

- **L0** — `NEXT.md`, ~200 tokens, always loaded. Continue / Decide / Blocked, at most 15 lines, updated at the end of each session.
- **L1** — `CLAUDE.md` + `_context.md`, ~500 tokens, always loaded. Overview and a document index with one-sentence summaries.
- **L2** — full documents, 1-2K tokens each, loaded on demand when the L1 index says they are relevant.

Consequences: measured over 20 sessions, session-start context dropped from ~5,200 to ~700 tokens with no measurable loss in task quality; L2 is read in roughly 30% of sessions. Open: whether L2 needs its own tiering at larger project sizes. Term definitions: `docs/GLOSSARY.md`.
