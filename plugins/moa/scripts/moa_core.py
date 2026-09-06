#!/usr/bin/env python3
"""Deterministic baseline routing and diagnostics for MOA v0.1."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from copy import deepcopy
from pathlib import Path
from typing import Any


USER_HOME = Path.home()
AI_OS = USER_HOME / ".codex" / "ai-os"
AGENT_REGISTRY = AI_OS / "registry" / "agent-registry.json"
SKILL_REGISTRY = AI_OS / "registry" / "skill-registry.json"
PLUGIN_ROOT = Path(__file__).resolve().parents[1]
BROKER_CLI = AI_OS / "bin" / "aios_skills.py"


TASK_SIGNALS = {
    "FIX": ("fix", "repair", "bug", "typo", "broken", "debug"),
    "AUDIT": ("audit", "inspect", "review code", "security review"),
    "DESIGN": ("design", "wireframe", "prototype"),
    "LAUNCH": ("launch", "deploy", "publish", "release"),
    "EXPERIMENT": ("experiment", "a/b test", "hypothesis"),
    "RESEARCH": ("research", "find sources", "investigate", "discover"),
    "COMPARE": ("compare", "versus", " vs "),
    "DECIDE": ("should i", "worth", "choose", "decide", "what should"),
    "PLAN": ("plan", "roadmap", "strategy"),
    "BUILD": ("build", "create", "implement", "develop", "mvp", "application", "portfolio"),
    "ANALYSE": ("analyse", "analyze", "explain", "evaluate"),
}

CAPABILITY_SIGNALS = {
    "first-principles-analysis": ("overengineer", "kubernetes", "kafka", "microservices", "works", "assumption"),
    "evidence-quality-analysis": ("evidence", "research", "worth", "no users", "should i", "verify"),
    "systems-analysis": ("system", "complex", "dependencies", "long term"),
    "behavioral-analysis": ("six months", "sunk", "still can't choose", "procrast", "fear", "no users"),
    "comparative-decision-analysis": ("should i", "worth", "choose", "compare", "buy", "decision"),
    "strategic-foresight": ("long term", "career", "strategy", "future"),
    "incentive-analysis": ("negotiate", "stakeholder", "incentive", "competitor"),
    "premortem-analysis": ("risk", "launch", "major", "six months", "no users"),
    "adversarial-analysis": ("red team", "challenge", "six months", "no users", "high stakes"),
}


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def normalize_task(task: str) -> str:
    return re.sub(r"^\s*@?moa\b[:\s]*", "", task, flags=re.IGNORECASE).strip()


def classify_task(task: str) -> str:
    text = f" {normalize_task(task).lower()} "
    matched = []
    for task_type, signals in TASK_SIGNALS.items():
        if any(signal in text for signal in signals):
            matched.append(task_type)
    decision_types = {"DECIDE", "COMPARE", "PLAN", "ANALYSE"}
    execution_types = {"BUILD", "FIX", "AUDIT", "DESIGN", "LAUNCH", "EXPERIMENT"}
    if decision_types.intersection(matched) and execution_types.intersection(matched):
        return "MIXED"
    if "RESEARCH" in matched and execution_types.intersection(matched):
        return "MIXED"
    for preferred in ("FIX", "AUDIT", "LAUNCH", "EXPERIMENT", "RESEARCH", "COMPARE", "DECIDE", "PLAN", "DESIGN", "BUILD", "ANALYSE"):
        if preferred in matched:
            return preferred
    return "ANALYSE"


def minister_level(task: str, task_type: str) -> tuple[str, str]:
    text = normalize_task(task).lower()
    critical = ("immigration", "visa", "skilled worker", "legal", "life-changing", "irreversible", "bankruptcy")
    deep = ("six months", "no users", "career", "major financial", "£1,500", "1500", "sunk cost", "high stakes")
    light = ("typo", "one-line", "tiny", "small css", "rename variable")
    if any(item in text for item in critical):
        return "CRITICAL", "CRITICAL"
    if any(item in text for item in deep):
        return "DEEP", "COUNCIL"
    if any(item in text for item in light):
        return "LIGHT", "LIGHT"
    if task_type in {"BUILD", "FIX", "DESIGN"} and not any(item in text for item in ("complex", "production", "full platform")):
        return "LIGHT", "LIGHT"
    return "STANDARD", "STANDARD"


def validate_agent_registry(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    agents = data.get("agents")
    if not isinstance(agents, list):
        return ["agents must be an array"]
    ids: set[str] = set()
    required = {
        "id", "name", "type", "description", "capabilities", "triggers", "scope",
        "status", "enabled", "installed", "authority", "dependencies", "requires_minister",
        "supports_parallel", "cost_profile", "risk_profile", "trust_level", "version",
        "source", "notes", "last_validated",
    }
    for index, agent in enumerate(agents):
        missing = required.difference(agent)
        if missing:
            errors.append(f"agent[{index}] missing: {', '.join(sorted(missing))}")
            continue
        if agent["id"] in ids:
            errors.append(f"duplicate agent id: {agent['id']}")
        ids.add(agent["id"])
        path = Path(agent["source"]["path"])
        if agent["installed"] and not path.exists():
            errors.append(f"installed agent path missing: {agent['id']}")
        if agent["status"] == "AVAILABLE" and not agent["enabled"]:
            errors.append(f"available agent is disabled: {agent['id']}")
        if agent["status"] == "NOT_INSTALLED" and agent["installed"]:
            errors.append(f"not-installed agent marked installed: {agent['id']}")
    for core in ("minister", "forge", "moa"):
        if core not in ids:
            errors.append(f"missing core agent: {core}")
    return errors


def selectable_agents(data: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        agent for agent in data["agents"]
        if agent["enabled"] and agent["installed"] and agent["status"] == "AVAILABLE"
    ]


def select_skills(task: str, skill_registry: dict[str, Any]) -> dict[str, Any]:
    text = normalize_task(task).lower()
    capabilities = [capability for capability, signals in CAPABILITY_SIGNALS.items() if any(signal in text for signal in signals)]
    if classify_task(task) in {"DECIDE", "COMPARE", "MIXED"} and "comparative-decision-analysis" not in capabilities:
        capabilities.append("comparative-decision-analysis")
    command = [sys.executable, "-B", str(BROKER_CLI), "broker", "--task", normalize_task(task)]
    for capability in capabilities:
        command.extend(["--capability", capability])
    try:
        result = subprocess.run(command, capture_output=True, text=True, timeout=30, check=False)
        if result.returncode != 0:
            return {"status": "BLOCKED", "selected": [], "missing_capabilities": capabilities, "required_capabilities": capabilities}
        payload = json.loads(result.stdout)
        selected = [item["id"] for item in payload.get("selected", [])]
        available = {
            item["id"] for item in skill_registry.get("skills", [])
            if item.get("enabled") and item.get("installed") and item.get("status") == "AVAILABLE"
        }
        return {
            "status": "PASS",
            "selected": [item for item in selected if item in available][:8],
            "missing_capabilities": payload.get("missing_capabilities", []),
            "required_capabilities": payload.get("required_capabilities", capabilities),
        }
    except (OSError, subprocess.SubprocessError, json.JSONDecodeError):
        return {"status": "BLOCKED", "selected": [], "missing_capabilities": capabilities, "required_capabilities": capabilities}


def find_agent_for_capability(agents: list[dict[str, Any]], capability: str) -> dict[str, Any] | None:
    candidates = [agent for agent in agents if capability in agent.get("capabilities", []) and agent["id"] not in {"moa", "minister"}]
    candidates.sort(key=lambda item: (item["type"] == "build-agent", item["id"]))
    return candidates[0] if candidates else None


def make_node(node_id: str, task: str, agent: str, skills: list[str], dependencies: list[str], parallelizable: bool, output: str, verification: str) -> dict[str, Any]:
    return {
        "id": node_id,
        "task": task,
        "assigned_agent": agent,
        "required_skills": skills,
        "inputs": ["framed user request"],
        "dependencies": dependencies,
        "parallelizable": parallelizable,
        "expected_output": output,
        "verification_requirement": verification,
        "status": "PENDING",
    }


def execution_graph(task_type: str, selected_agents: list[str], skills: list[str], conditional_build: bool = False) -> list[dict[str, Any]]:
    graph = [make_node("minister-initial", "Judge direction before execution", "Minister", skills, [], False, "initial verdict and conditions", "Minister verdict present")]
    previous = "minister-initial"
    if "Scout" in selected_agents:
        graph.append(make_node("scout-research", "Investigate material claims and produce a source-verified evidence pack", "Scout", skills, [previous], True, "traceable evidence pack with freshness, contradictions, and unknowns", "Scout completion gate passes or reports an explicit limitation"))
        previous = "scout-research"
    if "Forge" in selected_agents:
        build_task = "Implement within Minister conditions"
        if conditional_build:
            build_task = "Implement only if Minister initial verdict approves building"
        graph.append(make_node("forge-execution", build_task, "Forge", skills, [previous], False, "verified engineering deliverable", "Forge verification gate passes"))
        graph.append(make_node("verification", "Verify acceptance criteria", "Verification", [], ["forge-execution"], False, "current test evidence", "required checks pass"))
        previous = "verification"
    graph.append(make_node("minister-final", "Judge outcome fit and unresolved risk", "Minister", skills, [previous], False, "APPROVE, conditions, REWORK, REJECT, or DEFER", "material limitations are not blindly approved"))
    graph.append(make_node("completion", "Determine whether user outcome is achieved", "MOA", [], ["minister-final"], False, "completion status and evidence", "completion contract satisfied"))
    return graph


def handoff(objective: str, agent: str, constraints: list[str], output: str, criteria: list[str]) -> dict[str, Any]:
    return {
        "OBJECTIVE": objective,
        "CONTEXT": "Bounded MOA execution node",
        "INPUTS": ["framed task", "upstream verified outputs"],
        "CONSTRAINTS": constraints,
        "REQUIRED OUTPUT": output,
        "ACCEPTANCE CRITERIA": criteria,
        "AUTHORITY": agent,
        "KNOWN RISKS": ["scope drift", "unverified completion"],
        "WHAT NOT TO DO": ["expand scope silently", "ignore Minister conditions", "claim unsupported success"],
    }


def route_task(task: str, agent_data: dict[str, Any] | None = None, skill_data: dict[str, Any] | None = None) -> dict[str, Any]:
    agent_data = deepcopy(agent_data) if agent_data is not None else load_json(AGENT_REGISTRY)
    skill_data = deepcopy(skill_data) if skill_data is not None else load_json(SKILL_REGISTRY)
    errors = validate_agent_registry(agent_data)
    if errors:
        raise ValueError("Invalid Agent Registry: " + "; ".join(errors))
    normalized = normalize_task(task)
    task_type = classify_task(normalized)
    level, runtime_level = minister_level(normalized, task_type)
    agents = selectable_agents(agent_data)
    selected_agents = ["Minister"]
    missing: list[str] = []
    conditions: list[str] = []
    broker = select_skills(normalized, skill_data)
    skills = broker["selected"]
    text = normalized.lower()

    conditional_build = task_type == "MIXED" and any(word in text for word in ("worth", "if yes", "if it is"))
    research_needed = task_type == "RESEARCH" or (
        task_type == "MIXED" and any(signal in text for signal in ("research", "investigate", "verify", "find sources", "current evidence", "current framework"))
    )
    if research_needed:
        research_agent = find_agent_for_capability(agents, "research")
        if research_agent:
            selected_agents.append(research_agent["name"])
        else:
            missing.append("dedicated research agent")

    implementation_types = {"BUILD", "FIX", "AUDIT", "DESIGN", "LAUNCH", "MIXED"}
    if task_type in implementation_types:
        forge = next((agent for agent in agents if agent["id"] == "forge"), None)
        if forge:
            selected_agents.append("Forge")
        else:
            missing.append("software-implementation agent")

    specialized = ("wet-lab", "genomic sequencing", "clinical procedure", "licensed structural engineering")
    if any(signal in text for signal in specialized):
        missing.append("specialized real-world execution agent")

    if any(signal in text for signal in ("kubernetes", "kafka", "microservices")) and any(signal in text for signal in ("tiny", "small", "portfolio")):
        conditions.append("Challenge unnecessary infrastructure and pass a simplified architecture to Forge")

    selected_agents = list(dict.fromkeys(selected_agents))
    missing.extend(broker["missing_capabilities"])
    return {
        "task": normalized,
        "task_type": task_type,
        "minister_participation": level,
        "minister_runtime_mode": runtime_level,
        "selected_agents": selected_agents,
        "selected_shared_skills": skills,
        "skill_broker_status": broker["status"],
        "required_shared_capabilities": broker["required_capabilities"],
        "conditions": conditions,
        "missing_capabilities": list(dict.fromkeys(missing)),
        "execution_graph": execution_graph(task_type, selected_agents, skills, conditional_build),
        "handoffs": [handoff(normalized, agent, conditions, "bounded result", ["acceptance criteria met", "verification evidence supplied"]) for agent in selected_agents],
        "direct_plugin_to_plugin_orchestration": "EMULATED",
        "routing_note": "Installed skills are composed in the current Codex task; separate plugin process invocation is unavailable.",
    }


def arbitrate(dispute_type: str) -> str:
    mapping = {
        "strategy": "Minister",
        "implementation": "Forge Integrator",
        "evidence": "Scout",
        "scope": "MOA",
        "orchestration": "MOA",
    }
    return mapping.get(dispute_type.lower(), "MOA frames the dispute, then assigns domain authority")


def completion_governance(*, deliverable: bool, tests_passed: bool, minister_final: str, material_limitation: bool, high_issues: int = 0) -> str:
    if minister_final == "REJECT":
        return "REJECT"
    if minister_final == "DEFER":
        return "DEFER"
    if material_limitation or high_issues:
        return "REWORK" if not deliverable or not tests_passed else "APPROVE WITH CONDITIONS"
    if not deliverable or not tests_passed or minister_final not in {"APPROVE", "APPROVE WITH CONDITIONS"}:
        return "REWORK"
    return "OUTCOME ACHIEVED" if minister_final == "APPROVE" else "EXECUTED WITH CONDITIONS"


def find_desktop_codex() -> Path | None:
    root = USER_HOME / "AppData" / "Local" / "OpenAI" / "Codex" / "bin"
    candidates = sorted(root.glob("*/codex.exe"), key=lambda item: item.stat().st_mtime, reverse=True) if root.exists() else []
    return candidates[0] if candidates else None


def native_plugin_list() -> dict[str, Any]:
    executable = find_desktop_codex()
    if not executable:
        return {"status": "BLOCKED", "reason": "desktop Codex runtime not found"}
    result = subprocess.run([str(executable), "plugin", "list"], capture_output=True, text=True, timeout=30, check=False)
    output = (result.stdout + result.stderr).strip()
    installed = [line.split("@")[0].strip() for line in output.splitlines() if "installed, enabled" in line and "@" in line]
    detection = "codex-plugin-list"
    if result.returncode == 0 and not installed:
        cache_root = USER_HOME / ".codex" / "plugins" / "cache"
        cached = []
        if cache_root.exists():
            for marketplace in cache_root.iterdir():
                if not marketplace.is_dir() or marketplace.name.startswith("."):
                    continue
                for plugin in marketplace.iterdir():
                    if plugin.is_dir() and any(child.is_dir() for child in plugin.iterdir()):
                        cached.append(plugin.name)
        installed = sorted(set(cached))
        detection = "installed-cache-fallback"
    return {
        "status": "SUPPORTED" if result.returncode == 0 else "BLOCKED",
        "executable": str(executable),
        "installed_plugins": installed,
        "detection": detection,
        "raw_exit": result.returncode,
    }


def health() -> dict[str, Any]:
    checks: dict[str, bool] = {
        "moa_source": (PLUGIN_ROOT / ".codex-plugin" / "plugin.json").exists(),
        "minister_source": (USER_HOME / "plugins" / "minister" / ".codex-plugin" / "plugin.json").exists(),
        "forge_source": (USER_HOME / "plugins" / "forge" / ".codex-plugin" / "plugin.json").exists(),
        "agent_registry": AGENT_REGISTRY.exists(),
        "skill_registry": SKILL_REGISTRY.exists(),
        "skill_broker": (USER_HOME / ".codex" / "skills" / "skill-broker" / "SKILL.md").exists(),
    }
    errors = validate_agent_registry(load_json(AGENT_REGISTRY)) if checks["agent_registry"] else ["agent registry missing"]
    native = native_plugin_list()
    discovered = set(native.get("installed_plugins", []))
    checks["installed_state_consistent"] = native.get("status") == "SUPPORTED" and {"moa", "minister", "forge"}.issubset(discovered)
    return {
        "status": "PASS" if all(checks.values()) and not errors else "FAIL",
        "checks": checks,
        "registry_errors": errors,
        "native_discovery": native["status"],
        "direct_plugin_to_plugin_orchestration": "EMULATED",
    }


def command_agents(discover: bool) -> dict[str, Any]:
    data = load_json(AGENT_REGISTRY)
    result = {
        "registry_version": data["registry_version"],
        "active_agents": [
            {"id": item["id"], "name": item["name"], "type": item["type"], "version": item["version"], "capabilities": item["capabilities"]}
            for item in selectable_agents(data)
        ],
        "inactive_agents": [
            {"id": item["id"], "status": item["status"], "installed": item["installed"]}
            for item in data["agents"] if item not in selectable_agents(data)
        ],
    }
    if discover:
        result["native_plugin_discovery"] = native_plugin_list()
    return result


def command_skills() -> dict[str, Any]:
    data = load_json(SKILL_REGISTRY)
    active = [item for item in data.get("skills", []) if item.get("enabled") and item.get("installed") and item.get("status") == "AVAILABLE"]
    return {
        "broker": "PASS" if any(item["id"] == "skill-broker" for item in active) else "FAIL",
        "registry_version": data.get("registry_version"),
        "active_count": len(active),
        "skills": [item["id"] for item in active],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="MOA routing and diagnostics")
    sub = parser.add_subparsers(dest="command", required=True)
    route_parser = sub.add_parser("route")
    route_parser.add_argument("task")
    agents_parser = sub.add_parser("agents")
    agents_parser.add_argument("--discover", action="store_true")
    sub.add_parser("skills")
    sub.add_parser("health")
    explain = sub.add_parser("explain-routing")
    explain.add_argument("task")
    args = parser.parse_args(argv)

    if args.command in {"route", "explain-routing"}:
        payload = route_task(args.task)
    elif args.command == "agents":
        payload = command_agents(args.discover)
    elif args.command == "skills":
        payload = command_skills()
    else:
        payload = health()
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 0 if payload.get("status") != "FAIL" else 1


if __name__ == "__main__":
    sys.exit(main())
