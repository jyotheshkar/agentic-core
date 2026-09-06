---
name: moa-capability-discovery
description: Discover enabled agents and trusted shared skills for an active MOA task from live registries and native Codex plugin state. Use only inside an MOA workflow or MOA diagnostics.
---

# MOA Capability Discovery

Inspect `<HOME>\.codex\ai-os\registry\agent-registry.json` and `<HOME>\.codex\ai-os\registry\skill-registry.json`. For current native discovery, use `python ../../scripts/moa_core.py agents --discover`.

Consider only records that are enabled, AVAILABLE, installed where required, and have usable dependencies. Treat public capability plugins as tools or specialist capabilities unless their metadata establishes an autonomous agent role. Invoke `$skill-broker` for shared skill selection.

Return available agents, relevant capability plugins, selected shared skills, missing capabilities, trust state, and stale or contradictory metadata. Do not install, enable, or fabricate anything merely because the task would benefit from it.
