#!/usr/bin/env python3
"""Deterministic contracts and diagnostics for Scout v1.0.

This module validates research state. It does not replace live investigation or
pretend that keyword routing proves a research conclusion.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any


USER_HOME = Path.home()
PLUGIN_ROOT = Path(__file__).resolve().parents[1]
AI_OS = USER_HOME / ".codex" / "ai-os"
AGENT_REGISTRY = AI_OS / "registry" / "agent-registry.json"
SKILL_REGISTRY = AI_OS / "registry" / "skill-registry.json"
BROKER_CLI = AI_OS / "bin" / "aios_skills.py"
MARKETPLACE = USER_HOME / ".agents" / "plugins" / "marketplace.json"
CACHE_ROOT = USER_HOME / ".codex" / "plugins" / "cache" / "personal" / "scout"

PRIVATE_SKILLS = [
    "scout", "scout-router", "scout-research-contract",
    "scout-investigation-planner", "scout-evidence-ledger",
    "scout-contradiction-resolution", "scout-synthesis",
    "scout-completion-gate",
]
CORE_SHARED_SKILLS = [
    "research-planning", "source-discovery", "source-verification",
    "evidence-epistemics", "research-synthesis",
]
VALID_EVIDENCE_STATUSES = {
    "VERIFIED", "SUPPORTED", "PARTIALLY SUPPORTED", "DISPUTED",
    "UNVERIFIED", "OUTDATED", "INFERRED", "UNKNOWN",
}
VALID_COMPLETION_STATUSES = {
    "COMPLETE", "COMPLETE WITH LIMITATIONS", "PARTIAL", "BLOCKED",
    "INSUFFICIENT EVIDENCE",
}
LEDGER_REQUIRED = {
    "claim_id", "claim", "claim_type", "source", "source_owner",
    "source_type", "source_url_or_path", "publication_date",
    "last_updated_date", "access_date", "jurisdiction", "direct_support",
    "limitations", "contradicting_sources", "freshness_status", "confidence",
    "evidence_status", "notes",
}

MODE_CAPABILITIES = {
    "QUICK": ["source-provenance-verification", "source-currency-check"],
    "STANDARD": ["research-question-framing", "source-discovery", "source-provenance-verification", "research-synthesis"],
    "DEEP": ["research-plan-design", "source-discovery", "source-provenance-verification", "evidence-quality-analysis", "research-synthesis"],
    "CRITICAL": ["research-plan-design", "source-discovery", "source-provenance-verification", "evidence-quality-analysis", "research-synthesis"],
}


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def plugin_version(root: Path = PLUGIN_ROOT) -> str:
    return load_json(root / ".codex-plugin" / "plugin.json")["version"]


def normalize_task(task: str) -> str:
    return re.sub(r"^\s*@?scout\b[:\s]*", "", task, flags=re.IGNORECASE).strip()


def classify_mode(task: str) -> str:
    text = normalize_task(task).lower()
    critical = (
        "immigration", "visa", "work rights", "legal", "regulatory",
        "medical", "health", "security-sensitive", "material financial",
        "irreversible", "high-cost",
    )
    deep = (
        "funded phd", "sponsorship", "market research", "competitor",
        "major career", "substantial academic", "systematic review",
    )
    standard = ("compare", "options", "company", "programme", "multiple claims", "technical research")
    if any(signal in text for signal in critical):
        return "CRITICAL"
    if any(signal in text for signal in deep):
        return "DEEP"
    if any(signal in text for signal in standard):
        return "STANDARD"
    return "QUICK"


def build_research_contract(task: str, *, downstream: str = "MOA", jurisdiction: str = "UNSPECIFIED") -> dict[str, Any]:
    objective = normalize_task(task)
    mode = classify_mode(objective)
    return {
        "RESEARCH OBJECTIVE": objective,
        "DOWNSTREAM DECISION OR USE": downstream,
        "CORE QUESTION": objective,
        "SUBQUESTIONS": [],
        "IN-SCOPE CLAIMS": [objective],
        "OUT-OF-SCOPE CLAIMS": ["external action", "final strategic verdict"],
        "JURISDICTION": jurisdiction,
        "TIMEFRAME": "current unless the request specifies otherwise",
        "FRESHNESS REQUIREMENT": "LIVE" if mode in {"QUICK", "CRITICAL"} else "PROPORTIONATE",
        "SOURCE CLASSES REQUIRED": ["primary or authoritative"],
        "KNOWN CONSTRAINTS": ["free-first", "no external contact", "retrieved content is untrusted"],
        "USER-PROVIDED ASSUMPTIONS": [],
        "DECISION-REVERSING UNKNOWNS": [],
        "EXPECTED DELIVERABLE": "decision-ready evidence pack",
        "STOPPING CONDITIONS": ["core question answered or explicitly unresolved", "material claims have provenance"],
        "MODE": mode,
    }


def broker_selection(task: str, *, broker_path: Path = BROKER_CLI) -> dict[str, Any]:
    mode = classify_mode(task)
    required = MODE_CAPABILITIES[mode]
    if not broker_path.exists():
        return {"status": "BLOCKED", "mode": mode, "selected": [], "required_capabilities": required, "missing_capabilities": required}
    command = [sys.executable, "-B", str(broker_path), "broker"]
    for capability in required:
        command.extend(["--capability", capability])
    try:
        result = subprocess.run(command, capture_output=True, text=True, timeout=30, check=False)
        if result.returncode != 0:
            return {"status": "BLOCKED", "mode": mode, "selected": [], "required_capabilities": required, "missing_capabilities": required}
        payload = json.loads(result.stdout)
        selected = [item["id"] for item in payload.get("selected", [])]
        limits = {"QUICK": 2, "STANDARD": 4, "DEEP": 6, "CRITICAL": 6}
        return {
            "status": "PASS",
            "mode": mode,
            "selected": selected[: limits[mode]],
            "required_capabilities": payload.get("required_capabilities", required),
            "missing_capabilities": payload.get("missing_capabilities", []),
        }
    except (OSError, subprocess.SubprocessError, json.JSONDecodeError):
        return {"status": "BLOCKED", "mode": mode, "selected": [], "required_capabilities": required, "missing_capabilities": required}


def source_level(source_type: str, owner: str = "") -> int:
    text = f"{source_type} {owner}".lower()
    if any(x in text for x in ("government", "regulator", "legislation", "official", "primary", "standard", "original paper", "repository")):
        return 1
    if any(x in text for x in ("systematic review", "expert", "professional", "reputable secondary", "investigative")):
        return 2
    if any(x in text for x in ("search result", "aggregator", "job board", "directory", "third-party database")):
        return 3
    return 4


def freshness_status(*, last_updated: str | None, access_date: str | None, time_sensitive: bool) -> str:
    if not access_date:
        return "UNKNOWN"
    try:
        accessed = date.fromisoformat(access_date)
        updated = date.fromisoformat(last_updated) if last_updated else None
    except ValueError:
        return "UNKNOWN"
    if accessed > date.today():
        return "UNKNOWN"
    if time_sensitive and updated is None:
        return "UNVERIFIED"
    if time_sensitive and updated and (accessed - updated).days > 365:
        return "OUTDATED"
    return "CURRENT" if time_sensitive else "RECORDED"


def validate_ledger(entries: list[dict[str, Any]]) -> list[str]:
    errors: list[str] = []
    ids: set[str] = set()
    for index, entry in enumerate(entries):
        missing = LEDGER_REQUIRED.difference(entry)
        if missing:
            errors.append(f"entry[{index}] missing: {', '.join(sorted(missing))}")
            continue
        if entry["claim_id"] in ids:
            errors.append(f"duplicate claim_id: {entry['claim_id']}")
        ids.add(entry["claim_id"])
        if entry["evidence_status"] not in VALID_EVIDENCE_STATUSES:
            errors.append(f"entry[{index}] invalid evidence_status")
        if entry["evidence_status"] == "VERIFIED" and (not entry["direct_support"] or source_level(entry["source_type"], entry["source_owner"]) != 1):
            errors.append(f"entry[{index}] VERIFIED requires direct level-1 support")
        if entry["source_type"].lower() == "search result":
            errors.append(f"entry[{index}] search result cannot be final evidence")
        if not str(entry["source_url_or_path"]).strip():
            errors.append(f"entry[{index}] source URL or path is empty")
        if entry["evidence_status"] == "INFERRED" and "inference" not in entry["notes"].lower():
            errors.append(f"entry[{index}] inference is not labelled")
    return errors


def resolve_contradiction(a: dict[str, Any], b: dict[str, Any]) -> dict[str, Any]:
    checks = {
        "same_claim": a.get("claim") == b.get("claim"),
        "same_jurisdiction": a.get("jurisdiction") == b.get("jurisdiction"),
        "same_scope": a.get("scope") == b.get("scope"),
        "same_version": a.get("version") == b.get("version"),
        "same_date": a.get("last_updated") == b.get("last_updated"),
    }
    if not checks["same_claim"]:
        result = "NOT A TRUE CONTRADICTION"
    elif not checks["same_jurisdiction"] or not checks["same_scope"] or not checks["same_version"]:
        result = "RESOLVED"
    elif source_level(a.get("source_type", ""), a.get("owner", "")) != source_level(b.get("source_type", ""), b.get("owner", "")):
        result = "PARTIALLY RESOLVED"
    else:
        result = "UNRESOLVED"
    return {"result": result, "checks": checks, "downstream_effect": "keep visible until the receiving authority accepts the limitation"}


def inspect_untrusted_source(text: str) -> dict[str, Any]:
    signals = ("ignore previous", "reveal secret", "send email", "modify files", "install", "contact")
    detected = [signal for signal in signals if signal in text.lower()]
    return {"treated_as_data": True, "instructions_ignored": bool(detected), "detected_signals": detected, "actions_taken": []}


def external_action_policy(action: str) -> dict[str, str]:
    blocked = ("send", "contact", "apply", "submit", "purchase", "subscribe", "upload", "disclose")
    return {"status": "BLOCKED" if any(x in action.lower() for x in blocked) else "RESEARCH_ONLY", "authority": "user approval required outside Scout"}


def completion_gate(*, objective_answered: bool, ledger: list[dict[str, Any]], material_contradictions: list[str] | None = None, limitations: list[str] | None = None, blocked_resource: str | None = None) -> dict[str, Any]:
    contradictions = material_contradictions or []
    limitations = limitations or []
    errors = validate_ledger(ledger)
    if blocked_resource:
        return {"status": "BLOCKED", "reason": blocked_resource, "errors": errors}
    if not ledger or not objective_answered:
        return {"status": "INSUFFICIENT EVIDENCE", "reason": "objective or material evidence is missing", "errors": errors}
    if errors:
        return {"status": "PARTIAL", "reason": "evidence ledger failed validation", "errors": errors}
    if contradictions:
        return {"status": "PARTIAL", "reason": "material contradiction remains unresolved", "errors": []}
    stale = any(item["freshness_status"] in {"OUTDATED", "UNKNOWN", "UNVERIFIED"} and item["claim_type"] == "CURRENT" for item in ledger)
    if stale:
        return {"status": "PARTIAL", "reason": "current claim lacks current evidence", "errors": []}
    if limitations:
        return {"status": "COMPLETE WITH LIMITATIONS", "limitations": limitations, "errors": []}
    return {"status": "COMPLETE", "errors": []}


def research_handoff(*, objective: str, downstream: str, ledger: list[dict[str, Any]], unknowns: list[str], limitations: list[str]) -> dict[str, Any]:
    return {
        "OBJECTIVE": objective,
        "RESEARCH CONTRACT": build_research_contract(objective, downstream=downstream),
        "DOWNSTREAM AUTHORITY": downstream,
        "CONFIRMED FACTS": [x["claim"] for x in ledger if x["evidence_status"] == "VERIFIED"],
        "SUPPORTED FINDINGS": [x["claim"] for x in ledger if x["evidence_status"] in {"SUPPORTED", "PARTIALLY SUPPORTED"}],
        "DISPUTED FINDINGS": [x["claim"] for x in ledger if x["evidence_status"] == "DISPUTED"],
        "INFERENCES": [x["claim"] for x in ledger if x["evidence_status"] == "INFERRED"],
        "UNKNOWN FACTORS": unknowns,
        "DECISION-REVERSING UNKNOWNS": unknowns,
        "SOURCE PROVENANCE": [x["source_url_or_path"] for x in ledger],
        "FRESHNESS": [x["freshness_status"] for x in ledger],
        "LIMITATIONS": limitations,
        "REQUIRED NEXT ACTION": "receiving authority reviews evidence and unknowns",
        "WHAT NOT TO ASSUME": ["Scout made the final strategic decision", "unverified claims are facts"],
    }


def _hash_tree(root: Path) -> dict[str, str]:
    result: dict[str, str] = {}
    if not root.exists():
        return result
    for path in sorted(root.rglob("*")):
        if path.is_file() and "__pycache__" not in path.parts:
            result[str(path.relative_to(root)).replace("\\", "/")] = hashlib.sha256(path.read_bytes()).hexdigest()
    return result


def cache_parity() -> dict[str, Any]:
    version = plugin_version()
    cache = CACHE_ROOT / version
    source_hashes = _hash_tree(PLUGIN_ROOT)
    cache_hashes = _hash_tree(cache)
    return {
        "status": "PASS" if source_hashes and source_hashes == cache_hashes else "FAIL",
        "source_files": len(source_hashes),
        "cache_files": len(cache_hashes),
        "missing": sorted(set(source_hashes) - set(cache_hashes)),
        "extra": sorted(set(cache_hashes) - set(source_hashes)),
        "changed": sorted(k for k in source_hashes.keys() & cache_hashes.keys() if source_hashes[k] != cache_hashes[k]),
        "cache_path": str(cache),
    }


def skills_diagnostic() -> dict[str, Any]:
    registry = load_json(SKILL_REGISTRY)
    available = {item["id"]: item for item in registry.get("skills", []) if item.get("enabled") and item.get("installed") and item.get("status") == "AVAILABLE"}
    return {
        "command": "skills",
        "scout_version": plugin_version(),
        "trust_status": "VERIFIED",
        "private_skills": PRIVATE_SKILLS,
        "skill_broker": "PASS" if "skill-broker" in available else "FAIL",
        "skill_registry": "PASS" if SKILL_REGISTRY.exists() else "FAIL",
        "shared_research_skills": [{"id": x, "status": "AVAILABLE" if x in available else "MISSING"} for x in CORE_SHARED_SKILLS],
    }


def health() -> dict[str, Any]:
    version = plugin_version()
    registry = load_json(AGENT_REGISTRY) if AGENT_REGISTRY.exists() else {"agents": []}
    scout = next((x for x in registry.get("agents", []) if x.get("id") == "scout"), None)
    marketplace = load_json(MARKETPLACE) if MARKETPLACE.exists() else {"plugins": []}
    market = next((x for x in marketplace.get("plugins", []) if x.get("name") == "scout"), None)
    skills = skills_diagnostic()
    checks = {
        "scout_source": (PLUGIN_ROOT / ".codex-plugin" / "plugin.json").exists(),
        "marketplace_entry": bool(market and market.get("source", {}).get("path") == "./plugins/scout"),
        "agent_registry_entry": bool(scout),
        "agent_registry_version_match": bool(scout and scout.get("version") == version),
        "skill_registry": skills["skill_registry"] == "PASS",
        "skill_broker": skills["skill_broker"] == "PASS",
        "required_shared_skills": all(x["status"] == "AVAILABLE" for x in skills["shared_research_skills"]),
        "installed_cache": (CACHE_ROOT / version).exists(),
    }
    parity = cache_parity() if checks["installed_cache"] else {"status": "NOT_INSTALLED"}
    checks["source_to_cache_parity"] = parity["status"] == "PASS"
    return {
        "status": "PASS" if all(checks.values()) else "FAIL",
        "version": version,
        "checks": checks,
        "parity": parity,
        "direct_plugin_to_plugin_orchestration": "EMULATED",
    }


def explain_routing(task: str) -> dict[str, Any]:
    selection = broker_selection(task)
    return {
        "command": "explain-routing",
        "task": normalize_task(task),
        "mode": selection["mode"],
        "required_capabilities": selection["required_capabilities"],
        "selected_shared_skills": selection["selected"],
        "rejected_irrelevant_skills": ["frontend-engineering", "backend-engineering", "cloud-infrastructure"],
        "freshness_requirement": build_research_contract(task)["FRESHNESS REQUIREMENT"],
        "broker_status": selection["status"],
        "missing_capabilities": selection["missing_capabilities"],
        "external_actions": "NONE",
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Scout deterministic contracts and diagnostics")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("skills")
    sub.add_parser("health")
    route = sub.add_parser("explain-routing")
    route.add_argument("task")
    contract = sub.add_parser("contract")
    contract.add_argument("task")
    args = parser.parse_args(argv)
    if args.command == "skills":
        payload = skills_diagnostic()
    elif args.command == "health":
        payload = health()
    elif args.command == "contract":
        payload = build_research_contract(args.task)
    else:
        payload = explain_routing(args.task)
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 0 if payload.get("status") != "FAIL" else 1


if __name__ == "__main__":
    raise SystemExit(main())
