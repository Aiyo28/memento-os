---
name: grill-me
version: 1.1.0
description: >
  Stress-test a plan, design, or architecture through relentless structured
  interviewing. Produces reasoning artifacts as byproduct — every gap found
  becomes a [D], [I], or [S] artifact.
  Triggers: "grill me", "stress test this plan", "poke holes", "challenge
  my design", "devil's advocate", "what am I missing".
user_invocable: true
---

# /grill-me

Interview relentlessly until every branch of the decision tree is walked and resolved. The goal is shared understanding — not critique for its own sake, but surfacing the gaps that would bite later.

## Context Loading (Vault Retrieval Gate)

Before grilling, run the retrieval gate to surface prior decisions:

1. Scan `_context.md` Active Reasoning Artifacts table for `[D]` entries matching the domain
2. Glob `Decisions/*{topic}*` for full artifact files
3. If prior decision found → use as grilling context: "You decided X on {date}. Has the invalidation trigger fired?"
4. Load domain-relevant vault knowledge:
   - **Technical** → Glob `{vault_path}/Knowledge/AI*`, `Knowledge/MOC — *` if exists
   - **Business** → Glob `{vault_path}/Knowledge/Business*`
5. Use matched notes + prior decisions as grilling ammunition

## Before You Start

1. Read the plan/design the user is referring to (file, conversation context, or ask them to state it)
2. If a codebase exists, explore it first — don't ask questions you could answer by reading code

## Grilling Protocol

Work through these dimensions one at a time. For each, ask pointed questions, wait for answers, and probe deeper before moving on. Don't shotgun a list of 10 questions — go one branch at a time and resolve it.

### 1. Assumptions
What are you taking for granted? What must be true for this to work? Ask about each assumption and whether it's been validated.

### 2. Dependencies
What does this depend on? What depends on this? Walk the dependency chain and look for circular dependencies, bottlenecks, or single points of failure.

### 3. Edge Cases
What happens when inputs are unexpected? When scale changes? When the user does something you didn't plan for? When things fail halfway through?

### 4. Trade-offs
What did you give up to get this design? Are you aware of the cost? Would a different trade-off serve you better?

### 5. Alternatives
Why this approach and not the obvious alternatives? If the user can't articulate why, that's a gap.

### 6. Sequencing
What order does this need to happen in? What can be parallelized? What's the critical path? Where's the first place this could stall?

## Rules of Engagement

- **One question at a time.** Wait for the answer. Follow up. Then move on.
- **Explore the codebase** instead of asking when the answer is in the code.
- **Be direct.** "What happens when X fails?" not "Have you considered the failure scenario?"
- **Push back** when answers are hand-wavy. "We'll figure it out later" is a red flag — name what specifically needs figuring out.
- **Acknowledge strong answers.** When a dimension is well-covered, say so and move on. Don't manufacture problems.
- **Track resolved vs. open.** Keep a mental tally. Surface it if the user asks "where are we?"

## Artifact Production

As gaps are found and resolved, capture them:
- **Resolved forks** → `[D]` decision artifacts
- **Surprising findings** → `[I]` insight artifacts
- **"Not now but when X"** → `[S]` seed artifacts

Don't wait until the end — capture artifacts inline as they emerge.

## Done Condition

The grilling is complete when:
- All 6 dimensions have been walked for every major component of the plan
- No open questions remain that could block implementation
- The user confirms they feel confident in the plan

When done, provide a brief summary: what was solid from the start, what gaps were found and resolved, and any remaining risks the user has consciously accepted.
