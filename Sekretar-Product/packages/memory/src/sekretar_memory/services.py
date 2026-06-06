"""Memory domain service placeholders.

Service implementations are intentionally deferred. These classes define the
approved service surface for the Memory implementation layer.
"""


class MemoryIngestionService:
    """Accepts source references and candidate knowledge."""


class KnowledgeAcceptanceService:
    """Accepts, rejects, defers, merges, or flags candidate knowledge."""


class KnowledgeLifecycleService:
    """Manages conceptual lifecycle transitions for knowledge."""


class KnowledgeCorrectionService:
    """Applies user or system corrections to knowledge."""


class KnowledgeRelationService:
    """Manages meaningful knowledge relations and contradictions."""


class MemoryContextService:
    """Prepares scenario-specific context for other blocks."""


class MemoryQueryService:
    """Provides domain-level Memory read operations."""
