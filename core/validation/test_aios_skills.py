#!/usr/bin/env python3
"""Tests A to I for Personal AI OS Skill Core v0.1."""

from __future__ import annotations

import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


BIN_DIR = Path(__file__).resolve().parents[1] / "broker"
sys.path.insert(0, str(BIN_DIR))

from aios_skills import (  # noqa: E402
    DEFAULT_REGISTRY,
    broker,
    capability_candidates,
    duplicate_report,
    load_json,
    validate_registry,
)


class AIOSSkillCoreTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.registry = load_json(DEFAULT_REGISTRY)

    def test_a_basic_discovery(self) -> None:
        result = broker(self.registry, None, ["first-principles-analysis"])
        self.assertEqual([item["id"] for item in result["selected"]], ["first-principles"])
        self.assertEqual(result["missing_capabilities"], [])

    def test_b_multiple_capabilities(self) -> None:
        result = broker(
            self.registry,
            "Evaluate whether this plan is based on unsupported assumptions and identify system-wide consequences.",
            [],
        )
        self.assertEqual(
            {item["id"] for item in result["selected"]},
            {"first-principles", "evidence-epistemics", "systems-thinking"},
        )
        self.assertEqual(
            set(result["required_capabilities"]),
            {"assumption-challenge", "evidence-quality-analysis", "systems-analysis"},
        )

    def test_c_minimum_sufficient_routing(self) -> None:
        result = broker(self.registry, "Challenge the fundamental assumptions behind this idea.", [])
        self.assertEqual([item["id"] for item in result["selected"]], ["first-principles"])

    def test_d_unknown_capability(self) -> None:
        result = broker(self.registry, None, ["quantum-teleportation-operations"])
        self.assertEqual(result["selected"], [])
        self.assertEqual(result["missing_capabilities"], ["quantum-teleportation-operations"])

    def test_e_disabled_skill_is_not_selected(self) -> None:
        registry = copy.deepcopy(self.registry)
        entry = next(item for item in registry["skills"] if item["id"] == "first-principles")
        entry.update({"enabled": False, "status": "DISABLED", "trust_level": "DISABLED"})
        candidates, rejected = capability_candidates(registry, "first-principles-analysis")
        self.assertEqual(candidates, [])
        self.assertEqual(rejected[0]["id"], "first-principles")

    def test_f_authoritative_beats_community_for_equivalent_capability(self) -> None:
        registry = {"schema_version": "0.1.0", "registry_version": "0.1.0", "skills": []}
        template = copy.deepcopy(next(item for item in self.registry["skills"] if item["id"] == "first-principles"))
        for skill_id, trust, publisher_type in (
            ("candidate-authoritative", "AUTHORITATIVE", "vendor"),
            ("candidate-community", "COMMUNITY", "community"),
        ):
            entry = copy.deepcopy(template)
            entry.update({
                "id": skill_id,
                "name": skill_id,
                "scope": "external",
                "location": f"metadata://{skill_id}",
                "trust_level": trust,
                "publisher": {"name": skill_id, "type": publisher_type},
                "capabilities": ["equivalent-capability"],
            })
            registry["skills"].append(entry)
        candidates, _ = capability_candidates(registry, "equivalent-capability")
        self.assertEqual(candidates[0]["id"], "candidate-authoritative")

    def test_g_duplicate_metadata_is_detected(self) -> None:
        registry = copy.deepcopy(self.registry)
        registry["skills"].append(copy.deepcopy(registry["skills"][0]))
        duplicates = duplicate_report(registry)
        self.assertIn("skill-broker", duplicates["duplicate_ids"])
        result = validate_registry(registry, Path("temporary-registry.json"), run_official=False)
        self.assertFalse(result["passed"])
        self.assertTrue(any("duplicate skill id" in error for error in result["errors"]))

    def test_h_broken_reference_fails_validation(self) -> None:
        with tempfile.TemporaryDirectory(prefix="aios-broken-ref-") as temporary:
            skill_root = Path(temporary) / "first-principles"
            skill_root.mkdir()
            (skill_root / "SKILL.md").write_text(
                "---\nname: first-principles\ndescription: Valid temporary test description.\n---\n\n[Broken](references/missing.md)\n",
                encoding="utf-8",
            )
            registry = copy.deepcopy(self.registry)
            entry = next(item for item in registry["skills"] if item["id"] == "first-principles")
            entry["location"] = str(skill_root)
            result = validate_registry(registry, Path(temporary) / "registry.json", run_official=False)
            self.assertFalse(result["passed"])
            self.assertTrue(any("broken reference link" in error for error in result["errors"]))

    def test_i_shared_skills_are_outside_plugin_roots(self) -> None:
        for entry in self.registry["skills"]:
            self.assertEqual(entry["scope"], "shared")
            path = Path(entry["location"])
            self.assertTrue((path / "SKILL.md").exists())
            self.assertNotIn("plugins", {part.lower() for part in path.parts})

    def test_maintenance_disable_enable_remove_is_isolated(self) -> None:
        with tempfile.TemporaryDirectory(prefix="aios-maintenance-") as temporary:
            registry_path = Path(temporary) / "registry.json"
            registry_path.write_text(json.dumps(self.registry), encoding="utf-8")
            cli = BIN_DIR / "aios_skills.py"

            for arguments in (
                ["disable", "--id", "systems-thinking"],
                ["enable", "--id", "systems-thinking", "--trust-level", "VERIFIED"],
                ["remove", "--id", "systems-thinking"],
            ):
                completed = subprocess.run(
                    [sys.executable, "-B", str(cli), "--registry", str(registry_path), *arguments],
                    capture_output=True,
                    text=True,
                    check=False,
                )
                self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)

            final_registry = json.loads(registry_path.read_text(encoding="utf-8"))
            self.assertNotIn("systems-thinking", {entry["id"] for entry in final_registry["skills"]})
            self.assertTrue(Path(next(entry for entry in self.registry["skills"] if entry["id"] == "systems-thinking")["location"]).exists())

    def test_maintenance_add_and_update_validate_candidate(self) -> None:
        with tempfile.TemporaryDirectory(prefix="aios-add-update-") as temporary:
            temporary_root = Path(temporary)
            registry_path = temporary_root / "registry.json"
            registry_path.write_text(json.dumps(self.registry), encoding="utf-8")
            entry = copy.deepcopy(next(item for item in self.registry["skills"] if item["id"] == "first-principles"))
            entry.update({
                "id": "example-external-skill",
                "name": "Example External Skill",
                "scope": "external",
                "location": "metadata://example-external-skill",
                "publisher": {"name": "Example Community", "type": "community"},
                "trust_level": "COMMUNITY",
                "capabilities": ["example-capability"],
                "triggers": ["use example capability"],
            })
            entry_path = temporary_root / "entry.json"
            entry_path.write_text(json.dumps(entry), encoding="utf-8")
            cli = BIN_DIR / "aios_skills.py"

            added = subprocess.run(
                [sys.executable, "-B", str(cli), "--registry", str(registry_path), "add", "--entry-file", str(entry_path)],
                capture_output=True, text=True, check=False,
            )
            self.assertEqual(added.returncode, 0, added.stdout + added.stderr)

            entry["notes"] = "Updated through the full-record maintenance contract."
            entry_path.write_text(json.dumps(entry), encoding="utf-8")
            updated = subprocess.run(
                [sys.executable, "-B", str(cli), "--registry", str(registry_path), "update", "--entry-file", str(entry_path)],
                capture_output=True, text=True, check=False,
            )
            self.assertEqual(updated.returncode, 0, updated.stdout + updated.stderr)
            persisted = next(item for item in json.loads(registry_path.read_text(encoding="utf-8"))["skills"] if item["id"] == entry["id"])
            self.assertEqual(persisted["notes"], entry["notes"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
