---
name: retrieval-augmented-generation
description: Design retrieval-augmented generation systems with grounded corpora, indexing, retrieval evaluation, citation behavior, context assembly, and abstention. Use when answers must draw from controlled evidence.
---

# Retrieval Augmented Generation

## Workflow

1. Define the answer domain, source authority, freshness, permissions, and abstention policy.
2. Design ingestion, chunking, metadata, indexing, retrieval, reranking, and context assembly from evidence.
3. Evaluate retrieval separately from generation using answerable and unanswerable cases.
4. Require source traceability and monitor corpus, index, and query drift.

## Output contract

A RAG design or implementation with retrieval evals, grounding controls, and citations.

State evidence, assumptions, uncertainty, and missing capability separately when they affect the result. Stop or defer when a decision-reversing unknown cannot be resolved safely.

## Boundary

Retrieval can surface irrelevant or stale content. It does not guarantee factual generation.

This skill is advisory expertise. MOA owns orchestration, Minister owns strategic judgment, Forge owns engineering implementation, and verification owns completion evidence.

## Evidence basis

Use the relevant parts of the [primary guidance](https://arxiv.org/abs/2005.11401) when standards or formal evidence are material. Verify currency before making a time-sensitive claim.
