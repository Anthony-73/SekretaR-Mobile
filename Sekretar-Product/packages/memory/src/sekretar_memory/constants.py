"""Memory domain constants."""

from .enums import ConfidenceLevel, KnowledgeStatus

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
