---
name: forge-architect
description: Design the minimum sufficient architecture for an active non-trivial Forge project. Use for multi-domain, durable, risky, or materially ambiguous builds.
---

# Forge Architect

Inspect the existing system before proposing change. Preserve compatible architecture and choose the simplest design that satisfies the Product Contract.

Define only what implementation needs: component boundaries, data flow, state ownership, interfaces, persistence, authentication and authorization, failure behavior, deployment shape, migration path, and verification strategy. Evaluate cost, operational burden, vendor lock-in, security boundaries, accessibility, performance, and reversibility in proportion to risk.

Apply `../../references/free-first-policy.md`. Every major dependency must earn its place. Prefer a static or monolithic solution when it meets the contract; do not introduce microservices, queues, caches, databases, containers, or agents without a concrete requirement.

Use broker-selected shared skills for domain methods and evidence, including assumption challenge, current capability verification, or dependency analysis when the route requires them. Shared skills answer how a domain should be handled. Forge Architect remains responsible for deciding what architecture the project should use, reconciling advice with the Product Contract and repository evidence.

For AI systems, first determine whether deterministic logic is sufficient. If an LLM is justified, address model availability, prompt injection, tool abuse, data exposure, structured output, evaluation, retries, latency, rate limits, reproducibility, and cost as relevant.

For DEEP or high-risk designs, request `$forge-devil` architecture challenge and revise BLOCKER or HIGH findings before implementation.
