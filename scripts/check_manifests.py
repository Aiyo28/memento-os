#!/usr/bin/env python3
"""Fail if the plugin manifests are missing, or drift from each other or the docs.

Each assertion here exists because the corresponding thing actually broke:

- marketplace.json missing  -> it was never `git add`ed; the plugin was uninstallable by any
  path while `claude plugin validate` passed, because that checks manifest shape only.
- version drift             -> plugin.json and marketplace.json can disagree silently.
- llms.txt version          -> it is what AI assistants read; it lagged three releases.
- README skill count        -> README said 5 skills while the repo shipped 7.
- github source             -> a `github` source clones this repo a second time over SSH and
  fails for anyone who does not own it, i.e. every user.
- skill folder vs name      -> folders `memento-lint` / `memento-decay` held `memento:lint` /
  `memento:decay`; the Codex skills ran scripts from folders a copy never created.
- README command names      -> the plugin was named `memento-os`, so Claude Code registered
  `/memento-os:end` while every doc said `/memento:end`. Claude Code names a command
  <plugin name>:<skill folder or command file>.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
errors: list[str] = []


def fail(msg: str) -> None:
    errors.append(msg)


plugin_path = ROOT / ".claude-plugin" / "plugin.json"
market_path = ROOT / ".claude-plugin" / "marketplace.json"

for path in (plugin_path, market_path):
    if not path.exists():
        fail(f"MISSING: {path.relative_to(ROOT)} — the plugin is uninstallable without it")

if errors:
    print("\n".join(errors))
    sys.exit(1)

plugin = json.loads(plugin_path.read_text(encoding="utf-8"))
market = json.loads(market_path.read_text(encoding="utf-8"))
version = plugin["version"]

entry = next((p for p in market["plugins"] if p["name"] == plugin["name"]), None)
if entry is None:
    fail(f"marketplace.json does not list the plugin {plugin['name']!r}")
else:
    if entry.get("version") != version:
        fail(f"version drift: plugin.json {version} vs marketplace {entry.get('version')}")
    source = entry.get("source")
    if isinstance(source, dict) and source.get("source") == "github":
        fail(
            "marketplace source is `github` — that clones this repo again over SSH and fails "
            "with Permission denied for anyone who does not own it. Use the relative path './'."
        )

llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
found = re.search(r"Plugin version (\d+\.\d+\.\d+), MIT\.", llms)
if not found:
    fail("llms.txt has no `Plugin version X.Y.Z, MIT.` line to check")
elif found.group(1) != version:
    fail(f"llms.txt says {found.group(1)}, plugin.json says {version}")

skills_on_disk = len([d for d in (ROOT / "skills").iterdir() if d.is_dir()])
for claimed in re.findall(r"(\d+) skills", (ROOT / "README.md").read_text(encoding="utf-8")):
    if int(claimed) != skills_on_disk:
        fail(f"README claims {claimed} skills; {skills_on_disk} directories exist in skills/")

# A skill named X lives in skills/X/ (as `memento:X`) and in adapters/codex/skills/X/ (as `X`).
codex_dir = ROOT / "adapters" / "codex" / "skills"
for skills_dir, prefix in ((ROOT / "skills", "memento:"), (codex_dir, "")):
    for skill in sorted(d for d in skills_dir.iterdir() if d.is_dir()):
        name = re.search(r"^name:\s*(\S+)", (skill / "SKILL.md").read_text(encoding="utf-8"), re.M)
        if not name or name.group(1) != prefix + skill.name:
            fail(f"{skill.relative_to(ROOT)}/SKILL.md is named {name and name.group(1)!r}, expected {prefix + skill.name!r}")
root_skills = {d.name for d in (ROOT / "skills").iterdir() if d.is_dir()}
codex_skills = {d.name for d in codex_dir.iterdir() if d.is_dir()}
if root_skills != codex_skills:
    fail(f"Codex skills differ from skills/: {sorted(root_skills ^ codex_skills)}")

# Every /memento:X the README names must be a command Claude Code actually registers.
if plugin["name"] != "memento":
    fail(f"plugin name is {plugin['name']!r}; the docs' /memento:... commands need it to be 'memento'")
registered = root_skills | {f.stem for f in (ROOT / "commands").glob("*.md")}
readme = (ROOT / "README.md").read_text(encoding="utf-8")
for named in sorted(set(re.findall(r"/memento:([a-z-]+)", readme)) - registered):
    fail(f"README names /memento:{named}, which is not a skill folder or commands/*.md")

if errors:
    print("\n".join(f"  {e}" for e in errors))
    sys.exit(1)

print(f"ok - {plugin['name']} v{version}, {skills_on_disk} skills, manifests consistent")
