#!/usr/bin/env python3
"""Deterministic baseline router for Forge prompts and AI OS shared skills."""

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


def _shared_capabilities(text: str) -> list[str]:
    """Translate task signals into capability IDs, never installed skill names."""
    required: list[str] = []
    infrastructure = re.findall(
        r"\b(kubernetes|kafka|redis|postgres(?:ql)?|microservices?|containers?|queues?|multiple backend services)\b",
        text,
    )
    if len(set(infrastructure)) >= 3 or re.search(
        r"\b(overengineer(?:ed|ing)?|challenge (?:the )?assumptions?|from first principles)\b", text
    ):
        required.append("first-principles-analysis")

    if re.search(
        r"\b(definitely|certainly|guaranteed|current(?:ly)?|latest|verify|evidence|claim(?:s|ed)?|supports? feature)\b",
        text,
    ):
        required.append("evidence-quality-analysis")

    interacting = re.findall(
        r"\b(authentication|auth|billing|payments?|background jobs?|queues?|database|persistent data|file uploads?|ai processing|notifications?|analytics)\b",
        text,
    )
    if len(set(interacting)) >= 3 or re.search(
        r"\b(system dependencies|feedback loops?|second-order|local-first\b.{0,50}\bpersistent)\b", text
    ):
        required.append("systems-analysis")

    if re.search(r"\b(web security|csrf|xss|csp|owasp|secure web|security hardening)\b", text):
        required.append("web-security")

    return list(dict.fromkeys(required))


def _run_broker(
    prompt: str,
    capabilities: list[str],
    broker_script: Path,
    registry_path: Path,
) -> dict[str, Any]:
    if not broker_script.is_file():
        return {
            "status": "UNAVAILABLE",
            "used": False,
            "selected": [],
            "missing_capabilities": capabilities,
            "error": f"broker script unavailable: {broker_script}",
        }
    if not registry_path.is_file():
        return {
            "status": "UNAVAILABLE",
            "used": False,
            "selected": [],
            "missing_capabilities": capabilities,
            "error": f"registry unavailable: {registry_path}",
        }

    command = [
        sys.executable,
        str(broker_script),
        "--registry",
        str(registry_path),
        "broker",
        "--task",
        prompt,
    ]
    for capability in capabilities:
        command.extend(["--capability", capability])
    try:
        completed = subprocess.run(command, capture_output=True, text=True, timeout=15, check=False)
    except (OSError, subprocess.SubprocessError) as exc:
        return {
            "status": "UNAVAILABLE",
            "used": False,
            "selected": [],
            "missing_capabilities": capabilities,
            "error": str(exc),
        }
    if completed.returncode != 0:
        return {
            "status": "INVALID",
            "used": False,
            "selected": [],
            "missing_capabilities": capabilities,
            "error": completed.stderr.strip() or completed.stdout.strip() or "broker failed",
        }
    try:
        payload = json.loads(completed.stdout)
        selected = [item["id"] for item in payload.get("selected", []) if isinstance(item, dict) and item.get("id")]
        missing = payload.get("missing_capabilities", [])
        if not isinstance(missing, list):
            raise ValueError("missing_capabilities must be a list")
    except (json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
        return {
            "status": "INVALID",
            "used": False,
            "selected": [],
            "missing_capabilities": capabilities,
            "error": f"invalid broker response: {exc}",
        }
    return {
        "status": "AVAILABLE",
        "used": True,
        "selected": list(dict.fromkeys(selected)),
        "missing_capabilities": list(dict.fromkeys(str(item) for item in missing)),
        "error": None,
    }


def broker_inventory(broker_script: Path = DEFAULT_BROKER, registry_path: Path = DEFAULT_REGISTRY) -> dict[str, Any]:
    if not broker_script.is_file() or not registry_path.is_file():
        return {"status": "UNAVAILABLE", "skills": []}
    completed = subprocess.run(
        [sys.executable, str(broker_script), "--registry", str(registry_path), "list"],
        capture_output=True,
        text=True,
        timeout=15,
        check=False,
    )
    if completed.returncode != 0:
        return {"status": "INVALID", "skills": []}
    try:
        skills = json.loads(completed.stdout)
    except json.JSONDecodeError:
        return {"status": "INVALID", "skills": []}
    return {"status": "AVAILABLE", "skills": skills}


def route(
    prompt: str,
    broker_script: Path = DEFAULT_BROKER,
    registry_path: Path = DEFAULT_REGISTRY,
) -> dict[str, Any]:
    text = prompt.strip().lower()
    if re.fullmatch(r"(?:show\s+)?(?:skills|capabilities)\??", text):
        inventory = broker_inventory(broker_script, registry_path)
        return {
            "command": "skills",
            "mode": "QUICK",
            "domains": [],
            "roles": ["forge"],
            "external": [],
            "broker_status": inventory["status"],
            "shared_inventory": inventory["skills"],
        }

    explain_match = re.fullmatch(r"explain routing(?:\s+for)?\s*:?\s*(.+)", text)
    if explain_match:
        prompt = explain_match.group(1)
        text = prompt.strip().lower()

    domains: list[str] = []
    external: list[str] = []
    roles = ["forge", "forge-router", "forge-verification-gate"]

    def add_domain(name: str, pattern: str) -> None:
        if re.search(pattern, text):
            domains.append(name)

    add_domain("frontend", r"\b(react|next\.?js|frontend|portfolio|responsive|ui|ux|css|card|shadcn|web app)\b")
    add_domain("backend", r"\b(api|backend|server|database|persistent|postgres|supabase|convex|cloudflare|d1|upload(?:ed|s|ing)?)\b")
    add_domain("auth", r"\b(auth|authentication|authori[sz]ation|session|login|sign[ -]?in|rls)\b")
    add_domain("ai", r"\b(llm|rag|retrieval|embedding|model|agent|prompt|pdfs?|ai (?:app|application|system|assistant|feature|model|agent|processing))\b")
    add_domain("mobile", r"\b(expo|react native|ios|android|mobile app)\b")
    add_domain("infrastructure", r"\b(kubernetes|kafka|redis|microservices?|containers?|queues?)\b")
    add_domain("security", r"\b(web security|csrf|xss|csp|owasp|secure web|security hardening)\b")
    add_domain("deployment", r"\b(deploy|production|domain|hosting|vercel|workers)\b")
    add_domain("payment-blocker", r"\b(paid[- ]only|must pay|purchase|billing|subscription|buy credits?)\b")

    tiny = bool(re.search(r"\b(fix|adjust|rename|spacing|typo)\b", text)) and len(text.split()) < 16 and len(domains) <= 1
    project_build = bool(re.search(r"\b(build|create|implement)\b", text) and re.search(r"\b(app|application|portfolio|site|website|system|platform)\b", text))
    deep = project_build or len(domains) >= 3 or any(d in domains for d in ("auth", "ai", "infrastructure", "security", "deployment", "payment-blocker"))
    mode = "QUICK" if tiny else "DEEP" if deep else "STANDARD"

    if mode != "QUICK":
        roles.append("forge-product")
    if mode == "DEEP" or len(domains) >= 2:
        roles.extend(["forge-architect", "forge-devil", "forge-integrator"])

    if "frontend" in domains:
        if re.search(r"\b(react|next\.?js|shadcn|portfolio)\b", text):
            external.append("vercel:react-best-practices")
        if re.search(r"\bnext\.?js\b", text):
            external.append("vercel:nextjs")
        if re.search(r"\bshadcn\b", text):
            external.append("vercel:shadcn")
        if mode != "QUICK":
            external.append("vercel:agent-browser-verify")
    if "ai" in domains and re.search(r"\b(openai|agents sdk)\b", text):
        external.append("openai-developers:agents-sdk")
    if "backend" in domains and re.search(r"\bconvex\b", text):
        external.append("convex:convex-expert")

    capabilities = _shared_capabilities(text)
    broker_result = _run_broker(prompt, capabilities, broker_script, registry_path)
    shared = broker_result["selected"]
    return {
        "command": "explain-routing" if explain_match else "execute",
        "mode": mode,
        "domains": list(dict.fromkeys(domains)),
        "roles": list(dict.fromkeys(roles)),
        "required_shared_capabilities": capabilities,
        "shared": shared,
        "external": list(dict.fromkeys(external)),
        "missing_shared_capabilities": broker_result["missing_capabilities"],
        "broker_status": broker_result["status"],
        "broker_used": broker_result["used"],
        "broker_error": broker_result["error"],
        "active_count": len(set(roles + shared + external)),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Route a Forge prompt")
    parser.add_argument("prompt")
    parser.add_argument("--broker", type=Path, default=DEFAULT_BROKER)
    parser.add_argument("--registry", type=Path, default=DEFAULT_REGISTRY)
    args = parser.parse_args()
    print(json.dumps(route(args.prompt, args.broker, args.registry), indent=2))


if __name__ == "__main__":
    main()
