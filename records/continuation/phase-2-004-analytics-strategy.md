# Phase 2.004: Descriptive Analytics and Strategy

## Status

VERIFIED WITH LIMITATIONS

## Goal

Add descriptive response-rate analysis by role type, UK country, and fit-score band. Outputs may recommend evidence review, but cannot alter policy, thresholds, rankings, or application actions.

## Scope

- Aggregate explicit user-supplied lifecycle outcomes only.
- Report insufficient evidence rather than fabricate response rates.
- Keep deterministic gates authoritative and preserve the existing DQN/RL shadow-only boundary.

## Acceptance Criteria

1. Analytics distinguishes observed outcomes from missing outcomes.
2. Aggregates are available for role, country, and fit-score band.
3. Results contain no policy mutation, ranking update, threshold update, or external action.
4. Sparse groups are labelled insufficient evidence.
5. Tests cover sparse data, interview/rejection outcomes, and no-policy-change behavior.

## Affected Paths

- `products/job-searching-agent/site/lib/**`
- `products/job-searching-agent/site/app/api/performance/route.ts`
- `products/job-searching-agent/site/tests/**`

## Rollback and Recovery

- Revert only this phase's added or modified product files.
- No stored user state, threshold, model, or external account is changed by this phase.

## Verification Evidence

- Drizzle generated `0002_famous_korg.sql`, adding explicit `role_type` to the jobs contract.
- `npm run test`: PASS, 24 tests across six files.
- `npm run lint`: PASS.
- `npm run build -- --outDir dist-phase-2-analytics-verification`: PASS.
- Limitation: live outcome data has not been approved for D1 promotion. Synthetic empty output correctly returns `NO_POLICY_CHANGE` and requires explicit outcomes.
