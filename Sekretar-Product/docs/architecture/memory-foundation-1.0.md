# Memory Foundation 1.0

Status: domain architecture specification

Scope: Memory block foundation

This document records the accepted domain-level foundation for the Memory block
in Sekretar-Product.

It does not define implementation entities, database tables, APIs, storage
technology, RAG, vector memory, or implementation-layer design.

## 1. Purpose

Memory is the central knowledge layer of Sekretar-Product.

Memory enables the long-term product direction:

```text
Sources
-> Knowledge
-> Context
-> Research
-> Assistant
-> Actions
```

Memory is not:

- Meeting History;
- Transcript Storage;
- Summary Storage;
- Task Storage;
- raw file storage;
- chat log storage;
- model-owned memory.

Memory preserves meaningful durable knowledge for an Account over time.

## 2. Block Responsibility

Memory is responsible for:

- preserving meaningful knowledge owned by an Account;
- distinguishing facts, decisions, context, preferences, relationships, and
  knowledge about people;
- preserving where knowledge came from;
- expressing confidence in knowledge;
- managing the lifecycle of knowledge;
- supporting correction, contradiction, deletion, and forgetting;
- connecting related knowledge;
- preparing context for future Research and Assistant scenarios;
- preventing Memory from becoming a dump of transcripts, summaries, tasks, or
  raw model output.

Memory is not responsible for:

- recording meetings;
- uploading files;
- STT;
- diarization;
- voice fingerprints;
- summary generation;
- task extraction;
- active task lifecycle;
- task execution;
- calendar integration;
- external research execution;
- DeepSeek or external model calls;
- ownership of recordings, transcripts, summaries, files, or chunks;
- Product API transport;
- Security policy;
- Billing policy.

## 3. Main Domain Concepts

### Account-Owned Memory

All Memory belongs to Account.

Device does not own Memory.

Session does not own Memory.

AI models do not own Memory.

This rule allows knowledge to survive device replacement, session expiration,
model replacement, and UI changes.

### Knowledge

Knowledge is meaningful information that can help the user or product
understand context later.

Examples:

- a fact;
- a decision;
- a reason behind a decision;
- a responsibility;
- a user or client preference;
- a relationship between a person, project, task, company, or meeting;
- stable working context;
- a confirmed research conclusion;
- a correction provided by the user.

Knowledge is not just copied source text. It is meaning that remains useful
outside the original source.

### Source

Source is the place where candidate knowledge first appears.

Examples:

- meeting;
- document;
- voice note;
- manual note;
- confirmed task;
- research result;
- integration;
- Assistant interaction;
- future source.

Source does not belong to Memory. Memory receives knowledge from sources but
does not own the lifecycle of the source itself.

### Candidate Knowledge

Candidate Knowledge is information that may become Memory but has not yet been
accepted as durable knowledge.

Candidate Knowledge may be:

- accepted;
- rejected;
- deferred;
- merged with existing knowledge;
- marked as unconfirmed;
- flagged as contradictory;
- sent for user clarification;
- ignored as low-value noise.

### Provenance

Provenance describes where knowledge came from.

It answers:

- which source produced the knowledge;
- when it appeared;
- whether it came from a meeting, document, research result, note, integration,
  or Assistant interaction;
- whether it was explicitly stated or model-inferred;
- whether it was user-confirmed.

Without provenance, Assistant cannot explain why the system knows something.

### Confidence

Confidence describes how trustworthy a piece of knowledge is.

It considers:

- whether the knowledge was explicitly stated;
- whether it was inferred;
- whether the user confirmed it;
- whether multiple sources support it;
- whether it conflicts with other knowledge.

Confidence is a product-level trust signal, not only a model score.

### Lifecycle

Lifecycle describes how knowledge changes over time.

Memory must distinguish:

- new knowledge;
- unconfirmed knowledge;
- active knowledge;
- confirmed knowledge;
- outdated knowledge;
- contradictory knowledge;
- corrected knowledge;
- deleted or forgotten knowledge.

Lifecycle is necessary because user context changes over time.

### Knowledge Relationship

Knowledge can be related to other knowledge.

Examples:

- a person is related to a project;
- a decision is related to a meeting;
- a task is related to a client;
- a research briefing is related to a confirmed task;
- new knowledge updates old knowledge;
- new knowledge contradicts old knowledge.

Memory can connect knowledge, but it must not become the owner of every product
object.

### Context

Context is a selected subset of Memory relevant to a specific situation.

Context may be used by:

- Research Intelligence;
- Assistant;
- Tasks;
- Meetings;
- User Context;
- future Actions.

Context is not all Memory. It is the relevant knowledge selected for a
question, task, research scenario, or action.

### Correction

Correction is a user or system update that changes knowledge.

Correction allows Memory to remain trustworthy. A user must be able to correct
wrong, incomplete, or outdated knowledge.

### Contradiction

Contradiction is a conflict between new knowledge and existing knowledge.

Memory should not silently overwrite conflicting knowledge. It should preserve
the fact that the knowledge changed, conflicted, or needs confirmation.

### Forgetting And Deletion

Memory must support deletion and forgetting.

Forgetting may be required because:

- the knowledge is wrong;
- the user requests deletion;
- the knowledge is private or sensitive;
- the knowledge is outdated;
- the knowledge should no longer be used as context.

Memory must be able not only to remember, but also to stop using knowledge.

## 4. Knowledge Source Model

Sources are inputs that may produce Candidate Knowledge.

The full content of a source must not automatically become Memory.

### Existing Sources

From current Sekretar product experience:

- meeting recording;
- uploaded audio or video file;
- transcript;
- summary;
- task proposals;
- confirmed tasks;
- meeting history;
- Android Recorder flow;
- browser recorder flow.

Transcript, summary, and task proposals are artifacts or source outputs. They
are not Memory by themselves.

### Near-Term Sources

Expected near-term sources:

- structured meeting analysis;
- Speaker Intelligence output;
- user-confirmed tasks;
- research briefings;
- manual notes;
- uploaded documents;
- Assistant interactions;
- user corrections.

### Future Sources

Future sources may include:

- calendar integrations;
- CRM-like integrations;
- email or document integrations;
- project management tools;
- voice assistant conversations;
- external research sources;
- team or company knowledge sources.

## 5. Provenance Model

Every accepted piece of durable knowledge should have provenance.

Provenance must make it possible to answer:

- where the knowledge came from;
- when it appeared;
- whether it was stated, inferred, or corrected;
- whether a user confirmed it;
- which source can explain it later.

Provenance allows future Assistant responses to be explainable.

Examples:

- "This was discussed in the June planning meeting."
- "This came from a confirmed research briefing."
- "The user corrected this during an Assistant interaction."
- "This was inferred from a meeting but has not been confirmed."

Knowledge without provenance should not become stable trusted Memory.

## 6. Confidence Model

Confidence expresses trust in knowledge.

Confidence must account for:

- explicit statements;
- model inference;
- user confirmation;
- repeated support from multiple sources;
- contradiction with other knowledge;
- age of knowledge;
- source reliability.

Conceptually, confidence can indicate:

- directly confirmed knowledge;
- strongly supported knowledge;
- inferred but useful knowledge;
- unconfirmed knowledge;
- doubtful knowledge;
- contradicted knowledge.

Confidence must be used when Memory provides context to Research or Assistant.

## 7. Knowledge Lifecycle

The conceptual lifecycle of knowledge is:

```text
Source Appears
-> Candidate Knowledge Detected
-> Relevance Evaluation
-> Provenance Attached
-> Confidence Estimated
-> Accepted / Deferred / Rejected
-> Active Knowledge
-> Used As Context
-> Reconfirmed / Corrected / Contradicted / Outdated
-> Archived / Deleted / Forgotten
```

### Source Appears

A meeting, document, note, research result, integration event, or Assistant
interaction appears.

The source itself is not Memory.

### Candidate Knowledge Detected

Possible knowledge is detected from the source.

At this stage, it is only candidate knowledge.

### Relevance Evaluation

The product determines whether the candidate has future value.

Questions:

- Will this help the user later?
- Does it relate to a project, person, task, decision, company, or context?
- Is it temporary noise?
- Is it a duplicate?

### Provenance Attached

If the candidate is preserved, provenance must be attached.

Knowledge without provenance should not become trusted stable Memory.

### Confidence Estimated

The product estimates how trustworthy the knowledge is.

The estimate should consider whether it was stated, inferred, confirmed,
supported, or contradicted.

### Accepted / Deferred / Rejected

The candidate may be:

- accepted as active knowledge;
- deferred as unconfirmed;
- rejected as low-value or noisy;
- merged with existing knowledge;
- flagged as contradiction.

### Active Knowledge

Accepted knowledge becomes part of Memory and may be used as context.

### Used As Context

Knowledge may support Assistant, Research, Tasks, Meetings, or future Actions.

Confidence and lifecycle must be considered when knowledge is used.

### Reconfirmed / Corrected / Contradicted / Outdated

Knowledge may later be:

- reconfirmed by another source;
- corrected by the user;
- contradicted by newer knowledge;
- marked outdated.

### Archived / Deleted / Forgotten

Knowledge may stop being used as active context or may be deleted.

Memory must support forgetting as a first-class product capability.

## 8. Relationship With Other Blocks

### Identity

Memory receives:

- Account ownership context;
- User context;
- Device and Session context as access metadata only.

Memory gives:

- no Memory content ownership back to Identity.

Memory must not:

- create Account;
- manage Session;
- manage DeviceGrant;
- perform authentication;
- store knowledge as device-owned data.

### Meetings

Memory receives:

- candidate knowledge from meetings;
- source references to meetings;
- decisions;
- facts;
- responsibilities;
- project context;
- participant-related signals;
- reasons behind decisions.

Memory gives:

- relevant prior knowledge when a meeting needs context;
- related knowledge for future Assistant explanations.

Memory must not:

- own meeting lifecycle;
- store raw transcripts as Memory;
- store summaries as Memory;
- perform STT;
- generate summaries;
- manage upload;
- become meeting history.

### Tasks

Memory receives:

- confirmed task context;
- responsibility signals;
- outcomes that change knowledge;
- user corrections related to tasks.

Memory gives:

- context for task execution;
- previous decisions;
- preferences;
- client, project, and people knowledge.

Memory must not:

- own task lifecycle;
- create active tasks on its own;
- confirm tasks for the user;
- execute tasks;
- manage calendar integration.

### Research Intelligence

Memory receives:

- confirmed research findings;
- prepared materials that become durable knowledge;
- risk notes;
- market, company, or topic conclusions;
- briefing conclusions accepted as useful knowledge.

Memory gives:

- internal context for research;
- known facts;
- previous decisions;
- project, client, and person context;
- constraints and preferences.

Memory must not:

- run external research;
- call DeepSeek;
- choose external models;
- decide research depth.

### Assistant

Memory receives:

- user corrections;
- clarified preferences;
- explicit notes;
- confirmed context from dialogue;
- user-provided knowledge.

Memory gives:

- relevant context;
- facts;
- decisions;
- relationships;
- explanations with provenance;
- confidence and lifecycle signals.

Memory must not:

- conduct dialogue;
- generate final Assistant answers;
- initiate actions;
- own Assistant conversation lifecycle.

### Speaker Intelligence

Memory receives:

- participant signals;
- speaker identity hints;
- links between repeated voices and possible people;
- confidence about participant identity.

Memory may give:

- known person context for future disambiguation scenarios.

Memory must not:

- perform diarization;
- create voice fingerprints;
- match voices across meetings;
- decide who speaks without Speaker Intelligence.

The boundary is:

```text
Speaker Intelligence -> Who speaks
Memory -> What is known about this person
```

### External LLM Gateway

Memory gives:

- selected context through controlled Research or Assistant flows.

Memory receives:

- no required direct input from External LLM Gateway.

Memory must not:

- call external models;
- store model-private memory;
- depend on DeepSeek as a memory owner;
- expose all Memory without contextual selection.

## 9. Role Of Memory For Meetings, Tasks, Research, And Assistant

### Meetings

Meetings are one important source of Memory.

A meeting may produce transcript, summary, task proposals, participant signals,
decisions, facts, and context. Only meaningful durable knowledge should become
Memory.

Meeting remains a source and lifecycle object. It does not own Memory.

### Tasks

Tasks represent work to be done.

Memory represents what is known.

Tasks can use Memory as context, and completed or corrected tasks may update
Memory, but Memory does not own task execution.

### Research

Research Intelligence prepares materials for confirmed tasks.

Research can use Memory to understand internal context, and its confirmed
findings may later become Memory.

Memory does not execute research.

### Assistant

Assistant is the future user-facing layer that helps the user work with
accumulated context.

Assistant uses Memory to explain, connect, retrieve, and reason over the user's
knowledge.

Assistant does not own Memory.

## 10. What Counts As Knowledge

Information may become knowledge when it:

- has value beyond one source;
- helps understand a user, project, person, company, decision, or context;
- can help Assistant answer a future question;
- can help Research prepare materials;
- can explain a future action;
- has provenance;
- has confidence or an explicit unconfirmed state;
- can be updated, corrected, contradicted, or deleted.

Examples:

- "Client A prefers short commercial proposals."
- "Ivan is responsible for warehouse process design in Project X."
- "The team chose approach Y because of delivery risk."
- "Company A is sensitive to delivery timelines."
- "The user prefers a short briefing before detailed research."
- "The market analysis topic came from a confirmed task."

## 11. What Must Not Become Memory Automatically

The following must not automatically enter Memory:

- entire transcripts;
- entire summaries;
- entire meeting history;
- every sentence from a meeting;
- filler speech;
- temporary meeting logistics;
- duplicate statements;
- unhelpful model guesses;
- raw model output;
- all task proposals;
- all external search results;
- processing statuses;
- upload metadata;
- binary artifacts;
- files;
- chunks;
- calendar links without meaningful context.

Core rule:

```text
Source content is not Memory.
Meaningful durable knowledge may become Memory.
```

## 12. Architectural Constraints

Memory Foundation 1.0 follows these constraints:

1. Memory belongs to Account.
2. Memory does not belong to Device, Session, or Model.
3. Meeting is a source of Memory, not the owner of Memory.
4. Transcript is not Memory.
5. Summary is not Memory.
6. Task is not Memory.
7. Research result does not become Memory automatically.
8. Assistant uses Memory but does not own Memory.
9. Speaker Intelligence identifies who speaks; Memory stores what is known.
10. Knowledge without provenance must not become trusted stable Memory.
11. Knowledge must have confidence or an explicit unconfirmed state.
12. Knowledge must have lifecycle.
13. Memory must support correction.
14. Memory must support contradiction.
15. Memory must support deletion and forgetting.
16. Memory must not call LLMs as a required domain mechanism.
17. Models consume Memory; models do not own Memory.
18. Memory must remain independent of specific storage technology.
19. Memory must not define Product API transport.
20. Memory must not own Security or Billing policy.

## 13. Explicit Non-Goals

This document does not define:

- implementation entities;
- Python classes;
- database tables;
- database schemas;
- API endpoints;
- storage technology;
- vector search;
- RAG design;
- model prompts;
- retrieval algorithms;
- queue jobs;
- UI flows;
- implementation-layer services.

Those belong to later architecture and implementation phases.

## 14. Summary

Memory Foundation 1.0 defines Memory as the Account-owned knowledge layer of
Sekretar-Product.

Memory preserves meaningful durable knowledge, not raw source content.

Memory is built around:

- Knowledge;
- Source;
- Candidate Knowledge;
- Provenance;
- Confidence;
- Lifecycle;
- Relationships;
- Context;
- Correction;
- Contradiction;
- Forgetting.

Memory supports future Research and Assistant scenarios by providing trusted,
explainable, lifecycle-aware context.

Memory keeps Sekretar-Product from becoming only a meeting assistant.

It is the foundation that allows the product to become a personal AI platform
for knowledge, research, work support, and decision support.
