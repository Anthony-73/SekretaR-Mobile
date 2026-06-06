"""Memory domain event placeholders."""


class MemoryEvent:
    """Base domain event marker for Memory events."""


class CandidateKnowledgeDetected(MemoryEvent):
    """Emitted when source content produces candidate knowledge."""


class KnowledgeAccepted(MemoryEvent):
    """Emitted when candidate knowledge becomes durable Memory."""


class KnowledgeRejected(MemoryEvent):
    """Emitted when candidate knowledge is rejected."""


class KnowledgeDeferred(MemoryEvent):
    """Emitted when candidate knowledge remains unconfirmed or pending."""


class KnowledgeMerged(MemoryEvent):
    """Emitted when candidate knowledge is merged with existing knowledge."""


class KnowledgeConfirmed(MemoryEvent):
    """Emitted when knowledge is confirmed."""


class KnowledgeCorrected(MemoryEvent):
    """Emitted when knowledge is corrected."""


class KnowledgeContradictionDetected(MemoryEvent):
    """Emitted when knowledge conflicts with another knowledge item."""


class KnowledgeMarkedOutdated(MemoryEvent):
    """Emitted when knowledge is marked outdated."""


class KnowledgeArchived(MemoryEvent):
    """Emitted when knowledge is archived."""


class KnowledgeDeleted(MemoryEvent):
    """Emitted when knowledge is deleted."""


class KnowledgeForgotten(MemoryEvent):
    """Emitted when knowledge must no longer be used as context."""


class KnowledgeRelationCreated(MemoryEvent):
    """Emitted when a knowledge relation is created."""


class MemoryContextPrepared(MemoryEvent):
    """Emitted when Memory prepares scenario-specific context."""


class MemorySourceLinked(MemoryEvent):
    """Emitted when knowledge is linked to a source reference."""
