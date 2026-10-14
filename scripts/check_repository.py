#!/usr/bin/env python3
"""Check local Markdown links, portable skill metadata, and CSV template shape."""
import csv
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]


def main():
    errors = []
    for path in ROOT.rglob("*.md"):
        if ".git" in path.parts:
            continue
        text = path.read_text(encoding="utf-8")
        # Only inline local links; remote URLs and Markdown anchor targets are not fetched.
        for target in re.findall(r"\]\(([^\s)]+)(?:\s+\"[^\"]*\")?\)", text):
            parsed = urlsplit(target.strip("<>"))
            if parsed.scheme or parsed.netloc or not parsed.path:
                continue
            if not (path.parent / unquote(parsed.path)).exists():
                errors.append(f"{path.relative_to(ROOT)}: missing link target {target}")
    for skill in sorted((ROOT / "skills").iterdir()):
        if not skill.is_dir():
            continue
        path = skill / "SKILL.md"
        if not path.is_file():
            errors.append(f"{skill.name}: missing SKILL.md")
            continue
        text = path.read_text(encoding="utf-8")
        sections = text.split("---", 2)
        if len(sections) != 3 or sections[0].strip():
            errors.append(f"{skill.name}: missing YAML frontmatter")
            continue
        fields = dict(re.findall(r"^(name|description):\s*(.+)$", sections[1], re.M))
        if fields.get("name") != skill.name or not fields.get("description"):
            errors.append(f"{skill.name}: invalid name/description")
        metadata = skill / "agents/openai.yaml"
        if not metadata.is_file() or f"${skill.name}" not in metadata.read_text():
            errors.append(f"{skill.name}: missing agent metadata/default invocation")
        for template in (skill / "assets").glob("*.csv"):
            with template.open(newline="", encoding="utf-8-sig") as stream:
                rows = list(csv.reader(stream))
            if len(rows) != 1 or not rows[0] or len(set(rows[0])) != len(rows[0]) or any(not value for value in rows[0]):
                errors.append(f"{template.relative_to(ROOT)}: expected unique header-only CSV")
    for error in errors:
        print("ERROR:", error)
    print(f"{'FAIL' if errors else 'PASS'}: repository structure ({len(errors)} errors)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
