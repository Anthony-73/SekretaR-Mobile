# Memory Block

Memory is an independent block.

Meeting does not own Memory. Meeting is only one possible source of memory.

Responsibilities:

- user facts;
- project knowledge;
- decision history;
- knowledge about people and contacts;
- links between knowledge entries;
- provenance and source references;
- change history;
- confidence;
- correction and deletion.

Memory must not become a dump of meeting summaries. It needs classification, source tracking, deduplication, review, and lifecycle rules.

Memory does not perform STT, Recorder logic, Speaker Intelligence, or external LLM calls.

Memory must be designed so it can later move to a separate database or specialized storage without changing the rest of the architecture.
