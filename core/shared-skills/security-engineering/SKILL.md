---
name: security-engineering
description: Threat-model and implement proportionate security controls across identity, data, interfaces, dependencies, secrets, logging, and abuse cases. Use for material trust boundaries or explicit security work, not ritual activation on every edit.
---

# Security Engineering

## Workflow

1. Identify assets, actors, trust boundaries, abuse cases, and plausible impact.
2. Map controls to concrete threats across authentication, authorization, input, secrets, data, and dependencies.
3. Prefer fail-closed behavior and minimize privilege and sensitive-data exposure.
4. Verify controls with tests and record residual risk, ownership, and detection.

## Output contract

A threat model, implemented controls, verification evidence, and residual-risk register.

State evidence, assumptions, uncertainty, and missing capability separately when they affect the result. Stop or defer when a decision-reversing unknown cannot be resolved safely.

## Boundary

Do not claim secure or compliant from checklist presence alone. Verify the implemented control behavior.

This skill is advisory expertise. MOA owns orchestration, Minister owns strategic judgment, Forge owns engineering implementation, and verification owns completion evidence.

## Evidence basis

Use the relevant parts of the [primary guidance](https://owasp.org/www-project-application-security-verification-standard/) when standards or formal evidence are material. Verify currency before making a time-sensitive claim.
