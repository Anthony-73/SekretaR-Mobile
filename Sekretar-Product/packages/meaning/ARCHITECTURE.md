# Meaning Implementation Architecture

Status: package skeleton architecture

Scope: implementation-level package design without business logic

This document translates `Meaning Foundation 1.0` into the first package
skeleton for `packages/meaning`.

It does not define database schemas, API endpoints, storage technology,
Clarification orchestration, Speaker Intelligence implementation, or
infrastructure.

## 1. Package Structure

Target package tree:

```text
packages/meaning/
  README.md
  ARCHITECTURE.md
  src/
    sekretar_meaning/
      __init__.py
      README.md
      enums.py
      value_objects.py
      entities.py
      events.py
      errors.py
      repositories.py
      interfaces.py
  tests/
    README.md
    conftest.py
    test_account_ownership.py
    test_meaning_references.py
    test_meaning_evidence.py
    test_meaning_hypotheses.py
    test_decision_scopes.py
    test_meaning_entities.py
```

Deferred modules:

```text
constants.py
policies.py
services.py
```

Current skeleton creates the architectural module surface. Python modules
contain enums, immutable value objects, entity skeletons, event markers,
repository protocols, and integration port contracts only.

## 2. Domain Entities

### MeaningReference

Purpose: observed discourse or attribution referent.

Owner: Account.

Invariants:

- always observational;
- never a confirmed person, role, or CRM object;
- persists after entity promotion.

### MeaningHypothesis

Purpose: primary interpretive atom over references.

Owner: Account.

Invariants:

- must have evidence links before behavior policies are applied in later
  phases;
- not equivalent to a Memory claim.

### InterpretiveDecisionScopeRecord

Purpose: bounded interpretive question and its decision state.

Owner: Account.

Invariants:

- decision state applies only here;
- never stored as the primary state of `MeaningEntity`.

### MeaningEntity

Purpose: promoted continuity object.

Owner: Account.

Invariants:

- not a bootstrap object;
- role mentions do not automatically become person entities;
- validation state applies only here;
- does not store `voice_profile_ref` in Phase 1.

### MeaningContext

Purpose: scenario-specific interpretive snapshot.

Owner: Account.

Invariants:

- exposes references, hypotheses, scopes, entities, and states for consumers;
- does not own meeting, task, or action lifecycle.

## 3. Value Objects

Phase 1 value objects include:

- identifiers;
- `InterpretiveDecisionScope`;
- `MeaningEvidence` and `MeaningEvidenceLink`;
- `RoleAttribution`;
- `ResponsibilityAttribution`;
- `SpeakerAttributionEvidence`;
- `VoiceMatchEvidence`;
- `ClarificationCandidatePayload`.

## 4. Integration Ports

### Memory

- `MemoryContextConsumerPort`
- `MemoryReevaluationTriggerPort`

### Speaker Intelligence

- `SpeakerEvidenceIngressPort`

Voice evidence rules for Phase 1:

- `VoiceProfileRef`, `SpeakerAttributionEvidence`, and `VoiceMatchEvidence` are
  allowed as evidence and input contracts;
- Meaning may consume voice-related evidence through `SpeakerEvidenceIngressPort`
  and attach it to hypotheses via `MeaningEvidenceLink`;
- Person ↔ VoiceProfile persistent binding is deferred;
- `MeaningEntity` does not store `voice_profile_ref` in Phase 1;
- voice profiles belong to future Speaker Intelligence, not Meaning.

### Clarification

- `ClarificationCandidatePort`
- `ClarificationOutcomePort`

### Strict consumers

- `StrictConsumerEligibilityPort`

## 5. Phase 1 Wedge

```text
People -> Roles -> Responsibilities
```

Core flow:

```text
Reference -> Evidence -> Hypothesis -> Decision -> Entity -> Validation
```

## 6. Explicit Non-Goals

This skeleton does not implement:

- policy logic;
- service orchestration;
- repository implementations;
- Clarification capability;
- Speaker Intelligence;
- CRM or HR master data;
- task assignment;
- meeting intelligence;
- API or storage technology.
