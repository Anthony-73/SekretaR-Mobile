"""Memory domain constants."""

from .enums import CandidateKnowledgeStatus, ConfidenceLevel, KnowledgeStatus, SourceType

KNOWLEDGE_ITEM_STATUSES: frozenset[KnowledgeStatus] = frozenset(
    status
    for status in KnowledgeStatus
    if status is not KnowledgeStatus.CANDIDATE
)

ACCEPTANCE_INITIAL_STATUSES: frozenset[KnowledgeStatus] = frozenset(
    {
        KnowledgeStatus.ACTIVE,
        KnowledgeStatus.UNCONFIRMED,
    }
)

TERMINAL_KNOWLEDGE_STATUSES: frozenset[KnowledgeStatus] = frozenset(
    {
        KnowledgeStatus.ARCHIVED,
        KnowledgeStatus.DELETED,
        KnowledgeStatus.FORGOTTEN,
    }
)

RAW_DUMP_MARKERS: tuple[str, ...] = (
    "[TRANSCRIPT]",
    "[RAW_TRANSCRIPT]",
    "[RAW_MODEL_OUTPUT]",
    "[SUMMARY_DUMP]",
    "[TASK_LIST_DUMP]",
)

MAX_KNOWLEDGE_TEXT_LENGTH = 10_000

STATUS_CONFIDENCE_COMPATIBILITY: dict[KnowledgeStatus, frozenset[ConfidenceLevel]] = {
    KnowledgeStatus.ACTIVE: frozenset(
        {
            ConfidenceLevel.CONFIRMED,
            ConfidenceLevel.STRONGLY_SUPPORTED,
            ConfidenceLevel.INFERRED,
            ConfidenceLevel.UNCONFIRMED,
            ConfidenceLevel.DOUBTFUL,
        }
    ),
    KnowledgeStatus.UNCONFIRMED: frozenset(
        {
            ConfidenceLevel.UNCONFIRMED,
            ConfidenceLevel.INFERRED,
            ConfidenceLevel.DOUBTFUL,
        }
    ),
    KnowledgeStatus.CONFIRMED: frozenset(
        {
            ConfidenceLevel.CONFIRMED,
            ConfidenceLevel.STRONGLY_SUPPORTED,
        }
    ),
    KnowledgeStatus.CORRECTED: frozenset(
        {
            ConfidenceLevel.CONFIRMED,
            ConfidenceLevel.STRONGLY_SUPPORTED,
            ConfidenceLevel.INFERRED,
            ConfidenceLevel.UNCONFIRMED,
        }
    ),
    KnowledgeStatus.CONTRADICTED: frozenset(
        {
            ConfidenceLevel.CONTRADICTED,
            ConfidenceLevel.DOUBTFUL,
        }
    ),
    KnowledgeStatus.OUTDATED: frozenset(ConfidenceLevel),
    KnowledgeStatus.ARCHIVED: frozenset(ConfidenceLevel),
    KnowledgeStatus.DELETED: frozenset(ConfidenceLevel),
    KnowledgeStatus.FORGOTTEN: frozenset(ConfidenceLevel),
}

TERMINAL_CANDIDATE_STATUSES: frozenset[CandidateKnowledgeStatus] = frozenset(
    {
        CandidateKnowledgeStatus.ACCEPTED,
        CandidateKnowledgeStatus.REJECTED,
        CandidateKnowledgeStatus.MERGED,
    }
)

ACCEPTANCE_ELIGIBLE_CANDIDATE_STATUSES: frozenset[CandidateKnowledgeStatus] = frozenset(
    {
        CandidateKnowledgeStatus.EVALUATED,
    }
)

BLOCKING_CONFIDENCE_FOR_CANDIDATE_ACCEPTANCE: frozenset[ConfidenceLevel] = frozenset(
    {
        ConfidenceLevel.CONTRADICTED,
    }
)

CANDIDATE_CONFIDENCE_LEVELS: frozenset[ConfidenceLevel] = frozenset(ConfidenceLevel)

PHASE_1_SOURCE_TYPES: frozenset[SourceType] = frozenset(
    {
        SourceType.MEETING,
        SourceType.DOCUMENT,
        SourceType.VOICE_NOTE,
        SourceType.MANUAL_NOTE,
        SourceType.RESEARCH,
        SourceType.ASSISTANT_INTERACTION,
        SourceType.INTEGRATION,
        SourceType.CONFIRMED_TASK,
    }
)

RESERVED_SOURCE_TYPES: frozenset[SourceType] = frozenset(
    {
        SourceType.UNKNOWN,
    }
)

EXTERNAL_REFERENCE_PREFIX_BY_SOURCE_TYPE: dict[SourceType, str] = {
    SourceType.MEETING: "meeting:",
    SourceType.DOCUMENT: "document:",
    SourceType.RESEARCH: "research:",
    SourceType.ASSISTANT_INTERACTION: "assistant:",
    SourceType.INTEGRATION: "integration:",
    SourceType.CONFIRMED_TASK: "task:",
}
