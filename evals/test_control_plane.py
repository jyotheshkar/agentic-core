from __future__ import annotations

import importlib.util
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("aios_control", ROOT / "core/control-plane/aios_control.py")
assert SPEC and SPEC.loader
control = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(control)


class ControlPlaneTests(unittest.TestCase):
    def test_deterministic_handoff_contract(self) -> None:
        demo = control.demo_run()
        self.assertEqual([], control.validate_handoff(demo["handoffs"][0]))

    def test_negative_missing_authority_fails_closed(self) -> None:
        handoff = control.demo_run()["handoffs"][0]
        del handoff["AUTHORITY"]
        self.assertIn("missing handoff field: AUTHORITY", control.validate_handoff(handoff))

    def test_boundary_third_identical_blocker_becomes_blocked(self) -> None:
        component = {"status": "IN_PROGRESS"}
        for _ in range(3):
            component = control.transition(component, "REWORK", blocker="offline dependency")
            if component["status"] == "REWORK":
                component = control.transition(component, "IN_PROGRESS")
        self.assertEqual("BLOCKED", component["status"])

    def test_adversarial_tamper_in_audit_chain_fails(self) -> None:
        demo = control.demo_run()
        demo["audit_events"][2]["type"] = "TAMPERED"
        self.assertTrue(control.verify_audit_chain(demo["audit_events"]))

    def test_integration_demo_contains_required_cross_agent_evidence(self) -> None:
        self.assertEqual([], control.validate_run(control.demo_run()))

    def test_regression_completion_cannot_ignore_limitation(self) -> None:
        self.assertEqual("REWORK", control.completion_status(
            deliverable=True, verification_passed=True, minister_final="APPROVE",
            material_limitations=["critical unknown"], high_risks=0,
        ))


if __name__ == "__main__":
    unittest.main()
