# System Architecture

Agentic Core is a capability-routed, authority-separated operating architecture composed within the Codex runtime.

```text
User
  -> MOA: intent, routing, orchestration, completion governance
  -> Minister: decision conditions and final judgment
  -> Scout: current evidence and provenance
  -> Forge: bounded engineering and verification
  -> Shared Skill Broker: minimum sufficient specialist capability
  -> Independent Audit workflow: policy, evidence-quality, release-claim, and residual-risk review
```

Direct plugin-to-plugin process execution is currently `EMULATED`. The host composes the registered contracts inside one task. This is not presented as a distributed multi-agent runtime.

## Source ownership

- Installed plugin folders remain the live runtime source.
- This repository stores reviewed, sanitised engineering snapshots.
- External products may consume Agentic Core only through explicit interfaces. Their data, source, testing, and deployment are outside this repository and this control plane.
