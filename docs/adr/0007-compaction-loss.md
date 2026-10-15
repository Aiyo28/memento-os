# Save unwritten artifacts to disk before context compaction

Auto-compaction summarizes older conversation and destroys what has not been written down yet: unsaved decisions, partial reasoning, file paths and verbally stated preferences. A manual `strategic-compact` skill depends on the user remembering, and they usually remember after compaction has happened. We use a `PreCompact` hook that scans the conversation for unwritten `[D]`/`[I]`/`[E]`/`[S]` artifacts, updates the `_context.md` artifacts table (Kobe cap 24, evicted rows archived to `Decisions/`) and updates `NEXT.md`, silently and behind the initialization gate from ADR 0005 (`hooks/hooks.json`).

Open: whether the hook can detect approaching compaction rather than reacting to it, the right extraction format, and how to separate "worth saving" from routine context.
