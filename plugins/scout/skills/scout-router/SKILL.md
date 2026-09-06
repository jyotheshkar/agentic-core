---
name: scout-router
description: Select QUICK, STANDARD, DEEP, or CRITICAL research depth and the minimum sufficient shared capabilities for an active Scout investigation. Do not use for MOA agent selection or final judgment.
---

# Scout Router

Classify from the number of material claims, consequence, reversibility, uncertainty, source diversity, and freshness need. Topic seriousness alone does not justify CRITICAL.

## Activation

Use after the research request and downstream use are understood. Do not activate for `@Scout skills` or `@Scout health`, and do not route non-research implementation work.

## Mode rules

- QUICK: one narrow fact, definition, status, date, or official-page claim. Use one or two shared skills and one or a few strong sources.
- STANDARD: connected claims, normal comparisons, company or programme investigation, or several technical facts. Use two to four shared skills.
- DEEP: major career or education research, sponsorship investigation, substantial academic or market research, or several dependent subquestions. Use three to six shared skills.
- CRITICAL: actual high-consequence uncertainty involving immigration, work rights, legal or regulatory rules, material financial downside, health evidence, security-sensitive decisions, or difficult-to-reverse cost. Use only justified capabilities, even if fewer than DEEP.

Read [research-modes.md](../../references/research-modes.md) for the detailed mode contract.

## Capability selection

Pass required capabilities to `$skill-broker` and accept only installed, enabled, trusted canonical skills. Prefer source verification and currency checking for QUICK. Add research planning, discovery, epistemic analysis, and synthesis only when the question requires them. Exclude irrelevant engineering skills unless the downstream task truly needs technical specialist evidence.

If the broker is unavailable, report `BLOCKED`, list the missing capabilities, and do not claim the shared methods were used. If no registered capability covers a necessary method, surface the gap to MOA.

## Output

Return MODE, REASON, REQUIRED CAPABILITIES, SELECTED SHARED SKILLS, REJECTED IRRELEVANT SKILLS, FRESHNESS REQUIREMENT, ESCALATION REASON, BROKER STATUS, and MISSING CAPABILITIES.
