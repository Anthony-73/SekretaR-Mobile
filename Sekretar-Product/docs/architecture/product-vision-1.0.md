# Product Vision 1.0

Sekretar-Product is a personal AI platform for knowledge, research, work
support, and decision support.

It is not designed as another meeting transcription service. Meeting
processing remains an important entry point, but the product goal is broader:
to help a user preserve meaningful knowledge, understand context, prepare
materials, continue work after conversations, and make better decisions.

## Why Sekretar-Product Exists

The original SekretaR Mobile product proved a useful workflow:

```text
Meeting
-> Transcript
-> Summary
-> Tasks
-> Export
```

This workflow is valuable, but it is not enough to define the long-term
product. Many products can record meetings, transcribe speech, summarize
content, and extract tasks.

Sekretar-Product exists to solve the next problem: what happens after
information is captured.

The product should help the user:

- preserve important knowledge;
- understand previous context;
- connect decisions across meetings, documents, tasks, and projects;
- prepare materials before the user explicitly asks for them;
- support project work over time;
- answer questions using accumulated context;
- assist with actions after the user grants permission.

The long-term formula is:

```text
User
-> Memory
-> Research
-> Assistant
-> Actions
```

## Difference From Meeting Assistants

Classic meeting assistants usually focus on the meeting as the product:

- recording;
- transcription;
- summary;
- task extraction;
- calendar or document export.

Sekretar-Product treats meetings as sources, not as the final product.

A meeting can produce transcript, summary, task proposals, participant signals,
decisions, facts, and context. Some of this information may become long-term
knowledge. Some of it may remain only an artifact of the meeting. Some of it
may trigger research. Some of it may become confirmed work.

The product value is not just "what was said in this meeting." The product
value is "what this means for the user's future work."

## Why Meeting Is Not The Center

Meeting is an important source of information, but it is not the center of
Sekretar-Product.

The system must also support knowledge from:

- documents;
- voice notes;
- manual notes;
- research;
- integrations;
- user interactions with Assistant;
- future data sources.

If Meeting becomes the center, the architecture will repeat the limitations of
the old product. Knowledge would be trapped inside transcripts and summaries.
The user would have history, but not memory. The assistant would search old
meetings, but would not understand the user's working context.

The center of ownership and continuity is Account. The center of accumulated
knowledge is Memory.

## Why Memory Is Strategic

Memory is the strategic block because it gives the product continuity.

Without Memory, Sekretar-Product is a meeting processor with a better
interface. With Memory, it becomes a personal knowledge and work platform.

Memory allows the product to preserve:

- facts;
- decisions;
- project knowledge;
- knowledge about people;
- knowledge about companies and teams;
- working context;
- relationships between objects;
- source provenance;
- confidence and lifecycle state.

Memory must not be a dump of transcripts. Only meaningful knowledge should
enter Memory. The product should know where knowledge came from, when it
appeared, when it was last confirmed, and whether it is current, uncertain,
outdated, or contradictory.

Memory belongs to Account. It must survive device replacement, session
expiration, UI changes, and model replacement.

## Role Of Research Intelligence And DeepSeek

Research Intelligence is the product's research preparation layer.

Research does not run automatically for every extracted task. The intended
flow is:

```text
Meeting
-> Local Llama
-> Task Proposals
-> User confirms task
-> Research Intelligence
-> External LLM Gateway
-> DeepSeek or another external model
-> Prepared Materials / Research Brief
```

External LLMs such as DeepSeek are not the ordinary meeting-processing path.
They are used for heavier research scenarios, such as:

- market analysis;
- company checks;
- risk analysis;
- topic exploration;
- preparation of initial briefings;
- preparing materials for confirmed work.

DeepSeek is an external intellectual contour. It does not own product memory.
It consumes selected context through future Research Intelligence and External
LLM Gateway boundaries.

The final UX for external research may evolve. The user may work with prepared
materials inside Sekretar-Product, or the system may prepare a context handoff
to an external model. This decision belongs to future Research Intelligence,
External LLM Gateway, and Assistant work.

## Why Assistant Is The Final User Layer

Assistant is not a side feature. It is the final user-facing iteration of the
platform.

If Memory stores knowledge and Research prepares materials, Assistant is the
natural layer through which the user works with that knowledge.

The target interaction is:

```text
User
-> Assistant
-> Memory / Research / Meetings / Tasks
-> Answer / Explanation / Action
```

Assistant should eventually help the user ask questions such as:

- "Where did we discuss this?"
- "What did we decide about this project?"
- "Who is responsible for this task?"
- "Explain what was meant in that meeting."
- "What materials have already been collected on this topic?"
- "Why did we make this decision?"

Assistant does not own Memory. Assistant uses Memory, Research Intelligence,
Meetings, Tasks, and User Context to help the user understand and act.

Assistant should become available through text and voice. The future AI
Assistant / Second Brain should be a separate entry point in the existing UI,
not a replacement for the core meeting workflow.

## Long-Term Platform Evolution

The product evolves in layers:

1. Preserve the existing UX contract.
2. Establish Account-owned identity and access foundations.
3. Establish Product API contracts and request context.
4. Establish Memory as the central knowledge layer.
5. Treat Meetings as one important source for Memory.
6. Turn extracted tasks into user-confirmed actions.
7. Use Research Intelligence for confirmed tasks that need preparation.
8. Use External LLM Gateway for replaceable external reasoning providers.
9. Build Assistant on top of Memory, Research, Meetings, Tasks, and User
   Context.
10. Add voice interaction without breaking the existing product flow.

The existing UX remains a product contract:

```text
Start Page
-> Start Button
-> Intro Video
-> Workspace
-> Record Meeting / Upload File
-> Processing
-> Transcript
-> Summary
-> Tasks
-> History / New Meetings
```

New capabilities should enter through the existing experience: modal windows,
additional panels, or separate entry points. The product should remain simple
enough that the user does not need instructions for the basic workflow.

## Current Product Direction

Sekretar-Product is an AI platform for personal memory, research, and work
support.

Meeting processing is the first proven capture workflow.

Memory is the long-term knowledge layer.

Research prepares materials for confirmed work.

Assistant becomes the natural interface for using the platform.

Actions are initiated only when the product has the right context and the user
has granted the required permission.
