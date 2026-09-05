# v2.3.3 — Install works, and the hooks wait their turn

If you tried to install Memento OS before today and it didn't work, that was on us,
and it's fixed.

## Installing

```
/plugin marketplace add Aiyo28/memento-os
/plugin install memento-os@aiyo
```

Both steps are needed — the first registers the marketplace, the second installs from
it. The marketplace is called `aiyo` rather than `memento-os`, so future plugins can
live alongside this one instead of asking you to add a second marketplace.

Already installed? `claude plugin update memento-os@aiyo`. Updating the marketplace on
its own won't move an installed plugin.

## What was broken

- The marketplace manifest had never made it into the repository, so
  `/plugin marketplace add` returned a 404 and `/plugin install` had nothing to install
  from. Fixed in 2.3.1.
- After that, installs failed with `Permission denied (publickey)` — the plugin was
  being fetched over SSH from a repo you'd have needed a key for. Fixed in 2.3.2.

## Hooks now wait until you're set up

This is the part worth knowing about. The `Stop` and `PreCompact` hooks used to start
writing session logs the moment the plugin was enabled — including in projects where
you'd never run `/memento:init`, so they'd invent somewhere to put things.

Now they do nothing at all until a project is initialised. Nothing is written to a
project you haven't set up.

There's also a new `SessionStart` hook that prints a single line when Memento is
installed but not yet initialised here, so you're not left guessing what to do after
install. If there's a project where you never want Memento, `touch .memento-skip` and
it'll stay quiet.

## Housekeeping

- The test suite had quietly gone red back in June — a fixture with a hard-coded date
  that aged past its own assumption. Fixed, and CI now runs weekly as well as on every
  push, because a date-sensitive suite can break with nobody having touched it.
- The README was still advertising 5 skills. There are 7: `decide`, `grill-me`,
  `session-start`, `session-complete`, `vault-audit`, `decay`, `lint`.
- Donation link is Ko-fi throughout now, rather than disagreeing with itself.
