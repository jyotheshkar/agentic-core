# Shared Core Baseline

## Objective

Import a sanitised, repository-contained snapshot of the registered shared skills and active Agentic Core plugins without changing the installed runtime.

## Baseline and gap

The live shared core passed 11 tests. The first repository run failed because the imported validation test still expected the live `bin` layout. The repository copy was changed to use `core/broker` and `core/registry` while the live source remained unchanged.

## Evidence

- 39 unique skill registry records.
- 38 domain skills plus Skill Broker.
- 11 of 11 repository-contained shared-core tests passed.
- Minister 14 of 14, Scout 17 of 17, Forge 21 of 21, and MOA 12 of 12 live-source tests passed.
- Sanitised import manifest contains 211 allowlisted source files.
- Secret and private-path scan passed after path sanitisation.

## Decision

PASS for baseline import. Live runtime remains authoritative until an explicit migration is approved.

