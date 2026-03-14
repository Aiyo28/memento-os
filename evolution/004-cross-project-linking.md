# 004 — Cross-Project Linking

**Status:** Solved
**Score impact:** Cross-file linking from 3/10 → 7/10
**Date:** 2026-03-13
**Core goal:** Both (token efficiency + memory loss prevention)

## The Problem

Seven active projects, each generating research, decisions, and patterns. The agent working on Project A had zero awareness of relevant findings from Project B. Three concrete examples from a single month:

1. **Duplicated competitive research.** A 12-competitor market scan written for a web app project contained pricing analysis directly applicable to a mobile app. The mobile app session — a different week, different context window — spent 3 hours redoing the same analysis from scratch. Same conclusions, same output, zero knowledge transfer.

2. **Re-discovered debugging pattern.** A session working on an API worker surfaced a non-obvious fix: when Cloudflare Workers return CORS errors on cross-origin POST requests, check that `Content-Type` is set before the `Authorization` header — certain proxies reject the reverse order. This was written in a session note and forgotten. Two weeks later, a different project hit the same CORS behavior. The agent spent 45 minutes debugging before finding the same fix. The note existed. It just wasn't findable.

3. **Missed regulatory connection.** A cybersecurity project's research identified data residency requirements under a regional framework. A fintech project in parallel was subject to the same framework. The connection was never made — both projects proceeded with independent legal research, each incomplete without the other.

Each project was an island. Knowledge stayed in its silo even when it was directly relevant elsewhere. The agent isn't at fault — it can only see what's loaded. The problem is structural: there was no mechanism to connect knowledge across project boundaries.

## What We Tried

**Approach 1: One big folder.** Move all research into a single flat `Knowledge/` directory shared across projects. Became unnavigable within two weeks — 60+ files, no structure, no project attribution. The agent couldn't find relevant documents without being told the exact filename. An AI that requires exact filenames to retrieve knowledge is not a knowledge system.

**Approach 2: Tag-based indexing.** Add tags to every document, then use grep or search to find by tag. Tags proliferated instantly — within a month there were 100+ unique tags, many semantically overlapping (`pricing`, `monetization`, `revenue-model`, `business-model`). Nobody searched by tag consistently. The agent didn't use tags for discovery. Tags are metadata about documents; they are not navigation paths to documents.

**Approach 3: Full-text search on demand.** Let the agent search the filesystem when it needed cross-project knowledge. Found exact-string matches. Completely missed semantic connections: "pricing tier analysis" would not match "SaaS monetization strategy" even though both documents answered the same question. Also required the agent to know it should search — which it often didn't, because it had no signal that cross-project knowledge existed.

All three approaches failed at the same layer: **discovery**. The agent can use knowledge it can find. The problem was helping it find knowledge it didn't know existed.

## What Worked

Three mechanisms, each solving a different failure mode.

### MOC (Map of Content) Hub Files

Four semantic hub documents in `Knowledge/`, each gathering related notes across all projects:

```markdown
# MOC — Competitive Intelligence

## Methodology
- [[Competitive Intelligence Template]] — 13-part analysis structure, reusable across any market

## By Domain
### Web Products
- [[Competitor A Analysis]] — AI summarization, freemium, 200K users, declining engagement
- [[Competitor B Analysis]] — Manual highlights, $9.99/mo, B2B pivot in progress

### Mobile
- [[Pet App Market Scan]] — 12 competitors, engagement patterns, churn benchmarks

### B2B / Security
- [[Vendor Landscape]] — 8 vendors, TAM $150M, 3 acqui-hire targets identified
```

MOCs don't hold content — they hold connections. One read reveals related work across every project. The agent reads the Competitive Intelligence MOC and immediately knows that three projects have produced research relevant to market positioning, without loading any of those documents. It can then make a targeted load decision based on what the index reveals.

Four MOCs cover the full domain space: Competitive Intelligence, AI & Infrastructure, Business & Monetization, Technical Patterns.

### Pattern Extraction Discipline

When a session reveals a reusable insight, it gets extracted to `Knowledge/patterns/` with a standard schema. The format is project-neutral — a pattern from a web app looks identical to a pattern from a mobile app, and both are equally discoverable:

```markdown
---
title: "Header Order Fix — Cloudflare Workers CORS"
type: knowledge-extract
tags: [tech/networking, tech/cloudflare]
summary: >
  When Cloudflare Workers return CORS errors on cross-origin POST,
  check that Content-Type is set before Authorization in the response
  headers. Certain proxies reject the reverse order silently.
---

## Context
Debugging CORS errors on Cloudflare Worker endpoints receiving
cross-origin POST requests with auth headers.

## Pattern
Set `Content-Type` before `Authorization` in the response headers object.
The error manifests as a generic CORS rejection with no indication of
header order as the cause.

## Why
Certain edge proxies enforce a processing order for response headers.
When `Authorization` precedes `Content-Type`, some proxies reject the
response before the CORS headers are evaluated. The error message
gives no indication of this — it presents as a standard CORS failure.

## Verified In
- API worker project (2026-01-22)
- Payment webhook service (2026-02-08)
```

This specific pattern — after being extracted — was surfaced automatically during a third project's CORS debugging session two months later. The agent read the Technical Patterns MOC, saw a summary matching the failure mode, loaded the pattern file, and applied the fix in under 5 minutes. Previous cost without the pattern: 45 minutes.

### Canonical Tag Taxonomy

A single controlled vocabulary for tags, stored in `Knowledge/meta/tag-taxonomy.md` and referenced in global CLAUDE.md:

```
## Approved Tags

ai/agents, ai/llm, ai/infrastructure
business/strategy, business/pricing, business/competitive, business/regulatory
tech/networking, tech/security, tech/web, tech/mobile, tech/cloudflare
product/ux, product/onboarding, product/monetization
```

Rules enforced in CLAUDE.md:
- Use `domain/subtopic` format — two levels, no more
- Project identity goes in `project:` frontmatter field, never as a tag
- Tags describe *what the content is about*, not *which project it belongs to*
- Before creating a new tag, check the taxonomy. If it's not there, use the closest match and propose the addition separately

This makes tags useful for cross-project discovery. Searching `business/pricing` finds pricing research from every project — not because the documents are co-located, but because they share a controlled vocabulary.

## Why It Works

The three mechanisms each address a different failure mode:

**MOCs solve the discovery problem.** Without them, the agent needs to know a specific document exists at a specific path. With them, the agent reads one hub file and discovers all related knowledge across every project. One read, full map.

**Pattern extraction solves the reuse problem.** Patterns live in a project-neutral location with a standard format. A debugging fix discovered on Project A is stored identically to a fix discovered on Project B. When Project C needs it, the agent finds it via the Technical Patterns MOC — not by knowing it was originally found on Project A.

**The tag taxonomy solves the proliferation problem.** Without a controlled vocabulary, tags multiply and become meaningless. With one, 40+ documents share ~25 tags, and those tags reliably surface relevant content on search. Tags are edges in the knowledge graph; controlled vocabulary ensures the edges are consistent.

Together these create a knowledge graph with a defined structure:

- **MOC files** are hub nodes — high connectivity, low content
- **Project `_context.md` files** are spoke nodes — project-scoped, link out to MOCs
- **Pattern files** are shared nodes — project-neutral, reachable from any hub
- **Tags** are semantic edges — controlled vocabulary, cross-project reach

The graph is navigable without loading it. The agent follows hub → spoke or hub → pattern paths based on what L1 summaries reveal, loading only what's needed.

## Verification

- Agent applied a competitive intelligence pattern (extracted from a web app project's market scan) to a mobile app's positioning analysis — without being told the pattern existed. It found it by reading the Competitive Intelligence MOC during session start. The connection saved an estimated 3 hours of duplicated research.
- The CORS header-order fix (extracted after its second independent discovery) was retrieved and applied correctly in a third project session. Cost: under 5 minutes. Previous cost for the same debugging session without the pattern: 45 minutes.
- The pricing tier pattern (depth-gating, originally developed for a web app's subscription model) was reused in two subsequent projects. Each reuse saved an estimated 2-3 hours of pricing research and design debate.
- Pattern library grew to 6 entries in 3 weeks. Each entry was used at least once in a project context different from where it originated — confirming that extraction and cross-project retrieval actually works, not just that patterns exist.
- Tag count stabilized: 40+ documents using 23 tags from the canonical taxonomy. Previous uncontrolled system: 100+ tags for 30 documents, with near-zero retrieval value.

## Open Questions

- At what scale do MOCs need their own hierarchy — a MOC of MOCs? The current four-MOC structure handles seven projects without strain. At 15+ projects it may become unwieldy.
- Should the agent proactively suggest pattern extraction when it detects a reusable insight mid-session? Currently this requires a user prompt or session-end skill invocation. Automatic detection could improve capture rates, but risks extracting patterns that aren't actually reusable.
- Obsidian's graph view helps humans see connection density and identify orphaned nodes. Can the agent use a similar signal — e.g., counting MOC back-links — to detect under-connected documents that should be linked or consolidated?
- The current structure assumes a human curates the MOCs. If the agent writes to MOCs autonomously, link quality may degrade. Needs a review mechanism before this is automated.
