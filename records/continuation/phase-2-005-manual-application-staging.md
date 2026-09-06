# Phase 2.005: Manual Application Staging

## Status

VERIFIED WITH LIMITATIONS

## Goal

Create a local, review-required staging-package contract for an already qualified role. It is not an Applying Agent and must never submit an application, solve a CAPTCHA, contact anyone, or claim a visa/sponsorship outcome.

## Scope

- Generate deterministic package metadata and reviewer tasks only.
- Require the role-qualification gate created in Phase 2.002.
- Make missing user-provided CV or cover-letter content an explicit review requirement, not an invented draft.

## Acceptance Criteria

1. Ineligible roles produce a refusal state, not a staging package.
2. Eligible roles produce a `READY_FOR_USER_REVIEW` local payload only.
3. The payload contains no external-action command, credential, personal document content, or eligibility claim.
4. Tests cover qualifying boundary, non-confirmed sponsorship, low confidence, and missing user materials.

## Affected Paths

- `products/job-searching-agent/site/lib/**`
- `products/job-searching-agent/site/tests/**`

## Rollback and Recovery

- Revert only this phase's product library and tests.
- No file package, database record, browser action, or contact is created by this foundation phase.

## Verification Evidence

- `npm run test`: PASS, 27 tests across seven files.
- `npm run lint`: PASS.
- `npm run build -- --outDir dist-phase-2-staging-final-verification`: PASS.
- Limitation: this phase defines local staging metadata only. Tailored CV and cover-letter content requires user-provided source materials and a separate review step.
