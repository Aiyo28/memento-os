# Quickstart: Memento OS

## Plugin Install (Recommended)

```bash
/plugin marketplace add Aiyo28/memento-os
/plugin install memento@aiyo
/memento:init
```

The marketplace must be added first; the install has no other source.

That's it. The init command asks 3 questions and sets up your memory folder.

## What Happens Next

| Session | What to do |
|---------|-----------|
| Session 1 | `/memento:init` → answer 3 questions → first artifact captured |
| Session 2+ | `/memento:recall` → see your briefing with active decisions |
| During work | `/memento:decide` when facing choices, `/memento:grill-me` to stress-test plans |
| End of session | `/memento:end` → extracts artifacts, updates NEXT.md |
| Periodically | `/memento:audit` → health check, staleness scan |
| Anytime | `/memento:stats` → memory score, artifact breakdown |

## Manual Install (Without Plugin)

If you prefer to install components individually, copy from the repo:

```bash
# Skills
cp -r skills/* ~/.claude/skills/

# Commands
cp -r commands/* ~/.claude/commands/

# Hooks — merge into your existing settings.json
# See hooks/hooks.json for the Stop and PreCompact hook definitions
```

## Verify

Start a new Claude Code session and run `/memento:recall`. You should see a briefing with your first artifact from init.

## Evolution Log

Want to understand the design decisions? Read the [evolution entries](../evolution/) — each one is a problem we hit, what we tried, and what worked.
