# Knowledge Provenance Vision 1.0

Status: architecture vision

Scope: long-term role of Provenance in Sekretar-Product Memory

This document defines what Provenance is in Sekretar-Product and what it must
become over time. It does not define entities, database schemas, APIs,
repositories, storage, or implementation code.

It builds on:

- Product Vision 1.0
- Memory Vision 1.0
- Memory Foundation 1.0
- implemented Memory domain entities: MemorySource, CandidateKnowledge,
  KnowledgeItem, KnowledgeLifecycleRecord

---

## 1. What Problem Provenance Solves

Provenance exists because Memory must remain **explainable, auditable, and
trustworthy over time**.

Sekretar-Product is not a meeting archive. It is a long-term knowledge platform:

```text
Account
-> Memory
-> Research
-> Assistant
-> Actions
```

In this architecture, the user and future Assistant must be able to answer:

- why does the system know this;
- where this knowledge first appeared;
- through what path it entered Memory;
- whether it was said, inferred, imported, corrected, or confirmed later;
- which source can explain it now;
- what changed in the origin story when knowledge evolved.

Without Provenance, Memory becomes a black box of assertions. Confidence alone
cannot explain origin. Lifecycle alone cannot explain source. MemorySource alone
cannot explain how knowledge was derived from the source.

Provenance solves four product problems:

1. **Explainability** — Assistant can justify answers using origin, not only text.
2. **Auditability** — the product can show how knowledge entered and changed.
3. **Trust calibration** — provenance gives context for confidence and lifecycle.
4. **Cross-source continuity** — knowledge from meetings, documents, research,
   Assistant, and integrations remains comparable over time.

Provenance is not optional decoration. In Memory Foundation 1.0, trusted stable
knowledge requires provenance.

---

## 2. What Provenance Is

Provenance is the **origin story of knowledge**.

It is an append-only account of how a piece of knowledge became known to Memory,
linked to a source and to the knowledge lifecycle, without owning the source
object itself.

A provenance record answers questions like:

- which MemorySource produced or supports this knowledge;
- when this origin observation was recorded;
- whether the knowledge was stated, inferred, imported, corrected, researched,
  or otherwise acquired;
- who or what actor contributed to the origin story, when known;
- what note or explanation should be preserved for future Assistant use.

Provenance is **not** the knowledge text itself.
Provenance is **not** the source artifact.
Provenance is **not** the current trust score.
Provenance is **not** the current lifecycle state.

Provenance is the durable explanation layer between source and knowledge.

---

## 3. How Provenance Differs From Nearby Concepts

### MemorySource

**MemorySource** answers: *where is the external source object?*

It identifies the source type and external reference:

- meeting
- document
- research result
- Assistant interaction
- integration

MemorySource is a stable source passport. It does not explain how knowledge
was extracted, interpreted, accepted, corrected, or reconfirmed.

**Provenance uses MemorySource. It does not replace it.**

### CandidateKnowledge

**CandidateKnowledge** answers: *what might become knowledge, but is not
accepted yet?*

CandidateKnowledge carries an initial provenance snapshot because even
pre-acceptance information must remain explainable and rejectable without losing
auditability.

**Provenance begins before acceptance and continues after acceptance.**

### KnowledgeItem

**KnowledgeItem** answers: *what does Memory currently assert as durable
knowledge?*

KnowledgeItem may carry a minimal current provenance snapshot for fast reads,
but the full provenance history must not be collapsed into the aggregate root.

**KnowledgeItem owns the knowledge. Provenance explains its origin history.**

### Confidence

**Confidence** answers: *how trustworthy is this knowledge now?*

Confidence is a current product-level trust signal. It may change when:

- the user confirms knowledge;
- another source supports it;
- contradiction appears;
- knowledge ages or becomes doubtful.

Provenance explains **why** confidence may have changed, but confidence remains
a separate dimension.

Example:

- Provenance: "model inferred from June planning meeting"
- Confidence: "unconfirmed"

These must not be merged into one field.

### Lifecycle

**Lifecycle** answers: *what is the current state of knowledge over time?*

Lifecycle records transitions such as:

- accepted
- confirmed
- corrected
- contradicted
- outdated
- archived
- deleted
- forgotten

A lifecycle transition may create a new provenance record, but lifecycle itself
is about state movement, not origin explanation.

Example:

- Lifecycle: `CORRECTED`
- Provenance: "user corrected during Assistant interaction on 2026-06-06"

Lifecycle tells us what happened to knowledge.
Provenance tells us how we know that story.

---

## 4. What Roles Provenance Must Play

Provenance in Sekretar-Product is not a single narrow role. It is a
**combination of roles**:

| Role | Included | Not primary responsibility |
|------|----------|----------------------------|
| Passport of origin | Yes | Own source lifecycle |
| Explainability mechanism | Yes | Generate Assistant answers |
| Confirmation system | Partially | Confidence + lifecycle own current trust/state |
| Audit history | Yes | Store raw source content |

### Passport of origin

Provenance links knowledge to MemorySource and preserves when the origin was
observed or recorded.

### Explainability mechanism

Provenance gives Assistant the material for answers such as:

- "This was discussed in the June planning meeting."
- "This came from a confirmed research briefing."
- "You corrected this during an Assistant interaction."
- "This was inferred from a meeting and has not yet been confirmed."

### Confirmation support, not confirmation ownership

Confirmation is not a replacement for confidence or lifecycle.

When a user confirms knowledge, Memory should:

1. update confidence and/or lifecycle;
2. append a provenance record describing the confirmation event.

Provenance preserves the confirmation story. It does not own the confirmation
decision.

### Audit history

Provenance must remain append-only. Corrections, reconfirmations, imports, and
contradiction resolutions add history; they do not silently rewrite origin.

---

## 5. Simple Origin Model vs Extended Origin Model

Today the implemented domain already uses a simple provenance snapshot:

- source reference via `MemorySource` / `source_id`
- `ProvenanceType`
- optional note and timestamp

This is enough for Phase 1 implementation, but it is not enough for the full
long-term product vision.

The product should also support a richer origin vocabulary over time.

### Simple model

```text
Source
Timestamp
Speaker / Actor
ProvenanceType
```

This is necessary but incomplete for Sekretar-Product.

### Extended origin categories

Examples discussed for long-term modeling:

- Observed
- Stated
- Decided
- Confirmed
- Imported
- ResearchDerived
- UserProvided
- AssistantInferred
- ExternalEvidence
- Documented

These categories are attractive because they sound closer to human explanation.
They must not all be collapsed into one enum without architectural separation.

---

## 6. Are Extended Categories Part of Provenance?

**Partially yes, partially no.**

Not all of these categories belong to the same domain layer.

Recommended separation:

### A. Provenance layer

Belongs to provenance because it explains origin acquisition:

- **Stated** — knowledge directly expressed in a source
- **Observed** — knowledge recorded as observed behavior or fact in context
- **Imported** — knowledge entered from an integration
- **ResearchDerived** — knowledge derived from research output accepted into Memory
- **UserProvided** — knowledge explicitly provided by the user
- **AssistantInferred** — knowledge inferred during Assistant interaction
- **Documented** — knowledge grounded in a document source
- **ExternalEvidence** — knowledge supported by external evidence reference

These describe **how knowledge entered the origin story**.

### B. Confidence layer

Does not belong primarily to provenance:

- **Confirmed**

"Confirmed" is a trust outcome. It may produce a provenance record such as
"user confirmed on date X", but confirmation itself is a confidence/lifecycle
event.

### C. Knowledge semantics layer

Does not belong primarily to provenance:

- **Decided**

"Decided" is usually knowledge semantics (`KnowledgeType.DECISION`) plus origin
context. The decision content belongs to knowledge. The origin story belongs to
provenance.

Example:

- Knowledge: "Team chose approach Y because of delivery risk."
- Knowledge type: `DECISION`
- Provenance mode: `STATED` or `DECIDED_IN_CONTEXT`
- Source: June planning meeting

This separation prevents one overloaded enum from carrying meaning, trust, and
state at the same time.

---

## 7. Is a Separate Domain Layer Needed?

Yes, for long-term architecture.

Memory Foundation should treat provenance as one layer in a small origin stack:

```text
MemorySource
-> Provenance Record
-> Optional Origin Mode / Acquisition Mode
-> Optional Actor Attribution
-> KnowledgeItem / CandidateKnowledge
```

Recommended conceptual layers:

1. **Source layer** — `MemorySource`
2. **Provenance record layer** — append-only origin events
3. **Origin mode layer** — epistemic/acquisition classification
4. **Attribution layer** — user, speaker, integration system, Assistant actor
5. **Trust/state layers** — confidence and lifecycle

This means extended categories should not all become one `ProvenanceType` enum.

Instead, long-term architecture should allow:

- `ProvenanceType` or equivalent for acquisition channel
- `OriginMode` or equivalent for epistemic character
- optional attribution facets

This can evolve without breaking the current foundation.

---

## 8. What Must Be Laid Down in Memory Foundation Now

Memory Foundation should **not** implement the full extended taxonomy now.

It should, however, lay down these architectural commitments now:

1. **Provenance is append-only.**
2. **Provenance is separate from confidence and lifecycle.**
3. **Provenance references MemorySource but does not own it.**
4. **CandidateKnowledge and KnowledgeItem may carry only a current provenance
   snapshot; full history belongs to provenance records.**
5. **Corrections and reconfirmations add provenance; they do not erase it.**
6. **The provenance model must allow additional origin dimensions later without
   rewriting accepted knowledge.**

Phase 1 may continue to use the current compact `ProvenanceType` set:

- `EXPLICITLY_STATED`
- `MODEL_INFERRED`
- `USER_CORRECTED`
- `RESEARCH_DERIVED`
- `INTEGRATION_IMPORTED`

But the vision document explicitly reserves space for a future `OriginMode` or
similar layer.

### What should not be deferred

- append-only provenance history
- source linkage
- actor/speaker optional attribution
- timestamp of origin observation
- distinction between initial provenance and later correction/reconfirmation
  provenance

### What can be deferred

- full enum expansion for all extended categories
- speaker identity integration with Speaker Intelligence
- rich evidence objects
- document page/section anchors
- external evidence graph

These should be tracked in Open Architecture Decisions if they create cross-block
dependencies.

---

## 9. Benefits for Future Assistant

A strong provenance model gives Assistant five long-term advantages:

1. **Better answer framing**

Assistant can distinguish:

- "You said..."
- "It was decided in..."
- "The system inferred..."
- "This was imported from..."
- "You later confirmed..."

2. **Appropriate caution**

Assistant can hedge when provenance is inferred, imported, or uncorrected.

3. **Correction-friendly dialogue**

When the user challenges a fact, Assistant can show the origin story and invite
correction without guessing.

4. **Cross-source reasoning**

The same knowledge type can be explained consistently whether it came from a
meeting, research briefing, document, or Assistant interaction.

5. **Action safety**

Before Actions, Assistant can verify whether a fact is confirmed, inferred, or
source-grounded.

Provenance is one of the main reasons Sekretar can become a platform rather than
a meeting chatbot with memory.

---

## 10. Risks of the Extended Model

The extended origin model creates real risks if implemented too early or too
flat.

### Risk 1 — Taxonomy explosion

Too many overlapping labels will confuse developers and models.

Example overlap:

- `Stated` vs `ExplicitlyStated`
- `Confirmed` vs `Confidence.CONFIRMED`
- `Decided` vs `KnowledgeType.DECISION`
- `AssistantInferred` vs `MODEL_INFERRED`

### Risk 2 — Duplication across layers

If provenance also owns trust and state, confidence and lifecycle become weak.

### Risk 3 — Premature block coupling

Speaker, document anchors, research evidence, and integration metadata can push
Provenance into owning external block semantics too early.

### Risk 4 — Meeting-centrism by accident

If provenance is designed only around meeting speaker/time/source, document,
research, Assistant, and integration origins will become second-class.

### Risk 5 — Implementation pressure before product need

A large taxonomy without services and UI benefit will slow Memory Foundation
without improving current product behavior.

The architecture must therefore grow by layers, not by one giant enum.

---

## 11. What Is Lost If This Is Not Laid Down Now

If Memory Foundation implements only a minimal source pointer and never reserves
space for provenance history and origin modes, the product will likely lose:

1. **Explainability depth**

Assistant answers will collapse into "the system knows this" without durable
origin detail.

2. **Retrofitting cost**

Adding provenance history later may require reprocessing old knowledge or
accepting permanent gaps.

3. **Correction auditability**

User corrections may overwrite meaning without preserving origin evolution.

4. **Cross-source comparability**

Meetings, documents, research, and integrations will each invent local origin
semantics.

5. **Future legal/compliance usefulness**

Deletion, forgetting, and traceability become harder if origin history is thin.

The current foundation already avoids the worst case by requiring provenance
for trusted knowledge. The next step is to ensure provenance becomes a real
append-only origin history, not only a snapshot field on CandidateKnowledge and
KnowledgeItem.

---

## 12. Provenance Across Future Sources

Provenance must work consistently across all future source families.

### Meetings

Origin may include:

- meeting source reference
- stated/inferred mode
- optional speaker attribution
- time of observation

Meetings are important, but must not define the only provenance shape.

### Documents

Origin may include:

- document source reference
- documented/imported mode
- optional section or passage note

### Research

Origin may include:

- research briefing reference
- research-derived mode
- link to confirmed task or research scenario

### Assistant

Origin may include:

- assistant interaction reference
- user-provided / assistant-inferred / user-corrected modes
- actor user

### Integrations

Origin may include:

- integration reference
- imported/external-evidence modes
- external system identity

### Memory evolution

When knowledge is corrected, reconfirmed, contradicted, or replaced, provenance
must append a new record rather than rewrite the old story.

---

## 13. Architectural Position for KnowledgeProvenance Entity

When `KnowledgeProvenance` is implemented, it should be understood as:

**An append-only origin record attached to CandidateKnowledge or KnowledgeItem,
linked to Account and MemorySource, optionally linked to actors and later
evidence references.**

It should not:

- own MemorySource;
- own knowledge text;
- replace confidence;
- replace lifecycle;
- store raw source content;
- depend on FastAPI, storage, or external block implementations.

It should:

- preserve origin history;
- support Assistant explainability;
- survive acceptance, correction, contradiction, and deletion/forgetting policy
  reviews;
- allow future origin-mode expansion.

---

## 14. Recommended Long-Term Formula

```text
MemorySource
-> CandidateKnowledge / KnowledgeItem
-> KnowledgeProvenance records (append-only)
-> Confidence snapshot
-> Lifecycle snapshot
-> MemoryContext selection
-> Research / Assistant / Actions
```

Within one knowledge item:

```text
What is known?        -> KnowledgeItem.text
Where from?           -> MemorySource + Provenance history
How acquired?         -> Provenance type / future origin mode
How trustworthy now?  -> Confidence
What state now?       -> Lifecycle
Why still relevant?   -> Context selection policy
```

This keeps Provenance in a clear place.

---

## 15. Decision Summary

### Provenance is

- the origin story of knowledge;
- append-only;
- source-linked;
- explainability-oriented;
- separate from confidence and lifecycle;
- required for trusted Memory.

### Provenance is not

- Memory itself;
- the source object;
- candidate state;
- current trust score;
- current lifecycle state;
- raw transcript/summary storage.

### Extended origin categories

- are directionally correct for long-term Assistant quality;
- must not all be flattened into one enum;
- should be split across provenance, confidence, and knowledge semantics;
- should influence Memory Foundation conceptually now;
- should be implemented in layers, not all at once.

### Memory Foundation now should commit to

- append-only provenance history;
- source linkage;
- correction/reconfirmation provenance events;
- reserved space for future origin modes and attribution.

### Memory Foundation now should not commit to

- full extended taxonomy implementation;
- speaker/document/evidence structures from external blocks;
- storage, API, or repository design.

---

## 16. Relation to Next Implementation Step

The next implementation step may introduce `KnowledgeProvenance` as a domain
entity and tests.

That implementation should follow this vision:

- compact Phase 1 provenance types are enough to begin;
- provenance history must be real and append-only;
- current snapshots on CandidateKnowledge and KnowledgeItem remain denormalized
  views, not the system of record;
- future origin-mode expansion must remain possible without breaking existing
  records.

If a broader taxonomy is needed before implementation, it should be recorded as
an Open Architecture Decision rather than hidden inside code comments.

---

## 17. Summary

Provenance is one of the core reasons Sekretar-Product can evolve from meeting
processing into a durable personal knowledge platform.

It makes Memory explainable to the future Assistant, auditable to the user, and
comparable across meetings, documents, research, integrations, and product
evolution.

The product should start with a compact provenance model, but architect toward a
layered origin system:

- source passport
- provenance history
- origin mode
- attribution
- confidence
- lifecycle

That is the long-term role of Provenance in Sekretar-Product.
