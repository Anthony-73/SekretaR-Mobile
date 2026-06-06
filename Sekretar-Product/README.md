# SekretaR Product

Architecture Foundation: 0.3

This folder is the new architecture skeleton for SekretaR as a product platform.

SekretaR is designed as a platform for personal memory, knowledge, research, and actions.

Meeting is an important source of data, but it is not the center of the product.

The center of the system is:

User -> Memory -> Research -> Assistant -> Actions

## Core Principles

- Recorder starts the meeting lifecycle.
- Product API is the entry point, not the central brain.
- Product API is an orchestration layer.
- Heavy AI processing is isolated from product-facing APIs.
- Worker and queue are mandatory parts of the architecture.
- Speaker Intelligence is an independent block between STT and structured meeting analysis.
- User Memory is an independent block.
- Research Intelligence is an independent block.
- Identity is separate from Security.
- Security Intelligence is separate from Security.
- Billing is separate from authorization and security.
- Configuration is provided through environment variables.
- Secrets, tokens, IP addresses, virtual environments, and runtime storage do not belong in the repository.

## Structure

- `apps/` contains runnable product applications and services.
- `blocks/` contains architectural responsibility blocks.
- `packages/` contains shared contracts and infrastructure libraries.
- `infra/` contains deployment and operations scaffolding.
- `docs/architecture/` contains architecture decisions and migration notes.

This skeleton intentionally contains no migrated code, no business logic, and no API endpoint implementation.
