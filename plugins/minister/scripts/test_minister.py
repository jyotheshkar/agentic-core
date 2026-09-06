#!/usr/bin/env python3
"""Behavioral and structural acceptance tests for Minister."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

from route_minister import route


class MinisterRoutingTests(unittest.TestCase):
    def assert_shared(self, prompt: str, expected: set[str]) -> dict:
        result = route(prompt)
        self.assertTrue(expected.issubset(set(result["shared"])), result)
        self.assertEqual(result["broker_status"], "AVAILABLE")
        self.assertEqual(result["missing_shared_capabilities"], [])
        self.assertIn("executive-judgment", result["private_roles"])
        return result

    def test_a_simple_purchase(self) -> None:
        result = self.assert_shared(
            "Should I spend £1,500 on a new laptop when my current laptop works?",
            {"decision-science", "behavioral-psychology", "risk-premortem"},
        )
        self.assertEqual(result["mode"], "STANDARD")

    def test_b_sunk_cost(self) -> None:
        self.assert_shared(
            "I've already spent six months on this project, so I should continue even though there is little evidence anyone wants it.",
            {"behavioral-psychology", "evidence-epistemics", "decision-science", "adversarial-red-team"},
        )

    def test_c_career_decision(self) -> None:
        self.assert_shared(
            "I have a stable job and another offer that pays 25% more but is materially riskier. Which should I choose?",
            {"decision-science", "strategic-foresight", "risk-premortem"},
        )

    def test_d_negotiation(self) -> None:
        self.assert_shared(
            "I have an offer and want to negotiate compensation without losing it.",
            {"game-theory-incentives", "behavioral-psychology", "risk-premortem", "strategic-foresight"},
        )

    def test_e_insufficient_information_flags_defer(self) -> None:
        result = self.assert_shared(
            "Should I accept this offer if sponsorship is available? I do not know whether sponsorship is available.",
            {"decision-science", "evidence-epistemics", "strategic-foresight"},
        )
        self.assertEqual(result["mode"], "CRITICAL")
        self.assertTrue(result["defer_if_unresolved"])

    def test_f_unlisted_alternative_is_required(self) -> None:
        result = route("Should I choose option A or option B for this reversible decision?")
        self.assertTrue(result["alternative_generation"])

    def test_g_skill_disagreement_requires_resolution(self) -> None:
        result = route("One option has higher expected value, but the other has much lower risk. Which should I choose?")
        self.assertTrue(result["conflict_resolution"])
        self.assertIn("executive-judgment", result["private_roles"])

    def test_h_trivial_reversible_decision_is_minimal(self) -> None:
        result = route("Should I try a new lunch place today?")
        self.assertEqual(result["mode"], "LIGHT")
        self.assertLessEqual(len(result["shared"]), 2)

    def test_i_full_council_for_major_life_decision(self) -> None:
        result = route("Should I leave my job and move country for a major career change?")
        self.assertEqual(result["mode"], "CRITICAL")
        self.assertEqual(len(result["shared"]), 9)

    def test_j_forge_review_does_not_route_implementation(self) -> None:
        result = route("Review this Forge architecture proposal and decide whether the plan should proceed.")
        self.assertTrue(result["review_only"])
        self.assertEqual(result["private_roles"], ["minister", "minister-router", "executive-judgment"])

    def test_k_broker_failure_degrades_gracefully(self) -> None:
        result = route("Should I accept this job offer?", broker_script=Path("Z:/minister-test/no-broker.py"))
        self.assertEqual(result["broker_status"], "UNAVAILABLE")
        self.assertFalse(result["broker_used"])
        self.assertEqual(result["shared"], [])
        self.assertIn("executive-judgment", result["private_roles"])

    def test_l_shared_scope_has_no_minister_copies(self) -> None:
        plugin_skills = Path(__file__).resolve().parents[1] / "skills"
        registry = json.loads((Path.home() / ".codex" / "ai-os" / "registry" / "skill-registry.json").read_text(encoding="utf-8"))
        shared = {
            "first-principles", "evidence-epistemics", "systems-thinking", "behavioral-psychology",
            "decision-science", "strategic-foresight", "game-theory-incentives", "risk-premortem",
            "adversarial-red-team",
        }
        records = {item["id"]: item for item in registry["skills"]}
        for skill_id in shared:
            self.assertEqual(records[skill_id]["scope"], "shared")
            self.assertTrue(Path(records[skill_id]["location"]).is_dir())
            self.assertFalse((plugin_skills / skill_id).exists())

    def test_skills_diagnostic_lists_registered_core(self) -> None:
        result = route("skills")
        ids = {item["id"] for item in result["shared_inventory"]}
        self.assertEqual(result["broker_status"], "AVAILABLE")
        self.assertTrue({"skill-broker", "decision-science", "adversarial-red-team"}.issubset(ids))

    def test_private_authority_contract_is_present(self) -> None:
        skill = (Path(__file__).resolve().parents[1] / "skills" / "executive-judgment" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("only final decision authority", skill)
        self.assertIn("Correctness is more important than agreement", skill)
        self.assertIn("DEFER", skill)


if __name__ == "__main__":
    unittest.main(verbosity=2)
