#!/usr/bin/env python3
"""Behavioral contract tests for Forge routing and verification."""

from __future__ import annotations

import unittest
from pathlib import Path

from route_forge import route
from verify_gate import evaluate


class RoutingTests(unittest.TestCase):
    def test_tiny_frontend_task_stays_quick(self) -> None:
        result = route("Fix the spacing on this React card.")
        self.assertEqual(result["mode"], "QUICK")
        self.assertEqual(result["domains"], ["frontend"])
        self.assertNotIn("backend", result["domains"])
        self.assertNotIn("forge-architect", result["roles"])
        self.assertEqual(result["shared"], [])
        self.assertTrue(result["broker_used"])

    def test_frontend_project_has_qa_without_backend(self) -> None:
        result = route("Build a modern responsive AI engineer portfolio.")
        self.assertIn("frontend", result["domains"])
        self.assertNotIn("backend", result["domains"])
        self.assertNotIn("ai", result["domains"])
        self.assertIn("forge-devil", result["roles"])
        self.assertIn("vercel:agent-browser-verify", result["external"])

    def test_full_stack_project_routes_core_domains(self) -> None:
        result = route("Build a task-management web app with authentication and persistent data.")
        self.assertTrue({"backend", "auth"}.issubset(result["domains"]))
        self.assertEqual(result["mode"], "DEEP")
        self.assertIn("forge-architect", result["roles"])
        self.assertIn("forge-verification-gate", result["roles"])

    def test_ai_rag_project_routes_ai_and_data_without_paid_api(self) -> None:
        result = route("Build a local-first RAG application for querying uploaded PDFs.")
        self.assertIn("ai", result["domains"])
        self.assertIn("backend", result["domains"])
        self.assertFalse(any("openai" in skill for skill in result["external"]))

    def test_paid_blocker_is_explicit(self) -> None:
        result = route("Build the product but it must use a paid-only SMS subscription.")
        self.assertIn("payment-blocker", result["domains"])
        self.assertEqual(result["mode"], "DEEP")

    def test_skills_command_does_not_execute(self) -> None:
        result = route("skills")
        self.assertEqual(result["command"], "skills")
        self.assertEqual(result["roles"], ["forge"])

    def test_router_does_not_activate_every_skill(self) -> None:
        result = route("Build a modern responsive AI engineer portfolio.")
        self.assertLessEqual(result["active_count"], 10)
        self.assertNotIn("convex:convex-expert", result["external"])

    def test_architecture_assumption_selects_first_principles_only(self) -> None:
        result = route(
            "Build a tiny personal portfolio using Kubernetes, Kafka, Redis, "
            "PostgreSQL, microservices and multiple backend services."
        )
        self.assertEqual(result["shared"], ["first-principles"])
        self.assertIn("forge-architect", result["roles"])
        self.assertEqual(result["missing_shared_capabilities"], [])

    def test_current_technology_claim_selects_evidence(self) -> None:
        result = route("Build using framework X because it definitely supports feature Y.")
        self.assertEqual(result["shared"], ["evidence-epistemics"])
        self.assertEqual(result["required_shared_capabilities"], ["evidence-quality-analysis"])

    def test_interacting_system_selects_systems_thinking(self) -> None:
        result = route(
            "Design a SaaS app with authentication, billing, background jobs, "
            "database, file uploads and AI processing."
        )
        self.assertEqual(result["shared"], ["systems-thinking"])
        self.assertIn("forge-integrator", result["roles"])

    def test_minimum_sufficient_selection_across_tasks(self) -> None:
        prompts = [
            "Fix spacing on a React card.",
            "Build using framework X because it definitely supports feature Y.",
            "Challenge the assumptions in this overengineered application.",
            "Map system dependencies and feedback loops for this platform.",
        ]
        counts = [len(route(prompt)["shared"]) for prompt in prompts]
        self.assertEqual(counts, [0, 1, 1, 1])
        self.assertTrue(all(count < 3 for count in counts))

    def test_missing_shared_capability_is_reported_without_hallucination(self) -> None:
        result = route("Build a secure web app with CSRF protection.")
        self.assertEqual(result["shared"], [])
        self.assertEqual(result["missing_shared_capabilities"], ["web-security"])
        self.assertEqual(result["broker_status"], "AVAILABLE")

    def test_missing_broker_degrades_gracefully(self) -> None:
        result = route(
            "Build using framework X because it definitely supports feature Y.",
            broker_script=Path("Z:/forge-test/no-broker.py"),
        )
        self.assertFalse(result["broker_used"])
        self.assertEqual(result["broker_status"], "UNAVAILABLE")
        self.assertEqual(result["shared"], [])
        self.assertEqual(result["missing_shared_capabilities"], ["evidence-quality-analysis"])
        self.assertIn("forge-verification-gate", result["roles"])

    def test_shared_skills_are_user_scoped_not_copied(self) -> None:
        forge_skills = Path(__file__).resolve().parents[1] / "skills"
        user_skills = Path.home() / ".codex" / "skills"
        for name in ("first-principles", "evidence-epistemics", "systems-thinking", "skill-broker"):
            self.assertTrue((user_skills / name / "SKILL.md").is_file())
            self.assertFalse((forge_skills / name).exists())

    def test_skills_diagnostic_reports_broker_inventory(self) -> None:
        result = route("capabilities")
        self.assertEqual(result["command"], "skills")
        self.assertEqual(result["broker_status"], "AVAILABLE")
        ids = {item["id"] for item in result["shared_inventory"]}
        self.assertTrue({"skill-broker", "first-principles", "evidence-epistemics", "systems-thinking"}.issubset(ids))

    def test_realistic_project_keeps_full_forge_chain_and_broker(self) -> None:
        result = route("Build a responsive local-first task management app with persistent data.")
        expected_roles = {
            "forge", "forge-router", "forge-product", "forge-architect", "forge-devil",
            "forge-integrator", "forge-verification-gate",
        }
        self.assertTrue(expected_roles.issubset(result["roles"]))
        self.assertEqual(result["shared"], ["systems-thinking"])
        self.assertTrue(result["broker_used"])

    def test_explain_routing_is_diagnostic_not_execution(self) -> None:
        result = route("explain routing: Fix spacing on a React card.")
        self.assertEqual(result["command"], "explain-routing")
        self.assertEqual(result["mode"], "QUICK")


class VerificationTests(unittest.TestCase):
    def test_failed_check_blocks_completion(self) -> None:
        passed, errors = evaluate({
            "product_contract_satisfied": True,
            "checks": [{"name": "build", "status": "failed"}],
            "findings": [],
            "claims": {"fully_working": False},
        })
        self.assertFalse(passed)
        self.assertTrue(errors)

    def test_unresolved_high_blocks_completion(self) -> None:
        passed, _ = evaluate({
            "product_contract_satisfied": True,
            "checks": [{"name": "tests", "status": "passed"}],
            "findings": [{"severity": "HIGH", "status": "open", "title": "auth bypass"}],
            "claims": {"fully_working": False},
        })
        self.assertFalse(passed)

    def test_mock_cannot_be_called_fully_working(self) -> None:
        passed, _ = evaluate({
            "product_contract_satisfied": True,
            "checks": [{"name": "tests", "status": "passed"}],
            "findings": [],
            "claims": {"fully_working": True},
            "critical_integrations_mocked": True,
        })
        self.assertFalse(passed)

    def test_clean_report_passes(self) -> None:
        passed, errors = evaluate({
            "product_contract_satisfied": True,
            "checks": [{"name": "tests", "status": "passed"}],
            "findings": [{"severity": "HIGH", "status": "resolved", "title": "fixed"}],
            "claims": {"fully_working": True},
            "critical_integrations_mocked": False,
        })
        self.assertTrue(passed)
        self.assertEqual(errors, [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
