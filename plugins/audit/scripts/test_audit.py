#!/usr/bin/env python3
"""Deterministic, negative, adversarial, authority, and regression tests for Audit."""

from __future__ import annotations

from copy import deepcopy

from audit_core import PROHIBITED_AUTHORITIES, health, recommend, route, validate_audit_record, validate_finding


def check(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def finding(**overrides: object) -> dict[str, object]:
    result: dict[str, object] = {
        "id": "AUD-001", "title": "Evidence is traceable", "severity": "LOW",
        "evidence": ["record:integration-demo"], "confidence": 0.9,
        "limitations": [], "recommendation": "APPROVE", "escalation_conditions": ["evidence changes"],
    }
    result.update(overrides)
    return result


def record(**overrides: object) -> dict[str, object]:
    result: dict[str, object] = {
        "audit_id": "audit-demo", "scope": "independent-assurance",
        "audited_artifacts": ["record:integration-demo"], "findings": [finding()],
        "prohibited_authorities": sorted(PROHIBITED_AUTHORITIES), "status": "APPROVE",
    }
    result.update(overrides)
    return result


def test_a_valid_finding() -> None:
    check(not validate_finding(finding()), "valid finding failed")


def test_b_missing_evidence_fails() -> None:
    check(validate_finding(finding(evidence=[])), "missing evidence was accepted")


def test_c_confidence_boundary() -> None:
    check(not validate_finding(finding(confidence=0)), "zero confidence boundary failed")
    check(validate_finding(finding(confidence=1.1)), "out-of-range confidence was accepted")


def test_d_missing_escalation_fails() -> None:
    check(validate_finding(finding(escalation_conditions=[])), "missing escalation was accepted")


def test_e_valid_record() -> None:
    check(not validate_audit_record(record()), "valid record failed")


def test_f_non_overlap_is_strict() -> None:
    candidate = record(prohibited_authorities=sorted(PROHIBITED_AUTHORITIES - {"software-implementation"}))
    check(validate_audit_record(candidate), "missing non-overlap boundary was accepted")


def test_g_critical_finding_forces_rework() -> None:
    check(recommend(record(findings=[finding(severity="CRITICAL")])) == "REWORK", "critical finding did not force rework")


def test_h_limitation_requires_conditions() -> None:
    check(recommend(record(findings=[finding(limitations=["runtime invocation unavailable"])])) == "APPROVE WITH CONDITIONS", "limitation was blindly approved")


def test_i_empty_findings_defers() -> None:
    check(recommend(record(findings=[])) == "DEFER", "empty evidence did not defer")


def test_j_adversarial_tamper_fails() -> None:
    candidate = deepcopy(record())
    candidate["findings"] = [finding(id="bad id")]
    check(validate_audit_record(candidate), "tampered identifier was accepted")


def test_k_release_route_is_minimum_sufficient() -> None:
    selected = route("Audit release readiness claim")["selected_private_skills"]
    check(selected == ["audit-evidence-policy", "audit-release-gate", "audit-adversarial-assurance"], "release routing is wrong")


def test_l_health_and_registry() -> None:
    result = health()
    check(result["status"] == "PASS", f"Audit health failed: {result}")


def test_m_authority_overlap_is_rejected() -> None:
    result = route("Browse for sources and research the web before making the strategic decision")
    check(result["selected_private_skills"] == [], "Audit accepted an overlapping authority request")
    check(set(result["rejected_authority_overlap"]) == {"primary-web-research", "strategic-tradeoff-judgment"}, "overlap was not identified")


TESTS = [("A VALID FINDING", test_a_valid_finding), ("B MISSING EVIDENCE", test_b_missing_evidence_fails), ("C CONFIDENCE BOUNDARY", test_c_confidence_boundary), ("D ESCALATION", test_d_missing_escalation_fails), ("E VALID RECORD", test_e_valid_record), ("F NON-OVERLAP", test_f_non_overlap_is_strict), ("G CRITICAL", test_g_critical_finding_forces_rework), ("H LIMITATION", test_h_limitation_requires_conditions), ("I EMPTY EVIDENCE", test_i_empty_findings_defers), ("J ADVERSARIAL", test_j_adversarial_tamper_fails), ("K ROUTING", test_k_release_route_is_minimum_sufficient), ("L HEALTH", test_l_health_and_registry), ("M AUTHORITY OVERLAP", test_m_authority_overlap_is_rejected)]


def main() -> int:
    passed = 0
    for name, test in TESTS:
        try:
            test()
            passed += 1
            print(f"PASS {name}")
        except Exception as exc:
            print(f"FAIL {name}: {exc}")
    print(f"AUDIT TESTS: {passed}/{len(TESTS)} passed")
    return 0 if passed == len(TESTS) else 1


if __name__ == "__main__":
    raise SystemExit(main())
