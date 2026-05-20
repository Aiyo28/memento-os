# NEXT — Memento OS

Path B (OSS + reputation). No kill rule. Ship when there's substance.

## Continue

### Release v2.3.0 (ready to ship)

v2.2 + v2.3 are both built, tested (37/37 assertions pass), and ready to tag. v2.1.0 was never tagged either — single release cycle catches up history.

Punch list:

1. **Commit current changes** — all v2.2 + v2.3 work uncommitted on `main`.
2. **Retro-tag v2.1.0** at the head of the v2.1 commit chain (last commit before v2.2 lint/decay work).
3. **Tag v2.2.0** at the commit that adds `skills/memento-lint/` + `skills/memento-decay/` + `tests/`.
4. **Tag v2.3.0** at HEAD.
5. **Push tags** to GitHub.
6. **Create three GitHub Releases** — v2.1.0, v2.2.0, v2.3.0 — using respective CHANGELOG sections.
7. **Draft launch post for v2.3.0** — X post + portfolio blog post (deliverables in progress; user requested).
8. **Update vault** — `Projects/memento-os/_context.md` Status field: "v2.3.0 tagged + released" with release URLs.

## Decide

- Bundle v2.4 as one release or patch cadence? (Spec recommends bundle.)
- Q1–Q6 in `docs/specs/2026-05-20-v2.4-knowledge-os-feature-port.md` open questions table.

## Blocked

- Nothing pending.

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

Updated: 2026-05-20
