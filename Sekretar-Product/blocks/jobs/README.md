# Jobs Block

Jobs describes background work and queue execution.

All long-running, retryable, external, or expensive work should be represented as jobs.

Responsibilities:

- job identity;
- job type;
- job status;
- attempts;
- retry policy;
- error records;
- produced artifact references;
- timing and observability metadata.

Jobs are the foundation for 24/7 operation and recovery.
