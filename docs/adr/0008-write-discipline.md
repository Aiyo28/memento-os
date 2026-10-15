# Capture memory automatically at session boundaries, not by manual skill invocation

Skills for memory capture (`session-complete`, `process-inbox`, `strategic-compact`, `knowledge`) all required manual invocation, and users skip them exactly when it matters: at the end of a long session, before context fills, after a critical decision, when switching projects. We use a `Stop` hook that appends a session log entry and the turn's `[D]`/`[I]`/`[E]`/`[S]` artifacts without asking for confirmation, behind the initialization gate from ADR 0005; `PreCompact` covers the context-pressure case (ADR 0007). See `hooks/hooks.json`.

Open: the cost of automatic extraction at every session boundary, how to handle sessions that end abruptly (crash, timeout, terminal closed), and whether a confirm-before-saving prompt is a useful middle ground.
