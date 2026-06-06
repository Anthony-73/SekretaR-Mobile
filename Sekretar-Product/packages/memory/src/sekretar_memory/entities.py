"""Memory domain entity placeholders.

These classes describe the approved Memory domain surface. They intentionally
contain no business logic, persistence behavior, or implementation details.
"""


class KnowledgeItem:
    """Primary unit of durable Account-owned knowledge."""


class MemorySource:
    """Source reference that may produce candidate knowledge."""


class CandidateKnowledge:
    """Information that may become Memory but is not accepted yet."""


class KnowledgeProvenance:
    """Explanation of where knowledge came from."""


class KnowledgeConfidence:
    """Product-level trust signal for knowledge."""


class KnowledgeLifecycleRecord:
    """Record of knowledge lifecycle movement over time."""


class KnowledgeRelation:
    """Meaningful relation between knowledge and another reference."""


class MemoryCorrection:
    """User or system correction applied to knowledge."""


class MemoryContradiction:
    """Explicit conflict between knowledge items or candidates."""


class MemoryContext:
    """Scenario-specific subset of Memory for another block."""
