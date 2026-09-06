---
name: llm-engineering
description: Design reliable language-model workflows using task contracts, model selection, prompting, tools, structured outputs, evaluation, guardrails, and cost controls. Use for LLM-backed product behavior, not ordinary deterministic logic.
---

# LLM Engineering

## Workflow

1. Define the task contract, permitted evidence, failure modes, and non-LLM baseline.
2. Choose the minimum capable model and context, tool, and output structure.
3. Build eval cases before optimizing prompts or adding agent complexity.
4. Add validation, refusal, fallback, observability, privacy, and explicit cost ceilings.

## Output contract

A tested LLM workflow with contract, evals, controls, and known limitations.

State evidence, assumptions, uncertainty, and missing capability separately when they affect the result. Stop or defer when a decision-reversing unknown cannot be resolved safely.

## Boundary

Do not expose secrets, grant authority through prompts, or treat fluent output as verified truth.

This skill is advisory expertise. MOA owns orchestration, Minister owns strategic judgment, Forge owns engineering implementation, and verification owns completion evidence.

## Evidence basis

Use the relevant parts of the [primary guidance](https://platform.openai.com/docs/guides) when standards or formal evidence are material. Verify currency before making a time-sensitive claim.
