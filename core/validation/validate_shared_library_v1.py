#!/usr/bin/env python3
"""Release validation for Personal AI OS Shared Skill Library v1.0."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import urllib.error
import urllib.request
from collections import Counter, defaultdict
from pathlib import Path
from urllib.parse import urlparse


AI_OS = Path.home() / ".codex" / "ai-os"
REGISTRY = AI_OS / "registry" / "skill-registry.json"
QUICK_VALIDATE = Path.home() / ".codex" / "skills" / ".system" / "skill-creator" / "scripts" / "quick_validate.py"
BIN = AI_OS / "bin"
sys.path.insert(0, str(BIN))

from aios_skills import broker, duplicate_report, load_json, validate_registry  # noqa: E402


EXPECTED = {
    "reasoning": 9,
    "research": 4,
    "product-design": 5,
    "engineering": 9,
    "ai": 6,
    "operations-quality": 5,
}
ALLOWED_SOURCE_HOSTS = {
    "www.prisma-statement.org", "www.crossref.org", "www.nist.gov", "airc.nist.gov",
    "www.gov.uk", "www.iso.org", "committee.iso.org", "www.w3.org", "www.sei.cmu.edu", "insights.sei.cmu.edu", "developer.mozilla.org",
    "12factor.net", "spec.openapis.org", "www.postgresql.org", "owasp.org", "www.istqb.org",
    "web.dev", "developers.google.com", "platform.openai.com", "arxiv.org", "sre.google",
    "csrc.nist.gov", "opentelemetry.io",
}


def source_url(entry: dict) -> str | None:
    marker = "Evidence basis: "
    notes = entry.get("notes", "")
    return notes.split(marker, 1)[1].strip() if marker in notes else None


def online_source_status(url: str) -> tuple[bool, str]:
    request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 AI-OS-Validator/1.0"})
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            status = getattr(response, "status", 200)
            return 200 <= status < 400, str(status)
    except urllib.error.HTTPError as exc:
        return False, str(exc.code)
    except (urllib.error.URLError, TimeoutError) as exc:
        return False, type(exc).__name__


def run(online: bool) -> dict:
    data = load_json(REGISTRY)
    errors: list[str] = []
    warnings: list[str] = []
    structural = validate_registry(data, REGISTRY, run_official=False)
    errors.extend(structural["errors"])
    warnings.extend(structural["warnings"])

    domain = [entry for entry in data["skills"] if entry["category"] in EXPECTED]
    counts = Counter(entry["category"] for entry in domain)
    if counts != Counter(EXPECTED):
        errors.append(f"category counts differ: {dict(counts)}")
    if len(domain) != 38:
        errors.append(f"domain skill total is {len(domain)}, expected 38")
    if len(data["skills"]) != 39:
        errors.append(f"registry total is {len(data['skills'])}, expected 39 including Skill Broker")
    if data.get("registry_version") != "1.0.0":
        errors.append("registry_version is not 1.0.0")

    duplicate = duplicate_report(data)
    if duplicate["duplicate_ids"]:
        errors.append(f"duplicate ids: {duplicate['duplicate_ids']}")
    if duplicate["duplicate_capabilities_within_entry"]:
        errors.append("duplicate capabilities exist within an entry")
    if duplicate["cross_skill_capability_overlaps"]:
        errors.append(f"duplicate canonical capabilities: {duplicate['cross_skill_capability_overlaps']}")

    validation_failures = []
    broken_references = []
    for entry in data["skills"]:
        root = Path(entry["location"])
        result = subprocess.run([sys.executable, "-B", str(QUICK_VALIDATE), str(root)], capture_output=True, text=True, check=False)
        if result.returncode != 0:
            validation_failures.append(entry["id"])
        text = (root / "SKILL.md").read_text(encoding="utf-8") if (root / "SKILL.md").exists() else ""
        if "[TODO" in text or len(text.split()) < 70:
            errors.append(f"quality gate failed for {entry['id']}")
        for target in __import__("re").findall(r"\[[^\]]+\]\(([^)]+)\)", text):
            if target.startswith(("http://", "https://", "#")):
                continue
            if not (root / target.split("#", 1)[0]).resolve().exists():
                broken_references.append(f"{entry['id']}:{target}")
    if validation_failures:
        errors.append(f"skill validation failures: {validation_failures}")
    if broken_references:
        errors.append(f"broken references: {broken_references}")

    source_results = {}
    new_entries = [entry for entry in data["skills"] if entry["category"] != "reasoning" and entry["id"] != "skill-broker"]
    for entry in new_entries:
        url = source_url(entry)
        if not url:
            errors.append(f"missing evidence source: {entry['id']}")
            continue
        host = urlparse(url).hostname
        if host not in ALLOWED_SOURCE_HOSTS:
            errors.append(f"unapproved evidence host for {entry['id']}: {host}")
        if online:
            passed, status = online_source_status(url)
            source_results[url] = {"passed": passed, "status": status}
            if not passed:
                errors.append(f"external source unavailable: {entry['id']} {url} ({status})")

    routing_failures = []
    for entry in domain:
        result = broker(data, None, [entry["capabilities"][0]])
        ids = [item["id"] for item in result["selected"]]
        if ids != [entry["id"]] or result["missing_capabilities"]:
            routing_failures.append({"skill": entry["id"], "selected": ids})
    if routing_failures:
        errors.append(f"routing failures: {routing_failures}")

    negative_cases = [
        ("Challenge the fundamental assumptions behind this plan.", {"first-principles"}),
        ("Design an end-to-end accessible user flow.", {"experience-design"}),
        ("Plan incident containment and recovery.", {"incident-response"}),
        ("Fix one typo in a React label.", set()),
    ]
    negative_failures = []
    for task, expected in negative_cases:
        selected = {item["id"] for item in broker(data, task, [])["selected"]}
        if selected != expected:
            negative_failures.append({"task": task, "expected": sorted(expected), "selected": sorted(selected)})
    if negative_failures:
        errors.append(f"negative routing failures: {negative_failures}")

    access = defaultdict(set)
    for entry in domain:
        for agent in entry["recommended_agents"]:
            if agent in {"Forge", "Minister", "MOA"}:
                access[agent].add(entry["category"])
    access_results = {agent: sorted(access[agent]) for agent in ("Forge", "Minister", "MOA")}
    for agent, categories in access_results.items():
        if set(categories) != set(EXPECTED):
            errors.append(f"{agent} lacks recommended access across categories: {categories}")

    return {
        "status": "PASS" if not errors else "FAIL",
        "release": "AI OS SHARED SKILL LIBRARY v1.0",
        "category_counts": dict(counts),
        "domain_total": len(domain),
        "registry_total": len(data["skills"]),
        "custom_quality_gate": "PASS" if not validation_failures and not broken_references else "FAIL",
        "external_source_validation": "PASS" if online and source_results and all(item["passed"] for item in source_results.values()) else ("NOT_RUN" if not online else "FAIL"),
        "registry": "PASS" if not structural["errors"] else "FAIL",
        "skill_broker": "PASS" if not routing_failures else "FAIL",
        "routing_evals": "PASS" if not routing_failures else "FAIL",
        "negative_routing": "PASS" if not negative_failures else "FAIL",
        "agent_access": access_results,
        "duplicate_canonical_skills": "NONE" if not duplicate["cross_skill_capability_overlaps"] and not duplicate["duplicate_ids"] else "FOUND",
        "broken_references": "NONE" if not broken_references else broken_references,
        "critical": 0 if not errors else len(errors),
        "high": 0,
        "warnings": warnings,
        "errors": errors,
        "source_results": source_results,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--online", action="store_true")
    parser.add_argument("--report")
    args = parser.parse_args()
    report = run(args.online)
    payload = json.dumps(report, indent=2, ensure_ascii=False)
    print(payload)
    if args.report:
        Path(args.report).write_text(payload + "\n", encoding="utf-8")
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
