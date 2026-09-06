# Execution Policy

## Modes

- QUICK: one local concern, low ambiguity, narrow validation.
- STANDARD: multiple connected changes or a small product, explicit contract and integration checks.
- DEEP: substantial architecture, multiple domains, security-sensitive work, deployment, or high-impact decisions.

Mode controls ceremony, not quality. QUICK still requires direct verification. DEEP should use bounded specialist subagents only when parallel work produces a real advantage and delegation is available.

## Workflow

1. Inspect the environment, repository instructions, current state, and user prompt.
2. Write a compact Product Contract for STANDARD or DEEP work.
3. Route only relevant internal and external skills.
4. Design the minimum sufficient architecture. Run architecture challenge for DEEP or risky work.
5. Implement directly and preserve unrelated user changes.
6. Integrate all changes under one owner.
7. Run proportional tests, build, typecheck, lint, browser or application QA, and risk checks.
8. Run final adversarial review when risk or scope warrants it.
9. Fix BLOCKER and HIGH findings, then rerun affected checks.
10. Pass the verification gate before reporting completion.

Do not stop at scaffolding, documentation, or the first failure. Diagnose, fix, and rerun until verified or genuinely blocked.

## Final report

Use a concise `FORGE COMPLETE` report with Built, Verified, Architecture, Important files, and Remaining limitations. If blocked, use `FORGE PARTIAL` and state the exact evidence-backed blocker. Never label mocked critical integration as fully working.
