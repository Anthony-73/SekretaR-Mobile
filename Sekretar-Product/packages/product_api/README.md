# Product API Package

Framework-agnostic foundation for the SekretaR Product API block.

Product API is the contract and orchestration layer. It does not own Identity,
Security, Billing, Capability, Meetings, Memory, Research, or integration
business rules.

Phase 1 covers:

- product error codes and error envelopes;
- product response envelopes;
- request metadata;
- API version primitives;
- request context objects;
- identity error mapping;
- shared contract primitives.

This package intentionally contains no FastAPI endpoints, HTTP transport
implementation, database access, or product block business logic.
