# Update plan — memento-os, 2026-09-05

Prioritised by impact × effort. Companion to
`docs/specs/2026-09-05-v2.3.1-install-integrity.md` (the near-term release) and
`docs/specs/2026-05-20-v2.4-knowledge-os-feature-port.md` (the feature backlog).

Every number below was re-verified on 2026-09-05, not inherited.

## State of play

| Fact | Verified how |
|---|---|
| `.claude-plugin/marketplace.json` untracked; **404 on GitHub** | `git ls-files`, `gh api .../contents/...` |
| `plugin.json` committed and served | `gh api` → sha `0a9e9db` |
| Published README omits `/plugin marketplace add` | published `README.md:31` |
| Published + **working-tree** README both say "5 skills"; repo ships **7** | `README.md:95`, `README.md:97`, `ls skills` |
| Working-tree `llms.txt` correctly says `Skills (7)` | local `llms.txt:46` |
| **Test suite is RED: 36 passed, 1 failed, exit 1** | `./tests/run.sh` |
| Failure is a rotting fixture, not a code bug | fixture row 4 hardcoded `2026-05-15`; assertion at `run.sh:90` calls it "5 days old" |
| Tags v2.1.0 / v2.2.0 / v2.3.0 exist; 3 GitHub releases dated 2026-05-23 | `git tag`, `gh release list` |
| Donation split: `FUNDING.yml` Ko-fi vs README PayPal badge | both read |
| 14-day traffic: 3 views / 2 unique, 3 clones, 1 reddit referrer | GitHub traffic API |
| 7 adapters must be re-ported for v2.4 | `ls adapters` |

Three items in `NEXT.md`'s punch list — and its "37/37 assertions pass" — are stale. Correcting
that is S5.

## The reasoning, tested rather than inherited

The working hypothesis handed to this plan was "broken install and stale skill count outrank v2.4
features." Testing it turned up something stronger: **the install is not merely under-documented,
it is impossible.** The marketplace manifest is not on GitHub at all, so both the published
instruction and the owner's uncommitted fix fail. That moves the item from "important" to
"prerequisite" — and it means the README fix, shipped alone, would be a regression, because it
tells users to run a command that 404s.

Against that, v2.4's own maturity table concedes blocks A, C and D are spec-only in Knowledge OS
— never implemented anywhere — and the release mandates porting all four blocks across 7
adapters. So v2.4 is high effort, medium risk, and its payoff is feedback on unproven design from
an audience that currently cannot install the plugin.

The hypothesis holds, and more firmly than stated.

## Sequence

### P0 — v2.3.1 "install integrity" · ~1.5 h · **do first**

**S0 + S0b + S0c ship as one commit.** Splitting them documents a 404.

- [ ] `git add .claude-plugin/marketplace.json` — the whole release turns on this one line
- [ ] Ship the owner's uncommitted `README.md`, `llms.txt`, `AGENTS.md` **as written**
- [ ] Add on top: README `5 skills` → `7 skills` at line 95, and the Codex row at line 97
- [ ] Bump `plugin.json` **and** `marketplace.json` to `2.3.1`; CHANGELOG entry
- [ ] Push, tag `v2.3.1`, create the release
- [ ] **Run the two documented commands on a clean machine.** The chain is only provably fixed by
      executing it end to end; record the result in `NEXT.md`

Why first: every other item's value is gated on the plugin being installable. A feature shipped
into an uninstallable plugin reaches nobody, and a launch post pointing at a broken install spends
the one launch you get.

### P1 — de-rot the tests, then gate them · ~1 h

- [ ] Rewrite the decay fixture so `tests/run.sh` generates it with dates relative to today
      (option A in the spec — keeps the test-only concern in the harness)
- [ ] Prove it is genuinely relative: regenerate at `today - 400 days` and assert `#4` now *does*
      surface. A fixture that only passes today is the same bug with a later fuse
- [ ] Add `.github/workflows/ci.yml` running `./tests/run.sh` on push/PR to `main`. Python 3 only,
      no install step
- [ ] Add the badge **after** the suite is green

Why second: it is cheap, and until it is done "the tests pass" is not a claim that can honestly be
made when tagging anything — including v2.4.

### P2 — one donation channel · ~10 min

- [ ] README PayPal badge + link → Ko-fi, matching `FUNDING.yml`
- [ ] Grep `llms.txt`, `adapters/*/`, `RELEASE.md` for further PayPal references

Sequenced after P0 only to avoid two people editing the same README lines.

### P3 — truth-up `NEXT.md` · ~15 min

- [ ] Delete punch-list items 1–6 (done 2026-05-23)
- [ ] Replace "37/37 assertions pass" with the real number and the CI link
- [ ] Carry forward what is genuinely outstanding: launch post (item 7), vault `_context.md`
      status (item 8), v2.4
- [ ] Add the clean-machine install verification result from P0

### P4 — discovery · ~3–4 h

Only now, because these all point at an install that must work.

- [ ] Submit to community Claude Code plugin marketplaces — a marketplace-of-one in its own repo
      is why traffic is 3 views a fortnight
- [ ] Launch post (X + portfolio blog) — punch-list item 7, never written, and no post on
      ayal.tech names the project
- [ ] Seed a Discussions thread now that Discussions is enabled

### P5 — v2.4.0 · ~6–8 h + adapter ports

Build only after P0–P1. Order within the release, easiest-to-riskiest:

1. **Block D — Emission Discipline.** Declarative rule change; smallest blast radius
2. **Block B — Project-Class taxonomy.** The only block *partially live* in KOS, so the least
   speculative
3. **Block A — Funnel Architecture.** Needs migration tooling; touches lint, decay,
   session-complete
4. **Block C — HEAD/Archive split.** Largest schema change, spec-only in KOS

Then the mandatory port across all 7 adapters (`aider cline codex continue cursor gemini
windsurf`). That port is the bulk of the estimate and the real maintenance multiplier — worth
confirming before committing to bundling.

## Bundle or patch?

**Bundle as v2.4.0** — agreeing with the spec's own recommendation, but for a different reason
than the spec gives.

The spec argues bundling on narrative grounds ("structured cap shapes, not just structured
grammar"). That is the weaker argument. The stronger one is the **7-adapter port**: it is
mandatory for v2.4 and it is per-release overhead, not per-block overhead. Splitting A–D into
v2.3.2–v2.3.5 multiplies that port by four for no user-visible gain, on a project whose stated
operating rule is *ship on substance, not cadence*.

The counter-argument — lower per-release risk — is real, and blocks A and C are spec-only in KOS.
Bundling means four unproven changes land together. Mitigate inside the release by ordering
D → B → A → C as above and porting adapters once at the end, rather than by splitting the release.

Note this is a **v2.4.0** decision. It does not apply to **v2.3.1**, which must ship alone and
immediately: it is a fix release, it has no adapter surface, and holding it back to bundle with
features would keep the plugin uninstallable for the duration.

## Open questions Q1–Q6

Every one already has a recommended default in the v2.4 spec. Classification after checking each
against the code:

| # | Resolvable from the codebase? | Finding |
|---|---|---|
| Q1 | **Yes — take the default** | `lint.py` never resolves `#N` across files (`NEW_HEADER_RE` matches markdown headings; `[{type}]#{number}` at line 202 is display only). Nothing mechanical breaks either way, so "preserve" is a readability call and the default stands |
| Q2 | **Yes — take the default** | No token estimation exists anywhere. `decay.py:149` uses `re.findall` for word tokens, unrelated. There is no house convention to match, so `len(text) // 4` is unopposed |
| Q4 | **Yes — but tighten the wording** | The default says "session-start stays read-only". It is *not* read-only today: `skills/session-start/SKILL.md:81` writes `~/.claude/memento-auto-log`. It is **vault**-read-only. Take the default, restate the invariant as "session-start does not write to the vault" |
| Q5 | **Yes — take the default** | `grep -rn emitted_by skills/ system/ commands/ hooks/` returns nothing. R10 would have nothing to validate. Defer, exactly as the default says |
| **Q3** | **Owner** | Ship pre-created class folders in the starter vault, or create on demand? Cheap either way and reversible, but it sets what a new user sees on first run — taste, not mechanics |
| **Q6** | **Owner — recommendation above** | Release shape. Answered: bundle, for the adapter-port reason |

So four of six are unblocked and should simply be recorded as confirmed defaults when v2.4 starts.
Only Q3 and Q6 need the owner, and Q6 has a recommendation with a reason.

## Explicitly not in this plan

- **DICE.** Stays in AIYO OS. Standing anti-pattern, untouched
- **Scheduled releases.** Every item above is triggered by readiness, never by a date
- **Any paid-course / academy surface**
- **An MCP server for memento-os.** It is skills + hooks operating on files; there is nothing an
  MCP server would add, and the plugin format is already correct
- **Rewriting the owner's `AGENTS.md` restructure.** It ships as written
