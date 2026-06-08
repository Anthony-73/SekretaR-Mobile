"""Memory domain policies."""

from __future__ import annotations

from .constants import (
    ACCEPTANCE_INITIAL_STATUSES,
    KNOWLEDGE_ITEM_STATUSES,
    STATUS_CONFIDENCE_COMPATIBILITY,
    TERMINAL_KNOWLEDGE_STATUSES,
)
from .enums import ConfidenceLevel, KnowledgeStatus
from .errors import (
    ConfidenceRequired,
    InvalidKnowledgeContent,
    InvalidKnowledgeLifecycleTransition,
    KnowledgeAlreadyDeleted,
    KnowledgeImmutable,
    KnowledgeNotEligibleForContext,
    KnowledgeOwnershipMismatch,
    KnowledgeStatusMismatch,
    LifecycleRecordInvalid,
    LifecycleRecordOwnershipMismatch,
    ProvenanceRequired,
)
from .value_objects import AccountId, KnowledgeId, KnowledgeText, SourceId

ALLOWED_KNOWLEDGE_TRANSITIONS: dict[KnowledgeStatus, frozenset[KnowledgeStatus]] = {
    KnowledgeStatus.ACTIVE: frozenset(
        {
            KnowledgeStatus.CONFIRMED,
            KnowledgeStatus.CORRECTED,
            KnowledgeStatus.CONTRADICTED,
            KnowledgeStatus.OUTDATED,
            KnowledgeStatus.ARCHIVED,
            KnowledgeStatus.DELETED,
            KnowledgeStatus.FORGOTTEN,
        }
    ),
    KnowledgeStatus.UNCONFIRMED: frozenset(
        {
            KnowledgeStatus.ACTIVE,
            KnowledgeStatus.CONFIRMED,
            KnowledgeStatus.CORRECTED,
            KnowledgeStatus.CONTRADICTED,
            KnowledgeStatus.OUTDATED,
            KnowledgeStatus.ARCHIVED,
            KnowledgeStatus.DELETED,
            KnowledgeStatus.FORGOTTEN,
        }
    ),
    KnowledgeStatus.CONFIRMED: frozenset(
        {
            KnowledgeStatus.CORRECTED,
            KnowledgeStatus.CONTRADICTED,
            KnowledgeStatus.OUTDATED,
            KnowledgeStatus.ARCHIVED,
            KnowledgeStatus.DELETED,
            KnowledgeStatus.FORGOTTEN,
        }
    ),
    KnowledgeStatus.CORRECTED: frozenset(
        {
            KnowledgeStatus.CONFIRMED,
            KnowledgeStatus.CONTRADICTED,
            KnowledgeStatus.OUTDATED,
            KnowledgeStatus.ARCHIVED,
            KnowledgeStatus.DELETED,
            KnowledgeStatus.FORGOTTEN,
        }
    ),
    KnowledgeStatus.CONTRADICTED: frozenset(
        {
            KnowledgeStatus.CORRECTED,
            KnowledgeStatus.CONFIRMED,
            KnowledgeStatus.OUTDATED,
            KnowledgeStatus.ARCHIVED,
            KnowledgeStatus.DELETED,
            KnowledgeStatus.FORGOTTEN,
        }
    ),
    KnowledgeStatus.OUTDATED: frozenset(
        {
            KnowledgeStatus.ARCHIVED,
            KnowledgeStatus.DELETED,
            KnowledgeStatus.FORGOTTEN,
        }
    ),
    KnowledgeStatus.ARCHIVED: frozenset(),
    KnowledgeStatus.DELETED: frozenset(),
    KnowledgeStatus.FORGOTTEN: frozenset(),
}


def ensure_account_ownership(*, knowledge_account_id: AccountId, expected_account_id: AccountId) -> None:
    if knowledge_account_id.value != expected_account_id.value:
        raise KnowledgeOwnershipMismatch(
            "Knowledge does not belong to the expected Account."
        )


def ensure_knowledge_item_status(status: KnowledgeStatus) -> None:
    if status not in KNOWLEDGE_ITEM_STATUSES:
        raise InvalidKnowledgeLifecycleTransition(
            f"Status {status.value!r} is not valid for KnowledgeItem."
        )


def ensure_acceptance_initial_status(status: KnowledgeStatus) -> None:
    ensure_knowledge_item_status(status)
    if status not in ACCEPTANCE_INITIAL_STATUSES:
        raise InvalidKnowledgeLifecycleTransition(
            f"KnowledgeItem may only be created with initial status "
            f"{KnowledgeStatus.ACTIVE.value!r} or {KnowledgeStatus.UNCONFIRMED.value!r}."
        )


def ensure_provenance_present(
    *,
    primary_source_id: SourceId | None,
    primary_provenance_type: object | None,
) -> None:
    if primary_source_id is None or primary_provenance_type is None:
        raise ProvenanceRequired("Accepted knowledge must include provenance.")


def ensure_confidence_present(confidence_level: ConfidenceLevel | None) -> None:
    if confidence_level is None:
        raise ConfidenceRequired("Accepted knowledge must include confidence.")


def ensure_not_raw_source_dump(text: KnowledgeText) -> None:
    # KnowledgeText already rejects known raw dump markers at construction time.
    if not text.value:
        raise InvalidKnowledgeContent("Knowledge text must not be empty.")


def ensure_status_confidence_compatible(
    *,
    status: KnowledgeStatus,
    confidence_level: ConfidenceLevel,
) -> None:
    ensure_knowledge_item_status(status)
    allowed_levels = STATUS_CONFIDENCE_COMPATIBILITY[status]
    if confidence_level not in allowed_levels:
        raise KnowledgeStatusMismatch(
            f"Status {status.value!r} is incompatible with confidence "
            f"{confidence_level.value!r}."
        )


def ensure_lifecycle_transition_allowed(
    *,
    current_status: KnowledgeStatus,
    new_status: KnowledgeStatus,
) -> None:
    ensure_knowledge_item_status(current_status)
    ensure_knowledge_item_status(new_status)

    if current_status in TERMINAL_KNOWLEDGE_STATUSES:
        raise KnowledgeImmutable(
            f"Knowledge in terminal status {current_status.value!r} cannot transition."
        )

    allowed_targets = ALLOWED_KNOWLEDGE_TRANSITIONS[current_status]
    if new_status not in allowed_targets:
        raise InvalidKnowledgeLifecycleTransition(
            f"Transition from {current_status.value!r} to {new_status.value!r} is not allowed."
        )


def ensure_not_terminal_for_active_use(status: KnowledgeStatus) -> None:
    if status in TERMINAL_KNOWLEDGE_STATUSES:
        if status is KnowledgeStatus.DELETED:
            raise KnowledgeAlreadyDeleted("Deleted knowledge cannot be used as active Memory.")
        raise KnowledgeImmutable(
            f"Knowledge in status {status.value!r} cannot be used as active Memory."
        )


def is_eligible_for_context(
    *,
    status: KnowledgeStatus,
    confidence_level: ConfidenceLevel,
    strict: bool = False,
) -> bool:
    if status in TERMINAL_KNOWLEDGE_STATUSES:
        return False
    if status is KnowledgeStatus.CONTRADICTED:
        return False
    if status is KnowledgeStatus.OUTDATED:
        return False
    if confidence_level is ConfidenceLevel.CONTRADICTED:
        return False
    if strict:
        if status is KnowledgeStatus.UNCONFIRMED:
            return False
        if confidence_level in {ConfidenceLevel.UNCONFIRMED, ConfidenceLevel.DOUBTFUL}:
            return False
    return True


def ensure_eligible_for_context(
    *,
    status: KnowledgeStatus,
    confidence_level: ConfidenceLevel,
    strict: bool = False,
) -> None:
    if not is_eligible_for_context(
        status=status,
        confidence_level=confidence_level,
        strict=strict,
    ):
        raise KnowledgeNotEligibleForContext(
            "Knowledge is not eligible for Memory context."
        )


def ensure_lifecycle_record_identity_present(
    *,
    knowledge_id: KnowledgeId | None,
    account_id: AccountId | None,
) -> None:
    if knowledge_id is None or account_id is None:
        raise LifecycleRecordInvalid(
            "Lifecycle record requires both knowledge_id and account_id."
        )


def ensure_lifecycle_record_transition(
    *,
    previous_status: KnowledgeStatus,
    new_status: KnowledgeStatus,
) -> None:
    ensure_knowledge_item_status(previous_status)
    ensure_knowledge_item_status(new_status)
    if previous_status is new_status:
        raise LifecycleRecordInvalid(
            "Lifecycle record must capture an actual status transition."
        )


def ensure_lifecycle_record_matches_knowledge(
    *,
    expected_knowledge_id: KnowledgeId,
    expected_account_id: AccountId,
    record_knowledge_id: KnowledgeId,
    record_account_id: AccountId,
) -> None:
    if expected_knowledge_id.value != record_knowledge_id.value:
        raise LifecycleRecordOwnershipMismatch(
            "Lifecycle record knowledge_id does not match KnowledgeItem."
        )
    if expected_account_id.value != record_account_id.value:
        raise LifecycleRecordOwnershipMismatch(
            "Lifecycle record account_id does not match KnowledgeItem."
        )
