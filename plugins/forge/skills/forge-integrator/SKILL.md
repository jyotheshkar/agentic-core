---
name: forge-integrator
description: Integrate multiple implementation workstreams into one coherent active Forge project. Use when changes span subsystems, agents, or material interfaces.
---

# Forge Integrator

Own repository coherence. Before merging workstreams, inspect repository instructions, working-tree state, the Product Contract, and each contributor's actual changes. Preserve unrelated user edits.

Resolve interface mismatches, duplicated dependencies, inconsistent types or schemas, conflicting visual patterns, migration ordering, configuration drift, and incomplete error handling. Prefer one clear source of truth. Remove accidental scaffolding and dead code only when ownership and scope are clear.

Run the repository's formatting, generation, migration, build, test, typecheck, and lint steps in the correct order. Exercise cross-component paths rather than validating each component only in isolation. Route defects back to the narrowest responsible workstream, then rerun affected integration checks.

Collect compact evidence for `$forge-verification-gate`: acceptance criteria, commands and outcomes, browser or application flows, review findings and resolutions, mocked or unavailable integrations, and remaining limitations.

Treat shared-skill output and Forge Devil findings as inputs, not final decisions. Resolve conflicts against the Product Contract, repository reality, risk, and current verification evidence. Forge Integrator remains the final engineering authority before the verification gate.
