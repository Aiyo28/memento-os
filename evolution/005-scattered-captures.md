# 005 — Scattered Captures

**Status:** In Progress
**Score impact:** TBD
**Date:** 2026-03-14
**Core goal:** Memory loss prevention

## The Problem

Knowledge captures end up in the wrong location. Session logs land in skill inboxes instead of the vault. Research notes accumulate in agent memory instead of the knowledge vault. Implementation plans sit in `~/.claude/plans/` instead of project docs. Each misplaced file is a future retrieval failure — the knowledge exists but nobody can find it.

An audit of our own system revealed:
- A session log with critical skill architecture decisions trapped in a skill inbox folder
- Two research documents (OSS tool evaluations, context pattern analysis) sitting in agent memory instead of the vault
- An implementation plan with 400+ lines of task breakdown stranded in a plans directory, disconnected from the project it belonged to

The pattern: every tool in the system has its own "dump here" location. Without routing discipline, knowledge fragments across all of them.

## What We Tried

(In progress — documenting the cleanup of our own system as the case study)

## What Worked

(In progress)

## Why It Works

(In progress)

## Verification

(In progress)

## Open Questions

- What's the right granularity for routing rules? Per file type? Per content category?
- Can routing be automated (hooks that detect misplacement), or does it always need human judgment?
- How do you handle the "vault is unreachable" case without creating permanent orphans?
