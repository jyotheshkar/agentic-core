# Current Codex Skill Environment, 2026-08-31

- Runtime inspected: desktop bundled `codex-cli 0.151.0-alpha.7.2`; plugins and native skill search are enabled.
- Supported skill shape: one direct skill folder containing `SKILL.md` with YAML `name` and `description`; optional `agents/openai.yaml`, `references/`, `scripts/`, and `assets/`.
- User-scoped skill root: `<HOME>\.codex\skills`. This is the location used by the bundled skill creator and current discovery catalog. `<HOME>\.agents\skills` was absent and was not invented.
- Personal plugin source root: `<HOME>\plugins`; installed plugin cache: `<HOME>\.codex\plugins\cache\personal`.
- User skills are discovered independently of plugins. Plugin-scoped skills are versioned inside their plugin cache and remain owned by that plugin.
- Existing personal plugins at inspection: Forge and Devil. Minister was not installed. Existing user skill `hatch-pet` and system skills were preserved. External skills are supplied by installed bundled, curated, and Claude Cowork plugin caches.
- Metadata inspection: Codex exposes skill names and descriptions for selection before loading a full `SKILL.md`. The AI OS registry supplements this with capabilities, trust, status, compatibility, provenance, dependencies, and activation cost.
- Official local validation: `<HOME>\.codex\skills\.system\skill-creator\scripts\quick_validate.py`. AI OS validation calls it and adds registry, reference, dependency, provenance, duplication, size, and script checks.
- Symlinks: a local Windows symbolic-link creation test failed because administrator privilege is required. v0.1 does not depend on symlinks.
- Cross-plugin evidence: a fresh read-only Codex process invoked Forge, loaded user-scoped `skill-broker` and `first-principles`, and returned `CROSS_PLUGIN_REUSE PASS` with distinct plugin and user-skill paths.
