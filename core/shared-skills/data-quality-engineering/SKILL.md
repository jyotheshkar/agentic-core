---
name: data-quality-engineering
description: Assess and improve dataset fitness through schema, lineage, coverage, representativeness, leakage, label quality, drift, privacy, and reproducible validation. Use for ML or analytical datasets with material quality risk.
---

# Data Quality Engineering

## Workflow

1. Define intended use, population, unit, time window, target, and collection process.
2. Profile schema, missingness, duplicates, outliers, labels, splits, and lineage.
3. Test representativeness, leakage, temporal validity, privacy, and subgroup coverage.
4. Create reproducible validation gates and monitoring for material drift.

## Output contract

A dataset fitness report with failures, evidence, remediation, and use limitations.

State evidence, assumptions, uncertainty, and missing capability separately when they affect the result. Stop or defer when a decision-reversing unknown cannot be resolved safely.

## Boundary

A clean schema does not establish representativeness, fairness, or causal validity.

This skill is advisory expertise. MOA owns orchestration, Minister owns strategic judgment, Forge owns engineering implementation, and verification owns completion evidence.

## Evidence basis

Use the relevant parts of the [primary guidance](https://airc.nist.gov/airmf-resources/airmf/) when standards or formal evidence are material. Verify currency before making a time-sensitive claim.
