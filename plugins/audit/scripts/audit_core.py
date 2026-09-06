#!/usr/bin/env python3
"""Fail-closed assurance contracts for the standalone Audit plugin."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


USER_HOME = Path.home()
PLUGIN_ROOT = Path(__file__).resolve().parents[1]
AGENT_REGISTRY = USER_HOME / ".codex" / "ai-os" / "registry" / "agent-registry.json"
FINDING_FIELDS = {"id", "title", "severity", "evidence", "confidence", "limitations", "recommendation", "escalation_conditions"}
SEVERITIES = {"INFO", "LOW", "MEDIUM", "HIGH", "CRITICAL"}
RECOMMENDATIONS = {"APPROVE", "APPROVE WITH CONDITIONS", "REWORK", "DEFER", "BLOCKED"}
PROHIBITED_AUTHORITIES = {"primary-web-research", "software-implementation", "strategic-tradeoff-judgment", "system-orchestration"}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def nonempty_string_list(value: Any) -> bool:
    return isinstance(value, list) and bool(value) and all(isinstance(item, str) and item.strip() for item in value)


def validate_finding(finding: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    missing = sorted(FINDING_FIELDS - set(finding))
    if missing:
        return ["missing finding fields: " + ", ".join(missing)]
    if not isinstance(finding["id"], str) or not re.fullmatch(r"[A-Z][A-Z0-9-]{2,63}", finding["id"]):
        errors.append("finding id must be uppercase, stable, and at least three characters")
    if not isinstance(finding["title"], str) or not finding["title"].strip():
        errors.append("finding title must be non-empty")
    if finding["severity"] not in SEVERITIES:
        errors.append("finding severity is invalid")
    if not nonempty_string_list(finding["evidence"]):
        errors.append("finding requires at least one inspectable evidence identifier or link")
    if not isinstance(finding["confidence"], (float, int)) or isinstance(finding["confidence"], bool) or not 0 <= finding["confidence"] <= 1:
        errors.append("finding confidence must be a number from 0 to 1")
    if not isinstance(finding["limitations"], list) or not all(isinstance(item, str) and item.strip() for item in finding["limitations"]):
        errors.append("finding limitations must be a string list")
    if finding["recommendation"] not in RECOMMENDATIONS:
        errors.append("finding recommendation is invalid")
    if not nonempty_string_list(finding["escalation_conditions"]):
        errors.append("finding requires explicit escalation conditions")
    return errors


def validate_audit_record(record: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    required = {"audit_id", "scope", "audited_artifacts", "findings", "prohibited_authorities", "status"}
    missing = sorted(required - set(record))
    if missing:
        return ["missing audit record fields: " + ", ".join(missing)]
    if not isinstance(record["audit_id"], str) or not record["audit_id"].strip():
        errors.append("audit_id must be non-empty")
    if record["scope"] != "independent-assurance":
        errors.append("Audit scope must be independent-assurance")
    if not nonempty_string_list(record["audited_artifacts"]):
        errors.append("audited_artifacts must contain inspectable identifiers")
    if not isinstance(record["findings"], list):
        errors.append("findings must be a list")
    else:
        identifiers: set[str] = set()
        for index, finding in enumerate(record["findings"]):
            if not isinstance(finding, dict):
                errors.append(f"finding {index} must be an object")
                continue
            errors.extend(f"finding {index}: {item}" for item in validate_finding(finding))
            identifier = finding.get("id")
            if isinstance(identifier, str) and identifier in identifiers:
                errors.append(f"duplicate finding id: {identifier}")
            identifiers.add(identifier)
    prohibited = set(record["prohibited_authorities"]) if isinstance(record["prohibited_authorities"], list) else set()
    if prohibited != PROHIBITED_AUTHORITIES:
        errors.append("Audit must explicitly preserve all four non-overlap boundaries")
    if record["status"] not in RECOMMENDATIONS:
        errors.append("audit status is invalid")
    return errors


def recommend(record: dict[str, Any]) -> str:
    """Return a fail-closed recommendation based only on stated audit evidence."""
    errors = validate_audit_record(record)
    if errors:
        return "REWORK"
    findings = record["findings"]
    if not findings:
        return "DEFER"
    if any(item["recommendation"] == "BLOCKED" for item in findings):
        return "BLOCKED"
    if any(item["recommendation"] == "DEFER" for item in findings):
        return "DEFER"
    if any(item["severity"] in {"CRITICAL", "HIGH"} or item["recommendation"] == "REWORK" for item in findings):
        return "REWORK"
    if any(item["limitations"] for item in findings):
        return "APPROVE WITH CONDITIONS"
    return "APPROVE"


def route(task: str) -> dict[str, Any]:
    text = task.lower()
    overlap_signals = {
        "primary-web-research": ("research the web", "browse for sources", "find current sources"),
        "software-implementation": ("implement", "repair code", "fix code"),
        "strategic-tradeoff-judgment": ("what should we choose", "make the strategic decision", "strategic decision"),
        "system-orchestration": ("orchestrate the system", "route the full system"),
    }
    overlaps = [authority for authority, signals in overlap_signals.items() if any(signal in text for signal in signals)]
    if overlaps:
        return {
            "task": task.strip(), "selected_private_skills": [], "authority": "independent-assurance",
            "prohibited_authorities": sorted(PROHIBITED_AUTHORITIES), "rejected_authority_overlap": overlaps,
            "composition": "EMULATED_HOST_MEDIATED",
        }
    selected = ["audit-evidence-policy"]
    if any(signal in text for signal in ("release", "deploy", "publish", "completion")):
        selected.append("audit-release-gate")
    if any(signal in text for signal in ("challenge", "adversarial", "risk", "claim")):
        selected.append("audit-adversarial-assurance")
    return {
        "task": task.strip(),
        "selected_private_skills": selected,
        "authority": "independent-assurance",
        "prohibited_authorities": sorted(PROHIBITED_AUTHORITIES),
        "composition": "EMULATED_HOST_MEDIATED",
    }


def health() -> dict[str, Any]:
    checks = {
        "plugin_source": (PLUGIN_ROOT / ".codex-plugin" / "plugin.json").exists(),
        "entrypoint": (PLUGIN_ROOT / "skills" / "audit" / "SKILL.md").exists(),
        "registry": AGENT_REGISTRY.exists(),
    }
    registry_errors: list[str] = []
    if checks["registry"]:
        agents = load_json(AGENT_REGISTRY).get("agents", [])
        audit = next((agent for agent in agents if agent.get("id") == "audit"), None)
        checks["registered"] = bool(audit and audit.get("enabled") and audit.get("installed") and audit.get("status") == "AVAILABLE")
        if audit and set(audit.get("authority", [])) & PROHIBITED_AUTHORITIES:
            registry_errors.append("Audit registry grants a prohibited authority")
    else:
        checks["registered"] = False
    return {"status": "PASS" if all(checks.values()) and not registry_errors else "FAIL", "checks": checks, "registry_errors": registry_errors, "composition": "EMULATED_HOST_MEDIATED"}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Audit assurance diagnostics")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("health")
    skills = sub.add_parser("skills")
    skills.add_argument("task", nargs="?", default="")
    assess = sub.add_parser("assess")
    assess.add_argument("record", type=Path)
    args = parser.parse_args(argv)
    if args.command == "health":
        payload = health()
    elif args.command == "skills":
        payload = route(args.task)
    else:
        record = load_json(args.record)
        payload = {"validation_errors": validate_audit_record(record), "recommendation": recommend(record)}
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 0 if payload.get("status", "PASS") == "PASS" and not payload.get("validation_errors") else 1


if __name__ == "__main__":
    sys.exit(main())
