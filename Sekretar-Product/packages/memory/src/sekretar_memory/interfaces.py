"""External Memory service interfaces.

These interfaces describe how future blocks should interact with Memory without
giving Memory ownership of their lifecycles.
"""


class MeetingsMemoryInterface:
    """Contract boundary between Meetings and Memory."""


class TasksMemoryInterface:
    """Contract boundary between Tasks and Memory."""


class ResearchMemoryInterface:
    """Contract boundary between Research Intelligence and Memory."""


class AssistantMemoryInterface:
    """Contract boundary between Assistant and Memory."""


class SpeakerMemoryInterface:
    """Contract boundary between Speaker Intelligence and Memory."""


class ExternalLLMMemoryInterface:
    """Contract boundary for selected context through external LLM flows."""
