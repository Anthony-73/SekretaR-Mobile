# `sekretar_memory`

Source package for Memory Foundation.

This package contains the approved architectural module surface for Memory.
Modules are placeholders with docstrings, marker classes, enums, protocols, and
TODO-level contracts only.

Current modules:

- `entities.py`
- `value_objects.py`
- `enums.py`
- `events.py`
- `errors.py`
- `policies.py`
- `repositories.py`
- `services.py`
- `interfaces.py`

No business logic, persistence implementation, service implementation,
transport layer, storage integration, RAG, or embeddings are implemented at this
stage.

All future implementation must follow:

- `docs/architecture/memory-foundation-1.0.md`
- `packages/memory/ARCHITECTURE.md`
