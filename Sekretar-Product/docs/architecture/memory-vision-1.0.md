# Memory Vision 1.0

Memory is the long-term knowledge layer of Sekretar-Product.

It is not meeting history, not transcript storage, not summary storage, and not
a task list. Memory is the part of the product that preserves meaningful
knowledge for an Account over time.

## What Memory Is

Memory stores knowledge that remains useful beyond the source where it first
appeared.

It may include:

- facts;
- decisions;
- relationships between objects;
- project knowledge;
- knowledge about people;
- knowledge about companies;
- knowledge about teams;
- working context;
- recurring preferences;
- important explanations;
- links between previous conversations, documents, meetings, tasks, and
  research.

Memory belongs to Account. It should survive device replacement, session
expiration, model replacement, and UI changes.

## What Memory Is Not

Memory is not a complete copy of every source.

Memory is not:

- the full history of meetings;
- raw transcripts;
- summaries;
- task lists;
- uploaded files;
- chat logs;
- a vector dump;
- a private memory owned by a model.

Sources can produce artifacts. Memory stores only the knowledge that should
remain useful after the artifact itself is no longer the primary object of
attention.

## Difference From Meeting History

Meeting history answers:

"What meetings happened, when, and what was produced?"

Memory answers:

"What does the system know now, based on all available sources?"

A meeting can remain in history without all of its content becoming Memory.
Only meaningful facts, decisions, relationships, participant knowledge, or
working context should be considered for Memory.

Meeting is a source. Memory is accumulated knowledge.

## Difference From Summary

Summary is a short explanation of one source.

Memory is durable knowledge extracted from many sources over time.

A summary may say:

"The team discussed warehouse responsibilities."

Memory may preserve:

"For Project X, Ivan is currently responsible for warehouse process design.
This was agreed during the June planning meeting and has not yet been
reconfirmed."

Summary helps the user understand a source. Memory helps the product understand
the user's context.

## Difference From Tasks

Tasks describe work to be done.

Memory describes what is known.

A task may be:

"Prepare a commercial proposal for Client A by Friday."

Memory may know:

"Client A prefers short proposals, previously rejected a long technical
document, and is sensitive to delivery timelines."

Tasks can use Memory. Research can use Memory. Assistant can use Memory.
Memory does not become the owner of task execution.

## Sources Of Memory

Memory can be populated from:

- meetings;
- documents;
- voice notes;
- manual notes;
- confirmed research outputs;
- integrations;
- tasks and project activity;
- user corrections;
- interaction with Assistant;
- future product sources.

No source automatically becomes Memory in full.

The product should extract candidate knowledge, preserve provenance, and allow
the knowledge to become confirmed, updated, corrected, or removed over time.

## What Counts As Knowledge

Knowledge is information that can help the user or product understand context
later.

Examples:

- a confirmed decision;
- a stable fact about a project;
- an important preference;
- a responsibility assignment;
- a relationship between people, companies, projects, and tasks;
- a recurring constraint;
- a reason behind a decision;
- a useful research conclusion;
- a correction provided by the user.

Knowledge should be meaningful outside the exact wording of the original
source.

## What Does Not Count As Knowledge

The following should not automatically become Memory:

- every sentence in a transcript;
- filler speech;
- temporary meeting logistics;
- duplicate facts already known;
- uncertain guesses without useful context;
- raw model output;
- every extracted task;
- every search result from external research;
- low-value details that do not help future work.

The system should avoid turning Memory into a data dump.

## Provenance, Confidence, And Lifecycle

Memory must preserve where knowledge came from.

Provenance answers:

- which source produced this knowledge;
- when it appeared;
- which meeting, document, research result, note, or assistant interaction it
  came from;
- whether it was user-confirmed or model-inferred.

Confidence answers:

- how reliable this knowledge is;
- whether it was directly stated or inferred;
- whether it was confirmed by the user;
- whether multiple sources support it.

Lifecycle answers:

- whether knowledge is current;
- whether it is unconfirmed;
- whether it is outdated;
- whether it conflicts with newer knowledge;
- whether it was corrected or deleted.

The product must be able to distinguish:

- actual knowledge;
- unconfirmed knowledge;
- outdated knowledge;
- contradictory knowledge.

Without provenance, confidence, and lifecycle, Memory would become unreliable
and difficult to trust.

## Account Ownership

Memory belongs to Account.

Device does not own Memory.

Session does not own Memory.

A model does not own Memory.

This ownership rule is required because the user's knowledge must remain
available across devices, sessions, UI changes, and model changes.

Identity provides the Account/User/Device context. Memory uses that context for
ownership, but Identity does not own Memory content.

## Models Consume Memory

AI models are consumers of Memory, not owners of Memory.

Correct flow:

```text
Memory
-> Context
-> Model
-> Response
```

Incorrect flow:

```text
Model
-> Own Memory
```

Models can be replaced. Memory must persist.

Local Llama may use Memory for meeting-related context and local operations.
External models such as DeepSeek may receive selected context through Research
Intelligence and External LLM Gateway. Neither local nor external models should
become the storage layer for user knowledge.

## How Assistant Uses Memory

Assistant is the future user-facing layer that helps the user work with
accumulated context.

Assistant uses Memory to answer questions such as:

- "Where did we discuss this?"
- "What did we decide about this project?"
- "Who is responsible for this?"
- "Why did we make this decision?"
- "What do we know about this client?"
- "What materials have already been prepared?"

Assistant should be able to explain, connect, and retrieve knowledge across
meetings, documents, tasks, research, projects, and user interactions.

Assistant does not own Memory. Assistant asks Memory for relevant context and
uses that context to help the user understand or act.

## How Sources Populate Memory

Meetings can contribute:

- decisions;
- facts;
- responsibilities;
- participant signals;
- project context;
- task-related context;
- reasons behind decisions.

Documents can contribute:

- stable facts;
- project materials;
- requirements;
- external context;
- reference knowledge.

Research can contribute:

- prepared materials;
- findings;
- risk notes;
- market or company context;
- briefing conclusions.

Assistant interactions can contribute:

- user corrections;
- clarified preferences;
- confirmed context;
- new notes;
- explicit instructions.

Integrations can contribute:

- calendar context;
- document metadata;
- CRM-like information;
- external work context.

Each source should produce candidate knowledge. Memory should preserve only what
is meaningful, traceable, and useful for future work.

## Relationship With Other Blocks

Memory depends on Identity for Account ownership context.

Memory receives information from Meetings, Documents, Research, Integrations,
Tasks, Assistant interactions, and future sources.

Memory may receive participant-related signals from Speaker Intelligence, but
Speaker Intelligence remains responsible for identifying who speaks.

Memory may support Research Intelligence by providing internal context.

Memory may support Assistant by providing relevant knowledge.

Memory should not own:

- meeting lifecycle;
- task execution;
- external research execution;
- diarization;
- voice fingerprints;
- Product API transport;
- security policy;
- billing policy.

## Direction

Memory is the foundation that allows Sekretar-Product to become more than a
meeting assistant.

It turns captured information into durable context.

It allows Research to prepare better materials.

It allows Assistant to become useful rather than generic.

It allows future Actions to be based on the user's real working context.

Memory Foundation should be designed after this vision is accepted, but this
document intentionally does not define entities, tables, APIs, storage choices,
or implementation details.
