"""Static acceptance checks for the @Devil behavioral contract."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "devil" / "SKILL.md"

REQUIRED_COMMANDS = (
    "@Devil attack this",
    "@Devil defend this",
    "@Devil decide",
    "@Devil pre-mortem",
    "@Devil bias check",
    "@Devil alternatives",
    "@Devil reality check",
    "@Devil worst case",
    "@Devil make it stronger",
)

REQUIRED_VERDICTS = (
    "STRONG YES",
    "YES, WITH CONDITIONS",
    "UNCERTAIN",
    "NO, BETTER ALTERNATIVE EXISTS",
    "HARD NO",
)

REQUIRED_SECTIONS = (
    "## VERDICT",
    "## WHY",
    "## STRONGEST CASE AGAINST IT",
    "## KEY RISKS",
    "## WHAT YOU MAY BE MISSING",
    "## STRONGEST CASE FOR IT",
    "## BETTER ALTERNATIVE",
    "## WHAT WOULD CHANGE MY VERDICT",
    "## NEXT MOVE",
)


def main() -> None:
    text = SKILL.read_text(encoding="utf-8")
    missing = [
        item
        for item in REQUIRED_COMMANDS + REQUIRED_VERDICTS + REQUIRED_SECTIONS
        if item not in text
    ]
    assert not missing, f"Missing behavioral requirements: {missing}"
    assert "exactly one primary verdict" in text
    assert "exactly one recommended next action" in text
    assert "I tried to break this idea. It survives the stress test." in text
    assert "Never pretend an assumption was checked." in text
    assert "Apply greater scrutiny" in text
    assert "\u2014" not in text, "Em dash found"
    print("@Devil behavioral contract: PASS")


if __name__ == "__main__":
    main()
