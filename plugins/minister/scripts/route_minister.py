#!/usr/bin/env python3
"""Deterministic Minister router backed by the Personal AI OS Skill Broker."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any


DEFAULT_BROKER = Path.home() / ".codex" / "ai-os" / "bin" / "aios_skills.py"
DEFAULT_REGISTRY = Path.home() / ".codex" / "ai-os" / "registry" / "skill-registry.json"


def required_capabilities(text: str, mode: str) -> list[str]:
    required: list[str] = []

    def add(capability: str, pattern: str) -> None:
        if re.search(pattern, text):
            required.append(capability)

    add("comparative-decision-analysis", r"\b(should|choose|which|decision|decide|buy|spend|accept|continue|option|offer|proceed)\b")
    add("behavioral-analysis", r"\b(sunk|already spent|six months|current .{0,20} works|bias|pressure|fear|overconfiden|indecis|procrastinat|negotiate|losing it)\b")
    add("evidence-quality-analysis", r"\b(evidence|unknown|uncertain|not sure|do not know|don't know|definitely|claim|verify|research|support(?:s|ed)?)\b")
    add("strategic-foresight", r"\b(job|career|move country|relocat|offer|negotiate|saas|business|long[- ]term|future|university|education)\b")
    add("systems-analysis", r"\b(move country|immigration|major life|system dependencies|architecture proposal|auth.{0,80}billing|career path)\b")
    add("incentive-analysis", r"\b(negotiate|compensation|offer|employer|recruiter|manager|university|bargain|counter[- ]?offer)\b")
    add("premortem-analysis", r"(?:£|\$|€)\s?[\d,]{4,}|\b(risk|riskier|leave (?:my )?job|move country|negotiate|saas|major|irreversible|high stakes|proceed)\b")
    add("adversarial-analysis", r"\b(sunk|little evidence|saas|forge|proposal|plan|proceed|major|critical|red team)\b")
    add("first-principles-analysis", r"\b(leave (?:my )?job|move country|saas|forge architecture|overengineer|fundamental|major life)\b")

    if mode == "CRITICAL":
        required.extend([
            "first-principles-analysis", "comparative-decision-analysis", "behavioral-analysis",
            "strategic-foresight", "systems-analysis", "evidence-quality-analysis",
            "incentive-analysis", "premortem-analysis", "adversarial-analysis",
        ])

    limits = {"LIGHT": 3, "STANDARD": 6, "COUNCIL": 9, "CRITICAL": 20}
    return list(dict.fromkeys(required))[: limits[mode]]


def choose_mode(text: str) -> str:
    if re.search(r"\b(leave (?:my )?job.{0,30}move country|immigration|skilled worker|sponsorship|major life|hard to reverse|irreversible)\b", text):
        return "CRITICAL"
    if re.search(r"\b(stable job|pays? \d+% more|negotiate|compensation|saas|business idea|forge|architecture proposal|materially riskier)\b", text):
        return "COUNCIL"
    if re.search(r"(?:£|\$|€)\s?[\d,]{4,}|\b(sunk|already spent|six months|career|offer|purchase|laptop)\b", text):
        return "STANDARD"
    if len(text.split()) <= 16 or re.search(r"\b(trivial|reversible|lunch|accessory|under £?100)\b", text):
        return "LIGHT"
    return "STANDARD"


def run_broker(prompt: str, capabilities: list[str], broker_script: Path, registry_path: Path) -> dict[str, Any]:
    if not broker_script.is_file() or not registry_path.is_file():
        missing = capabilities
        target = broker_script if not broker_script.is_file() else registry_path
        return {"status": "UNAVAILABLE", "used": False, "selected": [], "missing": missing, "error": f"unavailable: {target}"}
    command = [sys.executable, str(broker_script), "--registry", str(registry_path), "broker", "--task", prompt]
    for capability in capabilities:
        command.extend(["--capability", capability])
    try:
        result = subprocess.run(command, capture_output=True, text=True, timeout=15, check=False)
    except (OSError, subprocess.SubprocessError) as exc:
        return {"status": "UNAVAILABLE", "used": False, "selected": [], "missing": capabilities, "error": str(exc)}
    if result.returncode != 0:
        return {"status": "INVALID", "used": False, "selected": [], "missing": capabilities, "error": result.stderr.strip() or result.stdout.strip()}
    try:
        payload = json.loads(result.stdout)
        selected = [item["id"] for item in payload.get("selected", []) if isinstance(item, dict) and item.get("id")]
        missing = [str(item) for item in payload.get("missing_capabilities", [])]
    except (json.JSONDecodeError, KeyError, TypeError) as exc:
        return {"status": "INVALID", "used": False, "selected": [], "missing": capabilities, "error": f"invalid response: {exc}"}
    return {"status": "AVAILABLE", "used": True, "selected": list(dict.fromkeys(selected)), "missing": list(dict.fromkeys(missing)), "error": None}


def inventory(broker_script: Path, registry_path: Path) -> dict[str, Any]:
    if not broker_script.is_file() or not registry_path.is_file():
        return {"status": "UNAVAILABLE", "skills": []}
    result = subprocess.run([sys.executable, str(broker_script), "--registry", str(registry_path), "list"], capture_output=True, text=True, timeout=15, check=False)
    if result.returncode != 0:
        return {"status": "INVALID", "skills": []}
    try:
        return {"status": "AVAILABLE", "skills": json.loads(result.stdout)}
    except json.JSONDecodeError:
        return {"status": "INVALID", "skills": []}


def route(prompt: str, broker_script: Path = DEFAULT_BROKER, registry_path: Path = DEFAULT_REGISTRY) -> dict[str, Any]:
    text = prompt.strip().lower()
    if re.fullmatch(r"(?:show\s+)?(?:skills|capabilities)\??", text):
        state = inventory(broker_script, registry_path)
        return {"command": "skills", "mode": "LIGHT", "private_roles": ["minister"], "broker_status": state["status"], "shared_inventory": state["skills"]}

    explain = re.fullmatch(r"explain routing(?:\s+for)?\s*:?\s*(.+)", text)
    if explain:
        prompt = explain.group(1)
        text = prompt.lower()

    mode = choose_mode(text)
    capabilities = required_capabilities(text, mode)
    broker = run_broker(prompt, capabilities, broker_script, registry_path)
    reversing_unknown = bool(re.search(r"\b(unknown|do not know|don't know|not sure|depends on whether|if .{0,80}\?)\b", text))
    review_only = bool(re.search(r"\b(forge|architecture proposal|completed output|implementation plan)\b", text))
    return {
        "command": "explain-routing" if explain else "decide",
        "mode": mode,
        "private_roles": ["minister", "minister-router", "executive-judgment"],
        "required_shared_capabilities": capabilities,
        "shared": broker["selected"],
        "missing_shared_capabilities": broker["missing"],
        "broker_status": broker["status"],
        "broker_used": broker["used"],
        "broker_error": broker["error"],
        "alternative_generation": True,
        "conflict_resolution": True,
        "defer_if_unresolved": reversing_unknown,
        "review_only": review_only,
        "active_count": 3 + len(broker["selected"]),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Route a Minister decision")
    parser.add_argument("prompt")
    parser.add_argument("--broker", type=Path, default=DEFAULT_BROKER)
    parser.add_argument("--registry", type=Path, default=DEFAULT_REGISTRY)
    args = parser.parse_args()
    print(json.dumps(route(args.prompt, args.broker, args.registry), indent=2))


if __name__ == "__main__":
    main()
