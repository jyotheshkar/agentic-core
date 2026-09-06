from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
AUDIT_SPEC = importlib.util.spec_from_file_location("audit_core_snapshot", ROOT / "plugins/audit/scripts/audit_core.py")
CONTROL_SPEC = importlib.util.spec_from_file_location("control_snapshot", ROOT / "core/control-plane/aios_control.py")
assert AUDIT_SPEC and AUDIT_SPEC.loader and CONTROL_SPEC and CONTROL_SPEC.loader
audit = importlib.util.module_from_spec(AUDIT_SPEC)
control = importlib.util.module_from_spec(CONTROL_SPEC)
AUDIT_SPEC.loader.exec_module(audit)
CONTROL_SPEC.loader.exec_module(control)


class AuditIntegrationTests(unittest.TestCase):
    def test_a_registry_has_exactly_five_enabled_core_agents(self) -> None:
        registry = json.loads((ROOT / "core/registry/agent-registry.json").read_text(encoding="utf-8"))
        enabled = {agent["id"] for agent in registry["agents"] if agent["enabled"] and agent["status"] == "AVAILABLE"}
        self.assertEqual({"moa", "minister", "scout", "forge", "audit"}, enabled)
        devil = next(agent for agent in registry["agents"] if agent["id"] == "devil")
        self.assertTrue(devil["installed"])
        self.assertFalse(devil["enabled"])

    def test_b_audit_route_preserves_non_overlap(self) -> None:
        route = audit.route("Audit this release readiness claim and challenge the evidence")
        self.assertEqual(["audit-evidence-policy", "audit-release-gate", "audit-adversarial-assurance"], route["selected_private_skills"])
        self.assertEqual(sorted(audit.PROHIBITED_AUTHORITIES), route["prohibited_authorities"])

    def test_c_control_plane_requires_audit(self) -> None:
        self.assertEqual([], control.validate_run(control.demo_run()))
        run = control.demo_run()
        run["routing"]["selected_agents"].remove("Audit")
        self.assertIn("routing must record standalone Audit assurance", control.validate_run(run))


if __name__ == "__main__":
    unittest.main()
