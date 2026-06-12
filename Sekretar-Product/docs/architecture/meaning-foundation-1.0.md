# Meaning Foundation 1.0

Status: domain architecture specification

Scope: Meaning block foundation — Phase 1

This document records the accepted domain-level foundation for the Meaning block
in Sekretar-Product.

It translates `meaning-foundation-vision-1.0.md` into foundation-level rules
sufficient for future implementation, without defining Python classes, database
tables, APIs, repositories, storage, UI, or implementation-layer design.

It builds on:

- Product Vision 1.0
- Memory Vision 1.0
- Memory Foundation 1.0
- Meaning Foundation Vision 1.0
- OAD-004 — Clarification Capability (deferred)
- completed Memory Foundation Phase 1 domain model

---

## 1. Purpose

Meaning Foundation is the interpretive layer above Memory.

Memory answers:

- what the system knows;
- where knowledge came from;
- what was corrected or contradicted;
- which knowledge is current.

Meaning answers:

- what those claims mean in the user's working world;
- who likely refers to whom;
- which roles and responsibilities are likely connected;
- whether interpretation is safe enough for downstream use.

Meaning does not store facts. Meaning interprets facts.

Core boundary:

```text
Memory  = claims
Meaning = interpretation over claims
```

Meaning exists to make meeting-centric interpretation explicit, revisable,
auditable, and safe for tasks, meeting protocols, Research, and Assistant.

---

## 2. Phase 1 Scope

Meaning Foundation Phase 1 is intentionally narrow.

### In scope

Interpretive wedge:

```text
People -> Roles -> Responsibilities
```

Phase 1 covers:

- person mentions and speaker attribution;
- role mentions in discourse;
- responsibility scopes mentioned in meetings;
- identity, role, and responsibility interpretation across meetings;
- safe interpretation for meeting protocols and task assignment context.

### Out of scope for Phase 1

- full organization graph;
- project/team ontology as Meaning-owned objects;
- Predict or Initiative;
- CRM or HR master data;
- task, meeting, or action lifecycle ownership;
- Clarification orchestration implementation;
- Speaker Intelligence implementation.

Phase 1 may operate with few or no promoted entities in early meetings. That is
expected.

---

## 3. Boundaries

### 3.1 Meaning is not CRM or HR

Meaning must not become:

- a contact registry;
- an employee directory;
- an org chart system;
- a formal job-title management layer.

People, roles, and responsibilities exist in Meaning only to support
understanding of meetings, tasks, decisions, and future Assistant behavior.

### 3.2 Meaning does not own Memory

Memory owns:

- `KnowledgeItem`;
- provenance, lifecycle, correction, contradiction, relation;
- `MemoryContext`.

Meaning consumes Memory outputs. Meaning must not duplicate claim storage or
claim lifecycle policy.

### 3.3 Meaning does not own Clarification

Clarification is a future cross-cutting Foundation Capability. See OAD-004.

Meaning:

- emits clarification candidates;
- consumes clarification outcomes affecting interpretation.

Meaning does not:

- rank clarification questions;
- enforce question budget;
- own clarification session/history;
- phrase user-facing questions.

### 3.4 Meaning does not own Speaker Intelligence

Speaker Intelligence owns diarization, voice profiles, and speaker matching.

Meaning may consume opaque `speaker_ref` and `voice_match_signal` metadata as
evidence. Meaning must not own raw audio, embeddings, fingerprints, or speaker
recognition logic.

### 3.5 Meaning does not own Actions

Actions Foundation and product action blocks own execution, permissions, and
action lifecycle.

Meaning may supply interpretation context and strict-use eligibility signals.
Meaning must not initiate, schedule, or execute actions.

### 3.6 Additional non-ownership

Meaning does not own:

- Assistant phrasing or UI;
- Product API transport;
- meeting or task lifecycle;
- storage technology;
- LLM execution.

---

## 4. Core Flow

Meaning Foundation Phase 1 follows one core interpretive flow:

```text
Reference
-> Evidence
-> Hypothesis
-> Decision
-> Entity
-> Validation
```

Compact meaning:

| Step | Concept | Question |
|------|---------|----------|
| 1 | `MeaningReference` | What was observed? |
| 2 | `MeaningEvidence` | What supports or weakens interpretation? |
| 3 | `MeaningHypothesis` | What does it likely mean? |
| 4 | `InterpretiveDecisionScope` + `MeaningDecisionState` | Is the interpretive question resolved? |
| 5 | `MeaningEntity` | Should continuity be promoted? |
| 6 | `MeaningEntityValidationState` | May strict consumers rely on this entity? |

This is not a heavy global state machine. It is a sequence of commitments with
simple, auditable rules at each step.

Promotion, resolution, and validation are separate:

```text
Promotion  = create or reuse a continuity object
Resolution = close an interpretive question
Validation = approve an entity for strict reuse
```

---

## 5. Main Domain Concepts

### 5.1 MeaningReference

Observational primitive. Always low commitment.

Phase 1 reference kinds:

- `PERSON_MENTION`
- `ROLE_MENTION`
- `RESPONSIBILITY_MENTION`
- `SPEAKER_REF`
- `GROUP_MENTION`

Rules:

- a reference is never a confirmed person, role, or CRM object;
- `"Анна"` and `"Анна Евгеньевна"` remain distinct references until
  interpretation says otherwise;
- `SPEAKER_REF` is attribution observation, not a person entity;
- references persist even after entity promotion.

### 5.2 MeaningEvidence

Evidence justifies interpretation. Evidence links attach to hypotheses,
promotion decisions, and decision-scope evaluation.

Evidence strength (Phase 1):

- `DIRECT`
- `STRONG`
- `WEAK`

Evidence role (Phase 1):

- `SUPPORTS`
- `WEAKENS`
- `CONFLICTS`

Evidence may come from Memory claims, Memory signals, Clarification outcomes,
`speaker_ref`, and `voice_match_signal` metadata.

### 5.3 MeaningHypothesis

Primary interpretive atom.

Phase 1 hypothesis types:

- `CO_REFERENCE`
- `ROLE_ATTRIBUTION`
- `RESPONSIBILITY`
- `SPEAKER_IDENTITY`
- `DECISION_INTERPRETATION`

Hypothesis lifecycle status is separate from decision state and validation
state. A hypothesis may be `SUPPORTED` while the decision scope remains
`UNRESOLVED`.

### 5.4 InterpretiveDecisionScope

A bounded interpretive question, for example:

- do these two person mentions refer to the same person?
- does this role mention attach to this person?
- does `Speaker_2` map to this person?
- who owns this responsibility scope?

`MeaningDecisionState` applies only to a decision scope, never to a raw
reference, hypothesis object, or entity directly.

### 5.5 MeaningEntity

Promoted continuity object.

Phase 1 entity kinds:

- `PERSON`
- `RESPONSIBILITY_SCOPE`

Role mentions do not automatically become person entities. Roles remain
reference-level or become bindings attached to a person entity.

### 5.6 MeaningContext

Scenario snapshot of references, hypotheses, decision states, entities, and
validation states.

Phase 1 purposes:

- `MEETING_INTERPRETATION`
- `TASK_ASSIGNMENT`

---

## 6. Meaning Decision State

### 6.1 Attachment rule

`MeaningDecisionState` applies only to `InterpretiveDecisionScope`.

It must not be stored as the primary state of `MeaningEntity`.

### 6.2 Values

| State | Meaning |
|-------|---------|
| `RESOLVED` | The interpretive question is sufficiently closed for the current scope |
| `UNRESOLVED` | Evidence is insufficient or no commitment has been made |
| `CONFLICTED` | Competing interpretations remain active and unsafe |

### 6.3 Who sets decision state

Meaning domain policy sets decision state based on:

- active hypotheses in the scope;
- evidence strength and conflict;
- Memory contradiction signals on supporting claims;
- Clarification outcomes;
- superseded or rejected competing hypotheses.

Clarification may provide the outcome that moves a scope from `UNRESOLVED` or
`CONFLICTED` to `RESOLVED`.

Memory does not own decision state. Memory events may trigger Meaning
re-evaluation.

### 6.4 Simple transition rules

```text
UNRESOLVED -> RESOLVED
  when a leading hypothesis is confirmed and no active competitor remains

UNRESOLVED -> CONFLICTED
  when competing hypotheses have non-trivial support

CONFLICTED -> RESOLVED
  when one interpretation is confirmed and competitors are rejected or superseded

RESOLVED -> UNRESOLVED
  when supporting evidence is weakened, outdated, or withdrawn

RESOLVED -> CONFLICTED
  when a new competing interpretation gains non-trivial support
```

Decision state is reversible.

### 6.5 Allowed combinations with validation

| Decision State | Typical Entity Validation | Meaning |
|----------------|---------------------------|---------|
| `UNRESOLVED` | not applicable or `UNVALIDATED` | Early or open interpretation |
| `CONFLICTED` | `UNVALIDATED` or `CONTRADICTED` | Unsafe for strict use |
| `RESOLVED` | `UNVALIDATED` | Resolved question, entity not yet strict-safe |
| `RESOLVED` | `VALIDATED` | Safe for strict consumers |

### 6.6 Unsafe combinations

These require immediate re-evaluation:

| Combination | Rule |
|-------------|------|
| `RESOLVED` + `CONTRADICTED` | Decision must reopen to `CONFLICTED` or `UNRESOLVED` |
| `CONFLICTED` + `VALIDATED` in same binding scope | Validation must not remain `VALIDATED` |
| strict consumer uses `UNRESOLVED` or `CONFLICTED` scope | forbidden |

---

## 7. Meaning Entity Validation State

### 7.1 Attachment rule

`MeaningEntityValidationState` applies only to `MeaningEntity`.

It must not be attached to `MeaningReference` or `MeaningHypothesis`.

If no entity exists, validation is `NOT_APPLICABLE`.

### 7.2 Values

| State | Meaning |
|-------|---------|
| `UNVALIDATED` | Entity exists, but strict reuse is not yet allowed |
| `VALIDATED` | Entity is approved for strict reuse |
| `CORRECTED` | Entity or bindings were corrected after prior validation |
| `CONTRADICTED` | Entity conflicts with active evidence or competing interpretation |

### 7.3 Who sets validation state

Meaning domain policy sets validation state based on:

- promotion policy outcome;
- Clarification confirm/reject/correct;
- Memory correction or contradiction on supporting claims;
- supersession of prior bindings.

`KnowledgeItem` confidence or `KnowledgeStatus.CONFIRMED` does not
automatically set `VALIDATED`.

### 7.4 Simple transition rules

```text
UNVALIDATED -> VALIDATED
  after Clarification confirm or explicit validation policy

VALIDATED -> CORRECTED
  after correction of entity bindings or supporting claim correction

VALIDATED or UNVALIDATED -> CONTRADICTED
  after Memory contradiction or competing interpretation affects entity bindings

CORRECTED -> VALIDATED
  only after re-validation or successful re-resolution

CONTRADICTED -> UNVALIDATED or CORRECTED
  after conflict handling, never directly to VALIDATED without re-validation
```

### 7.5 Naming rules for future implementation

To avoid developer confusion:

| Use | Do not use |
|-----|------------|
| `MeaningDecisionState` | `MeaningState` |
| `MeaningEntityValidationState` | `ValidationStatus` |
| `InterpretiveDecisionScope` | `Decision` alone |
| `decision_state` | `state` |
| `entity_validation_state` | `validation` |
| `DECISION_CONFLICTED` | bare `CONFLICTED` when scope is ambiguous |
| `ENTITY_CONTRADICTED` | bare `CONTRADICTED` when scope is ambiguous |

---

## 8. Evidence Rules

Phase 1 uses three evidence strengths only. No numeric scoring model.

### 8.1 DIRECT

Meaning: explicit or user-confirmed support.

Examples from meetings:

- user answered Clarification: "Да, это одна и та же Анна";
- claim explicitly states: "Анна Евгеньевна отвечает за бюджет";
- provenance is `EXPLICITLY_STATED` and directly supports the hypothesis;
- confirmed speaker-person binding after Clarification.

Rule:

- may support `RESOLVED` decision;
- may support promotion;
- may support `VALIDATED` only through validation policy or Clarification;
- does not alone override an active `CONFLICTED` scope without resolution.

### 8.2 STRONG

Meaning: consistent support, but not explicit confirmation.

Examples from meetings:

- `"Анна Евгеньевна"` and `"Анна"` appear across multiple meetings with
  consistent finance context;
- several Memory claims reinforce the same role/responsibility binding;
- `Speaker_2` is supported by discourse and strong `voice_match_signal`;
- `KnowledgeRelation.SUPPORTS` patterns align with the same interpretation.

Rule:

- may move hypothesis to `SUPPORTED`;
- may support provisional promotion to `UNVALIDATED` entity;
- is not enough alone for strict consumer use;
- is not enough alone for `VALIDATED`.

### 8.3 WEAK

Meaning: suggestive but insufficient.

Examples from meetings:

- one mention of `"Дима"` without disambiguation;
- `"финансовый директор"` with no linked person mention;
- one model-inferred claim with low confidence;
- weak or ambiguous `voice_match_signal`;
- indirect reference such as "по деньгам спросите у неё".

Rule:

- may keep scope `UNRESOLVED`;
- must not promote entity;
- must not mark scope `RESOLVED`;
- may justify Clarification candidate if impact is high.

### 8.4 Evidence conflict rule

If evidence links with role `CONFLICTS` remain active and non-trivial:

- decision scope must be `CONFLICTED` or remain `UNRESOLVED`;
- strict consumers must be blocked.

---

## 9. Promotion Policy

`MeaningEntity` is created only through promotion policy. Promotion is not the
same as validation.

### 9.1 General rule

A hypothesis may promote an entity only when:

- its decision scope is `RESOLVED` or policy explicitly allows provisional
  promotion while scope remains open;
- no active competing hypothesis remains in the same scope;
- at least one non-weak evidence link supports promotion;
- promotion type matches hypothesis type.

Role mentions alone do not promote `PERSON` entities.

### 9.2 Direct evidence promotion

Allowed when:

- Clarification confirms the interpretation;
- direct claim or explicit user-confirmed evidence supports the binding.

Typical result:

- `MeaningEntity(PERSON)` or `RESPONSIBILITY_SCOPE` created;
- validation usually `UNVALIDATED` unless Clarification also validates reuse;
- if Clarification explicitly confirms reuse, entity may become `VALIDATED`.

### 9.3 Accumulated indirect evidence promotion

Allowed only under stricter policy when:

- multiple `STRONG` evidence links support the same scope;
- evidence comes from more than one meeting or more than one independent claim
  cluster;
- no active `CONFLICTED` competitor remains;
- hypothesis type is `CO_REFERENCE`, `ROLE_ATTRIBUTION`, `RESPONSIBILITY`, or
  `SPEAKER_IDENTITY`.

Typical result:

- entity may be created as `UNVALIDATED`;
- strict consumers remain blocked until validation;
- voice match alone is never sufficient.

### 9.4 Clarification-confirmed promotion

Preferred path for strict-safe continuity.

Allowed when:

- Clarification outcome confirms hypothesis and entity reuse.

Typical result:

- entity created or updated;
- decision scope `RESOLVED`;
- entity `VALIDATED` if Clarification confirms reuse for strict contexts.

### 9.5 Promotion forbidden

Promotion must not happen from:

- single weak mention;
- role phrase alone;
- voice match alone;
- similar first name alone;
- model inference alone;
- numeric observation count alone.

---

## 10. Clarification Trigger Model

Clarification is triggered by interpretive state, not by the number of observed
facts.

Meaning emits clarification candidates. Clarification orchestration remains
outside Meaning.

### 10.1 Primary triggers

| Trigger | Condition |
|---------|-----------|
| unresolved interpretation | decision scope = `UNRESOLVED` and downstream impact is high |
| active conflict | decision scope = `CONFLICTED` |
| rising confidence without direct evidence | hypothesis is `SUPPORTED`, decision still `UNRESOLVED`, impact is high |
| strict consumer needs validated entity | strict use requested, entity missing or `UNVALIDATED` |

### 10.2 Not triggers by themselves

- N mentions observed;
- N meetings observed;
- N weak evidence links;
- numeric score threshold;
- presence of `Speaker_2` alone;
- presence of role phrase alone.

### 10.3 Candidate payload

A clarification candidate should identify:

- decision scope;
- current decision state;
- linked references and hypotheses;
- linked evidence summary;
- linked Memory claim ids where relevant;
- expected clarification value;
- intent: confirm, disambiguate, reject, correct, defer.

### 10.4 Outcome application

Clarification outcomes may:

- confirm or reject hypothesis;
- move decision scope to `RESOLVED` or keep it open;
- create or update entity;
- change entity validation state;
- trigger Memory outcomes through separate orchestrated flows.

Meaning applies interpretive outcomes. Memory applies claim outcomes.

---

## 11. Strict Consumer Contract

Some downstream uses require confirmed interpretation, not provisional
continuity.

### 11.1 Strict requirement

For critical actions, consumers must require:

```text
MeaningDecisionState = RESOLVED
MeaningEntityValidationState = VALIDATED
```

for the relevant person, role, or responsibility binding.

### 11.2 Critical actions

- sending emails on behalf of inferred person/role attribution;
- creating external tasks assigned to inferred person;
- exporting tasks to calendar with inferred assignee;
- issuing official directives or formal assignments;
- Research that relies on a specific person or role as a confirmed fact.

### 11.3 Non-critical actions

Non-critical actions may use `UNVALIDATED` entity or `UNRESOLVED` scope only
with explicit provisional labeling such as:

- "предположительно";
- "требует подтверждения";
- `Speaker_2` instead of a person name.

Examples:

- draft meeting protocol for internal review;
- draft task proposal inside the product;
- Assistant explanation with uncertainty visible;
- internal meeting summary not exported as formal record.

### 11.4 Consumer obligations

Strict consumers must:

- read `MeaningContext`, not raw hypotheses alone;
- check both decision state and validation state;
- fail closed when state is insufficient;
- not infer validation from Memory claim confidence.

---

## 12. Speaker Integration Contract

Speaker Intelligence is not implemented in Phase 1, but Meaning must define the
integration contract now.

### 12.1 Ingress

Meaning may receive:

- `speaker_ref`
- meeting-local speaker label
- segment attribution references
- opaque `voice_profile_ref`
- `voice_match_signal` metadata

Meaning must not receive:

- raw audio;
- embeddings;
- fingerprint vectors;
- diarization logic.

### 12.2 Required flow

```text
speaker_ref
  -> MeaningReference(SPEAKER_REF)
  -> MeaningEvidence
  -> MeaningHypothesis(SPEAKER_IDENTITY)
  -> optional CO_REFERENCE / ROLE_ATTRIBUTION / RESPONSIBILITY
  -> Clarification if needed
  -> MeaningEntity(PERSON) only through promotion policy
  -> optional opaque voice_profile_ref on validated person entity
```

### 12.3 Voice signal rule

`voice_match_signal`:

- may strengthen or weaken `SPEAKER_IDENTITY`;
- is evidence only;
- is not truth;
- must not alone promote or validate a person entity.

### 12.4 Meeting protocol rule

A person name may replace `Speaker_N` in strict meeting interpretation only
when:

- relevant `SPEAKER_IDENTITY` scope is `RESOLVED`;
- related person entity is `VALIDATED` or explicitly allowed by corrected-active
  policy;
- no open conflict remains.

---

## 13. Memory Integration

### 13.1 Division of responsibility

| Layer | Owns |
|-------|------|
| Memory | claims, provenance, lifecycle, correction, contradiction, relation, `MemoryContext` |
| Meaning | references, evidence links, hypotheses, decision scopes, entities, validation, `MeaningContext` |

### 13.2 Meaning inputs from Memory

- `MemoryContext`
- `KnowledgeItem` claims relevant to people, roles, responsibilities, decisions
- provenance type and confidence signals
- `MemoryCorrection` and `MemoryContradiction` signals
- `KnowledgeRelation` patterns

### 13.3 Re-evaluation triggers

Memory events must trigger Meaning re-evaluation for affected scopes and
entities:

| Memory event | Meaning effect |
|--------------|----------------|
| claim corrected | decision may reopen; entity may become `CORRECTED` |
| contradiction detected | scope may become `CONFLICTED`; entity may become `CONTRADICTED` |
| claim outdated or deleted | scope may reopen to `UNRESOLVED` |
| claim confirmed | may strengthen evidence, but does not auto-validate entity |

### 13.4 Non-equivalence rule

```text
KnowledgeStatus.CONFIRMED != MeaningEntityValidationState.VALIDATED
Decision RESOLVED != Entity VALIDATED
Promotion != Validation
```

These distinctions are mandatory.

---

## 14. Anti-CRM Principle

Meaning uses people, roles, and responsibilities to understand work context.
It must not become master organizational data.

Rules:

- no enterprise contact registry;
- no HR title management;
- no automatic org chart;
- no assumption that every mentioned person is an employee;
- no assumption that every role mention is a formal position;
- multiple mentions of similar names remain distinct until interpretation
  confirms otherwise;
- entities are interpretive continuity anchors, not CRM records.

If a future block needs CRM-like behavior, it must be a separate block consuming
Meaning and Memory, not an expansion of Meaning into CRM.

---

## 15. Scenario Validation

The following scenarios must be used to validate the model before implementation.

### Scenario 1 — Планёрка

Meeting with 5–10 colleagues, many person mentions, few formal roles.

Expected:

- many `PERSON_MENTION` references;
- few early promotions;
- multiple scopes remain `UNRESOLVED`;
- protocols stay on `Speaker_N` or provisional labels in strict mode.

### Scenario 2 — Совещание проекта

Repeated mentions of project responsibility and known team phrases.

Expected:

- `RESPONSIBILITY` and `ROLE_ATTRIBUTION` hypotheses;
- promotion only after cross-meeting support or Clarification;
- task assignment remains non-strict until validation.

### Scenario 3 — Переговоры с подрядчиком

External people not in internal continuity model.

Expected:

- no automatic merge with internal person entities;
- external mentions remain separate references;
- no CRM-style contact creation.

### Scenario 4 — Разговор один на один

One speaker, direct names, simpler attribution.

Expected:

- `SPEAKER_IDENTITY` may become `RESOLVED` faster;
- entity may remain `UNVALIDATED` until Clarification if impact becomes strict.

### Scenario 5 — Встреча с неизвестными участниками

Only `Speaker_1`, `Speaker_2`, no reliable names.

Expected:

- only `SPEAKER_REF` references at first;
- no person entity promotion;
- decision scopes remain `UNRESOLVED`.

### Scenario 6 — Участник назван только по роли

Example: "финансовый директор согласен".

Expected:

- `ROLE_MENTION` reference;
- no `PERSON` entity promotion from role alone;
- role remains reference or binding hypothesis.

### Scenario 7 — Прямое обращение

Example: "Анна, как финансовый директор, прокомментируйте бюджет".

Expected:

- separate person and role references;
- `ROLE_ATTRIBUTION` hypothesis may link them;
- no immediate `VALIDATED` person entity without direct or clarified evidence.

### Scenario 8 — Конфликт ролей

One person mentioned with two roles or two people linked to one role.

Expected:

- scope becomes `CONFLICTED`;
- Clarification candidate emitted;
- strict consumers blocked.

### Scenario 9 — Смена роли человека

Older meetings say "ответственный за склад", new meeting assigns another person.

Expected:

- prior entity may become `CORRECTED` or `CONTRADICTED`;
- decision scope reopens;
- no silent overwrite of old bindings.

### Scenario 10 — Задача без явного ответственного

Task-like language without named assignee.

Expected:

- responsibility scope may be `UNRESOLVED`;
- no person promotion from task phrase alone;
- task consumer uses provisional labeling or asks Clarification.

---

## 16. Risks

### Premature promotion

If promotion policy is too permissive, the system will appear to "know people"
before identity is justified.

Mitigation:

- promotion policy gates in section 9;
- strict consumer contract in section 11;
- separate validation from promotion.

### CRM drift

If Meaning begins to store master person or role records, it will duplicate CRM
and corrupt interpretive boundaries.

Mitigation:

- anti-CRM principle in section 14;
- closed reference taxonomy;
- entities as continuity anchors only.

### Stale roles

Roles change faster than person identity. Validated role bindings may become
wrong while person entity remains validated.

Mitigation:

- role bindings are hypotheses/bindings, not permanent HR facts;
- Memory outdated/correction events trigger Meaning re-evaluation;
- `CORRECTED` and `CONTRADICTED` validation paths.

### Unresolved hypotheses buildup

Open hypotheses may accumulate without aging policy.

Mitigation:

- hypothesis supersession;
- decision scope stays explicit;
- Clarification driven by state and impact, not count;
- future aging policy deferred, but re-evaluation on Memory change is required now.

### Strict consumers ignoring validation

If Meetings, Tasks, Research, or Actions bypass `MeaningContext`, unsafe names
and assignees will leak into product behavior.

Mitigation:

- strict consumer contract;
- fail-closed rule;
- scenario validation before implementation.

---

## 17. Architectural Constraints

Meaning Foundation 1.0 follows these constraints:

1. Meaning belongs to Account.
2. Meaning does not belong to Device, Session, or Model.
3. Meaning does not store durable knowledge claims.
4. Meaning consumes Memory; it does not own Memory lifecycle.
5. Every hypothesis must have evidence links.
6. References are never silently promoted into entities.
7. Decision state applies only to interpretive decision scopes.
8. Validation state applies only to promoted entities.
9. `KnowledgeStatus.CONFIRMED` does not imply `VALIDATED`.
10. Clarification is cross-cutting and outside Meaning.
11. Speaker evidence is interpretive input, not truth.
12. Voice match alone must not promote or validate person entities.
13. Role mentions alone must not create person entities.
14. Strict consumers require `RESOLVED` + `VALIDATED`.
15. Meaning must remain independent of storage, API, and UI technology.
16. Meaning must not call LLMs as a required domain mechanism.
17. Meaning must not become CRM, HR, or org-chart master data.
18. Promotion, resolution, and validation remain separate commitments.
19. Interpretation must remain revisable and auditable.
20. New meetings always begin with new references.

---

## 18. Explicit Non-Goals

This document does not define:

- Python classes or package structure;
- database tables or schemas;
- API endpoints;
- repository implementations;
- storage technology;
- UI flows;
- Assistant dialogue;
- Clarification orchestration implementation;
- Speaker Intelligence implementation;
- implementation services;
- numeric confidence scoring;
- full organization graph;
- Predict or Initiative behavior.

Those belong to later architecture and implementation phases.

---

## 19. Summary

Meaning Foundation 1.0 defines Meaning as the Account-owned interpretive layer
above Memory in Sekretar-Product.

Meaning does not store facts. Meaning interprets facts.

Phase 1 focuses on:

```text
People -> Roles -> Responsibilities
```

The core flow is:

```text
Reference -> Evidence -> Hypothesis -> Decision -> Entity -> Validation
```

`MeaningReference` is the observational bridge.

`MeaningEvidence` justifies interpretation.

`MeaningHypothesis` is the primary interpretive mechanism.

`MeaningDecisionState` makes interpretive uncertainty explicit.

`MeaningEntity` provides continuity after promotion.

`MeaningEntityValidationState` determines whether strict consumers may rely on
that continuity.

Clarification is state-driven, not count-driven.

Speaker evidence is supported without creating a Speaker Foundation inside
Meaning.

Memory and Meaning remain separate: claims versus interpretation.

This specification is intended to be formal enough for future implementation
without turning Meaning into an overcomplicated state machine.
