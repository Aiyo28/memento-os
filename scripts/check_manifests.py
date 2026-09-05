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

if errors:
    print("\n".join(f"  {e}" for e in errors))
    sys.exit(1)

print(f"ok - {plugin['name']} v{version}, {skills_on_disk} skills, manifests consistent")
