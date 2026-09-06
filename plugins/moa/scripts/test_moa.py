#!/usr/bin/env python3
"""Behavioral acceptance tests A through L for MOA v0.1."""

from __future__ import annotations

from copy import deepcopy

from moa_core import (
    AGENT_REGISTRY,
    SKILL_REGISTRY,
    arbitrate,
    completion_governance,
    health,
    load_json,
    route_task,
    selectable_agents,
    validate_agent_registry,
)


def check(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def test_a() -> None:
    route = route_task("@MOA Should I buy a £1,500 laptop when my existing laptop works?")
    check(route["selected_agents"] == ["Minister"], "pure decision selected Forge")
    check("decision-science" in route["selected_shared_skills"], "decision skill missing")


def test_b() -> None:
    route = route_task("@MOA Build a modern responsive personal portfolio.")
    check(route["selected_agents"] == ["Minister", "Forge"], "build mixture is wrong")
    check(route["minister_participation"] == "LIGHT", "pure build should use Minister LIGHT")


def test_c() -> None:
    route = route_task("@MOA Build a tiny portfolio with Kubernetes, Kafka, Redis and microservices.")
    check("first-principles" in route["selected_shared_skills"], "first principles not selected")
    check(any("simplified architecture" in item for item in route["conditions"]), "simplification condition missing")


def test_d() -> None:
    route = route_task("@MOA I've spent six months on this project with no users. What should I do?")
    expected = {"behavioral-psychology", "evidence-epistemics", "decision-science", "risk-premortem", "adversarial-red-team"}
    check(route["minister_participation"] == "DEEP", "sunk cost should be DEEP")
    check("Forge" not in route["selected_agents"], "sunk cost decision selected Forge")
    check(expected.issubset(set(route["selected_shared_skills"])), "sunk cost skill mixture incomplete")


def test_e() -> None:
    route = route_task("@MOA I have an idea for a small SaaS. Determine if it is worth building and, if yes, create the MVP.")
    forge = next(node for node in route["execution_graph"] if node["id"] == "forge-execution")
    check("only if Minister" in forge["task"], "conditional build gate missing")
    check(route["execution_graph"][-2]["id"] == "minister-final", "final Minister review missing")


def test_f() -> None:
    route = route_task("@MOA Conduct a wet-lab genomic sequencing experiment for this sample.")
    check("specialized real-world execution agent" in route["missing_capabilities"], "missing agent capability hidden")


def test_g() -> None:
    route = route_task("@MOA Fix a typo in this React component.")
    check(route["minister_participation"] == "LIGHT", "typo did not use LIGHT")
    check(route["selected_agents"] == ["Minister", "Forge"], "typo mixture is not minimal")
    check(len(route["selected_shared_skills"]) <= 1, "typo activated too many shared skills")


def test_h() -> None:
    data = load_json(AGENT_REGISTRY)
    check({"minister", "forge", "moa"}.issubset({item["id"] for item in data["agents"]}), "core registry entries missing")
    mock = deepcopy(data["agents"][0])
    mock.update({"id": "disabled-mock", "name": "Disabled Mock", "enabled": False, "installed": True, "status": "DISABLED"})
    data["agents"].append(mock)
    check(not validate_agent_registry(data), "disabled mock made registry invalid")
    check("disabled-mock" not in {item["id"] for item in selectable_agents(data)}, "disabled mock was selectable")


def test_i() -> None:
    route = route_task("@MOA Build a tiny portfolio with Kubernetes, Kafka, and microservices.")
    check(arbitrate("strategy") == "Minister", "strategy authority is wrong")
    check(route["conditions"], "Minister simplification condition was not preserved")


def test_j() -> None:
    status = completion_governance(deliverable=True, tests_passed=True, minister_final="APPROVE", material_limitation=True)
    check(status == "APPROVE WITH CONDITIONS", "material limitation was blindly approved")


def test_k() -> None:
    data = load_json(AGENT_REGISTRY)
    scout = next((item for item in data["agents"] if item["id"] == "scout"), None)
    check(scout is not None and scout["enabled"] and scout["installed"], "registered Scout is unavailable")
    route = route_task("@MOA Research current battery technology.", data, load_json(SKILL_REGISTRY))
    check(route["selected_agents"] == ["Minister", "Scout"], "enabled Scout was not preferred for pure research")
    check("Forge" not in route["selected_agents"], "pure research selected Forge")


def test_l() -> None:
    result = health()
    check(result["status"] == "PASS", f"MOA health failed: {result}")
    check(all(result["checks"].values()), "a health component failed")


def test_m() -> None:
    route = route_task("@MOA Audit release readiness for this core system.")
    audit = next((node for node in route["execution_graph"] if node["id"] == "audit-review"), None)
    check(route["selected_workflows"] == ["independent-audit"], "audit was incorrectly promoted to a standalone agent")
    check(audit is not None and audit["assigned_agent"] == "Audit", "independent audit node missing")
    check(audit["dependencies"] == ["verification"], "audit must follow verification")


def test_n() -> None:
    route = route_task("@MOA Run a bounded local experiment for this hypothesis.")
    check(route["task_type"] == "EXPERIMENT", "experiment task class missing")
    check(route["selected_agents"] == ["Minister", "Forge"], "experiment should be composed through Forge")


TESTS = [
    ("A PURE DECISION", test_a),
    ("B PURE BUILD", test_b),
    ("C OVERENGINEERING", test_c),
    ("D SUNK COST", test_d),
    ("E BUILD AFTER DECISION", test_e),
    ("F MISSING AGENT", test_f),
    ("G MINIMAL ROUTING", test_g),
    ("H AGENT REGISTRY", test_h),
    ("I CONFLICT", test_i),
    ("J FINAL REVIEW", test_j),
    ("K FUTURE AGENT", test_k),
    ("L MOA HEALTH", test_l),
    ("M INDEPENDENT AUDIT WORKFLOW", test_m),
    ("N LAB WORKFLOW", test_n),
]


def main() -> int:
    passed = 0
    for name, test in TESTS:
        try:
            test()
            passed += 1
            print(f"PASS {name}")
        except Exception as exc:
            print(f"FAIL {name}: {exc}")
    print(f"MOA TESTS: {passed}/{len(TESTS)} passed")
    return 0 if passed == len(TESTS) else 1


if __name__ == "__main__":
    raise SystemExit(main())
