#!/usr/bin/env python3
"""Portable control-plane contracts for host-mediated Agentic Core workflows.

This module deliberately coordinates records, not autonomous plugin processes.
The Codex host composes MOA, Minister, Scout, Forge, and independent review
inside one task.  The module makes that composition inspectable and fail closed.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from copy import deepcopy
from pathlib import Path
from typing import Any


HANDOFF_FIELDS = (
    "OBJECTIVE", "CONTEXT", "INPUTS", "CONSTRAINTS", "REQUIRED OUTPUT",
    "ACCEPTANCE CRITERIA", "AUTHORITY", "KNOWN RISKS", "WHAT NOT TO DO",
)
TERMINAL_STATES = {"PASS", "REWORK", "DEFER", "BLOCKED", "REJECTED"}
ALL_STATES = {"PENDING", "IN_PROGRESS", *TERMINAL_STATES}
ALLOWED_TRANSITIONS = {
    "PENDING": {"IN_PROGRESS", "DEFER", "BLOCKED", "REJECTED"},
    "IN_PROGRESS": TERMINAL_STATES,
    "PASS": set(), "REWORK": {"IN_PROGRESS", "DEFER", "BLOCKED", "REJECTED"},
    "DEFER": {"IN_PROGRESS", "REJECTED"}, "BLOCKED": {"IN_PROGRESS", "REJECTED"},
    "REJECTED": set(),
}
AUTHORITIES = {"MOA", "Minister", "Scout", "Forge", "Audit", "Verification", "User"}
MAX_IDENTICAL_BLOCKER_ATTEMPTS = 3


def canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value).encode("utf-8")).hexdigest()


def validate_handoff(handoff: dict[str, Any]) -> list[str]:
    """Reject incomplete, unbounded, or authority-confused handoffs."""
    errors: list[str] = []
    for field in HANDOFF_FIELDS:
        if field not in handoff:
            errors.append(f"missing handoff field: {field}")
    if errors:
        return errors
    for field in ("OBJECTIVE", "CONTEXT", "REQUIRED OUTPUT", "AUTHORITY"):
        if not isinstance(handoff[field], str) or not handoff[field].strip():
            errors.append(f"handoff {field} must be a non-empty string")
    for field in ("INPUTS", "CONSTRAINTS", "ACCEPTANCE CRITERIA", "KNOWN RISKS", "WHAT NOT TO DO"):
        if not isinstance(handoff[field], list) or not handoff[field] or not all(isinstance(item, str) and item.strip() for item in handoff[field]):
            errors.append(f"handoff {field} must be a non-empty string list")
    if handoff.get("AUTHORITY") not in AUTHORITIES:
        errors.append(f"unknown handoff authority: {handoff.get('AUTHORITY')}")
    return errors


def transition(component: dict[str, Any], target: str, *, blocker: str | None = None) -> dict[str, Any]:
    """Apply one legal bounded transition, escalating a repeated blocker."""
    record = deepcopy(component)
    current = record.get("status", "PENDING")
    if current not in ALL_STATES or target not in ALL_STATES:
        raise ValueError("unknown lifecycle state")
    if target not in ALLOWED_TRANSITIONS[current]:
        raise ValueError(f"illegal transition: {current} -> {target}")
    if blocker:
        if not blocker.strip():
            raise ValueError("blocker must not be blank")
        same = record.get("last_blocker") == blocker
        attempts = int(record.get("blocker_attempts", 0)) + 1 if same else 1
        record["last_blocker"] = blocker
        record["blocker_attempts"] = attempts
        if attempts >= MAX_IDENTICAL_BLOCKER_ATTEMPTS:
            target = "BLOCKED"
    record["status"] = target
    return record


def append_audit_event(events: list[dict[str, Any]], event: dict[str, Any]) -> list[dict[str, Any]]:
    """Append a tamper-evident event without mutating the prior ledger."""
    if not isinstance(event.get("type"), str) or not event["type"].strip():
        raise ValueError("event requires a non-empty type")
    previous_hash = events[-1]["hash"] if events else "GENESIS"
    body = {key: value for key, value in event.items() if key != "hash"}
    body["previous_hash"] = previous_hash
    body["hash"] = digest(body)
    return [*deepcopy(events), body]


def verify_audit_chain(events: list[dict[str, Any]]) -> list[str]:
    errors: list[str] = []
    previous_hash = "GENESIS"
    for index, event in enumerate(events):
        body = {key: value for key, value in event.items() if key != "hash"}
        if event.get("previous_hash") != previous_hash:
            errors.append(f"event {index} has an invalid previous hash")
        if event.get("hash") != digest(body):
            errors.append(f"event {index} hash does not match its contents")
        previous_hash = event.get("hash", "")
    return errors


def completion_status(*, deliverable: bool, verification_passed: bool, minister_final: str,
                      material_limitations: list[str], blocker: str | None = None,
                      high_risks: int = 0) -> str:
    """Enforce evidence, risk, and Minister gates for an outcome claim."""
    if blocker:
        return "BLOCKED"
    if minister_final in {"DEFER", "REJECT"}:
        return minister_final
    if not deliverable or not verification_passed:
        return "REWORK"
    if high_risks or material_limitations:
        return "PASS" if minister_final == "APPROVE WITH CONDITIONS" else "REWORK"
    return "PASS" if minister_final == "APPROVE" else "REWORK"


def validate_run(run: dict[str, Any]) -> list[str]:
    """Validate a complete host-mediated run record before it can be released."""
    errors: list[str] = []
    required = {"run_id", "composition", "request_framing", "minister", "routing", "handoffs", "components", "audit_events", "completion"}
    missing = sorted(required - set(run))
    if missing:
        return ["missing run fields: " + ", ".join(missing)]
    if run["composition"] != "EMULATED_HOST_MEDIATED":
        errors.append("composition must disclose EMULATED_HOST_MEDIATED")
    if not isinstance(run["request_framing"], dict) or not run["request_framing"].get("outcome"):
        errors.append("request framing must name the intended outcome")
    minister = run["minister"]
    if not isinstance(minister, dict) or not minister.get("initial_conditions") or not minister.get("final_judgment"):
        errors.append("Minister initial conditions and final judgment are required")
    routing = run["routing"]
    if not isinstance(routing, dict) or "MOA" not in routing.get("selected_agents", []):
        errors.append("routing must record MOA orchestration")
    if "Minister" not in routing.get("selected_agents", []):
        errors.append("routing must record mandatory Minister participation")
    for index, handoff in enumerate(run["handoffs"]):
        errors.extend(f"handoff {index}: {error}" for error in validate_handoff(handoff))
    names = {component.get("name") for component in run["components"] if isinstance(component, dict)}
    for expected in {"Scout", "Forge", "Audit", "Verification"}:
        if expected not in names:
            errors.append(f"missing component record: {expected}")
    for component in run["components"]:
        if component.get("status") not in ALL_STATES:
            errors.append(f"invalid component status: {component.get('name')}")
    errors.extend(verify_audit_chain(run["audit_events"]))
    expected = completion_status(
        deliverable=bool(run["completion"].get("deliverable")),
        verification_passed=bool(run["completion"].get("verification_passed")),
        minister_final=str(minister.get("final_judgment")),
        material_limitations=list(run["completion"].get("material_limitations", [])),
        blocker=run["completion"].get("blocker"),
        high_risks=int(run["completion"].get("high_risks", 0)),
    )
    if run["completion"].get("status") != expected:
        errors.append(f"completion status must be {expected}")
    return errors


def demo_run() -> dict[str, Any]:
    """Return a synthetic, inspectable full-flow contract demonstration."""
    constraints = ["No external action", "No credentials or paid services", "Host-mediated composition only"]
    handoffs = [
        {"OBJECTIVE": "Verify the current core architecture claims", "CONTEXT": "Minister requires evidence before implementation", "INPUTS": ["sanitised repository snapshot"], "CONSTRAINTS": constraints, "REQUIRED OUTPUT": "Provenance-aware evidence handoff", "ACCEPTANCE CRITERIA": ["freshness stated", "limitations stated"], "AUTHORITY": "Scout", "KNOWN RISKS": ["stale runtime state"], "WHAT NOT TO DO": ["make the final strategic judgment"]},
        {"OBJECTIVE": "Implement control-plane contract hardening", "CONTEXT": "Use Scout findings and Minister conditions", "INPUTS": ["verified architecture evidence", "Minister conditions"], "CONSTRAINTS": constraints, "REQUIRED OUTPUT": "Tested source and tests", "ACCEPTANCE CRITERIA": ["all control-plane tests pass", "no secret data"], "AUTHORITY": "Forge", "KNOWN RISKS": ["scope expansion"], "WHAT NOT TO DO": ["claim native plugin composition"]},
        {"OBJECTIVE": "Independently assess release claim", "CONTEXT": "Review evidence after Forge verification", "INPUTS": ["test results", "audit ledger"], "CONSTRAINTS": constraints, "REQUIRED OUTPUT": "Residual-risk report", "ACCEPTANCE CRITERIA": ["policy conformance checked", "limitations retained"], "AUTHORITY": "Audit", "KNOWN RISKS": ["confirmation bias"], "WHAT NOT TO DO": ["duplicate Scout research or Forge implementation"]},
    ]
    events: list[dict[str, Any]] = []
    for event_type in ("REQUEST_FRAMED", "MINISTER_CONDITIONS", "CAPABILITY_DISCOVERED", "SCOUT_HANDOFF", "FORGE_HANDOFF", "AUDIT_REVIEW", "CONFLICT_ARBITRATED", "VERIFIED", "MINISTER_FINAL", "COMPLETION_GOVERNED"):
        events = append_audit_event(events, {"type": event_type, "mode": "SYNTHETIC_DEMONSTRATION"})
    return {
        "run_id": "demo-core-control-plane-v1",
        "composition": "EMULATED_HOST_MEDIATED",
        "request_framing": {"outcome": "A safe, evidence-governed core release candidate", "non_goals": ["external product work", "external actions"]},
        "minister": {"initial_conditions": ["Preserve authority boundaries", "Do not claim native agent execution"], "final_judgment": "APPROVE WITH CONDITIONS"},
        "routing": {"selected_agents": ["MOA", "Minister", "Scout", "Forge"], "selected_shared_skills": ["skill-broker", "evidence-epistemics", "quality-assurance", "release-readiness"]},
        "handoffs": handoffs,
        "components": [{"name": name, "status": "PASS"} for name in ("Scout", "Forge", "Audit", "Verification")],
        "conflict_arbitration": {"dispute": "whether a passing test suite proves native composition", "authority": "MOA", "decision": "No, label composition EMULATED_HOST_MEDIATED"},
        "audit_events": events,
        "completion": {"deliverable": True, "verification_passed": True, "material_limitations": ["Native plugin-to-plugin process execution is unavailable"], "high_risks": 0, "status": "PASS"},
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Agentic Core control-plane validator")
    sub = parser.add_subparsers(dest="command", required=True)
    validate = sub.add_parser("validate-run")
    validate.add_argument("path", type=Path)
    demo = sub.add_parser("write-demo")
    demo.add_argument("path", type=Path)
    args = parser.parse_args(argv)
    if args.command == "write-demo":
        payload = demo_run()
        args.path.parent.mkdir(parents=True, exist_ok=True)
        args.path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        print(f"wrote {args.path}")
        return 0
    payload = json.loads(args.path.read_text(encoding="utf-8"))
    errors = validate_run(payload)
    if errors:
        print("FAIL")
        print("\n".join(errors))
        return 1
    print("PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
