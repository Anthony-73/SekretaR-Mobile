"""Memory value object placeholders.

The classes in this module define the intended value-object surface of the
Memory package. They intentionally contain no validation or behavior yet.
"""


class AccountId:
    """Identifier of the Account that owns Memory."""


class UserId:
    """Identifier of the user acting within Account-owned Memory."""


class DeviceId:
    """Device identifier used as access metadata, not as Memory owner."""


class SessionId:
    """Session identifier used as temporary access metadata."""


class KnowledgeId:
    """Identifier of a durable knowledge item."""


class CandidateKnowledgeId:
    """Identifier of a candidate knowledge item."""


class SourceId:
    """Identifier of a source that may produce candidate knowledge."""


class SourceReference:
    """Reference to an external source object without transferring ownership."""


class SourceTimestamp:
    """Timestamp associated with source appearance or source evidence."""


class KnowledgeText:
    """Meaningful durable knowledge text, not a raw source dump."""


class KnowledgeSummary:
    """Short human-readable description of knowledge."""


class KnowledgeLanguage:
    """Language marker for knowledge content."""


class KnowledgeTags:
    """Tags that may help classify knowledge without owning relationships."""


class ProvenanceNote:
    """Human-readable note explaining where knowledge came from."""


class ProvenanceTimestamp:
    """Timestamp of provenance creation or source observation."""


class ConfidenceScore:
    """Optional product-level numeric confidence marker."""


class ConfidenceReason:
    """Reason explaining a confidence level."""


class LifecycleReason:
    """Reason for a lifecycle transition."""


class LifecycleTimestamp:
    """Timestamp of a lifecycle transition."""


class RelatedObjectReference:
    """Reference to related product object without transferring ownership."""
