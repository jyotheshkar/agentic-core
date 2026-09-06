# Core Control Plane

The control plane is a set of portable contracts and records, not a hidden autonomous runtime. Its execution mode is `EMULATED_HOST_MEDIATED`: the Codex host composes installed skills within one task because direct plugin-to-plugin process invocation is unavailable.

## Lifecycle and recovery

Every component records purpose, non-goals, authority, inputs, outputs, dependency and routing context, baseline, change hypothesis, acceptance criteria, evidence, defects, residual risk, next action, and one lifecycle state: `PENDING`, `IN_PROGRESS`, `PASS`, `REWORK`, `DEFER`, `BLOCKED`, or `REJECTED`.

The permitted recovery path is `REWORK`, `DEFER`, or `BLOCKED` back to `IN_PROGRESS`. An identical external blocker may be retried at most three times. The third occurrence records `BLOCKED`; independent work continues. Terminal success is never inferred from artifact existence alone.

## Governing contracts

- Authority: MOA routes and governs completion. Minister is mandatory for substantive judgment and final outcome judgment. Scout owns evidence. Forge owns engineering. Audit is the standalone independent-assurance agent. The user controls consequential external action.
- Handoffs: every handoff carries the nine required fields in the handoff contract. Minister conditions survive every downstream handoff.
- Registry and broker: the Agent Registry advertises routable authorities. The Skill Broker chooses the smallest trusted shared skill set. Disabled, unavailable, or uninstalled records are not selectable.
- Conflict arbitration: MOA identifies the dispute, then assigns it to the domain authority: Minister for strategy, Scout for evidence, Forge for implementation, and MOA for scope or orchestration.
- Verification and release: verification evidence, independent audit, Minister final judgment, and completion governance are all required. A material limitation needs `APPROVE WITH CONDITIONS`; a decision-reversing unknown needs `DEFER`.
- Privacy and security: repository evidence is sanitised and synthetic. Secrets, profiles, private documents, operational product data, credentials, and paid actions are excluded.
- Observability: the append-only, hash-linked audit ledger records framing, routing, handoffs, arbitration, verification, and final completion status.

See [the control-plane implementation](../../core/control-plane/aios_control.py), [the demo record](../../records/integration/core-control-plane-demo.json), and [the capability-family decisions](CAPABILITY_FAMILY_DECISIONS.md).
