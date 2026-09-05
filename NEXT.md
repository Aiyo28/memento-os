# NEXT — Memento OS

Path B (OSS + reputation). No kill rule. Ship when there's substance.

## Continue

### ✅ Install integrity — SHIPPED and VERIFIED 2026-09-05

**State, verified end-to-end:** `2.3.3` on `main`, CI green, `marketplace.json` returns 200 on
GitHub, `claude plugin marketplace add Aiyo28/memento-os` succeeds, and
`/plugin install memento-os@aiyo` completed on a real client. `bash tests/run.sh` → **38/38**.

It took three releases because each one was verified by a different check than a user performs:

- **2.3.1** — `.claude-plugin/marketplace.json` had never been `git add`ed. It 404'd, so
  `/plugin marketplace add` failed and `/plugin install` had no marketplace to resolve against.
  Shipped together with the README/`llms.txt`/`AGENTS.md` release content, skill count 5 → 7
  (the repo ships 7), Ko-fi alignment with `FUNDING.yml`, the fixture fix and CI. Marketplace
  named **`aiyo`**, not `memento-os`: Claude Code registers one marketplace per name per user
  and expects multiple plugins to share one manifest, so naming it after a single plugin would
  have stranded every future one. Install is `/plugin install memento-os@aiyo`.
- **2.3.2** — install still failed with `Permission denied (publickey)`. The marketplace listed
  the plugin with a `github` source, so Claude Code cloned this repo a *second* time over SSH to
  fetch a plugin already present in the copy it had just cloned. Nobody has an SSH key for a repo
  they do not own. Source is now the relative path `./`. ⚠ **Never give a plugin in this repo a
  `github` source.** `claude plugin validate` passes on the broken version — it checks manifest
  shape, not source reachability.
- **2.3.3** — the `Stop` and `PreCompact` hooks wrote into projects that were never initialized.
  Both told the model to append a session log and update `_context.md`, a file that does not
  exist until `/memento:init` runs, so on a fresh install it improvised a location — the exact
  failure `evolution/005-scattered-captures.md` is named after, shipped as the default. Both now
  gate on an initialization check. Added a `SessionStart` hook, because installing previously
  produced no greeting and no pointer to `/memento:init`; and `.memento-skip` to silence it.

⚠ **`claude plugin update memento-os@aiyo`** if your installed copy predates 2.3.3 — the
marketplace cache updating does not update an installed plugin.

**Tagged 2026-09-05:** `v2.3.1` `v2.3.2` `v2.3.3` at their commits, matching this repo's
convention of tagging every version. **GitHub Release still to cut** — one covering all
three; three notifications for same-day fixes would be noise.

### Test suite — GREEN, 38/38

Was red from 2026-06-14 to 2026-09-05 and nothing noticed, because there was no CI. Root cause
was a rotting fixture, not a code bug: `tests/fixtures/decay/_context.md` hardcoded `2026-05-15`
and `run.sh` asserted that row was "5 days old"; it had become 113. The fixture is now generated
relative to today inside `run.sh`, and a companion assertion regenerates it at `today − 400` to
prove the age filter discriminates rather than passing vacuously. CI runs on push **and weekly
on cron**, because a date-scored suite goes red with no commit at all.

### Outstanding from the v2.3.0 punch list

Items 1–6 (commit, retro-tag v2.1.0, tag v2.2.0, tag v2.3.0, push tags, three GitHub Releases)
are **DONE** — tags exist and all three releases are dated 2026-05-23. Do not re-do them. What
remains:

- **Launch post** — X post + portfolio blog. Never written; no post on ayal.tech names the
  project. The install now works, so the reason to hold it is gone.
- **Update vault** — `Projects/memento-os/_context.md` Status field, with release URLs.

## Decide

- **Bundle v2.4 as one release or patch cadence?** Plan recommends **bundle**, on the
  7-adapter-port argument rather than the narrative one: the port is mandatory and is per-release
  overhead, so splitting A–D multiplies it by four for no user-visible gain. Does not apply to
  v2.3.1, which ships alone and immediately.
- **Q1–Q6** in `docs/specs/2026-05-20-v2.4-knowledge-os-feature-port.md`. Four of six are
  resolvable from the codebase and their defaults stand (Q1, Q2, Q4, Q5 — see the plan for the
  evidence; Q4's wording needs tightening to "does not write **to the vault**", since
  session-start already writes `~/.claude/memento-auto-log`). **Only Q3 and Q6 need you.**

## Blocked

- Nothing blocked. v2.4 was gated on install integrity and a green suite; **both cleared
  2026-09-05**. Remaining gate is your Q3 answer.
- **Q3 answered 2026-09-05: pre-created class folders.** Owner notes this is free to change —
  it is a first-run presentation choice, not a data-model one, so switching to on-demand later
  touches the init command and nothing else.

## Next release (v2.4.0) — Option B locked

Port 4 Knowledge OS features (DIES stays, no DICE rename). Spec: `docs/specs/2026-05-20-v2.4-knowledge-os-feature-port.md`.

| Block | Feature | Status |
|-------|---------|--------|
| A | Funnel Architecture (`[I]` → `_insights.md`, 5K-token area cap) | spec'd |
| B | Project-Class taxonomy (`class:` field + `Projects/_types/{class}/_context.md`) | spec'd |
| C | HEAD/Archive Split (append-only `_archive.md`) | spec'd |
| D | Emission Discipline (only deliberation skills emit `[D]`) | spec'd |

Decision context: `docs/specs/2026-05-20-dies-vs-dice-architecture.html` (side-by-side analysis, Option B recommended and confirmed).

## Anti-pattern reminders

- **No scheduled releases.** Path B is reputation, not cadence. Ship when there's substance.
- **No "Memento Academy" / paid course.** Operator-claim-density disqualifier (vault `Knowledge/_context.md [S]#415`). Sell software, not curriculum.
- **No DICE in OSS Memento OS** — DICE belongs to AIYO OS (paid team product) as a commercial moat. (Decided 2026-05-20.)

Updated: 2026-09-05 (was 2026-05-20 — punch list items 1–6 were already done and are removed)
