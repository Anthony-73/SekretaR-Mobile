# Product API

Product API is the entry door into SekretaR.

It owns public contracts, authentication boundaries, request validation, and product lifecycle orchestration. It must not become the central brain of the system.

Responsibilities:

- public orchestration;
- Identity handoff for users and devices;
- meeting lifecycle state;
- upload session lifecycle;
- task confirmation and task state;
- history and result retrieval;
- capability checks;
- Billing-aware feature availability through Capability Service;
- Security event emission;
- job creation;
- access to artifacts through controlled references.

Non-responsibilities:

- heavy STT;
- Local LLM execution;
- External LLM research;
- long-term memory consolidation;
- direct filesystem ownership of runtime storage.

Product API must not become the hidden implementation location for Identity, Security, Billing, Memory, Research, Speaker Intelligence, or Assistant logic.
