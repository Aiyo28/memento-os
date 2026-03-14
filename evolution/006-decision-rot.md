# 006 — Decision Rot

**Status:** Upcoming
**Score impact:** Auto-capture reliability from 5.5/10 → target 7/10
**Date:** 2026-03-14
**Core goal:** Memory loss prevention

## The Problem

Decisions made during conversations never graduate to durable storage. They exist in three places, all ephemeral:

1. **Conversation context** — gone when the session ends
2. **Session logs** — append-only files that grow until nobody reads them
3. **The developer's memory** — unreliable, especially weeks later

An audit of 12 sessions on one project found 14+ architectural and product decisions that were never promoted to a DECISIONS.md file or typed memory entry. They lived in session logs, buried between status updates and debugging notes. When a decision needed to be revisited, nobody could find the original reasoning.

The result: decisions get re-made. Sometimes differently. Sometimes contradicting the original. Always wasting time.

## What We Tried

(Upcoming)

## What Worked

(Upcoming)

## Why It Works

(Upcoming)

## Verification

(Upcoming)

## Open Questions

- What constitutes a "decision" worth graduating? Not every choice needs durable storage.
- Should graduation be real-time (during session) or batch (weekly review)?
- How do you handle decision reversals — supersede the old entry or amend it?
