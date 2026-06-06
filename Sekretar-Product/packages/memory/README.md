# Memory Package

Framework-agnostic foundation package for the SekretaR Memory block.

Memory is the Account-owned knowledge layer of Sekretar-Product. It preserves
meaningful durable knowledge with provenance, confidence, lifecycle, correction,
contradiction, and forgetting rules.

This package is based on:

- `docs/architecture/memory-foundation-1.0.md`
- `docs/architecture/memory-vision-1.0.md`
- `docs/architecture/product-vision-1.0.md`
- `packages/identity`
- `packages/product_api`

## Current Status

This is the Memory Foundation Package Skeleton.

It intentionally contains no business logic, no repository implementation, no
service implementation, no FastAPI endpoints, no database design, no RAG, no
embeddings, and no infrastructure integration.

## Phase 1 Target

The first implementation phase should introduce framework-agnostic domain
objects and contracts for:

- Knowledge items;
- Memory sources;
- Candidate knowledge;
- Provenance;
- Confidence;
- Lifecycle records;
- Knowledge relations;
- Corrections;
- Contradictions;
- Memory context;
- Domain events;
- Repository interfaces;
- Domain service interfaces;
- Domain policies;
- Unit tests with in-memory test repositories.

## Non-Goals

The Memory package must not own:

- meeting lifecycle;
- task lifecycle;
- STT;
- diarization;
- summary generation;
- external research execution;
- Assistant dialogue;
- Product API transport;
- Security policy;
- Billing policy;
- runtime storage implementation.

## Principle

```text
Memory owns durable Account knowledge.
Sources provide candidates.
Models consume context.
Assistant explains and acts.
```
