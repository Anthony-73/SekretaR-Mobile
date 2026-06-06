# Worker

Worker executes background jobs from the queue.

Worker is mandatory in the target architecture, even if the first implementation has only one process and one queue.

Job categories:

- meeting processing;
- STT;
- diarization;
- speaker matching;
- summary generation;
- task extraction;
- memory extraction;
- memory consolidation;
- research jobs;
- External LLM calls;
- exports;
- calendar integrations;
- retries and recovery.

Worker should record attempts, errors, timings, model runs, and produced artifacts.
