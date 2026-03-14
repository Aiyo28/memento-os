# 007 — Compaction Loss

**Status:** Upcoming
**Score impact:** Compaction handling from 3/10 → target 7/10
**Date:** 2026-03-14
**Core goal:** Memory loss prevention

## The Problem

When a conversation exceeds the context window limit, the system auto-compacts — summarizing older content to make room. This is necessary for the conversation to continue, but it destroys detail:

- Decisions discussed but not yet written to disk
- Partial reasoning chains that informed the current approach
- File paths, variable names, and implementation context
- Nuanced user preferences stated verbally but never saved

A manual `strategic-compact` skill exists, but it must be invoked by the user. The user forgets. By the time they remember, the context has already been auto-compacted and the detail is gone.

The irony: the most valuable context — the kind you haven't had time to write down yet — is exactly what compaction destroys.

## What We Tried

(Upcoming)

## What Worked

(Upcoming)

## Why It Works

(Upcoming)

## Verification

(Upcoming)

## Open Questions

- Can the system detect approaching compaction and trigger extraction automatically?
- What's the right extraction format? Full decisions? Key-value pairs? Structured summaries?
- How do you distinguish "worth saving" from "routine context" during automated extraction?
- OpenClaw's silent agentic turn approach — is it reliable enough, or does it need a hook-based trigger?
