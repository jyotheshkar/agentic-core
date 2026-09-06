---
name: scout-completion-gate
description: Decide whether an active Scout investigation is complete, limited, partial, blocked, or unsupported based on provenance, freshness, contradiction, scope, and handoff quality. Use before any research completion claim.
---

# Scout Completion Gate

Read [completion-contract.md](../../references/completion-contract.md) and evaluate proportionately against the research contract.

## Gate checks

Confirm that the objective is answered or explicitly unresolved, material claims have valid provenance, current claims use current evidence, authoritative sources were preferred, contradictions were checked, decision-reversing unknowns remain visible, inferences are labelled, citations directly support nearby claims, inspected pages replace snippets where possible, dates and jurisdiction are recorded where needed, the result does not overstate exhaustiveness, and the bounded handoff is sufficient.

## Status rules

- `COMPLETE`: every material check passes and no material limitation is named or remains.
- `COMPLETE WITH LIMITATIONS`: the answer is usable and all material limitations are named.
- `PARTIAL`: some questions or validation checks remain incomplete.
- `BLOCKED`: a required resource, permission, tool, or external condition is inaccessible. Name it precisely.
- `INSUFFICIENT EVIDENCE`: available evidence cannot support a reliable answer. Name the evidence required.

Missing citations, fabricated or inaccessible provenance, stale current evidence, unresolved material contradiction, unlabeled inference, scope drift, or an incomplete handoff blocks unqualified `COMPLETE`.

Hard invariant: if the output contains a non-empty `MATERIAL LIMITATIONS` or `LIMITATIONS` field, the status cannot be `COMPLETE`. Use `COMPLETE WITH LIMITATIONS` when the answer remains usable, otherwise use `PARTIAL`, `BLOCKED`, or `INSUFFICIENT EVIDENCE`.

## Boundaries and failure handling

Do not lower the gate because the investigation took a long time or many sources were found. Do not turn a platform limitation into an evidence claim. Do not claim a draft or suggested external action occurred.

## Output

Return STATUS, PASSED CHECKS, FAILED CHECKS, LIMITATIONS, UNANSWERED QUESTIONS, BLOCKER OR REQUIRED EVIDENCE, DECISION-REVERSING UNKNOWNS, and NEXT ACTION. If the status is not `COMPLETE`, state exactly what prevents it.
