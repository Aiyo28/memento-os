# Route every capture to one location; an uninitialized project gets no writes

Knowledge ended up wherever a tool kept its own "dump here" location: session logs in skill inboxes, research notes in agent memory, an implementation plan in `~/.claude/plans/`. Each misplaced file is a future retrieval failure. We decided that captures are routed by rule to the project's `_context.md` and vault, and that the agent never improvises a location.

In 2.3.3 this was enforced in the `Stop` and `PreCompact` hooks: each starts with an initialization gate (a `_context.md` at the project root, under `./memento/`, or at the path in `.memento/config.yaml`) and writes nothing if none exists.

Open: the right granularity for routing rules (per file type or per content category), whether misplacement can be detected by a hook, and what to do when the vault is unreachable without creating permanent orphans.
