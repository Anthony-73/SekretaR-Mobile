"""Memory domain policies."""

from __future__ import annotations

from .constants import (
    ACCEPTANCE_ELIGIBLE_CANDIDATE_STATUSES,
    ACCEPTANCE_INITIAL_STATUSES,
    BLOCKING_CONFIDENCE_FOR_CANDIDATE_ACCEPTANCE,
    CANDIDATE_CONFIDENCE_LEVELS,
    EXTERNAL_REFERENCE_PREFIX_BY_SOURCE_TYPE,
    KNOWLEDGE_ITEM_STATUSES,
    PHASE_1_SOURCE_TYPES,
    RESERVED_SOURCE_TYPES,
    STATUS_CONFIDENCE_COMPATIBILITY,
    TERMINAL_CANDIDATE_STATUSES,
    TERMINAL_KNOWLEDGE_STATUSES,
)
from .enums import (
    CandidateKnowledgeStatus,
    ConfidenceLevel,
    ContradictionStatus,
    CorrectionStatus,
    KnowledgeStatus,
    RelationType,
    SourceType,
)
from .errors import (
    CandidateAlreadyResolved,
    CandidateNotEligibleForAcceptance,
    ConfidenceRequired,
    DuplicateKnowledgeRelation,
    InvalidCandidateTransition,
    InvalidContradictionTransition,
    InvalidCorrectionTransition,
    InvalidKnowledgeContent,
    InvalidKnowledgeLifecycleTransition,
    InvalidMemorySource,
    InvalidSourceReference,
    InvalidSourceType,
    KnowledgeAlreadyDeleted,
    KnowledgeImmutable,
    KnowledgeNotEligibleForContext,
    KnowledgeRelationInvalid,
    KnowledgeRelationOwnershipMismatch,
    KnowledgeOwnershipMismatch,
    KnowledgeStatusMismatch,
    LifecycleRecordInvalid,
    LifecycleRecordOwnershipMismatch,
    MemoryContextInvalid,
    MemoryContextOwnershipMismatch,
    MemoryCorrectionInvalid,
    MemoryCorrectionOwnershipMismatch,
    MemoryContradictionInvalid,
    MemoryContradictionOwnershipMismatch,
    MemorySourceInvalid,
    MemorySourceLinkMismatch,
    ProvenanceRecordInvalid,
    ProvenanceRecordOwnershipMismatch,
    ProvenanceRequired,
)
from .value_objects import AccountId, KnowledgeId, KnowledgeText, SourceId, SourceReference

ALLOWED_CANDIDATE_TRANSITIONS: dict[
    CandidateKnowledgeStatus,
    frozenset[CandidateKnowledgeStatus],
] = {
    CandidateKnowledgeStatus.DETECTED: frozenset(
        {
            CandidateKnowledgeStatus.EVALUATED,
            CandidateKnowledgeStatus.REJECTED,
            CandidateKnowledgeStatus.DEFERRED,
            CandidateKnowledgeStatus.CONTRADICTION,
        }
    ),
    CandidateKnowledgeStatus.EVALUATED: frozenset(
        {
            CandidateKnowledgeStatus.ACCEPTED,
            CandidateKnowledgeStatus.REJECTED,
            CandidateKnowledgeStatus.DEFERRED,
            CandidateKnowledgeStatus.MERGED,
            CandidateKnowledgeStatus.CONTRADICTION,
        }
    ),
    CandidateKnowledgeStatus.DEFERRED: frozenset(
        {
            CandidateKnowledgeStatus.EVALUATED,
            CandidateKnowledgeStatus.REJECTED,
            CandidateKnowledgeStatus.CONTRADICTION,
        }
    ),
    CandidateKnowledgeStatus.CONTRADICTION: frozenset(
        {
            CandidateKnowledgeStatus.EVALUATED,
            CandidateKnowledgeStatus.REJECTED,
        }
    ),
    CandidateKnowledgeStatus.ACCEPTED: frozenset(),
    CandidateKnowledgeStatus.REJECTED: frozenset(),
    CandidateKnowledgeStatus.MERGED: frozenset(),
}

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

ALLOWED_CORRECTION_TRANSITIONS: dict[CorrectionStatus, frozenset[CorrectionStatus]] = {
    CorrectionStatus.PROPOSED: frozenset(
        {
            CorrectionStatus.ACCEPTED,
            CorrectionStatus.REJECTED,
        }
    ),
    CorrectionStatus.ACCEPTED: frozenset({CorrectionStatus.APPLIED}),
    CorrectionStatus.REJECTED: frozenset(),
    CorrectionStatus.APPLIED: frozenset(),
}

ALLOWED_CONTRADICTION_TRANSITIONS: dict[
    ContradictionStatus,
    frozenset[ContradictionStatus],
] = {
    ContradictionStatus.DETECTED: frozenset({ContradictionStatus.REVIEWED}),
    ContradictionStatus.REVIEWED: frozenset(
        {
            ContradictionStatus.RESOLVED,
            ContradictionStatus.DISMISSED,
        }
    ),
    ContradictionStatus.RESOLVED: frozenset(),
    ContradictionStatus.DISMISSED: frozenset(),
}

PHASE_1_RELATION_TYPES = frozenset(
    {
        RelationType.REPLACES,
        RelationType.CONTRADICTS,
        RelationType.SUPPORTS,
        RelationType.DERIVED_FROM,
        RelationType.DUPLICATES,
    }
)

DIRECTIONAL_RELATION_TYPES = frozenset(
    {
        RelationType.REPLACES,
        RelationType.SUPPORTS,
        RelationType.DERIVED_FROM,
    }
)

SYMMETRIC_RELATION_TYPES = frozenset(
    {
        RelationType.CONTRADICTS,
        RelationType.DUPLICATES,
    }
)


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
    if status is KnowledgeStatus.CORRECTED:
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


def ensure_source_reference_present(*, source_id: SourceId | None) -> None:
    if source_id is None:
        raise InvalidMemorySource("Candidate knowledge must reference a source.")


def ensure_candidate_confidence_present(confidence_level: ConfidenceLevel | None) -> None:
    if confidence_level is None:
        raise ConfidenceRequired("Candidate knowledge must include confidence.")


def ensure_candidate_confidence_valid(confidence_level: ConfidenceLevel) -> None:
    if confidence_level not in CANDIDATE_CONFIDENCE_LEVELS:
        raise ConfidenceRequired(
            f"Confidence level {confidence_level.value!r} is not valid for candidate knowledge."
        )


def ensure_candidate_transition_allowed(
    *,
    current_status: CandidateKnowledgeStatus,
    new_status: CandidateKnowledgeStatus,
) -> None:
    if current_status in TERMINAL_CANDIDATE_STATUSES:
        raise CandidateAlreadyResolved(
            f"Candidate in terminal status {current_status.value!r} cannot transition."
        )

    allowed_targets = ALLOWED_CANDIDATE_TRANSITIONS[current_status]
    if new_status not in allowed_targets:
        raise InvalidCandidateTransition(
            f"Transition from {current_status.value!r} to {new_status.value!r} is not allowed."
        )


def is_eligible_for_acceptance(
    *,
    status: CandidateKnowledgeStatus,
    confidence_level: ConfidenceLevel,
    source_id: SourceId | None,
    provenance_type: object | None,
) -> bool:
    if status not in ACCEPTANCE_ELIGIBLE_CANDIDATE_STATUSES:
        return False
    if status is CandidateKnowledgeStatus.CONTRADICTION:
        return False
    if confidence_level in BLOCKING_CONFIDENCE_FOR_CANDIDATE_ACCEPTANCE:
        return False
    if source_id is None or provenance_type is None:
        return False
    return True


def ensure_eligible_for_acceptance(
    *,
    status: CandidateKnowledgeStatus,
    confidence_level: ConfidenceLevel,
    source_id: SourceId | None,
    provenance_type: object | None,
) -> None:
    if status in TERMINAL_CANDIDATE_STATUSES:
        raise CandidateAlreadyResolved("Candidate knowledge is already resolved.")

    if not is_eligible_for_acceptance(
        status=status,
        confidence_level=confidence_level,
        source_id=source_id,
        provenance_type=provenance_type,
    ):
        raise CandidateNotEligibleForAcceptance(
            "Candidate knowledge is not eligible for acceptance."
        )


def ensure_candidate_not_for_memory_context() -> None:
    raise KnowledgeNotEligibleForContext(
        "Candidate knowledge cannot be used in Memory context."
    )


def ensure_merge_target_present(*, merged_into_knowledge_id: KnowledgeId | None) -> None:
    if merged_into_knowledge_id is None:
        from .errors import CandidateInvalid

        raise CandidateInvalid(
            "Merged candidate must specify merged_into_knowledge_id."
        )


def ensure_merged_candidate_has_target(
    *,
    status: CandidateKnowledgeStatus,
    merged_into_knowledge_id: KnowledgeId | None,
) -> None:
    if status is CandidateKnowledgeStatus.MERGED and merged_into_knowledge_id is None:
        from .errors import CandidateInvalid

        raise CandidateInvalid(
            "Candidate in MERGED status must have merged_into_knowledge_id."
        )


def is_phase1_source_type(source_type: SourceType) -> bool:
    return source_type in PHASE_1_SOURCE_TYPES


def is_reserved_source_type(source_type: SourceType) -> bool:
    return source_type in RESERVED_SOURCE_TYPES


def ensure_source_type_present(*, source_type: SourceType | None) -> None:
    if source_type is None:
        raise InvalidSourceType("MemorySource requires source_type.")


def ensure_phase1_source_type(*, source_type: SourceType) -> None:
    ensure_source_type_present(source_type=source_type)
    if is_reserved_source_type(source_type):
        raise InvalidSourceType(
            f"Source type {source_type.value!r} is reserved and cannot be used directly."
        )
    if source_type not in PHASE_1_SOURCE_TYPES:
        raise InvalidSourceType(
            f"Source type {source_type.value!r} is not supported in Phase 1."
        )


def ensure_external_source_reference_present(
    *,
    external_reference: SourceReference | None,
) -> None:
    if external_reference is None:
        raise InvalidSourceReference("MemorySource requires external_reference.")


def ensure_external_reference_matches_source_type(
    *,
    source_type: SourceType,
    external_reference: SourceReference,
) -> None:
    expected_prefix = EXTERNAL_REFERENCE_PREFIX_BY_SOURCE_TYPE.get(source_type)
    if expected_prefix is None:
        return

    if not external_reference.value.startswith(expected_prefix):
        raise InvalidSourceReference(
            f"External reference for {source_type.value!r} must start with "
            f"{expected_prefix!r}."
        )


def ensure_memory_source_account_present(*, account_id: AccountId | None) -> None:
    if account_id is None:
        raise MemorySourceInvalid("MemorySource requires account_id.")


def ensure_candidate_references_memory_source(
    *,
    candidate_source_id: SourceId,
    candidate_account_id: AccountId,
    candidate_source_type: SourceType | None,
    source_id: SourceId,
    source_account_id: AccountId,
    source_type: SourceType,
) -> None:
    if candidate_source_id.value != source_id.value:
        raise MemorySourceLinkMismatch(
            "CandidateKnowledge.source_id does not match MemorySource.id."
        )
    if candidate_account_id.value != source_account_id.value:
        raise KnowledgeOwnershipMismatch(
            "CandidateKnowledge account does not match MemorySource account."
        )
    if candidate_source_type is not None and candidate_source_type is not source_type:
        raise MemorySourceLinkMismatch(
            "CandidateKnowledge.source_type does not match MemorySource.source_type."
        )


def ensure_knowledge_references_memory_source(
    *,
    knowledge_source_id: SourceId,
    knowledge_account_id: AccountId,
    source_id: SourceId,
    source_account_id: AccountId,
) -> None:
    if knowledge_source_id.value != source_id.value:
        raise MemorySourceLinkMismatch(
            "KnowledgeItem.primary_source_id does not match MemorySource.id."
        )
    if knowledge_account_id.value != source_account_id.value:
        raise KnowledgeOwnershipMismatch(
            "KnowledgeItem account does not match MemorySource account."
        )


def ensure_provenance_record_identity_present(
    *,
    knowledge_id: KnowledgeId | None,
    account_id: AccountId | None,
) -> None:
    if knowledge_id is None or account_id is None:
        raise ProvenanceRecordInvalid(
            "Provenance record requires both knowledge_id and account_id."
        )


def ensure_provenance_record_origin_present(
    *,
    source_id: SourceId | None,
    provenance_type: object | None,
) -> None:
    if source_id is None or provenance_type is None:
        raise ProvenanceRecordInvalid(
            "Provenance record requires source_id and provenance_type."
        )


def ensure_provenance_record_matches_knowledge(
    *,
    expected_knowledge_id: KnowledgeId,
    expected_account_id: AccountId,
    record_knowledge_id: KnowledgeId,
    record_account_id: AccountId,
) -> None:
    if expected_knowledge_id.value != record_knowledge_id.value:
        raise ProvenanceRecordOwnershipMismatch(
            "Provenance record knowledge_id does not match KnowledgeItem."
        )
    if expected_account_id.value != record_account_id.value:
        raise ProvenanceRecordOwnershipMismatch(
            "Provenance record account_id does not match KnowledgeItem."
        )


def ensure_correction_identity_present(
    *,
    original_knowledge_id: KnowledgeId | None,
    account_id: AccountId | None,
) -> None:
    if original_knowledge_id is None or account_id is None:
        raise MemoryCorrectionInvalid(
            "MemoryCorrection requires original_knowledge_id and account_id."
        )


def ensure_correction_replacement_valid(
    *,
    original_knowledge_id: KnowledgeId,
    corrected_knowledge_id: KnowledgeId | None,
) -> None:
    if corrected_knowledge_id is None:
        return
    if original_knowledge_id.value == corrected_knowledge_id.value:
        raise MemoryCorrectionInvalid(
            "Correction original_knowledge_id and corrected_knowledge_id must differ."
        )


def ensure_correction_state_consistent(
    *,
    status: CorrectionStatus,
    original_knowledge_id: KnowledgeId,
    corrected_knowledge_id: KnowledgeId | None,
    applied_at: object | None,
    rejected_at: object | None,
) -> None:
    ensure_correction_replacement_valid(
        original_knowledge_id=original_knowledge_id,
        corrected_knowledge_id=corrected_knowledge_id,
    )

    if status is CorrectionStatus.APPLIED:
        if corrected_knowledge_id is None:
            raise MemoryCorrectionInvalid(
                "Applied correction requires corrected_knowledge_id."
            )
        if applied_at is None:
            raise MemoryCorrectionInvalid("Applied correction requires applied_at.")
    if status is CorrectionStatus.REJECTED:
        if applied_at is not None:
            raise MemoryCorrectionInvalid("Rejected correction must not have applied_at.")
        if rejected_at is None:
            raise MemoryCorrectionInvalid("Rejected correction requires rejected_at.")


def ensure_correction_transition_allowed(
    *,
    current_status: CorrectionStatus,
    new_status: CorrectionStatus,
) -> None:
    allowed_targets = ALLOWED_CORRECTION_TRANSITIONS[current_status]
    if new_status not in allowed_targets:
        raise InvalidCorrectionTransition(
            f"Transition from {current_status.value!r} to {new_status.value!r} is not allowed."
        )


def ensure_correction_matches_knowledge(
    *,
    correction_account_id: AccountId,
    correction_knowledge_id: KnowledgeId,
    knowledge_account_id: AccountId,
    knowledge_id: KnowledgeId,
) -> None:
    if correction_account_id.value != knowledge_account_id.value:
        raise MemoryCorrectionOwnershipMismatch(
            "MemoryCorrection account_id does not match KnowledgeItem account."
        )
    if correction_knowledge_id.value != knowledge_id.value:
        raise MemoryCorrectionOwnershipMismatch(
            "MemoryCorrection original_knowledge_id does not match KnowledgeItem."
        )


def ensure_corrected_knowledge_matches_correction(
    *,
    correction_account_id: AccountId,
    original_knowledge_id: KnowledgeId,
    corrected_account_id: AccountId,
    corrected_knowledge_id: KnowledgeId,
) -> None:
    if correction_account_id.value != corrected_account_id.value:
        raise MemoryCorrectionOwnershipMismatch(
            "Corrected KnowledgeItem account does not match MemoryCorrection account."
        )
    ensure_correction_replacement_valid(
        original_knowledge_id=original_knowledge_id,
        corrected_knowledge_id=corrected_knowledge_id,
    )


def ensure_contradiction_identity_present(
    *,
    left_knowledge_id: KnowledgeId | None,
    right_knowledge_id: KnowledgeId | None,
    account_id: AccountId | None,
) -> None:
    if left_knowledge_id is None or right_knowledge_id is None or account_id is None:
        raise MemoryContradictionInvalid(
            "MemoryContradiction requires left_knowledge_id, right_knowledge_id, and account_id."
        )


def ensure_contradiction_pair_valid(
    *,
    left_knowledge_id: KnowledgeId,
    right_knowledge_id: KnowledgeId,
) -> None:
    if left_knowledge_id.value == right_knowledge_id.value:
        raise MemoryContradictionInvalid(
            "Contradiction left_knowledge_id and right_knowledge_id must differ."
        )


def ensure_contradiction_state_consistent(
    *,
    status: ContradictionStatus,
    left_knowledge_id: KnowledgeId,
    right_knowledge_id: KnowledgeId,
    resolved_at: object | None,
    dismissed_at: object | None,
) -> None:
    ensure_contradiction_pair_valid(
        left_knowledge_id=left_knowledge_id,
        right_knowledge_id=right_knowledge_id,
    )
    if status is ContradictionStatus.RESOLVED and resolved_at is None:
        raise MemoryContradictionInvalid("Resolved contradiction requires resolved_at.")
    if status is ContradictionStatus.DISMISSED and dismissed_at is None:
        raise MemoryContradictionInvalid("Dismissed contradiction requires dismissed_at.")


def ensure_contradiction_transition_allowed(
    *,
    current_status: ContradictionStatus,
    new_status: ContradictionStatus,
) -> None:
    allowed_targets = ALLOWED_CONTRADICTION_TRANSITIONS[current_status]
    if new_status not in allowed_targets:
        raise InvalidContradictionTransition(
            f"Transition from {current_status.value!r} to {new_status.value!r} is not allowed."
        )


def ensure_contradiction_knowledge_pair_matches(
    *,
    contradiction_account_id: AccountId,
    left_account_id: AccountId,
    right_account_id: AccountId,
    contradiction_left_knowledge_id: KnowledgeId,
    contradiction_right_knowledge_id: KnowledgeId,
    left_knowledge_id: KnowledgeId,
    right_knowledge_id: KnowledgeId,
) -> None:
    if contradiction_account_id.value != left_account_id.value:
        raise MemoryContradictionOwnershipMismatch(
            "Left KnowledgeItem account does not match MemoryContradiction account."
        )
    if contradiction_account_id.value != right_account_id.value:
        raise MemoryContradictionOwnershipMismatch(
            "Right KnowledgeItem account does not match MemoryContradiction account."
        )
    if contradiction_left_knowledge_id.value != left_knowledge_id.value:
        raise MemoryContradictionOwnershipMismatch(
            "MemoryContradiction left_knowledge_id does not match left KnowledgeItem."
        )
    if contradiction_right_knowledge_id.value != right_knowledge_id.value:
        raise MemoryContradictionOwnershipMismatch(
            "MemoryContradiction right_knowledge_id does not match right KnowledgeItem."
        )


def ensure_contradiction_resolution_correction_matches(
    *,
    contradiction_account_id: AccountId,
    left_knowledge_id: KnowledgeId,
    right_knowledge_id: KnowledgeId,
    correction_account_id: AccountId,
    correction_original_knowledge_id: KnowledgeId,
) -> None:
    if contradiction_account_id.value != correction_account_id.value:
        raise MemoryContradictionOwnershipMismatch(
            "Resolution correction account does not match MemoryContradiction account."
        )
    if correction_original_knowledge_id.value not in {
        left_knowledge_id.value,
        right_knowledge_id.value,
    }:
        raise MemoryContradictionOwnershipMismatch(
            "Resolution correction must correct one side of the contradiction."
        )


def ensure_relation_identity_present(
    *,
    left_knowledge_id: KnowledgeId | None,
    right_knowledge_id: KnowledgeId | None,
    account_id: AccountId | None,
    relation_type: RelationType | None,
) -> None:
    if (
        left_knowledge_id is None
        or right_knowledge_id is None
        or account_id is None
        or relation_type is None
    ):
        raise KnowledgeRelationInvalid(
            "KnowledgeRelation requires account_id, left_knowledge_id, right_knowledge_id, and relation_type."
        )


def ensure_phase1_relation_type(*, relation_type: RelationType) -> None:
    if relation_type not in PHASE_1_RELATION_TYPES:
        raise KnowledgeRelationInvalid(
            f"Relation type {relation_type.value!r} is not supported in Phase 1."
        )


def ensure_relation_pair_valid(
    *,
    left_knowledge_id: KnowledgeId,
    right_knowledge_id: KnowledgeId,
) -> None:
    if left_knowledge_id.value == right_knowledge_id.value:
        raise KnowledgeRelationInvalid(
            "KnowledgeRelation left_knowledge_id and right_knowledge_id must differ."
        )


def canonicalize_relation_pair(
    *,
    left_knowledge_id: KnowledgeId,
    right_knowledge_id: KnowledgeId,
    relation_type: RelationType,
) -> tuple[KnowledgeId, KnowledgeId]:
    ensure_phase1_relation_type(relation_type=relation_type)
    ensure_relation_pair_valid(
        left_knowledge_id=left_knowledge_id,
        right_knowledge_id=right_knowledge_id,
    )
    if relation_type in SYMMETRIC_RELATION_TYPES and left_knowledge_id.value > right_knowledge_id.value:
        return right_knowledge_id, left_knowledge_id
    return left_knowledge_id, right_knowledge_id


def is_symmetric_relation_type(relation_type: RelationType) -> bool:
    return relation_type in SYMMETRIC_RELATION_TYPES


def is_directional_relation_type(relation_type: RelationType) -> bool:
    return relation_type in DIRECTIONAL_RELATION_TYPES


def ensure_relation_knowledge_pair_matches(
    *,
    relation_account_id: AccountId,
    left_account_id: AccountId,
    right_account_id: AccountId,
    relation_left_knowledge_id: KnowledgeId,
    relation_right_knowledge_id: KnowledgeId,
    left_knowledge_id: KnowledgeId,
    right_knowledge_id: KnowledgeId,
    relation_type: RelationType,
) -> None:
    if relation_account_id.value != left_account_id.value:
        raise KnowledgeRelationOwnershipMismatch(
            "Left KnowledgeItem account does not match KnowledgeRelation account."
        )
    if relation_account_id.value != right_account_id.value:
        raise KnowledgeRelationOwnershipMismatch(
            "Right KnowledgeItem account does not match KnowledgeRelation account."
        )

    canonical_left, canonical_right = canonicalize_relation_pair(
        left_knowledge_id=left_knowledge_id,
        right_knowledge_id=right_knowledge_id,
        relation_type=relation_type,
    )
    if relation_left_knowledge_id.value != canonical_left.value:
        raise KnowledgeRelationOwnershipMismatch(
            "KnowledgeRelation left_knowledge_id does not match expected KnowledgeItem."
        )
    if relation_right_knowledge_id.value != canonical_right.value:
        raise KnowledgeRelationOwnershipMismatch(
            "KnowledgeRelation right_knowledge_id does not match expected KnowledgeItem."
        )


def ensure_no_duplicate_symmetric_relation(
    *,
    existing_relation_keys: set[tuple[str, str, str]],
    relation_type: RelationType,
    left_knowledge_id: KnowledgeId,
    right_knowledge_id: KnowledgeId,
) -> None:
    if not is_symmetric_relation_type(relation_type):
        return
    key = (
        relation_type.value,
        left_knowledge_id.value,
        right_knowledge_id.value,
    )
    if key in existing_relation_keys:
        raise DuplicateKnowledgeRelation(
            "Equivalent symmetric KnowledgeRelation already exists."
        )


def ensure_memory_context_account_present(*, account_id: AccountId | None) -> None:
    if account_id is None:
        raise MemoryContextInvalid("MemoryContext requires account_id.")


def ensure_memory_context_items_unique(*, knowledge_ids: tuple[KnowledgeId, ...]) -> None:
    seen: set[str] = set()
    for knowledge_id in knowledge_ids:
        if knowledge_id.value in seen:
            raise MemoryContextInvalid(
                "MemoryContext items must be unique by knowledge_id."
            )
        seen.add(knowledge_id.value)


def ensure_memory_context_item_account(
    *,
    context_account_id: AccountId,
    item_account_id: AccountId,
) -> None:
    if context_account_id.value != item_account_id.value:
        raise MemoryContextOwnershipMismatch(
            "MemoryContext item account_id does not match context account."
        )
