#!/usr/bin/env python3
"""Fail closed on a Forge verification report."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def evaluate(report: dict) -> tuple[bool, list[str]]:
    errors: list[str] = []
    if not report.get("product_contract_satisfied", False):
        errors.append("product contract is not satisfied")
    checks = report.get("checks", [])
    if not checks:
        errors.append("no verification checks recorded")
    for check in checks:
        if check.get("status") != "passed":
            errors.append(f"check did not pass: {check.get('name', 'unnamed')}")
    for finding in report.get("findings", []):
        if finding.get("severity") in {"BLOCKER", "HIGH"} and finding.get("status") != "resolved":
            errors.append(f"unresolved {finding.get('severity')}: {finding.get('title', 'untitled')}")
    if report.get("claims", {}).get("fully_working") and report.get("critical_integrations_mocked"):
        errors.append("fully working claimed while a critical integration is mocked")
    return not errors, errors


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate a Forge completion report")
    parser.add_argument("report", type=Path)
    args = parser.parse_args()
    data = json.loads(args.report.read_text(encoding="utf-8"))
    passed, errors = evaluate(data)
    print(json.dumps({"passed": passed, "errors": errors}, indent=2))
    raise SystemExit(0 if passed else 1)


if __name__ == "__main__":
    main()
