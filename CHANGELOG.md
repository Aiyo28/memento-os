# Changelog

## [2.2.0] — 2026-05-20

### Added
- **`memento:lint`** (Tier 1 / Claude Code) — schema validator for reasoning artifacts. Walks every `_context.md` under a vault root and enforces:
  - `[D]`/`[I]` must contain `invalidates if` / `invalidates when` / `dies if`
  - `[S]` must contain `Activation:` (or `activates when` in lax mode)
  - `[E]` must contain `fix:`
  - Every artifact must have a `#` number, a priority, and a `YYYY-MM-DD` date

  Exits non-zero on any violation — runnable as a pre-commit hook or in CI. `--strict`, `--format json`, `--quiet` flags. Script: `skills/memento-lint/lint.py`.
- **`memento:decay`** (Tier 1 / Claude Code) — finds aged `[D]` artifacts whose invalidation triggers may have fired. Scores decay from three signals:
  - Git log keyword search (best-effort; gracefully skipped when no repo)
  - Newer vault artifacts with overlapping terms (supersession evidence)
  - Age past 90 days with no other signal (weak)

  Emits ranked candidates (text or JSON). The agent reads JSON output and prompts user `y/n` on each `LIKELY STALE` candidate; on confirmation the artifact is marked `superseded`. Script: `skills/memento-decay/decay.py`.
- **`docs/specs/`** — new home for design docs. First entry covers both v2.2 verbs.
- **`tests/`** — bash-driven assertion harness with fixture `_context.md` files. `tests/run.sh` runs lint + decay against fixtures and asserts on exit codes and signal evidence. No external test framework added.

### Rationale
- Strategic seed `[S]#27` in `Projects/memento-os/_context.md` (2026-05-20): Jeff Su (~2M-sub productivity YouTuber, 2026-05-19) gave away the structured CLAUDE.md / memory.md / archive.md ontology free, with HubSpot sponsoring a paid course launching. The structural pattern is mass-market commodity within 2–3 months. Memento OS's durable differentiator collapses to the **judgment layer** — schema enforcement and drift detection — neither of which a prose template can replicate. `lint` + `decay` operationalize that layer.

### Deferred
- Tier 2/3 adapter ports (Codex full-skills mirror; Cursor/Windsurf/Cline/Gemini rule snippets; Aider/Continue manual docs) — planned for v2.2.x follow-up. Both verbs invoke language-neutral Python scripts, so ports are mechanical.

## [2.1.0] — 2026-05-20

### Added
- **Area-level artifact routing** — DIES (`[D]`/`[I]`/`[E]`/`[S]`) artifacts now route to the correct `_context.md` based on the file's area, instead of all landing in a single root file
- **`fix:` field on error artifacts** — `[E]` entries gain a `fix:` line across all 8 adapters (Claude Code, Codex, Cursor, Windsurf, Cline, Gemini, Aider, Continue), making the "what unblocks this" explicit
- **Knowledge OS gaps port** — L0.5 context directory pattern, confidence gate before mid-task decisions, `embedded`/`resolved` artifact states
- **PayPal donation link** — Path B reputation-lane CTA per project policy

### Changed
- README — area-level vault structure documented, error artifact `fix:` field illustrated
- Acknowledgments — credit to Matt Pocock for `grill-me` skill lineage
- `plugin.json` — `repository`/`homepage` URLs corrected to `Aiyo28/memento-os` (were stale `ayalnogovitsyn/memento-os`)
- `plugin.json` version bumped to 2.1.0

## [2.0.0] — 2026-04-11

### Added
- **Multi-AI adapters** — Memento OS now works with 8 AI coding tools:
  - Tier 1 (full skills): Claude Code, Codex (OpenAI CLI)
  - Tier 2 (rules): Cursor, Windsurf, Cline, Gemini Code Assist
  - Tier 3 (manual): Aider, Continue
- `adapters/` directory with per-tool install guides and config files
- **Artifact Tier System** (L0/L1/L2) — formal promotion, eviction, and lifecycle rules
- **Mid-Task Retrieval Protocol** — confidence gate + protected domains before decisions
- **People/Self.md** peer card template — loaded by session-start for communication calibration
- **Tag taxonomy template** — starter `_meta/tag-taxonomy.md` with 10 domains
- `experiment-context` document type for time-boxed explorations
- `superseded` status value for replaced artifacts
- MOC pattern formalization (naming, linking, creation triggers)
- Scaled Vault Pattern (INDEX.md) for large vaults
- Context Directory (L0.5) optional pattern for business projects
- Retrieval Patterns documentation (Telescope vs Radar)

### Changed
- conventions.md — 8 new sections covering tier system, retrieval, MOCs, experiments
- session-complete v4.2.0 — `superseded` status, expanded eviction rules (embedded, resolved, dormant)
- grill-me v1.1.0 — Context Loading upgraded to structured Vault Retrieval Gate
- vault-audit v1.1.0 — `superseded` status check, MOC orphan detection, experiment teardown, dormant seeds
- session-start v2.0.1 — Self.md reference improved, suggests creating on first session
- `_context.md` template — `repo_path`/`repo_docs_path` fields, Kobe cap annotation, Active Reasoning Artifacts table, `## Related` section
- init command — new `_context.md` template with Key Numbers table
- plugin.json version bumped to 2.0.0

## [0.4.0] — 2026-03-21

### Added
- `[S]` Seed artifacts — forward-looking ideas with activation triggers
- `/memento:init` command — 3-question onboarding, seeds first artifact
- `/memento:stats` command — memory score, artifact breakdown, session streak
- `/memento:grill-me` skill — stress-test plans, produces artifacts
- Memory score in session-start briefing
- AICEO/GEO: `llms.txt`, `AGENTS.md`, `.well-known/security.txt`, `.well-known/ai-plugin.json`
- SECURITY.md with threat model
- Banner (`assets/banner.png`)

### Changed
- All skills namespaced as `memento:*` (prevents collision with personal skills)
- session-start v2.0.0 — seed checking, memory score display
- session-complete v4.0.0 — extracts `[S]` seeds
- decide v2.0.0 — seed planting support
- README rewritten (Memento OS plugin pitch, not "Agentic Total Recall" field guide)
- quickstart.md updated for plugin install flow

### Removed
- Stale starter skills moved to `starter/archive/`

## [0.2.0] — 2026-03-17

### Added
- Pivot to "Memento OS" from "Agentic Total Recall"
- Priority matrix: confidence x impact → critical/volatile/settled/noise
- 24-artifact cap (Kobe rule) with priority-based eviction
- Auto-log toggle
- Plugin scaffold (plugin.json)

## [0.1.0] — 2026-03-14

### Added
- Repo scaffold with evolution/, system/, reference/, starter/ structure
- Evolution entries 001-004 (solved problems)
- Scorecard methodology (10 dimensions, 4-level rubrics)
- Starter kit: Claude Code configs, 3 safety hooks, 4 skills
- Starter kit: Obsidian vault skeleton with L0/L1/L2 templates
- OpenClaw comparison reference
- Initial README with manifesto and evolution index
