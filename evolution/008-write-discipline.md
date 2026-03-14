# 008 — Write Discipline

**Status:** Upcoming
**Score impact:** Auto-capture reliability from 5.5/10 → target 8/10
**Date:** 2026-03-14
**Core goal:** Memory loss prevention

## The Problem

The agent won't write memory unless explicitly told. Four skills exist for memory capture (session-complete, process-inbox, strategic-compact, knowledge), but all require manual invocation. The user must remember to run them — and they don't, especially at the moments that matter most:

- End of a long session (tired, just want to stop)
- Before context fills up (no warning signal)
- After a critical decision (focused on the next task, not on documentation)
- When switching projects (context switch absorbs all attention)

The system has the tools to capture knowledge. It lacks the discipline to use them automatically. This is the gap between a memory system that works when you remember it and one that works always.

## What We Tried

(Upcoming)

## What Worked

(Upcoming)

## Why It Works

(Upcoming)

## Verification

(Upcoming)

## Open Questions

- Should session-complete be a Stop hook (runs automatically when conversation ends)?
- What's the performance cost of automatic extraction at every session boundary?
- How do you handle sessions that end abruptly (crash, timeout, user closes terminal)?
- Is there a middle ground between "fully manual" and "fully automatic" — e.g., a prompt that asks "should I save this session's decisions?" before closing?
