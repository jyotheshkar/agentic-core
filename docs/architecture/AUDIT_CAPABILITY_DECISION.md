# Audit Capability Decision

## Decision

Do not add a standalone Audit plugin.

## Why

An additional plugin would duplicate existing authority boundaries:

- Scout independently audits source provenance, freshness, contradictions, and evidence completeness.
- Forge independently verifies implementation, tests, architecture, and release evidence.
- Minister independently judges strategic sufficiency and conditions.
- MOA governs the handoff sequence and prevents a returned artifact from being mistaken for an achieved outcome.

A standalone Audit plugin would have no distinct operational authority, would add another registry and cache lifecycle, and could create conflicting approval claims. The minimum sufficient design is an explicit audit workflow:

`Scout evidence review -> Forge technical verification -> Minister outcome judgment -> MOA completion governance`

## Required Audit Record

Every substantial release records scope, claims, evidence, test results, adversarial cases, security/privacy result, unresolved limitations, severity, rollback, and final Minister status. A critical or high finding blocks approval.

## Verification

The current core regression suite verifies Scout completion gates, Forge verification gates, Minister final judgment, and MOA completion governance. The Phase 2 continuation and iteration records implement the required release evidence format.
