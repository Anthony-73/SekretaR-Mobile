# Memory Implementation Architecture

Status: package skeleton architecture

Scope: implementation-level package design without business logic

This document translates `Memory Foundation 1.0` into the first package
skeleton for `packages/memory`.

It does not define database schemas, API endpoints, storage technology, RAG,
embeddings, FastAPI integration, or infrastructure.

## 1. Package Structure

Target package tree:

```text
packages/memory/
  README.md
  ARCHITECTURE.md
  src/
    sekretar_memory/
      __init__.py
      README.md
      entities.py
      value_objects.py
      enums.py
      events.py
      errors.py
      policies.py
      repositories.py
      services.py
      interfaces.py
  tests/
    README.md
    test_account_ownership.py
    test_knowledge_lifecycle.py
    test_memory_sources.py
    test_provenance.py
    test_confidence.py
    test_corrections.py
    test_contradictions.py
    test_memory_context.py
    test_memory_events.py
```

Current skeleton creates only README and architecture placeholders. Python
modules and tests are intentionally deferred to the next implementation step.

## 2. Domain Entities

### KnowledgeItem

Purpose: primary unit of durable Account-owned knowledge.

Responsibility:

- preserve meaningful knowledge;
- reference Account ownership;
- carry provenance, confidence, lifecycle, and relationships.

Lifecycle:

Candidate -> Active -> Confirmed / Corrected / Contradicted / Outdated ->
Archived / Deleted / Forgotten.

Owner: Account.

Invariants:

- must belong to Account;
- must not belong to Device, Session, or Model;
- stable knowledge must have provenance;
- stable knowledge must have confidence or explicit unconfirmed state;
- raw transcript, summary, task list, model output, file, or chunk must not
  become a KnowledgeItem directly.

### MemorySource

Purpose: describes where Candidate Knowledge came from.

Responsibility:

- identify the source type;
- keep source references;
- support provenance.

Lifecycle:

Created when a source can produce Candidate Knowledge. It may remain referenced
after knowledge is accepted, rejected, corrected, or deleted.

Owner: Account context through the knowledge it supports.

Invariants:

- source does not become Memory by itself;
- Memory does not own the lifecycle of the source object.

### CandidateKnowledge

Purpose: information that may become Memory but has not been accepted yet.

Responsibility:

- represent possible knowledge extracted from a source;
- preserve source and initial provenance;
- allow accept, reject, defer, merge, or contradiction decisions.

Lifecycle:

Detected -> Evaluated -> Accepted / Rejected / Deferred / Merged /
Contradiction.

Owner: Account.

Invariants:

- must reference a source;
- must not be treated as stable Memory until accepted;
- must be rejectable without losing source auditability.

### KnowledgeProvenance

Purpose: explain where knowledge came from.

Responsibility:

- capture source;
- capture when knowledge appeared;
- distinguish stated, inferred, corrected, imported, or research-derived origin;
- support future Assistant explanations.

Lifecycle:

Attached when candidate or knowledge is recorded. Additional provenance may be
added when knowledge is reconfirmed or corrected.

Owner: Account through related knowledge.

Invariants:

- trusted stable knowledge requires provenance;
- provenance must not imply ownership by source block.

### KnowledgeConfidence

Purpose: product-level trust signal for knowledge.

Responsibility:

- distinguish confirmed, supported, inferred, unconfirmed, doubtful, or
  contradicted knowledge;
- guide context usage.

Lifecycle:

Estimated when knowledge is accepted and updated after confirmation,
correction, contradiction, or aging.

Owner: related KnowledgeItem.

Invariants:

- confidence is not only a model score;
- confidence must be considered when Memory provides context.

### KnowledgeLifecycleRecord

Purpose: record how knowledge changes over time.

Responsibility:

- record acceptance, confirmation, correction, contradiction, outdated state,
  archive, deletion, and forgetting.

Lifecycle:

Append-only conceptual history for a KnowledgeItem.

Owner: related KnowledgeItem.

Invariants:

- lifecycle transitions must be valid;
- deletion/forgetting must prevent accidental active reuse.

### KnowledgeRelation

Purpose: connect knowledge to other knowledge or external product objects.

Responsibility:

- represent supports, contradicts, updates, replaces, explains, derived from,
  concerns person/project/task/meeting, and related-to relationships.

Lifecycle:

Created when a meaningful relation is discovered or confirmed. It may later be
superseded or invalidated through lifecycle events.

Owner: Account through related knowledge.

Invariants:

- relation must not make Memory owner of external objects;
- contradictions must be explicit, not silent overwrites.

### MemoryCorrection

Purpose: represent user or system correction of knowledge.

Responsibility:

- preserve correction reason;
- link correction to affected knowledge;
- update confidence and lifecycle.

Lifecycle:

Created when knowledge is corrected. May produce corrected knowledge or update
existing knowledge lifecycle.

Owner: Account.

Invariants:

- correction must preserve provenance;
- correction must not erase previous knowledge without lifecycle trace.

### MemoryContradiction

Purpose: represent conflict between knowledge items or candidate and existing
knowledge.

Responsibility:

- preserve conflicting statements;
- support later resolution or user confirmation.

Lifecycle:

Detected -> Open / Resolved / Superseded.

Owner: Account.

Invariants:

- contradiction must not silently replace older knowledge;
- contradicted knowledge must not be used as confirmed context.

### MemoryContext

Purpose: selected subset of Memory for a scenario.

Responsibility:

- provide relevant knowledge to Research, Assistant, Tasks, Meetings, or future
  User Context;
- include provenance, confidence, and lifecycle signals.

Lifecycle:

Prepared for a specific request or scenario. It is not the whole Memory.

Owner: Account.

Invariants:

- must respect lifecycle and confidence;
- must not expose all Memory by default.

## 3. Value Objects

### Ownership Value Objects

- `AccountId`: required owner of Memory.
- `UserId`: actor/user context; not Memory owner.
- `DeviceId`: access metadata; not Memory owner.
- `SessionId`: temporary access metadata; not Memory owner.

Rules:

- immutable;
- non-empty;
- AccountId is required for Account-owned objects.

### Source Value Objects

- `SourceId`
- `SourceType`
- `SourceReference`
- `SourceTimestamp`

Rules:

- immutable;
- must identify source without transferring source ownership to Memory.

### Knowledge Content Value Objects

- `KnowledgeText`
- `KnowledgeSummary`
- `KnowledgeLanguage`
- `KnowledgeTags`

Rules:

- immutable after creation;
- cannot be empty for accepted knowledge;
- must represent meaningful knowledge, not raw source dumps.

### Provenance Value Objects

- `ProvenanceType`
- `ProvenanceNote`
- `ProvenanceTimestamp`

Rules:

- immutable;
- must distinguish explicitly stated, model inferred, user corrected,
  research derived, and integration imported origins.

### Confidence Value Objects

- `ConfidenceLevel`
- `ConfidenceScore`
- `ConfidenceReason`

Rules:

- immutable per lifecycle record;
- must not be treated as only a model score.

### Lifecycle Value Objects

- `KnowledgeStatus`
- `LifecycleReason`
- `LifecycleTimestamp`

Rules:

- immutable per lifecycle record;
- transitions are controlled by policies.

### Relationship Value Objects

- `RelationType`
- `RelatedObjectReference`

Rules:

- immutable;
- relation must not imply ownership of external objects.

## 4. Domain Events

Memory publishes:

- `CandidateKnowledgeDetected`
- `KnowledgeAccepted`
- `KnowledgeRejected`
- `KnowledgeDeferred`
- `KnowledgeMerged`
- `KnowledgeConfirmed`
- `KnowledgeCorrected`
- `KnowledgeContradictionDetected`
- `KnowledgeMarkedOutdated`
- `KnowledgeArchived`
- `KnowledgeDeleted`
- `KnowledgeForgotten`
- `KnowledgeRelationCreated`
- `MemoryContextPrepared`
- `MemorySourceLinked`

Potential subscribers:

- Product API for response orchestration and audit visibility;
- Jobs/Worker for future asynchronous processing;
- Research Intelligence for confirmed context availability;
- Assistant for context refresh;
- Security/Security Intelligence for sensitive memory operations;
- Observability for audit and diagnostics.

## 5. Repository Interfaces

### KnowledgeRepository

Responsibility:

- store and retrieve KnowledgeItem contracts;
- list knowledge by Account, status, type, and source-related criteria.

Boundary:

- no search technology decisions;
- no RAG or vector behavior;
- no external block ownership.

### CandidateKnowledgeRepository

Responsibility:

- store candidates;
- list pending candidates by Account or source;
- update candidate decisions.

Boundary:

- does not decide acceptance policy.

### MemorySourceRepository

Responsibility:

- store source references;
- list sources by Account and type.

Boundary:

- does not own source lifecycle.

### ProvenanceRepository

Responsibility:

- store and retrieve provenance records for knowledge.

Boundary:

- does not validate external source existence.

### KnowledgeRelationRepository

Responsibility:

- store and retrieve knowledge relations;
- support contradiction/support/update relationship lookup.

Boundary:

- does not become graph storage design.

### KnowledgeLifecycleRepository

Responsibility:

- append lifecycle records;
- list lifecycle history;
- provide latest lifecycle state.

Boundary:

- does not own policy decisions.

### MemoryEventRepository

Responsibility:

- store Memory domain events;
- list events by Account and KnowledgeItem.

Boundary:

- does not implement event bus infrastructure.

## 6. Domain Services

### MemoryIngestionService

Responsibility:

- accept source references;
- accept candidate knowledge;
- record candidate detection;
- emit `CandidateKnowledgeDetected`.

Does not perform STT, summary, diarization, research, or model calls.

### KnowledgeAcceptanceService

Responsibility:

- accept, reject, defer, merge, or mark candidate as contradiction;
- enforce provenance and Account ownership rules;
- emit acceptance-related events.

### KnowledgeLifecycleService

Responsibility:

- confirm;
- mark outdated;
- archive;
- delete;
- forget;
- enforce lifecycle transitions.

### KnowledgeCorrectionService

Responsibility:

- apply user or system corrections;
- preserve correction provenance;
- update confidence/lifecycle;
- emit `KnowledgeCorrected`.

### KnowledgeRelationService

Responsibility:

- create support, contradiction, update, replacement, and related-to links;
- prevent silent overwrites;
- emit relation events.

### MemoryContextService

Responsibility:

- prepare scenario-specific context for Assistant, Research, Tasks, Meetings,
  or future User Context;
- include provenance, confidence, and lifecycle signals.

Does not implement RAG, embeddings, vector retrieval, or model prompting.

### MemoryQueryService

Responsibility:

- read Memory by Account, source, lifecycle, relation, and type;
- expose domain-level read contracts.

Does not expose transport APIs.

## 7. Domain Policies

Required policies:

- Account ownership is required for Memory.
- Device, Session, and Model cannot own Memory.
- Stable knowledge requires provenance.
- Knowledge requires confidence or explicit unconfirmed state.
- Raw transcripts, summaries, task lists, files, chunks, and model output cannot
  become Memory directly.
- Lifecycle transitions must be valid.
- Deleted or forgotten knowledge must not be returned as active context.
- Contradicted knowledge must not be treated as confirmed context.
- Research findings do not become Memory automatically.
- Assistant uses Memory but does not own Memory.
- Memory must not call LLMs as a domain requirement.
- Memory must remain storage-technology independent.

## 8. Test Architecture

Planned tests:

- `test_account_ownership.py`: Memory belongs to Account; Device/Session/Model
  do not own Memory.
- `test_knowledge_lifecycle.py`: valid lifecycle transitions and invalid
  transition rejection.
- `test_memory_sources.py`: sources create candidates but do not become Memory.
- `test_provenance.py`: stable knowledge requires provenance.
- `test_confidence.py`: confidence levels affect context eligibility.
- `test_corrections.py`: correction preserves lifecycle and provenance.
- `test_contradictions.py`: contradiction is explicit and prevents silent
  overwrite.
- `test_memory_context.py`: context is a selected subset and respects lifecycle.
- `test_memory_events.py`: important operations emit Memory domain events.

Tests should use in-memory test repositories only. No persistence
implementation is included in Phase 1.

## 9. Phase 1 Scope

Included in the first implementation phase:

- domain entities;
- value objects;
- enums;
- domain events;
- domain errors;
- policies;
- repository interfaces;
- domain service interfaces;
- framework-agnostic service layer;
- unit tests with in-memory repositories.

Deferred:

- database implementation;
- FastAPI endpoints;
- Product API adapters;
- PostgreSQL;
- vector search;
- RAG;
- embeddings;
- graph database;
- Assistant UI;
- Research execution;
- Meeting implementation;
- Worker jobs;
- storage infrastructure.

## 10. Current Skeleton Scope

This commit creates the package skeleton only:

- package README;
- implementation architecture document;
- source package placeholder;
- tests placeholder.

The next block will implement the Memory domain model.
