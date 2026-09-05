from __future__ import annotations

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
REQUIRED = (
    ".gitignore",
    "README.md",
    "SECURITY.md",
    "PRIVACY.md",
    "LICENSE-NOTICE.md",
    "docs/00-overview/CURRENT_STATUS.md",
    "docs/governance/PUBLIC_RELEASE_CHECKLIST.md",
    "docs/progress/RISKS_AND_BLOCKERS.md",
)
FORBIDDEN_SUFFIXES = (".db", ".sqlite", ".sqlite3", ".pyc")
FORBIDDEN_PARTS = {"node_modules", "__pycache__", "private-data", "personal-data"}


def main() -> int:
    errors: list[str] = []
    for relative in REQUIRED:
        if not (ROOT / relative).is_file():
            errors.append(f"missing required file: {relative}")

    for path in ROOT.rglob("*"):
        if ".git" in path.parts or not path.is_file():
            continue
        relative = path.relative_to(ROOT)
        if path.suffix.lower() in FORBIDDEN_SUFFIXES:
            errors.append(f"forbidden file type: {relative}")
        if FORBIDDEN_PARTS.intersection(relative.parts):
            errors.append(f"forbidden generated or private path: {relative}")

    if errors:
        print("Repository validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Repository validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
