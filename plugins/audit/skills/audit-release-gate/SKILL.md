---
name: audit-release-gate
description: Independently assess release-readiness and completion claims against current verification evidence and named limitations.
---

# Audit Release Gate

Require inspectable deliverables, current verification evidence, policy conformance, residual-risk assessment, preserved limitations, and appropriate Minister final judgment. A critical or high unresolved finding yields `REWORK`; decision-reversing missing evidence yields `DEFER`; an external dependency yields `BLOCKED`. Limitations require `APPROVE WITH CONDITIONS`, never unconditional approval.

Do not deploy, publish, change ownership, spend money, access credentials, or take an external action.
