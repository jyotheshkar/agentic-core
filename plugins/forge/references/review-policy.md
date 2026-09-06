# Review Policy

Forge review is independent from implementation when risk justifies it. The reviewer tests assumptions and inspects actual diffs and evidence rather than endorsing the plan.

Severity:

- BLOCKER: unsafe, data-loss-prone, nonfunctional core path, false success claim, or product contract failure.
- HIGH: serious security, correctness, accessibility, reliability, or maintainability defect likely to affect real use.
- MEDIUM: material but non-blocking weakness.
- LOW: polish or optional improvement.

Completion is forbidden while any BLOCKER or HIGH finding remains unresolved. Fix findings and rerun affected validation. A genuine external blocker must be declared precisely rather than silently downgraded.

Architecture challenge checks necessity, simpler alternatives, failure modes, security boundaries, cost, and operational burden. Final challenge checks the product contract, actual implementation, test evidence, user-visible behavior, and accuracy of the proposed completion report.
