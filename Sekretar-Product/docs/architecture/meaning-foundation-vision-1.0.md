# Meaning Foundation Vision 1.0

Status: architecture vision (updated)

Scope: long-term role of Meaning in Sekretar-Product

This document defines what Meaning Foundation is in Sekretar-Product and what it
must become over time. It does not define implementation entities, database
schemas, APIs, repositories, storage, UI, or implementation code.

It builds on:

- Product Vision 1.0
- Memory Vision 1.0
- Memory Foundation 1.0
- OAD-003 — Trust Calibration (deferred)
- OAD-004 — Clarification Capability (deferred)
- completed Memory Foundation Phase 1 domain model

Revision note:

This revision adds the Evidence Layer, Meaning Decision State, Validation
State, state-based Clarification trigger model, and Speaker Intelligence
integration points. It does not introduce new major foundations or redesign the
core Reference -> Hypothesis -> Entity model.

---

## 1. Purpose of Meaning Foundation

Memory Foundation answers:

- what the system knows;
- where knowledge came from;
- what was corrected or contradicted;
- which knowledge is current and eligible for use.

Meaning Foundation answers a different question:

**What does this knowledge mean in the user's working world?**

Meaning is the interpretive layer above Memory. It turns observed discourse,
claims, and participant signals into structured understanding that can support
tasks, meeting interpretation, Assistant explanations, and future work
continuity.

Meaning does not store facts. Meaning interprets facts.

The long-term product direction is:

```text
Sources
-> Memory (claims)
-> Meaning (interpretation)
-> Assistant / Tasks / Meetings / Research / Actions
```

Meaning gives Sekretar-Product the ability to move from:

```text
"The system knows several claims about people, roles, and decisions"
```

to:

```text
"The system understands who likely means what, in what role, with what
remaining uncertainty"
```

Without Meaning, Memory remains correct but under-connected. The product can
store that "Anna approved payment" and that "the finance director prepared a
forecast," but cannot responsibly reason about whether those observations refer
to the same person, the same role, or the same responsibility scope.

Meaning exists to make interpretation explicit, revisable, auditable, and safe
for a meeting-centric product.

---

## 2. Boundaries of Meaning Foundation

Meaning Foundation is responsible for:

- observing discourse referents without premature identity commitment;
- collecting and classifying evidence for interpretive decisions;
- building interpretive hypotheses over observed references;
- determining whether interpretation is resolved, unresolved, or conflicted;
- tracking validation state of promoted semantic objects;
- linking interpretation to Memory evidence;
- promoting stable semantic objects only after sufficient commitment;
- producing meaning context for downstream consumers;
- preserving interpretive history and uncertainty;
- emitting clarification candidates when interpretive state requires human
  validation.

Meaning Foundation is not responsible for:

- storing durable knowledge claims;
- provenance, correction, contradiction, or knowledge lifecycle;
- diarization or speaker recognition;
- voice fingerprint storage or voice matching;
- clarification orchestration, question ranking, or clarification history;
- Assistant phrasing or user-facing presentation;
- task, meeting, or project lifecycle ownership;
- Predict, Initiative, or proactive future-action modeling;
- Product API transport;
- storage technology or persistence implementation.

Core boundary:

```text
Memory   = what is known
Meaning  = what it likely means
```

Meaning must remain a framework-agnostic interpretive foundation, not a hidden
monolith inside Memory, Meetings, or Assistant.

---

## 3. Relationship With Other Foundations

### Memory Foundation

Memory provides the claim substrate for Meaning.

Memory gives Meaning:

- `KnowledgeItem` claims;
- confidence and lifecycle state;
- provenance and correction history;
- contradiction and relation signals;
- `MemoryContext` snapshots of eligible knowledge.

Meaning gives Memory:

- no direct claim storage;
- optional downstream outcomes after clarification or confirmation, such as
  stronger person knowledge, corrected interpretation, or new candidate
  acceptance flows orchestrated outside Meaning.

Meaning consumes Memory. Meaning does not replace Memory.

A hypothesis may interpret several `KnowledgeItem` instances together. That
interpretation must remain separate from the claims themselves.

```text
MemoryContext = eligible claims
MeaningContext = eligible interpretations
```

### Clarification Capability

Clarification is a future cross-cutting Foundation Capability. It is not part
of Meaning Foundation.

See OAD-004.

Meaning:

- detects interpretive uncertainty;
- may emit clarification candidates from hypotheses;
- consumes clarification outcomes to confirm, reject, correct, or defer
  interpretation.

Clarification:

- chooses which questions are worth asking;
- limits question budget;
- orchestrates when and how to ask;
- records clarification history;
- returns outcomes to Memory and Meaning.

Assistant phrases and presents clarification questions. Meaning does not own
clarification orchestration.

```text
Meaning -> clarification candidate
Clarification -> orchestration + outcome
Meaning -> apply interpretive outcome
Memory -> apply knowledge outcome
```

### Speaker Intelligence

Speaker Intelligence is a separate block.

Speaker Intelligence owns:

- diarization;
- meeting-local speaker labels such as `Speaker_1`, `Speaker_2`;
- voice fingerprints and voice profiles;
- cross-meeting voice matching;
- `speaker_ref` and `voice_match_signal`.

Meaning may consume `speaker_ref` and `voice_match_signal` as evidence for
`MeaningHypothesis(SPEAKER_IDENTITY)`, but Meaning must not own diarization,
raw audio, voice embeddings, or speaker recognition logic.

The boundary is:

```text
Speaker Intelligence -> who speaks
Memory               -> what is known about speech and people
Meaning              -> who this speaker likely is in the user's working world
```

Voice identity is evidence, not final truth. A strong voice match may support
or weaken a speaker-identity hypothesis, but must not alone confirm a person
or promote a `MeaningEntity`.

### Assistant Foundation

Assistant is the future user-facing layer that helps the user work with
accumulated knowledge and interpretation.

Assistant uses Meaning to explain:

- who likely means what;
- which roles or responsibilities are still uncertain;
- why the system believes two mentions may refer to the same person;
- when a meeting protocol may safely use a name instead of `Speaker_2`.

Assistant does not own Meaning. Assistant consumes `MeaningContext` and
presents interpretation to the user in understandable language.

Meaning does not formulate UI, dialogue, or final user-facing phrasing.

---

## 4. Core Concepts

Meaning Foundation is built on three core concepts.

### MeaningReference

`MeaningReference` is the observational primitive of Meaning.

It represents something observed in discourse or attribution, without asserting
that the system already understands what it is in the user's working world.

Examples:

- `PERSON_MENTION: "Анна Евгеньевна"`
- `PERSON_MENTION: "Анна"`
- `ROLE_MENTION: "финансовый директор"`
- `RESPONSIBILITY_MENTION: "по бюджету"`
- `SPEAKER_REF: Speaker_2`
- `GROUP_MENTION: "финансовый блок"`

A reference is always observational. It is not a confirmed person, role,
project, task, or CRM object.

`MeaningReference` is permanent. Even after a `MeaningEntity` is promoted, new
meetings continue to produce new references first.

### MeaningHypothesis

`MeaningHypothesis` is the primary interpretive atom of Meaning Foundation.

It expresses a proposed interpretation over one or more references, backed by
evidence links to Memory and optional external signals such as speaker
attribution or voice match metadata.

Examples:

- `CO_REFERENCE`: `"Анна"` may refer to `"Анна Евгеньевна"`
- `ROLE_ATTRIBUTION`: `"Анна Евгеньевна"` may be connected to finance-related
  responsibility
- `ROLE_ATTRIBUTION`: `"финансовый директор"` may refer to the same person as
  `"Анна Евгеньевна"`
- `SPEAKER_IDENTITY`: `Speaker_2` may refer to `"Сергей"`
- `RESPONSIBILITY`: a person reference may own a responsibility scope such as
  budget or integration
- `DECISION_INTERPRETATION`: a statement may be a decision rather than mere
  discussion

A hypothesis has interpretive status, such as proposed, supported, confirmed,
rejected, or superseded. It is revisable and auditable.

Meaning must not treat a hypothesis as equivalent to a Memory claim.

### MeaningEntity

`MeaningEntity` is a promoted continuity object.

It represents a stable semantic anchor in the user's working world only after
the system has enough evidence or user commitment to reuse that interpretation
across meetings and downstream scenarios.

Examples after promotion:

- `MeaningEntity(PERSON)` for a confirmed person anchor;
- `MeaningEntity(RESPONSIBILITY_SCOPE)` for a confirmed responsibility area.

`MeaningEntity` is not the starting point of Meaning. It is created through
entity promotion policy after confirmation, clarification, or sufficient
cross-meeting evidence.

A role mention such as `"финансовый директор"` should not automatically become a
person entity. Role language usually remains reference-level or becomes a binding
attached to a promoted person entity.

### Supporting concept: MeaningEvidence

Evidence is the bridge between observation and interpretation.

Meaning separates three layers:

```text
Observation -> Evidence -> Interpretation
```

| Layer | Meaning concept | Question |
|-------|-----------------|----------|
| Observation | `MeaningReference` | What was observed? |
| Evidence | `MeaningEvidence` / `MeaningEvidenceLink` | What supports or weakens interpretation? |
| Interpretation | `MeaningHypothesis`, `MeaningEntity` | What does it likely mean? |

Observation alone does not justify interpretation. A reference such as `"Анна"`
or `Speaker_2` is not evidence that two mentions are the same person. Evidence
is what allows Meaning to justify, revise, or reject a hypothesis.

`MeaningEvidenceLink` is the concrete attachment of evidence to a hypothesis,
entity promotion decision, or decision-state evaluation.

Evidence may come from:

- Memory claims and Memory signals;
- provenance, correction, contradiction, and relation links;
- Clarification outcomes;
- `speaker_ref` and `voice_match_signal` metadata from Speaker Intelligence;
- repeated cross-meeting observations.

Meaning must not store raw audio or voice embeddings. External speaker evidence
enters Meaning only as references and interpretable signals.

### Evidence types

Phase 1 uses a small evidence strength taxonomy.

#### Direct Evidence

Evidence that explicitly states or confirms the interpreted relationship.

Examples:

- user explicitly confirmed through Clarification;
- claim with `ProvenanceType.EXPLICITLY_STATED` that directly supports the
  hypothesis;
- confirmed speaker-person binding after Clarification;
- user-corrected interpretation recorded as a validated outcome.

Direct Evidence can support resolution, but does not automatically override an
active conflict without explicit resolution policy.

#### Strong Evidence

Evidence that strongly supports an interpretation without yet being explicit
confirmation.

Examples:

- multiple consistent Memory claims across meetings;
- confirmed `KnowledgeRelation` patterns that reinforce the same interpretation;
- `SPEAKER_IDENTITY` supported by discourse and strong `voice_match_signal`;
- consistent role and responsibility mentions linked to the same reference
  cluster.

Strong Evidence may move a hypothesis toward `SUPPORTED` and may contribute to
promotion policy, but is not sufficient alone for strict downstream use without
validation.

#### Weak Evidence

Evidence that suggests an interpretation but is insufficient for commitment.

Examples:

- single model-inferred claim;
- one meeting mention without disambiguation;
- role phrase without linked person evidence;
- weak or ambiguous `voice_match_signal`;
- indirect reference without explicit naming.

Weak Evidence may justify keeping a hypothesis open. It must not alone promote
a `MeaningEntity` or mark an interpretation as `Resolved`.

#### Additional types in later phases

Phase 1 does not require additional top-level evidence types such as
`Circumstantial`, `Hearsay`, or `Historical`. Those patterns can be expressed
through:

- evidence strength (`DIRECT`, `STRONG`, `WEAK`);
- evidence role on the link (`SUPPORTS`, `WEAKENS`, `CONFLICTS`);
- Memory provenance and confidence signals.

This avoids evidence taxonomy sprawl while keeping auditability.

### Supporting concept: MeaningContext

`MeaningContext` is a scenario-specific snapshot of active references, open or
confirmed hypotheses, and promoted entities.

It is the interpretive counterpart to `MemoryContext`.

Examples of purpose:

- meeting interpretation;
- task assignment interpretation;
- Assistant explanation context.

Consumers use `MeaningContext` to know which interpretations are safe enough
to rely on in a given scenario.

`MeaningContext` must expose not only hypotheses and entities, but also
decision state and validation state so consumers can behave safely.

---

## 5. Meaning Decision State

Meaning must make interpretive uncertainty explicit at the decision level.

### States

| State | Meaning |
|-------|---------|
| `RESOLVED` | The interpretation is sufficiently committed for the current decision scope |
| `UNRESOLVED` | The interpretation remains open; evidence is insufficient or no commitment has been made |
| `CONFLICTED` | Competing interpretations are active and cannot be used safely without resolution |

Decision state applies to interpretive questions such as:

- whether two mentions refer to the same person;
- whether a role mention belongs to a person;
- whether a speaker maps to a known person;
- whether a statement is a decision or discussion;
- whether a responsibility assignment is safe for task interpretation.

Decision state is not the same as hypothesis lifecycle status. A hypothesis may
be `SUPPORTED` while the overall decision remains `UNRESOLVED` or
`CONFLICTED`.

### Who sets decision state

Meaning Foundation sets decision state through domain policy based on:

- active hypotheses and their lifecycle status;
- evidence strength and conflict signals;
- competing hypotheses in the same decision scope;
- Memory contradiction signals on supporting claims;
- Clarification outcomes;
- consumer scenario requirements, such as strict meeting-protocol use.

Clarification does not own decision state. Clarification may provide the outcome
that allows Meaning to move from `UNRESOLVED` or `CONFLICTED` to `RESOLVED`.

Memory does not own Meaning decision state. Memory may cause Meaning to
re-evaluate decision state when claims are corrected, contradicted, or
outdated.

### When decision state changes

Typical transitions:

```text
UNRESOLVED -> RESOLVED
  when a hypothesis is confirmed or promotion policy is satisfied

UNRESOLVED -> CONFLICTED
  when competing hypotheses remain active with non-trivial evidence

CONFLICTED -> RESOLVED
  when one interpretation is confirmed and competitors are superseded or rejected

RESOLVED -> UNRESOLVED
  when new evidence weakens the prior commitment

RESOLVED -> CONFLICTED
  when new contradictory evidence or competing interpretation appears
```

Decision state must be reversible. Organizational reality changes. Meetings
introduce new ambiguity even when older interpretations were once resolved.

### Effect on Clarification

Clarification should be driven by decision state, not by counting observations.

Meaning should emit clarification candidates primarily when:

- decision state is `UNRESOLVED` and downstream impact is high;
- decision state is `CONFLICTED`;
- a promoted entity or binding is needed for strict consumer use but validation
  is not yet sufficient.

Meaning should not emit clarification merely because:

- N mentions were observed;
- N meetings occurred;
- a numeric threshold of weak evidence was reached.

See section 7.

---

## 6. Validation State

Every `MeaningEntity` carries a Validation State that describes whether the
promoted object is safe to treat as a reusable semantic commitment.

### States

| State | Meaning |
|-------|---------|
| `UNVALIDATED` | Entity exists or was promoted, but user or policy commitment is not yet strong enough for strict reuse |
| `VALIDATED` | Entity is confirmed for reuse in the current interpretive model |
| `CORRECTED` | Entity or its bindings were corrected after prior validation |
| `CONTRADICTED` | Entity is in active conflict with competing interpretation or supporting Memory claims |

Validation State applies to `MeaningEntity`, not to raw `MeaningReference`.
References remain observational regardless of entity validation.

### Relationship with Memory Foundation

Memory and Meaning validate different things.

| Layer | Validates |
|-------|-----------|
| Memory | whether a claim is current, supported, corrected, or contradicted |
| Meaning | whether a promoted interpretive object is safe to reuse |

Connections:

- Memory `Correction` on supporting claims may move a related entity toward
  `CORRECTED` in Meaning;
- Memory `Contradiction` on supporting claims may move a related entity toward
  `CONTRADICTED`;
- Clarification confirm may move `UNVALIDATED` to `VALIDATED`;
- Clarification reject or correction may prevent promotion or force
  supersession;
- entity promotion may begin at `UNVALIDATED` when policy allows provisional
  continuity, but strict consumers must treat it as non-validated.

Validation State must not be inferred directly from `KnowledgeItem.confidence`
alone. Claim confidence and entity validation are related but not identical.

### Validation and promotion

Promotion creates an entity. Validation determines whether that entity may be
used as a stable interpretive anchor.

Recommended Phase 1 rule:

```text
Promotion may create MeaningEntity
Validation determines whether strict consumers may rely on it
```

This allows Meaning to preserve continuity without pretending that promotion
equals truth.

---

## 7. Clarification Trigger Model

Clarification is a future cross-cutting capability. See OAD-004.

Earlier informal thinking sometimes treated Clarification as a numeric process:

- ask after N observations;
- ask after N meetings;
- ask when weak evidence count reaches a threshold.

That model is rejected for Meaning Foundation.

### Correct trigger basis

Clarification must be triggered by **interpretive state**, not observation
quantity.

Primary triggers:

| Trigger | Condition |
|---------|-----------|
| unresolved high-impact interpretation | decision state = `UNRESOLVED` and consumer impact is high |
| active conflict | decision state = `CONFLICTED` |
| unsafe strict use | strict consumer needs a binding, but validation is insufficient |
| speaker-person ambiguity | `SPEAKER_IDENTITY` remains unresolved or conflicted with high impact |

Secondary ranking inputs may include:

- evidence strength;
- meeting protocol impact;
- task assignment impact;
- decision authorship impact;
- Trust Calibration maturity when available.

But these are ranking factors for Clarification orchestration, not standalone
numeric triggers.

### What Meaning provides to Clarification

Meaning emits clarification candidates containing:

- decision scope;
- current decision state;
- linked references and hypotheses;
- linked evidence summaries;
- linked Memory claim identifiers where relevant;
- expected clarification value;
- recommended intent, such as confirm, disambiguate, reject, or defer.

Clarification then decides:

- whether to ask;
- which 1-3 questions to ask;
- when to ask;
- how to record the outcome.

### What Clarification returns

Clarification outcomes may:

- confirm a hypothesis;
- reject a hypothesis;
- correct a binding;
- defer interpretation;
- trigger entity promotion;
- change validation state;
- cause Memory outcomes through separate orchestrated flows.

Meaning applies interpretive outcomes. Memory applies claim outcomes. Assistant
phrases the question.

---

## 8. Speaker Integration Points

Speaker Intelligence is not implemented yet and Meaning Foundation must not
create a Speaker Foundation.

However, Meaning must define mandatory integration points for future Speaker
Intelligence.

### Integration boundary

```text
Speaker Intelligence -> speaker attribution and voice match signals
Memory               -> claims about what was said and about people
Meaning              -> interpretation of who the speaker likely is in the work world
```

Meaning must not own:

- diarization;
- voice fingerprint generation or storage;
- speaker recognition;
- raw audio or embeddings.

### Required integration flow

```text
Speaker_1 / Speaker_2 / speaker_ref
  -> MeaningReference(SPEAKER_REF)
  -> MeaningEvidence (voice_match_signal metadata, segment attribution)
  -> MeaningHypothesis(SPEAKER_IDENTITY)
  -> optional MeaningHypothesis(CO_REFERENCE / ROLE_ATTRIBUTION)
  -> Clarification if unresolved or conflicted
  -> MeaningEntity(PERSON) only after promotion policy
  -> optional opaque voice_profile_ref link on validated person entity
```

### Integration point 1 — Speaker ingress

Speaker Intelligence provides:

- `speaker_ref`;
- meeting-local speaker label;
- segment attribution;
- optional `voice_profile_ref`;
- optional `voice_match_signal`.

Meaning creates or resolves `MeaningReference(SPEAKER_REF)`.

### Integration point 2 — Evidence ingress

`voice_match_signal` enters Meaning only as evidence metadata on
`MeaningEvidenceLink`:

- match strength;
- match scope;
- conflict flags;
- opaque `voice_profile_ref`.

Voice match may support or weaken `SPEAKER_IDENTITY`. It must not alone confirm
identity or validate a person entity.

### Integration point 3 — Person hypothesis

Meaning links `SPEAKER_REF` to:

- `PERSON_MENTION` references;
- existing `MeaningEntity(PERSON)` when already promoted;
- role or responsibility hypotheses where discourse supports them.

This is where Speaker Intelligence influences person interpretation without
owning person identity.

### Integration point 4 — Promotion and validation

A person entity may be promoted only through Meaning promotion policy.

After promotion:

- entity may remain `UNVALIDATED` or become `VALIDATED` depending on evidence
  and Clarification;
- optional opaque `voice_profile_ref` may be attached for future cross-meeting
  continuity;
- future meetings may use voice match to suggest new `SPEAKER_IDENTITY`
  hypotheses against an existing validated person entity.

### Integration point 5 — Consumer safety

`MeaningContext(MEETING_INTERPRETATION, strict=true)` may expose a person name
for a speaker only when:

- `SPEAKER_IDENTITY` decision state is `RESOLVED`;
- related person entity is `VALIDATED` or policy explicitly allows corrected but
  active reuse;
- no competing conflicted interpretation remains open.

Otherwise consumers must continue using `Speaker_1`, `Speaker_2`, or equivalent
technical labels.

---

## 9. Why Meaning Is Hypothesis-First Rather Than Entity-First

Entity-first Meaning would assume that people, roles, and responsibilities
exist as stable objects before interpretation is sufficiently supported.

That assumption fits CRM-style systems. It does not fit Sekretar-Product's
meeting-centric reality.

In real meetings, the system usually encounters:

- names before identities;
- role phrases before formal roles;
- speaker labels before known people;
- repeated mentions before disambiguation;
- indirect references before stable assignment.

If Meaning starts with `MeaningEntity`, the system risks false stability:

```text
"We created Person: Anna, therefore we already know who Anna is"
```

That leads to:

- incorrect merging of different people with similar names;
- role phrases treated as people;
- unsafe meeting protocols and task assignment;
- poor auditability when interpretation later proves wrong.

Hypothesis-first Meaning preserves the correct order of understanding:

```text
observe -> interpret -> commit
```

This makes uncertainty explicit, keeps interpretation revisable, and gives
Clarification a natural target before the system commits to stable entities.

---

## 10. How Meaning Works in Messy Real-World Meetings

Meaning is designed for informal discourse, not pre-registered organizational
data.

### Example arc

Meeting 1:

```text
"Анна Евгеньевна, прокомментируйте бюджет."
```

Meeting 2:

```text
"Анна согласовала оплату."
```

Meeting 3:

```text
"Финансовый директор подготовил прогноз."
```

Meeting 4:

```text
"По деньгам спросите Анну Евгеньевну."
```

At this stage the system may reasonably form hypotheses:

- `"Анна"` may refer to `"Анна Евгеньевна"`
- `"Анна Евгеньевна"` may be connected to finance-related responsibility
- `"финансовый директор"` may refer to the same person or to a related finance
  function

But it should not yet confidently create:

```text
MeaningEntity(PERSON): Anna
MeaningEntity(ROLE): Finance Director
```

The correct early state is:

```text
MeaningReference -> MeaningHypothesis -> open uncertainty
```

Meaning must allow multiple references to remain distinct until a
`CO_REFERENCE` or related hypothesis is confirmed.

Meaning must also distinguish:

- person mention;
- role mention;
- speaker label;
- responsibility scope.

These are not interchangeable merely because they appear near each other in
conversation.

### Meeting protocol safety

Meeting protocols and downstream consumers should use person names only when
`MeaningContext` contains confirmed speaker-person or mention-person bindings.

If interpretation is only proposed or supported, consumers should continue to
use `Speaker_1`, `Speaker_2`, or otherwise mark uncertainty.

This prevents protocols from turning uncertain interpretation into apparent
fact.

---

## 11. Entity Promotion Philosophy

`MeaningEntity` is a commitment, not an inference side-effect.

Promotion exists to provide continuity after interpretation has crossed an
identity commitment threshold.

### Promotion may happen when

- Clarification confirms a hypothesis;
- `CO_REFERENCE` is confirmed across mentions;
- `SPEAKER_IDENTITY` is confirmed with sufficient discourse evidence;
- cross-meeting evidence policy is satisfied with consistent support;
- competing interpretations have been resolved or superseded.

### Promotion should not happen from

- a single meeting mention alone;
- a role phrase alone;
- a weak or ambiguous voice match alone;
- model inference without interpretive commitment;
- similar first names without disambiguation;
- automatic merging of references that remain observably distinct.

### Promotion principles

1. **Identity commitment must be explicit.**
2. **Promotion must be auditable back to references, hypotheses, and evidence.**
3. **Promotion must be reversible through supersession, not silent overwrite.**
4. **New meetings still begin with new references even when an entity exists.**
5. **Voice profile links, when used, are opaque references to Speaker
   Intelligence, not owned voice data.**

Entity promotion turns a confirmed interpretive cluster into a reusable anchor.
It does not erase the observational history that justified the commitment.

Promotion and validation are separate commitments:

```text
Promotion = create or reuse a continuity object
Validation = decide whether strict consumers may rely on it
```

A promoted person entity may exist in `UNVALIDATED` state until Clarification or
strong evidence policy validates it.

---

## 12. Phase 1 Scope

Meaning Foundation Phase 1 should remain narrow and meeting-relevant.

### In scope

Core concepts:

- `MeaningReference`
- `MeaningEvidence` / `MeaningEvidenceLink`
- `MeaningHypothesis`
- Meaning Decision State (`RESOLVED`, `UNRESOLVED`, `CONFLICTED`)
- Validation State (`UNVALIDATED`, `VALIDATED`, `CORRECTED`, `CONTRADICTED`)
- `MeaningContext`
- `MeaningEntity` as a promotion target, not a bootstrap requirement

Phase 1 interpretive wedge:

```text
People -> Roles -> Responsibilities
```

Phase 1 reference kinds:

- `PERSON_MENTION`
- `ROLE_MENTION`
- `RESPONSIBILITY_MENTION`
- `SPEAKER_REF`
- `GROUP_MENTION`

Phase 1 hypothesis types:

- `CO_REFERENCE`
- `ROLE_ATTRIBUTION`
- `RESPONSIBILITY`
- `SPEAKER_IDENTITY`
- `DECISION_INTERPRETATION`

Phase 1 inputs:

- `MemoryContext`
- Memory claims and relation/contradiction signals
- `speaker_ref`
- `voice_match_signal` metadata

Phase 1 evidence model:

- `DIRECT`, `STRONG`, `WEAK` evidence strength
- evidence role: `SUPPORTS`, `WEAKENS`, `CONFLICTS`

Phase 1 outputs:

- `MeaningContext` for meeting interpretation and task-assignment interpretation
- decision state and validation state for safe downstream use
- clarification candidates driven by interpretive state, not observation counts
- promotion of `MeaningEntity(PERSON)` and limited responsibility scope entities
  when policy allows

### Phase 1 operating mode

Meaning may operate initially as:

```text
MeaningReference -> MeaningHypothesis -> MeaningContext
```

with few or no promoted entities in early meetings. That is expected and
correct.

---

## 13. Explicit Out-of-Scope Items

The following are intentionally out of scope for Meaning Foundation Vision 1.0
and for Meaning Foundation Phase 1.

### Product layers

- Predict
- Initiative
- UI
- API
- Product API orchestration
- Assistant dialogue generation

### Infrastructure and implementation

- repositories
- storage technology
- database schemas
- persistence adapters
- LLM prompt design
- model execution

### Neighboring block ownership

- task lifecycle
- meeting lifecycle
- project lifecycle
- CRM or HR master data
- contact registry
- org chart management
- raw transcript ownership
- diarization
- voice fingerprint generation and matching

### Semantic anti-patterns

Meaning must not become:

- a second Memory for facts;
- a CRM of people and roles;
- a generic mention taxonomy for every product object type;
- a catch-all relation layer similar to rejected vague relation models;
- a speaker recognition subsystem;
- a clarification orchestration subsystem.

Reference taxonomy must remain a small, discourse-oriented closed set in Phase 1.
New reference kinds should require explicit architectural review, not enum
growth by convenience.

---

## 14. Recommended Implementation Roadmap After Memory Foundation

This roadmap describes the recommended order of work after Memory Foundation
Phase 1. It is directional only and does not define code or package structure.

### Step 1 — Accept Meaning Vision

Use this document as the architectural baseline before any Meaning package
implementation begins.

### Step 2 — Meaning Foundation 1.0 specification

Create a companion domain specification document that translates this vision
into foundation-level invariants, similar to `memory-foundation-1.0.md`.

That specification should define:

- observation/evidence/interpretation boundaries;
- reference/hypothesis/entity boundaries;
- evidence strength and conflict rules;
- decision state and validation state transitions;
- promotion policy;
- state-based Clarification candidate rules;
- Speaker Intelligence integration points;
- Clarification port boundaries.

### Step 3 — Meaning package skeleton

Introduce a framework-agnostic Meaning package with domain surface only:

- entities;
- enums;
- value objects;
- policies;
- errors;
- events;
- interfaces;
- unit tests for invariants.

No repositories, storage, API, or UI in this step.

### Step 4 — Reference and hypothesis core

Implement the Phase 1 core:

- `MeaningReference`
- `MeaningHypothesis`
- `MeaningEvidenceLink`
- `MeaningHypothesisHistory`

Focus on invariants such as:

- hypothesis without evidence is invalid;
- references are never silently promoted;
- role mentions do not become person entities by default.

### Step 5 — MemoryContext consumption contract

Define how Meaning consumes `MemoryContext` and clusters claims into references
and hypotheses.

Meaning must trust Memory eligibility rules and must not rebuild Memory
lifecycle policy.

### Step 6 — Speaker evidence contract

Define how `speaker_ref` and `voice_match_signal` enter Meaning as evidence for
`SPEAKER_IDENTITY` hypotheses without owning speaker recognition.

### Step 7 — MeaningContext

Implement scenario snapshots for:

- `MEETING_INTERPRETATION`
- `TASK_ASSIGNMENT`

Include strict interpretation rules for safe downstream use.

### Step 8 — Clarification ports

Define Meaning-side clarification candidate and outcome-application contracts
only. Do not implement Clarification Capability itself.

### Step 9 — Entity promotion policy

Implement promotion from confirmed hypotheses to `MeaningEntity`, including
optional opaque `voice_profile_ref` links after person promotion.

### Step 10 — Consumer boundary docs

Document how Meetings, Tasks, and Assistant should consume `MeaningContext`
without embedding interpretation logic inside those blocks.

### Suggested sequencing relative to other foundations

```text
Memory Foundation Phase 1        [completed]
Meaning Foundation Vision 1.0    [this document]
Meaning Foundation 1.0 spec
Meaning Foundation Phase 1 domain package
Clarification Capability design    [OAD-004, deferred implementation]
Assistant consumption contracts  [later]
```

Meaning Foundation should be designed and partially implemented before
Clarification implementation, because Clarification must consume meaningful
uncertainty from both Memory and Meaning. Meaning should not wait for
Clarification before establishing its own interpretive model.

---

## Direction

Meaning Foundation allows Sekretar-Product to move from stored knowledge to
responsible understanding.

Memory makes the product remember.

Meaning makes the product interpret.

Clarification helps the product learn where interpretation is still unsafe.

Assistant helps the user work with both.

The core model is:

```text
Observation
-> Evidence
-> Interpretation
-> Decision State
-> Validation State
-> Committed Entity
```

In compact form:

```text
MeaningReference
-> MeaningEvidence
-> MeaningHypothesis
-> MeaningEntity
```

`MeaningReference` is the observational bridge.

`MeaningEvidence` is the justification layer for interpretive decisions.

`MeaningHypothesis` is the primary interpretive mechanism.

Meaning Decision State makes uncertainty explicit.

Validation State makes promoted entities safe or unsafe for reuse.

`MeaningEntity` is the promoted continuity object.

Clarification is triggered by interpretive state, not by counting observations.

This architecture is hypothesis-first, evidence-grounded, meeting-realistic,
and designed to remain explainable as the product grows beyond Memory
Foundation.
