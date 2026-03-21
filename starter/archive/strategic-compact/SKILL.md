---
name: strategic-compact
description: >
  Guide context compaction timing. Suggests /compact at logical task boundaries
  rather than relying on arbitrary auto-compaction. Triggers: "compact context",
  "save context space", "context is getting long".
version: 1.0.0
---

# Strategic Context Management

Guide `/compact` timing for long sessions. With large context windows, compaction is about focus — keeping the working set clean so reasoning stays sharp.

## Compaction Decision Guide

| Phase Transition | Compact? | Why |
|-----------------|----------|-----|
| Research → Planning | Yes | Research is bulky; the plan is the distilled output |
| Planning → Implementation | Yes | Plan is in tasks/file; free up for code |
| Implementation → Testing | Maybe | Keep if tests reference recent code |
| Debugging → Next feature | Yes | Debug traces pollute unrelated work |
| Mid-implementation | No | Losing variable names and partial state is costly |
| After a failed approach | Yes | Clear dead-end reasoning before retrying |

## What Survives Compaction

| Persists | Lost |
|----------|------|
| CLAUDE.md instructions | Intermediate reasoning |
| Task list | File contents previously read |
| Memory files on disk | Multi-step conversation context |
| Git state | Tool call history |
| Files on disk | Nuanced verbal preferences |
| Conversation summary | Exact code snippets discussed |

## Before Compacting

1. **Write first** — save important findings to memory files before `/compact`
2. **Use custom message** — `/compact Focus on implementing auth middleware next`
3. **Check phase** — only compact at transitions, never mid-implementation

## Criteria

| # | Criterion | Test |
|---|-----------|------|
| C1 | Important context saved to files before recommending /compact | Critical conversation-only info written to disk? |
| C2 | Compaction recommended at a logical task boundary | Aligns with a phase transition in the guide? |
| C3 | User told what will be lost | "What Survives" table consulted? |
| C4 | Custom /compact message provided when next phase is known | Focused message, not bare /compact? |
