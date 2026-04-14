# Memento OS

This project uses Memento OS for persistent AI memory. Store conclusions, not notes.
The vault is a retrieval source — search before generating from training data.

---

## Conventions

### Artifact Format

Every piece of memory is a reasoning artifact — a pre-computed conclusion with an expiration condition.

```
[D] conclusion — invalidates if trigger [priority] [YYYY-MM-DD]
[I] insight — invalidates if condition [priority] [YYYY-MM-DD]
[E] what went wrong — root cause: why [settled] [YYYY-MM-DD]
[S] idea — activates when condition [priority] [YYYY-MM-DD]
```

| Prefix | Type | Purpose |
|--------|------|---------|
| `[D]` | Decision | A choice between alternatives — has an invalidation trigger |
| `[I]` | Insight | A reusable conclusion — survives the session that produced it |
| `[E]` | Error | A mistake with root cause + fix — defaults to settled |
| `[S]` | Seed | A deferred idea — activates when its condition is met, not when time passes |

Optional expiry for time-bound conclusions: append `— expires: YYYY-MM-DD` before priority.
Do NOT add expiry to foundational architecture decisions.

### Priority Matrix

Derived from **confidence × impact**:

|                      | High Impact   | Low Impact  |
|----------------------|---------------|-------------|
| **High Confidence**  | **critical**  | **settled** |
| **Medium Confidence**| **volatile**  | **settled** |
| **Low Confidence**   | **volatile**  | **noise**   |

- Propose confidence (high / medium / low), then ask user: "High or low impact?"
- `[E]` errors default to **settled**; once resolved → **noise**
- **noise**: ask "store anyway or discard?" — default: discard

### Kobe Cap: 24 Artifacts

Maximum 24 artifacts in the Active Reasoning Artifacts table per project.
Eviction order: noise → settled → volatile → critical (never auto-evict critical).
Archive evicted artifacts to `Decisions/` with status: `superseded`, `archived`, or `active`.
Additional eviction triggers: embedded artifacts unreferenced 30+ days, resolved errors, dormant seeds 90+ days.

### Vault File Frontmatter

```yaml
---
tags: [tech/architecture, ai/agents, product/auth]
type: decision          # or: research, insight, note, project-context
status: active          # or: draft, archived, superseded
confidence: high        # or: medium, low
---
```

Tag domains: `tech/`, `business/`, `product/`, `ai/`, `personal/`. Keep 3–7 tags per file.

### Vault Structure

```
project/memento/
├── _context.md          # Active artifacts table (load every session)
├── NEXT.md              # Session continuity (15 lines max)
├── Decisions/           # Full decision records (critical/volatile only)
├── Sessions/            # Session log + archive
└── patterns/            # Cross-project reusable patterns (optional)
```

Storage by priority: critical/volatile → full file in `Decisions/` + inline in `_context.md`. settled → inline only. noise → discard.

### Retrieval-First Protocol

Before any decision or gap-filling from training data:
1. Scan `_context.md` Active Reasoning Artifacts table for matching `[D]` entries
2. Glob `{vault}/Knowledge/*{topic}*` for existing knowledge notes
3. Glob `{vault}/Projects/*/Decisions/*{topic}*` for cross-project decisions
4. If prior decision found: surface it, ask "Reaffirm, revise, or override?"
5. If no prior decision: proceed with fresh analysis

---

## Session Start Workflow

Triggers: "start session", "what's the context", "where were we", "catch me up"

**Step 1 — L0:** Read `NEXT.md` (Continue, Decide, Blocked sections).

**Step 2 — L1 (~600 tokens):** Read vault `_context.md` top 3 sections only (Summary + Key Numbers + Active Reasoning Artifacts table). STOP before Doc Index / Decision Log. Read Peer Card `People/Self.md` Communication Style + Decision Patterns tables only. Skip if missing. Never auto-load full docs at session start.

**Step 3 — Seed check:** Scan `[S]` entries. Surface any with met activation conditions under "Seeds Ready". Flag seeds dormant > 90 days.

**Step 4 — Staleness check:** Flag artifacts past `expires:` date as EXPIRED. Then by priority:
- critical > 90 days → STALE
- volatile > 30 days → NEEDS RESOLUTION
- settled > 90 days → STALE
- noise → flag for immediate removal

**Step 5 — Briefing:**
```
## Session Briefing — {Project Name}
Date: {today}
Memory: {score}/10 | {total} artifacts | {seeds} seeds | streak: {n}

### Continue
{from NEXT.md}

### Active Decisions
{critical and volatile only, up to 7}

### Seeds Ready (if any)

### Stale Artifacts (if any)

### Pending
{from NEXT.md Decide section}
```

Memory score: artifact count (0–2) + critical decisions (0–2) + recency (0–2) + no stale (0–1.5) + seeds (0–1) + streak (0–1.5).

---

## Session Complete Workflow

Triggers: "done", "wrap up", "session complete", "end of session", "about to compact"

Modes: **default** (full extraction + log) or **compact** (quick extraction + NEXT.md only).

1. **Scan** conversation for `[D]`, `[I]`, `[E]`, `[S]` artifacts. Compact mode: skip impact prompt, default to `settled`.
2. **Contradiction check:** New supersedes existing → evict old to `Decisions/` with `status: superseded`. Conflict (both may be valid) → flag for user. Compact: auto-supersede, flag conflicts only.
3. **Confirm:** "I found these artifacts: [list]. Anything to add or correct?" Then: "High or low impact?" for each (skip in compact).
4. **Write:** inline entries to `_context.md`; full files to `Decisions/` for critical/volatile.
5. **Update NEXT.md:** move completed items, add new ones, update date, keep under 15 lines.
6. **Session log (default only):** Add to TOP of `Sessions/SESSION_LOG.md`:
   ```
   ### {YYYY-MM-DD} — {most important outcome}
   **Artifacts produced:** {count} ([D]: n, [I]: n, [E]: n, [S]: n)
   **Changed:** {1-2 sentences}
   **Next:** {next session focus}
   ```
   Archive entries beyond 200 lines to `SESSION_LOG_ARCHIVE.md`.
7. **Enforce cap:** If table > 24 entries, evict noise → settled → volatile. Never evict critical.
8. **Show delta:** `Memory: {old} → {new}/10 ({delta})`

---

## Decide Workflow

Triggers: "decide", "should we", "which option", "evaluate", "compare", "let's think about"

**Retrieval gate (always first):**
1. Scan `_context.md` for `[D]` entries matching the decision domain
2. Glob `{vault}/Knowledge/*{topic}*`
3. Glob `{vault}/Projects/*/Decisions/*{topic}*`
4. If found: surface it, ask "Reaffirm, revise, or override?"
5. If not found: proceed

**OODA loop:**
- **Observe:** Read `_context.md` and `NEXT.md`. Note existing decisions.
- **Orient:** Present 2–5 options with pros/cons/effort. Give recommendation. State confidence: High (>85%) / Medium (60–85%) / Low (<60%).
- **Decide:** Ask user to choose. Accept even if it differs from recommendation.
- **Act:** Propose confidence → ask "High or low impact?" → derive priority → write `[D] conclusion — invalidates if trigger [priority] [YYYY-MM-DD]`. If "not now but when X": plant `[S]` seed instead. Write to `_context.md` (all) + `Decisions/` file (critical/volatile).

---

## Vault Audit Workflow

Triggers: "vault audit", "check vault", "what's stale", "clean up vault"

1. **Structure:** Verify each project under `Projects/` has `_context.md` with Active Reasoning Artifacts table.
2. **Staleness scan:** Check expiry dates first (EXPIRED). Then priority-based: critical > 90d, volatile > 30d, settled > 90d, noise = immediate.
3. **Inbox:** Process `_inbox/` items — identify type, route to correct folder, add frontmatter, update `_context.md` doc index.
4. **Fluff:** Flag drafts > 30 days old, orphaned files (no wikilinks), dormant seeds > 90 days.
5. **Report:**
   ```
   ## Vault Audit — {date}
   Structure: {OK or issues}
   Stale artifacts: {count by priority}
   Inbox: {processed / remaining}
   Suggestions: {cleanup actions}
   ```

---

## Do Not

- Hardcode vault paths — users configure their vault location
- Store raw notes or conversation fragments — store conclusions only
- Auto-evict critical artifacts
- Add expiry to foundational architecture decisions
- Duplicate content — if a doc exists in a repo, the vault has a pointer, not a copy
