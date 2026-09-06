# Skill Validation v0.1

Validation combines Codex's bundled `quick_validate.py` with AI OS checks. Run:

```powershell
python <HOME>\.codex\ai-os\bin\aios_skills.py validate
python -B <HOME>\.codex\ai-os\validation\test_aios_skills.py
```

Blocking diagnostics include malformed registry or skill metadata, missing descriptions, duplicate IDs or capabilities within an entry, overly broad triggers, unavailable paths, missing or disabled required dependencies, invalid trust or status, suspicious AUTHORITATIVE provenance, broken reference links, empty references, broken Python scripts, and excessively large skill entrypoints.

Cross-skill capability overlap is reported as a warning because deliberate complementary overlap can be valid. Review and document it rather than silently ignoring it. Validation does not prove domain truth; use the quality rubric and risk-based source review as a second gate.

Tests use temporary directories and restore or discard temporary registry state. Production disable and enable operations should be validated immediately after mutation.
