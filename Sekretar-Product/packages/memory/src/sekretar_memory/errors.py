"""Memory domain errors."""


class MemoryError(Exception):
    """Base error for Memory domain failures."""


class KnowledgeNotFound(MemoryError):
    """Raised when knowledge cannot be found."""


class CandidateKnowledgeNotFound(MemoryError):
    """Raised when candidate knowledge cannot be found."""


class MemorySourceNotFound(MemoryError):
    """Raised when a memory source reference cannot be found."""


class ProvenanceRequired(MemoryError):
    """Raised when stable knowledge is missing provenance."""


class InvalidKnowledgeLifecycleTransition(MemoryError):
    """Raised when a lifecycle transition is not allowed."""


class KnowledgeOwnershipMismatch(MemoryError):
    """Raised when knowledge does not belong to the expected Account."""


class InvalidMemorySource(MemoryError):
    """Raised when a source cannot be used for Memory ingestion."""


class KnowledgeAlreadyDeleted(MemoryError):
    """Raised when deleted knowledge is used as active Memory."""


class ContradictionNotFound(MemoryError):
    """Raised when a contradiction reference cannot be found."""


class MemoryContextUnavailable(MemoryError):
    """Raised when context cannot be prepared for a scenario."""


class InvalidKnowledgeContent(MemoryError):
    """Raised when knowledge content violates Memory content rules."""


class ConfidenceRequired(MemoryError):
    """Raised when confidence is missing for accepted knowledge."""


class KnowledgeNotEligibleForContext(MemoryError):
    """Raised when knowledge cannot be used in Memory context."""


class KnowledgeStatusMismatch(MemoryError):
    """Raised when status and confidence are incompatible."""


class KnowledgeImmutable(MemoryError):
    """Raised when terminal knowledge is mutated."""


class LifecycleRecordInvalid(MemoryError):
    """Raised when a lifecycle record violates domain rules."""


class LifecycleRecordOwnershipMismatch(MemoryError):
    """Raised when a lifecycle record does not match knowledge ownership."""


class LifecycleRecordImmutable(MemoryError):
    """Raised when an append-only lifecycle record is mutated."""


class CandidateInvalid(MemoryError):
    """Raised when candidate knowledge violates domain rules."""


class CandidateAlreadyResolved(MemoryError):
    """Raised when a terminal candidate is mutated or reused."""


class CandidateNotEligibleForAcceptance(MemoryError):
    """Raised when candidate knowledge cannot be accepted."""


class InvalidCandidateTransition(MemoryError):
    """Raised when a candidate lifecycle transition is not allowed."""


class MemorySourceInvalid(MemoryError):
    """Raised when a memory source violates domain rules."""


class InvalidSourceType(MemoryError):
    """Raised when a source type is missing or not allowed."""


class InvalidSourceReference(MemoryError):
    """Raised when an external source reference is missing or invalid."""


class MemorySourceLinkMismatch(MemoryError):
    """Raised when candidate or knowledge does not match a memory source."""


class ProvenanceRecordInvalid(MemoryError):
    """Raised when a provenance record violates domain rules."""


class ProvenanceRecordOwnershipMismatch(MemoryError):
    """Raised when a provenance record does not match knowledge ownership."""


class ProvenanceRecordImmutable(MemoryError):
    """Raised when an append-only provenance record is mutated."""
