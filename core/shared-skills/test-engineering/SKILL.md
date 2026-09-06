---
name: test-engineering
description: Design an efficient test strategy across unit, integration, contract, system, regression, and exploratory checks based on risk and observable behavior. Use when verification scope or test architecture needs deliberate design.
---

# Test Engineering

## Workflow

1. Map requirements, risks, failure modes, and observability to test objectives.
2. Choose the lowest test level that provides reliable evidence, then add cross-boundary tests where needed.
3. Cover positive, negative, boundary, concurrency, recovery, and permission behavior proportionately.
4. Make failures diagnosable and keep flaky or environment-dependent tests visible rather than ignored.

## Output contract

A traceable test strategy and executable checks with clear evidence and limitations.

State evidence, assumptions, uncertainty, and missing capability separately when they affect the result. Stop or defer when a decision-reversing unknown cannot be resolved safely.

## Boundary

Passing tests show only what was checked in the tested environment. They do not prove absence of defects.

This skill is advisory expertise. MOA owns orchestration, Minister owns strategic judgment, Forge owns engineering implementation, and verification owns completion evidence.

## Evidence basis

Use the relevant parts of the [primary guidance](https://www.istqb.org/certifications/certified-tester-foundation-level) when standards or formal evidence are material. Verify currency before making a time-sensitive claim.
