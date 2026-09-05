# NEXT — Memento OS

Path B (OSS + reputation). No kill rule. Ship when there's substance.

## Continue

### ✅ v2.3.1 — install integrity. SHIPPED 2026-09-05.

> Committed and pushed: `marketplace.json` (marketplace named `aiyo`), the README/`llms.txt`/
> `AGENTS.md` release content, skill count 5 → 7, Ko-fi alignment, the fixture fix and CI.
> **One task remains and it is yours:** run both documented commands on a clean machine and
> confirm the plugin installs. Nothing below this line has been verified against a real install.

<details><summary>Original diagnosis, kept for the record</summary>

**The plugin cannot be installed by any documented path.** Verified 2026-09-05:
`.claude-plugin/marketplace.json` is **untracked** and returns **404** on GitHub, so
`/plugin marketplace add Aiyo28/memento-os` fails and `/plugin install memento-os` never gets a
marketplace to install from. `plugin.json` is committed and fine; the marketplace manifest never
was.

Spec: `docs/specs/2026-09-05-v2.3.1-install-integrity.md` · Plan:
`docs/plans/2026-09-05-update-plan.md`

</details>

1. **One atomic commit** — `git add .claude-plugin/marketplace.json` **together with** the
   uncommitted `README.md` / `llms.txt` / `AGENTS.md`. Shipping the README's new
   `/plugin marketplace add` line without the manifest documents a 404, which is worse than today.
2. **README still says "5 skills"** (lines 95 and 97). The repo ships **7**. The uncommitted edit
   fixed the install step but not the count; `llms.txt` already says 7, so the two now disagree.
3. Bump `plugin.json` **and** `marketplace.json` to `2.3.1`, CHANGELOG entry, tag, release.
4. **Verify by hand on a clean machine** — run both documented commands. The chain is only
   provably fixed by executing it end to end. Record the result here.

### 🔴 Test suite is RED — 36 passed, 1 failed

`./tests/run.sh` exits 1. The "37/37 assertions pass" claim below was true on 2026-05-20 and is
not now.

Root cause is a **rotting fixture, not a code bug**: `tests/fixtures/decay/_context.md` row 4 is
hardcoded `2026-05-15`, and `tests/run.sh:90` asserts `[D]#4` is absent from `--age 30` output,
labelled "5 days old". It is now 113 days old, so decay correctly surfaces it. The suite has been
red since roughly 2026-06-14 and nothing noticed, because there is no CI.

Fix: generate the fixture from `today - N days` inside `run.sh`, then add a CI workflow so it
cannot rot silently again.

### Outstanding from the v2.3.0 punch list

Items 1–6 (commit, retro-tag v2.1.0, tag v2.2.0, tag v2.3.0, push tags, three GitHub Releases)
are **DONE** — tags exist and all three releases are dated 2026-05-23. Do not re-do them. What
remains:

- **Launch post for v2.3.0** — X post + portfolio blog. Never written; no post on ayal.tech names
  the project. Sequence it *after* v2.3.1, so it does not point at a broken install.
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

- Nothing blocked. v2.4 is *gated*, not blocked: build it after v2.3.1 and the test fix, because
  features shipped into an uninstallable plugin reach nobody.

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
