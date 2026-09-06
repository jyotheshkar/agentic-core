# Verification Contract

Claims require fresh evidence from the current work:

| Claim | Minimum evidence |
| --- | --- |
| Built | Requested files and behavior exist in the target workspace |
| Tests pass | Relevant test command completed successfully |
| Build passes | Production or requested build completed successfully |
| Type-safe or lint-clean | Named typecheck or lint command completed successfully |
| UI works | Relevant flows exercised in a real browser or application where tooling permits |
| Deployed | Deployment command or platform state confirms the current version is live |
| Secure | Scoped checks support the claim, with limitations stated |
| Fully working | No critical integration is mocked or unverified |

Select checks proportionally. Typical frontend work needs build, interaction, responsiveness, keyboard and accessibility checks. Backend work needs tests, migrations or schema checks, authorization boundaries, and error-path checks. AI work needs deterministic behavior where possible plus prompt-injection, data-exposure, failure, evaluation, latency, and cost checks relevant to its design.

Record commands, exit status, and meaningful outcomes. A failed check blocks completion until fixed and rerun or declared as an exact unresolved blocker. Run `scripts/verify_gate.py <report.json>` when a substantial project produces a machine-readable gate report.
