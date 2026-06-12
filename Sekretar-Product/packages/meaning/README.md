# Meaning Package

Framework-agnostic foundation package for the SekretaR Meaning block.

Meaning is the Account-owned interpretive layer above Memory. It builds
references, evidence-backed hypotheses, decision scopes, and promoted entities
for People, Roles, and Responsibilities interpretation.

This package is based on:

- `docs/architecture/meaning-foundation-vision-1.0.md`
- `docs/architecture/meaning-foundation-1.0.md`
- `docs/architecture/memory-foundation-1.0.md`
- `packages/memory`

## Current Status

This is the Meaning Foundation Package Skeleton.

It intentionally contains no business logic, no policy implementation, no
service implementation, no repository implementation, no FastAPI endpoints, no
database design, and no infrastructure integration.

## Phase 1 Target

The first implementation phase should introduce framework-agnostic domain
objects and contracts for:

- Meaning references;
- Meaning evidence links;
- Meaning hypotheses;
- Interpretive decision scopes;
- Meaning entities;
- Meaning context;
- Domain events;
- Repository interfaces;
- Integration port contracts;
- Unit tests with in-memory test repositories.

## Non-Goals

The Meaning package must not own:

- durable knowledge claims;
- clarification orchestration;
- speaker recognition or diarization;
- meeting lifecycle;
- task lifecycle or task assignment;
- meeting intelligence;
- CRM or HR master data;
- Research, Predict, or Initiative behavior;
- Product API transport;
- runtime storage implementation.

## Principle

```text
Memory stores claims.
Meaning interprets claims.
References observe discourse.
Hypotheses propose interpretation.
Entities provide continuity after promotion.
```
