---
name: forge-verification-gate
description: Decide whether an active Forge project may claim completion using current, proportional evidence. Use at the end of every Forge execution.
---

# Forge Verification Gate

Read `../../references/verification-contract.md` and evaluate the current Product Contract against actual artifacts and fresh command or interaction evidence.

Require:

- every required acceptance criterion is satisfied or named as an exact blocker;
- relevant tests and builds pass after the latest material change;
- browser or application flows are exercised where relevant and tooling permits;
- risk-proportional security, accessibility, performance, data, and AI checks are complete;
- all BLOCKER and HIGH review findings are resolved and affected checks rerun;
- critical external integrations are not mocked when claiming fully working;
- deployment is claimed only when current deployment evidence exists;
- limitations and skipped checks are stated precisely.

For substantial work, create a temporary JSON gate report and run `python ../../scripts/verify_gate.py <report.json>` from this skill directory. A nonzero result forbids completion. Fix and rerun when possible. Do not reinterpret a failed gate as success.

Return `PASS` with supported claims and evidence, or `FAIL` with exact remaining blockers. Forge's final response must match this decision.
