from __future__ import annotations

import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class RepositoryBaselineTests(unittest.TestCase):
    def test_agent_registry_has_expected_authority_components(self) -> None:
        registry = json.loads((ROOT / "core/registry/agent-registry.json").read_text(encoding="utf-8"))
        agents = {agent["id"]: agent for agent in registry["agents"]}
        self.assertEqual({"minister", "scout", "forge", "moa", "audit", "devil"}, set(agents))
        self.assertEqual({"minister", "scout", "forge", "moa", "audit"}, {agent_id for agent_id, agent in agents.items() if agent["enabled"] and agent["status"] == "AVAILABLE"})
        self.assertFalse(agents["devil"]["enabled"])

    def test_skill_registry_has_39_unique_records(self) -> None:
        registry = json.loads((ROOT / "core/registry/skill-registry.json").read_text(encoding="utf-8"))
        identifiers = [skill["id"] for skill in registry["skills"]]
        self.assertEqual(39, len(identifiers))
        self.assertEqual(len(identifiers), len(set(identifiers)))
        for skill in registry["skills"]:
            self.assertTrue((ROOT / skill["location"]).is_dir(), skill["id"])

    def test_import_manifest_contains_no_private_home_path(self) -> None:
        manifest = (ROOT / "records/imports/agentic-core-runtime-baseline.json").read_text(encoding="utf-8")
        self.assertNotIn("C:\\Users\\", manifest)


if __name__ == "__main__":
    unittest.main()
