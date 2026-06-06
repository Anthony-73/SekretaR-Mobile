# External LLM Gateway Block

External LLM Gateway isolates all access to external API models.

External LLM is used for complex intelligence tasks, research, assistant reasoning, and future advanced AI features. It must be independently replaceable from Local LLM.

Responsibilities:

- provider abstraction;
- model selection;
- request policy;
- cost and rate control;
- privacy filtering;
- retries;
- model run logging.

External LLM should not be used as the default path for ordinary meeting processing.
