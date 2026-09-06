# Capability-Family Decisions

Status: PASS, reviewed 2026-09-06.

Agentic Core has five active authority-bearing plugins: MOA, Minister, Scout, Forge, and Audit. Devil is retained as a legacy, non-routable plugin. The following planned family labels describe capability families, not a quota for additional plugins.

| Family | Architecture decision | Owner and safeguards | Reason |
| --- | --- | --- | --- |
| Audit | Standalone plugin | Audit owns independent assurance of supplied artifacts, evidence, policy conformance, release readiness, residual risk, and completion claims. It issues inspectable findings and assurance recommendations. | The user selected a visible fifth agent. Its strict non-overlap contract prevents it from replacing Scout research, Forge implementation, Minister judgment, or MOA orchestration. |
| Fix | Forge task family | Forge implements a bounded repair. MOA retains routing and Minister remains mandatory where the repair has substantive or consequential trade-offs. | Repair is engineering execution, not a separate authority. |
| Design | Composed Minister plus Forge workflow | Minister judges outcome fit and constraints. Forge owns technical/product design. Shared product discovery, experience design, and architecture skills are broker-selected. | Design crosses decision and implementation but needs no fifth decision or build agent. |
| Launch | Guarded composed workflow | MOA coordinates Minister, Forge, Verification, and independent Audit. Any paid, credentialed, destructive, ownership-changing, public, or production action remains a user gate. | A launch plugin could not bypass the user’s external-action authority and would duplicate release gates. |
| Lab | Bounded experiment workflow | Scout frames current evidence and unknowns, Forge implements safe local experiments, Minister judges whether evidence changes a decision, and Audit checks claims. | Experimental work is a workflow, not an autonomous real-world laboratory authority. Wet-lab, clinical, licensed, or otherwise specialist execution remains explicitly missing and blocked. |

## Admission rule for future standalone agents

A new plugin is justified only if it has a durable, non-overlapping authority, reusable private workflow, registrable lifecycle, independent acceptance tests, and a user-value case that cannot be met through shared skills or composed workflows. Audit meets this rule because its independent assurance authority, finding contract, release gate, and adversarial review are both visible and non-overlapping. Future family labels alone do not satisfy the rule.
