---
name: risk-premortem
description: Assume a plan failed, work backward to identify material causes, and prioritize controls using likelihood, impact, detectability, recoverability, reversibility, dependencies, and early warnings. Use for consequential plans or concentrated downside.
---

# Risk Premortem

Focus on plausible failure mechanisms that change the plan, not an exhaustive fear list.

## Workflow

1. Define the plan, intended outcome, time horizon, risk boundary, and acceptable loss.
2. Assume the plan failed. Describe the concrete failure state before proposing causes.
3. Generate causes across execution, timing, finance, strategy, technology, security, legal or regulatory exposure, reputation, opportunity cost, external actors, hidden dependencies, and single points of failure as relevant.
4. Consolidate causes into distinct risks. Estimate likelihood, impact, detectability, recoverability, and reversibility using qualitative bands unless defensible data supports numbers.
5. Assign severity: CRITICAL, HIGH, MEDIUM, or LOW. Severity reflects impact and urgency, not theatrical wording.
6. For CRITICAL and HIGH risks, design prevention, contingency, owner, trigger, and an early warning signal. Prefer reducing exposure or creating an exit over merely monitoring.
7. Identify residual and tail risk after controls. State which assumptions or missing evidence limit the assessment.

For each major item return RISK, CAUSE, LIKELIHOOD, IMPACT, DETECTABILITY, RECOVERABILITY, MITIGATION, and EARLY WARNING SIGNAL. End with the dominant risk, stop conditions, and residual exposure.

Read [risk assessment method](references/risk-assessment-method.md) when the plan has multiple dependencies, irreversible exposure, or a need for ranked controls.

Do not multiply remote edge cases, hide correlated risks, call a risk controlled without an owner or mechanism, or imply that low probability means negligible exposure.
