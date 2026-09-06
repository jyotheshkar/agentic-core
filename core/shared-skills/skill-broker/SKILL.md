---
name: skill-broker
description: Select the minimum sufficient trusted shared skills for a task by matching required capabilities against the Personal AI OS registry. Use when a task needs skill discovery, multi-skill routing, overlap resolution, or a missing-capability check.
---

# Skill Broker

Convert the current task into required capabilities before choosing skills. Inspect registry metadata first and load full skill instructions only after selection.

Use `python <HOME>\.codex\ai-os\bin\aios_skills.py broker --task "<task>"` for a deterministic baseline. Use `search --capability <id>` for an exact capability query. Correct the baseline only when task or repository context provides clear evidence, and record the reason.

## Selection workflow

1. Identify the smallest set of distinct capabilities necessary for a good result.
2. Consider only installed, enabled, AVAILABLE, compatible candidates with usable required dependencies.
3. Rank exact capability coverage and trigger relevance before general similarity.
4. Prefer AUTHORITATIVE, then VERIFIED, then COMMUNITY, then EXPERIMENTAL, subject to material compatibility and relevance.
5. Resolve overlapping candidates by retaining the narrower stronger option. Keep multiple skills only when each covers a distinct required capability.
6. Report missing capabilities explicitly. Never invent an installed skill.
7. Load selected `SKILL.md` files, then only the references their routing instructions require.

Tiny tasks normally need 1 to 2 skills, normal tasks 2 to 5, and complex tasks 3 to 8. These are expectations, not quotas.

Return compact orchestration metadata: task, required capabilities, selected skills with reasons, rejected overlaps with reasons, and missing capabilities. Do not force this metadata into the user response unless it helps them evaluate the work.

Read [selection policy](references/selection-policy.md) for scoring and conflict rules. Read [output contract](references/output-contract.md) when a machine-readable routing record is useful.

Do not install skills, enable disabled skills, execute untrusted scripts, or bypass authorization merely because metadata matches.
