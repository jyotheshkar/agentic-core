---
name: minister-router
description: Route an active Minister decision to LIGHT, STANDARD, COUNCIL, or CRITICAL depth and the minimum sufficient AI OS reasoning capabilities. Use only inside a Minister workflow.
---

# Minister Router

Classify the decision by stakes, reversibility, uncertainty, time horizon, external control, and interaction complexity. Use the deterministic helper as a baseline:

```text
python ../../scripts/route_minister.py "<decision>"
```

Modes guide depth, not answer length:

- LIGHT: trivial, low-cost, reversible choice. Usually 1 to 3 shared skills.
- STANDARD: meaningful but bounded decision. Usually 3 to 6 shared skills.
- COUNCIL: consequential choice with several lenses or external actors. Usually 5 to 9 shared skills.
- CRITICAL: difficult-to-reverse life, career, financial, legal, immigration, or strategic decision. Use every materially relevant lens, not every installed skill.

Convert the decision into capability IDs before selecting skills. Invoke `$skill-broker`, prefer VERIFIED or stronger compatible entries, and load full instructions only after selection. Retain a skill only if it contributes a distinct material capability. Do not hard-code future shared skill names, privately copy shared expertise, or hallucinate a missing match.

Always route `minister`, `minister-router`, and `executive-judgment` for substantive decisions. Mark Forge plans as review-only. Minister may judge whether a plan should proceed but must not implement it.

Return mode, private roles, required shared capabilities, selected shared skills, missing capabilities, broker status, decision-reversing unknowns, and routing exclusions. Keep this internal unless diagnostics or a limitation is decision-relevant.
