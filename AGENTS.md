# Memento OS — Operator Letter

You are working on Memento OS with me. Read this before doing anything.

## What this is

Memento OS is a Claude Code plugin for persistent AI memory. The unit is
not "notes" — it's reasoning artifacts: `[D]` decisions, `[I]` insights,
`[E]` evidence/errors, `[S]` seeds. Each one carries an invalidation or
activation trigger. The vault is a retrieval source, not just a write
destination.

This is the OSS reputation lane. No paid tier. No closed cloud. There's a
donation CTA in the README — that's the whole monetization surface, and
it's not the point. The point is to publish the artifact-discipline
approach as a working plugin that people can adopt.

## Who I am here

Solo founder. The plugin ships to other Claude Code users; they install
it via `/memento:init` and get a starter vault. Their vault paths are
configured at install time. I do not know their paths. You do not know
their paths. Don't hardcode any vault path anywhere.

## What this is NOT

- Not "Knowledge OS" and not "Agentic Total Recall" — those are different
  projects. This is Memento OS. Don't conflate them in code, docs, or
  commit messages.
- Not a dev-workflow plugin. Not a project-management plugin. The mission
  is memory; if you find yourself adding a skill that lives outside the
  memory mission, stop and ask me.
- Not a notes app — store conclusions, not conversation fragments.

## How we work together

- Skills that make decisions retrieve before acting. Vault search comes
  first; fresh analysis fills gaps after.
- When you're about to make an architectural choice on a protected domain
  (auth, schema, API contracts, deployment, pricing logic, tag taxonomy),
  pause. Search the vault for prior `[D]` artifacts. Surface what you
  find. Then proceed.
- When you draft a new artifact, follow the format. Format drift across
  artifacts kills the whole retrieval premise.

## Glossary

- **Artifact** — `[D]` / `[I]` / `[E]` / `[S]` row in `_context.md`.
  Carries an invalidation or activation trigger.
- **Decision (`[D]`)** — committed conclusion. `[D] statement — invalidates if X`.
- **Insight (`[I]`)** — observation worth remembering. Same format.
- **Evidence (`[E]`)** — error or falsifiable claim being tracked.
- **Seed (`[S]`)** — future decision pending an explicit trigger.
  `[S] idea — activates when condition`.
- **Lifecycle** — `active → embedded → archived` (success), `active →
  superseded → archived` (replaced), `active → resolved → archived`
  (errors only).
- **Kobe cap** — 24 active artifacts per project `_context.md`. Evict
  noise first when over.
- **You** — the agent doing the work.
- **I / me / we** — the human running Memento OS.
- **Users** — installers of the plugin, with their own vaults.

## Doc index

- `README.md` — user-facing intro + install.
- `NEXT.md` — what to continue this session, what's blocked.
- `CHANGELOG.md` — versioned changes.
- Skills: `skills/*/SKILL.md` (namespaced `memento:*`).
- Commands: `commands/memento/*.md`.
- Hooks: `hooks/hooks.json` (Stop, PreCompact).
- Manifest: `.claude-plugin/plugin.json`.
- Adapters: `adapters/<tool>/` (one subdir per non-Claude-Code AI tool).
- Starter vault template: `starter/obsidian-vault/`.

---

# Critical Gotchas

1. **Never hardcode a vault path.** Users configure via `/memento:init`.
   A hardcoded path breaks every installation that isn't yours.
2. **The name is Memento OS.** Not Knowledge OS, not Agentic Total Recall.
   Cross-naming in code or docs confuses users between three separate
   products.
3. **Mission boundary is memory.** No dev workflow skills, no project
   management skills. Scope-creep here is how the plugin loses focus and
   stops getting adopted.
4. **Store conclusions, not notes.** Every artifact has an invalidation
   or activation trigger. If a draft artifact has neither, it's a note,
   not a memory.
5. **Protected domains always retrieve before deciding** — auth, schema,
   migrations, API contracts, deployment, pricing logic, tag taxonomy.
   Confidence gate: <96% → pause and retrieve, regardless of how obvious
   the decision feels.
6. **Artifact tiers are load-bearing.** L0 = CLAUDE.md "Critical Gotchas"
   (~20, always loaded). L0.5 = `context/` (~800 tok, session-start if
   present). L1 = `_context.md` artifacts table (Kobe-24, every session).
   L2 = `Decisions/` folder (unlimited, on demand). Promotion L1→L0 test:
   "Would violating this waste >1hr?"
7. **Artifact format is `[D|I|E|S] conclusion — invalidates/activates if
   trigger [priority] [date]`.** Drift kills retrieval.
