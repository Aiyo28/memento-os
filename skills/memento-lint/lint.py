#!/usr/bin/env python3
"""memento:lint — schema validator for reasoning artifacts.

Walks every _context.md under a vault root, parses the
'Active Reasoning Artifacts' table, validates each artifact row,
prints a grouped report, and exits non-zero on any violation.

Rules (case-insensitive):
  R1  [D]/[I]  must contain 'invalidates if' | 'invalidates when' | 'dies if'
  R2  [S]      must contain 'Activation:' | 'activates when' (strict mode: 'Activation:' only)
  R3  [E]      must contain 'fix:'
  R4  all      # column non-empty
  R5  all      priority column non-empty
  R6  all      row contains YYYY-MM-DD date
  R7  warning  malformed table row (unbalanced backticks, <4 cells, etc.) — promoted
               to violation under --strict; otherwise warn-only

Exit:  0 clean | 1 violations | 2 usage/IO error
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass, field, asdict
from pathlib import Path

SECTION_RE = re.compile(r"^##\s+Active Reasoning Artifacts\s*$", re.IGNORECASE)
NEW_HEADER_RE = re.compile(r"^#{1,3}\s+\S")
ROW_RE = re.compile(r"^\s*\|(.+)\|\s*$")
SEPARATOR_RE = re.compile(r"^\s*\|[\s|:-]+\|\s*$")
ARTIFACT_TYPE_RE = re.compile(r"\[([DIES])\]")
DATE_RE = re.compile(r"\b\d{4}-\d{2}-\d{2}\b")
INVALIDATES_RE = re.compile(r"invalidates if|invalidates when|dies if", re.IGNORECASE)
ACTIVATION_STRICT_RE = re.compile(r"activation:", re.IGNORECASE)
ACTIVATION_LAX_RE = re.compile(r"activation:|activates when", re.IGNORECASE)
FIX_RE = re.compile(r"\bfix:", re.IGNORECASE)


@dataclass
class Violation:
    rule: str
    message: str
    severity: str = "violation"  # "violation" | "warning"


@dataclass
class ArtifactCheck:
    file: str
    line: int
    number: str
    type: str
    summary: str
    violations: list[Violation] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.violations

    def has_violation(self, include_warnings: bool) -> bool:
        if include_warnings:
            return bool(self.violations)
        return any(v.severity == "violation" for v in self.violations)


def split_row(row_inner: str) -> list[str]:
    """Split a markdown table row body on unescaped pipes, ignoring backtick spans."""
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
    """Return (start_idx, end_idx) line indexes (0-based, exclusive end) for the table body
    under the '## Active Reasoning Artifacts' header, or None."""
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


def check_artifact(file_rel: str, lineno: int, cells: list[str], strict: bool) -> ArtifactCheck | None:
    if len(cells) < 4:
        return None
    num_cell, artifact_cell, priority_cell, date_cell = cells[0], cells[1], cells[2], cells[3]
    m = ARTIFACT_TYPE_RE.search(artifact_cell)
    if not m:
        return None
    a_type = m.group(1)
    summary = artifact_cell[:80].replace("`", "").strip()
    check = ArtifactCheck(file=file_rel, line=lineno, number=num_cell, type=a_type, summary=summary)

    if not num_cell:
        check.violations.append(Violation("R4", "missing # number"))
    if not priority_cell:
        check.violations.append(Violation("R5", "missing priority"))

    full_row_text = " | ".join(cells)
    if not DATE_RE.search(full_row_text):
        check.violations.append(Violation("R6", "no YYYY-MM-DD date in row"))

    if a_type in ("D", "I"):
        if not INVALIDATES_RE.search(artifact_cell):
            check.violations.append(
                Violation("R1", "missing 'invalidates if|invalidates when|dies if' clause")
            )
    elif a_type == "S":
        rx = ACTIVATION_STRICT_RE if strict else ACTIVATION_LAX_RE
        if not rx.search(artifact_cell):
            expected = "'Activation:'" if strict else "'Activation:' or 'activates when'"
            check.violations.append(Violation("R2", f"missing {expected} clause"))
    elif a_type == "E":
        if not FIX_RE.search(artifact_cell):
            check.violations.append(Violation("R3", "missing 'fix:' clause"))

    return check


def make_malformed_check(file_rel: str, lineno: int, reason: str) -> ArtifactCheck:
    check = ArtifactCheck(file=file_rel, line=lineno, number="?", type="?", summary="(malformed row)")
    check.violations.append(Violation("R7", f"malformed row ({reason}) — artifact not validated", severity="warning"))
    return check


def lint_file(path: Path, vault_root: Path, strict: bool) -> list[ArtifactCheck]:
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as e:
        print(f"warning: cannot read {path}: {e}", file=sys.stderr)
        return []
    lines = text.splitlines()
    section = find_artifact_section(lines)
    if section is None:
        return []
    start, end = section
    rel = str(path.relative_to(vault_root)) if path.is_relative_to(vault_root) else str(path)
    results: list[ArtifactCheck] = []
    for i in range(start, end):
        line = lines[i]
        if SEPARATOR_RE.match(line):
            continue
        m = ROW_RE.match(line)
        if not m:
            if line.lstrip().startswith("|") and ARTIFACT_TYPE_RE.search(line):
                results.append(make_malformed_check(rel, i + 1, "does not match table-row format"))
            continue
        if line.count("`") % 2 != 0 and ARTIFACT_TYPE_RE.search(line):
            results.append(make_malformed_check(rel, i + 1, "unbalanced backticks"))
            continue
        cells = split_row(m.group(1))
        if cells and cells[0].lower() == "#":
            continue
        if len(cells) < 4 and ARTIFACT_TYPE_RE.search(line):
            results.append(make_malformed_check(rel, i + 1, f"only {len(cells)} cells parsed"))
            continue
        check = check_artifact(rel, i + 1, cells, strict)
        if check is not None:
            results.append(check)
    return results


def discover_context_files(root: Path) -> list[Path]:
    return sorted(root.rglob("_context.md"))


def render_text(results: list[ArtifactCheck], vault_root: Path, quiet: bool) -> str:
    by_file: dict[str, list[ArtifactCheck]] = {}
    for r in results:
        by_file.setdefault(r.file, []).append(r)
    lines = [f"memento:lint — vault validation report (vault: {vault_root})", ""]
    total_violations = 0
    total_warnings = 0
    for file in sorted(by_file):
        checks = by_file[file]
        file_has_issues = any(not c.ok for c in checks)
        if quiet and not file_has_issues:
            continue
        lines.append(file)
        for c in checks:
            tag = f"[{c.type}]#{c.number or '?'}"
            if c.ok:
                if not quiet:
                    lines.append(f"  L{c.line:<5d}{tag:<10s} OK")
            else:
                for v in c.violations:
                    label = "WARN" if v.severity == "warning" else v.rule
                    lines.append(f"  L{c.line:<5d}{tag:<10s} {label}: {v.message}" if v.severity == "warning"
                                 else f"  L{c.line:<5d}{tag:<10s} {v.rule}: {v.message}")
                    if v.severity == "warning":
                        total_warnings += 1
                    else:
                        total_violations += 1
        lines.append("")
    artifact_count = len(results)
    files_with_violations = sum(1 for cs in by_file.values() if any(not c.ok for c in cs))
    summary = f"Summary: {total_violations} violations"
    if total_warnings:
        summary += f", {total_warnings} warnings"
    summary += f" across {files_with_violations} files ({artifact_count} artifacts checked)"
    lines.append(summary)
    return "\n".join(lines)


def render_json(results: list[ArtifactCheck], vault_root: Path) -> str:
    payload = {
        "vault_root": str(vault_root),
        "artifact_count": len(results),
        "violations": [
            {
                "file": r.file,
                "line": r.line,
                "number": r.number,
                "type": r.type,
                "summary": r.summary,
                "violations": [asdict(v) for v in r.violations],
            }
            for r in results
            if not r.ok
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
        prog="memento-lint",
        description="Validate reasoning artifacts in vault _context.md files.",
    )
    p.add_argument("vault_root", nargs="?", default=None, help="vault root (default: $MEMENTO_VAULT_ROOT or CWD)")
    p.add_argument("--strict", action="store_true", help="for [S], require literal 'Activation:' — disallow 'activates when'; promote R7 warnings to violations")
    p.add_argument("--format", choices=("text", "json"), default="text")
    p.add_argument("--quiet", action="store_true", help="suppress per-file OK lines")
    p.add_argument("--ci", action="store_true", help="sugar for --strict --quiet")
    args = p.parse_args(argv)

    if args.ci:
        args.strict = True
        args.quiet = True

    vault_root = resolve_vault_root(args.vault_root)
    if not vault_root.exists():
        print(f"error: vault root not found: {vault_root}", file=sys.stderr)
        return 2

    files = discover_context_files(vault_root)
    all_results: list[ArtifactCheck] = []
    for f in files:
        all_results.extend(lint_file(f, vault_root, args.strict))

    if args.strict:
        for r in all_results:
            for v in r.violations:
                if v.severity == "warning":
                    v.severity = "violation"

    if args.format == "json":
        print(render_json(all_results, vault_root))
    else:
        print(render_text(all_results, vault_root, args.quiet))

    has_violations = any(r.has_violation(include_warnings=False) for r in all_results)
    return 1 if has_violations else 0


if __name__ == "__main__":
    sys.exit(main())
