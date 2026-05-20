#!/usr/bin/env python3
"""memento:decay — find aged [D] artifacts whose invalidation triggers may have fired.

Walks every _context.md under a vault root, collects [D] artifacts older than
--age days, extracts the invalidator phrase, and scores decay likelihood from
three signals:

  (a) git log keyword search   — when a git repo is reachable
  (b) vault contradiction      — newer artifacts whose conclusion overlaps
  (c) age past threshold       — weak signal, always present

Emits a ranked candidate list (text or JSON). The Claude Code agent consumes
the JSON to drive the user-facing y/n confirmation prompt.

Exit:  0 always (scan-only; supersession is the agent's job)
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass, field, asdict
from datetime import date, datetime
from pathlib import Path

SECTION_RE = re.compile(r"^##\s+Active Reasoning Artifacts\s*$", re.IGNORECASE)
NEW_HEADER_RE = re.compile(r"^#{1,3}\s+\S")
ROW_RE = re.compile(r"^\s*\|(.+)\|\s*$")
SEPARATOR_RE = re.compile(r"^\s*\|[\s|:-]+\|\s*$")
ARTIFACT_TYPE_RE = re.compile(r"\[([DIES])\]")
DATE_RE = re.compile(r"\b(\d{4}-\d{2}-\d{2})\b")
INVALIDATES_RE = re.compile(
    r"(?:invalidates if|invalidates when|dies if)\s*(.+?)(?:\s*\[|$)",
    re.IGNORECASE,
)
DEFAULT_STOPWORDS = {
    "a", "an", "the", "is", "are", "was", "were", "be", "to", "for", "of",
    "in", "on", "by", "and", "or", "but", "if", "when", "than", "then", "that",
    "this", "these", "those", "it", "its", "as", "at", "from", "with", "without",
    "any", "all", "no", "not", "so", "do", "does", "did", "has", "have", "had",
    "we", "you", "they", "i", "user", "users",
    "invalidates", "activates", "dies", "trigger", "condition",
}


def load_stopwords(vault_root: Path, explicit_path: str | None) -> set[str]:
    """Load DEFAULT_STOPWORDS plus, if available, the explicit --stopwords file
    (when provided) or `<vault_root>/.memento-stopwords` (default lookup)."""
    words = set(DEFAULT_STOPWORDS)
    if explicit_path is not None:
        path = Path(explicit_path).expanduser()
    else:
        candidate = vault_root / ".memento-stopwords"
        path = candidate if candidate.exists() else None
    if path is None:
        return words
    try:
        for raw in path.read_text(encoding="utf-8").splitlines():
            word = raw.strip().lower()
            if word and not word.startswith("#"):
                words.add(word)
    except (OSError, UnicodeDecodeError):
        pass
    return words


@dataclass
class Artifact:
    file: str
    line: int
    number: str
    type: str
    raw: str
    date_str: str
    age_days: int
    invalidator: str | None


@dataclass
class Signal:
    type: str
    weight: int
    evidence: str


@dataclass
class Candidate:
    file: str
    line: int
    number: str
    artifact: str
    invalidator: str | None
    age_days: int
    score: int = 0
    signals: list[Signal] = field(default_factory=list)


def split_row(row_inner: str) -> list[str]:
    cells: list[str] = []
    buf: list[str] = []
    in_backtick = False
    for ch in row_inner:
        if ch == "`":
            in_backtick = not in_backtick
            buf.append(ch)
        elif ch == "|" and not in_backtick:
            cells.append("".join(buf).strip())
            buf = []
        else:
            buf.append(ch)
    cells.append("".join(buf).strip())
    return cells


def find_artifact_section(lines: list[str]) -> tuple[int, int] | None:
    start = None
    for i, line in enumerate(lines):
        if SECTION_RE.match(line):
            start = i + 1
            break
    if start is None:
        return None
    end = len(lines)
    for j in range(start, len(lines)):
        if NEW_HEADER_RE.match(lines[j]):
            end = j
            break
    return start, end


def parse_date(s: str) -> date | None:
    try:
        return datetime.strptime(s, "%Y-%m-%d").date()
    except ValueError:
        return None


def extract_invalidator(text: str) -> str | None:
    m = INVALIDATES_RE.search(text)
    if not m:
        return None
    return m.group(1).strip().strip("`").rstrip(".,;").strip()


def keywords(phrase: str, stopwords: set[str], limit: int = 4) -> list[str]:
    tokens = re.findall(r"[A-Za-z][A-Za-z0-9_-]{3,}", phrase.lower())
    seen: list[str] = []
    for t in tokens:
        if t in stopwords or t in seen:
            continue
        seen.append(t)
        if len(seen) >= limit:
            break
    return seen


def collect_artifacts(root: Path, today: date) -> list[Artifact]:
    artifacts: list[Artifact] = []
    for path in sorted(root.rglob("_context.md")):
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        lines = text.splitlines()
        section = find_artifact_section(lines)
        if section is None:
            continue
        start, end = section
        rel = str(path.relative_to(root)) if path.is_relative_to(root) else str(path)
        for i in range(start, end):
            line = lines[i]
            if SEPARATOR_RE.match(line):
                continue
            m = ROW_RE.match(line)
            if not m:
                continue
            cells = split_row(m.group(1))
            if len(cells) < 4 or (cells and cells[0].lower() == "#"):
                continue
            t = ARTIFACT_TYPE_RE.search(cells[1])
            if not t:
                continue
            row_text = " | ".join(cells)
            d_match = DATE_RE.search(row_text)
            if not d_match:
                continue
            d = parse_date(d_match.group(1))
            if d is None:
                continue
            artifacts.append(
                Artifact(
                    file=rel,
                    line=i + 1,
                    number=cells[0],
                    type=t.group(1),
                    raw=cells[1],
                    date_str=d_match.group(1),
                    age_days=(today - d).days,
                    invalidator=extract_invalidator(cells[1]),
                )
            )
    return artifacts


def find_git_root(start: Path) -> Path | None:
    p = start
    for _ in range(6):
        if (p / ".git").exists():
            return p
        if p.parent == p:
            return None
        p = p.parent
    return None


def git_signal(repo_root: Path, kws: list[str], since: str) -> list[Signal]:
    """Group git-log matches by commit hash; weight by per-commit keyword overlap.

    Single-keyword match in a commit = +1 (weak).
    Two keywords in the same commit = +3 (moderate).
    Three+ keywords in the same commit = +5 (strong).
    Total cap = +6.
    """
    if not kws:
        return []
    commit_keywords: dict[str, tuple[str, set[str]]] = {}
    try:
        for kw in kws:
            result = subprocess.run(
                [
                    "git", "-C", str(repo_root), "log",
                    f"--since={since}",
                    "--all",
                    "--pretty=format:%h\t%s",
                    "--grep", kw,
                    "-i",
                    "-n", "10",
                ],
                capture_output=True,
                text=True,
                timeout=8,
            )
            if result.returncode != 0:
                continue
            for line in result.stdout.splitlines():
                if "\t" not in line:
                    continue
                sha, subject = line.split("\t", 1)
                if sha not in commit_keywords:
                    commit_keywords[sha] = (subject, set())
                commit_keywords[sha][1].add(kw)
    except (subprocess.SubprocessError, OSError, FileNotFoundError):
        return []
    scored = []
    for sha, (subject, kw_set) in commit_keywords.items():
        n = len(kw_set)
        if n >= 3:
            weight = 5
        elif n == 2:
            weight = 3
        else:
            weight = 1
        scored.append((weight, n, sha, subject, sorted(kw_set)))
    scored.sort(key=lambda t: (-t[0], -t[1]))
    signals: list[Signal] = []
    total = 0
    for weight, n, sha, subject, sorted_kws in scored:
        if total >= 6:
            break
        capped = min(weight, 6 - total)
        if capped <= 0:
            break
        evidence = f"commit {sha} matched {n} keyword(s) [{','.join(sorted_kws)}]: {subject}"
        signals.append(Signal(type="git", weight=capped, evidence=evidence))
        total += capped
    return signals


def vault_signal(target: Artifact, all_artifacts: list[Artifact], stopwords: set[str]) -> list[Signal]:
    if not target.invalidator:
        return []
    kws = set(keywords(target.invalidator + " " + target.raw, stopwords, limit=6))
    if not kws:
        return []
    target_date = parse_date(target.date_str)
    if target_date is None:
        return []
    signals: list[Signal] = []
    for other in all_artifacts:
        if other is target:
            continue
        if other.type not in ("D", "I"):
            continue
        other_date = parse_date(other.date_str)
        if other_date is None or other_date <= target_date:
            continue
        other_kws = set(keywords(other.raw, stopwords, limit=8))
        overlap = kws & other_kws
        if len(overlap) >= 2:
            ev = f"{other.file} [{other.type}]#{other.number} ({other.date_str}) overlap: {','.join(sorted(overlap))}"
            signals.append(Signal(type="vault", weight=3, evidence=ev))
    return signals


def score(candidate: Candidate, signals: list[Signal], age_days: int) -> None:
    candidate.signals.extend(signals)
    candidate.score = sum(s.weight for s in signals)
    if age_days > 90 and not signals:
        candidate.signals.append(Signal(type="age", weight=1, evidence=f"age {age_days}d"))
        candidate.score += 1


def render_text(candidates: list[Candidate], vault_root: Path) -> str:
    lines = [f"memento:decay — aged decisions (vault: {vault_root})", ""]
    if not candidates:
        lines.append("No aged [D] artifacts past threshold. Vault is fresh.")
        return "\n".join(lines)
    candidates_sorted = sorted(candidates, key=lambda c: c.score, reverse=True)
    for c in candidates_sorted:
        tier = "LIKELY STALE" if c.score >= 3 else ("REVIEW" if c.score >= 1 else "AGE-ONLY")
        lines.append(f"[{tier}] {c.file} [D]#{c.number} (age {c.age_days}d, score {c.score})")
        lines.append(f"  artifact: {c.artifact[:140]}")
        if c.invalidator:
            lines.append(f"  invalidator: {c.invalidator[:120]}")
        for s in c.signals:
            lines.append(f"  + {s.type} (+{s.weight}): {s.evidence}")
        lines.append("")
    lines.append(f"Summary: {len(candidates)} candidates ({sum(1 for c in candidates if c.score >= 3)} likely stale)")
    return "\n".join(lines)


def render_json(candidates: list[Candidate], vault_root: Path) -> str:
    payload = {
        "vault_root": str(vault_root),
        "candidates": [
            {
                "file": c.file,
                "line": c.line,
                "number": c.number,
                "artifact": c.artifact,
                "invalidator": c.invalidator,
                "age_days": c.age_days,
                "score": c.score,
                "signals": [asdict(s) for s in c.signals],
            }
            for c in sorted(candidates, key=lambda x: x.score, reverse=True)
        ],
    }
    return json.dumps(payload, indent=2)


def resolve_vault_root(arg: str | None) -> Path:
    if arg:
        return Path(arg).expanduser().resolve()
    env = os.environ.get("MEMENTO_VAULT_ROOT")
    if env:
        return Path(env).expanduser().resolve()
    return Path.cwd().resolve()


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        prog="memento-decay",
        description="Find aged [D] artifacts whose invalidation triggers may have fired.",
    )
    p.add_argument("vault_root", nargs="?", default=None)
    p.add_argument("--age", type=int, default=30, help="minimum age in days (default 30)")
    p.add_argument("--format", choices=("text", "json"), default="text")
    p.add_argument("--no-git", action="store_true", help="skip git signal even if repo present")
    p.add_argument("--all", action="store_true", help="include score-0 candidates")
    p.add_argument("--stopwords", default=None, help="path to extra stopwords file (one word per line). Default: <vault_root>/.memento-stopwords if present")
    args = p.parse_args(argv)

    vault_root = resolve_vault_root(args.vault_root)
    if not vault_root.exists():
        print(f"error: vault root not found: {vault_root}", file=sys.stderr)
        return 2

    stopwords = load_stopwords(vault_root, args.stopwords)
    today = date.today()
    artifacts = collect_artifacts(vault_root, today)
    aged = [a for a in artifacts if a.type == "D" and a.age_days >= args.age]

    repo_root: Path | None = None
    if not args.no_git:
        repo_root = find_git_root(vault_root)

    candidates: list[Candidate] = []
    for a in aged:
        cand = Candidate(
            file=a.file,
            line=a.line,
            number=a.number,
            artifact=a.raw,
            invalidator=a.invalidator,
            age_days=a.age_days,
        )
        signals: list[Signal] = []
        if a.invalidator:
            signals.extend(vault_signal(a, artifacts, stopwords))
            if repo_root is not None:
                kws = keywords(a.invalidator, stopwords)
                since = (
                    datetime.strptime(a.date_str, "%Y-%m-%d").date().isoformat()
                )
                signals.extend(git_signal(repo_root, kws, since))
        score(cand, signals, a.age_days)
        if cand.score > 0 or args.all:
            candidates.append(cand)

    if args.format == "json":
        print(render_json(candidates, vault_root))
    else:
        print(render_text(candidates, vault_root))

    return 0


if __name__ == "__main__":
    sys.exit(main())
