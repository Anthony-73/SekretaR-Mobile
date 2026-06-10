"""Memory domain entities."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import uuid4

from .enums import (
    CandidateKnowledgeStatus,
    CandidateRejectionReason,
    ConfidenceLevel,
    ContradictionStatus,
    CorrectionStatus,
    KnowledgeStatus,
    KnowledgeType,
    MemoryContextPurpose,
    ProvenanceEventType,
    ProvenanceType,
    RelationType,
    SourceType,
)
from .errors import KnowledgeImmutable
from .policies import (
    ensure_acceptance_initial_status,
    ensure_account_ownership,
    ensure_candidate_confidence_present,
    ensure_candidate_confidence_valid,
    ensure_candidate_not_for_memory_context,
    ensure_candidate_transition_allowed,
    ensure_confidence_present,
    ensure_contradiction_identity_present,
    ensure_contradiction_knowledge_pair_matches,
    ensure_contradiction_pair_valid,
    ensure_contradiction_resolution_correction_matches,
    ensure_contradiction_state_consistent,
    ensure_contradiction_transition_allowed,
    ensure_corrected_knowledge_matches_correction,
    ensure_correction_identity_present,
    ensure_correction_matches_knowledge,
    ensure_correction_state_consistent,
    ensure_correction_transition_allowed,
    ensure_eligible_for_acceptance,
    ensure_eligible_for_context,
    ensure_candidate_references_memory_source,
    ensure_external_reference_matches_source_type,
    ensure_external_source_reference_present,
    ensure_knowledge_references_memory_source,
    ensure_memory_source_account_present,
    ensure_memory_context_account_present,
    ensure_memory_context_item_account,
    ensure_memory_context_items_unique,
    ensure_merge_target_present,
    ensure_merged_candidate_has_target,
    ensure_phase1_source_type,
    ensure_knowledge_item_status,
    ensure_lifecycle_record_identity_present,
    ensure_lifecycle_record_matches_knowledge,
    ensure_lifecycle_record_transition,
    ensure_lifecycle_transition_allowed,
    ensure_no_duplicate_symmetric_relation,
    ensure_not_raw_source_dump,
    ensure_not_terminal_for_active_use,
    ensure_provenance_present,
    ensure_provenance_record_identity_present,
    ensure_provenance_record_matches_knowledge,
    ensure_provenance_record_origin_present,
    ensure_relation_identity_present,
    ensure_relation_knowledge_pair_matches,
    canonicalize_relation_pair,
    ensure_source_reference_present,
    ensure_status_confidence_compatible,
    is_eligible_for_acceptance,
    is_eligible_for_context,
    is_phase1_source_type,
)
from .value_objects import (
    AccountId,
    CandidateKnowledgeId,
    ConfidenceReason,
    ConfidenceScore,
    ContradictionId,
    ContradictionReason,
    CorrectionId,
    CorrectionReason,
    KnowledgeId,
    KnowledgeLanguage,
    KnowledgeSummary,
    KnowledgeTags,
    KnowledgeText,
    LifecycleReason,
    LifecycleRecordId,
    MemoryContextReason,
    ProvenanceId,
    ProvenanceNote,
    RelationId,
    RelationReason,
    SourceId,
    SourceReference,
    SourceTimestamp,
    UserId,
)


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


def new_knowledge_id() -> KnowledgeId:
    return KnowledgeId(str(uuid4()))


def new_lifecycle_record_id() -> LifecycleRecordId:
    return LifecycleRecordId(str(uuid4()))


def new_candidate_knowledge_id() -> CandidateKnowledgeId:
    return CandidateKnowledgeId(str(uuid4()))


def new_source_id() -> SourceId:
    return SourceId(str(uuid4()))


def new_provenance_id() -> ProvenanceId:
    return ProvenanceId(str(uuid4()))


def new_correction_id() -> CorrectionId:
    return CorrectionId(str(uuid4()))


def new_contradiction_id() -> ContradictionId:
    return ContradictionId(str(uuid4()))


def new_relation_id() -> RelationId:
    return RelationId(str(uuid4()))


@dataclass(slots=True)
class KnowledgeItem:
    """Primary unit of durable Account-owned knowledge."""

    account_id: AccountId
    knowledge_type: KnowledgeType
    text: KnowledgeText
    status: KnowledgeStatus
    confidence_level: ConfidenceLevel
    primary_source_id: SourceId
    primary_provenance_type: ProvenanceType
    id: KnowledgeId = field(default_factory=new_knowledge_id)
    created_at: datetime = field(default_factory=utcnow)
    updated_at: datetime = field(default_factory=utcnow)
    summary: KnowledgeSummary | None = None
    language: KnowledgeLanguage = field(default_factory=lambda: KnowledgeLanguage("ru"))
    tags: KnowledgeTags = field(default_factory=lambda: KnowledgeTags(()))
    confidence_score: ConfidenceScore | None = None
    confidence_reason: ConfidenceReason | None = None
    accepted_from_candidate_id: CandidateKnowledgeId | None = None
    created_by_user_id: UserId | None = None
    supersedes_knowledge_id: KnowledgeId | None = None

    @classmethod
    def create_from_accepted(
        cls,
        *,
        account_id: AccountId,
        knowledge_type: KnowledgeType,
        text: KnowledgeText,
        status: KnowledgeStatus,
        confidence_level: ConfidenceLevel,
        primary_source_id: SourceId,
        primary_provenance_type: ProvenanceType,
        summary: KnowledgeSummary | None = None,
        language: KnowledgeLanguage | None = None,
        tags: KnowledgeTags | None = None,
        confidence_score: ConfidenceScore | None = None,
        confidence_reason: ConfidenceReason | None = None,
        accepted_from_candidate_id: CandidateKnowledgeId | None = None,
        created_by_user_id: UserId | None = None,
        supersedes_knowledge_id: KnowledgeId | None = None,
        knowledge_id: KnowledgeId | None = None,
        created_at: datetime | None = None,
    ) -> KnowledgeItem:
        ensure_acceptance_initial_status(status)
        ensure_provenance_present(
            primary_source_id=primary_source_id,
            primary_provenance_type=primary_provenance_type,
        )
        ensure_confidence_present(confidence_level)
        ensure_not_raw_source_dump(text)
        ensure_status_confidence_compatible(
            status=status,
            confidence_level=confidence_level,
        )

        timestamp = created_at or utcnow()
        return cls(
            id=knowledge_id or new_knowledge_id(),
            account_id=account_id,
            knowledge_type=knowledge_type,
            text=text,
            status=status,
            confidence_level=confidence_level,
            primary_source_id=primary_source_id,
            primary_provenance_type=primary_provenance_type,
            summary=summary,
            language=language or KnowledgeLanguage("ru"),
            tags=tags or KnowledgeTags(()),
            confidence_score=confidence_score,
            confidence_reason=confidence_reason,
            accepted_from_candidate_id=accepted_from_candidate_id,
            created_by_user_id=created_by_user_id,
            supersedes_knowledge_id=supersedes_knowledge_id,
            created_at=timestamp,
            updated_at=timestamp,
        )

    def belongs_to_account(self, account_id: AccountId) -> bool:
        return self.account_id.value == account_id.value

    def ensure_belongs_to_account(self, account_id: AccountId) -> None:
        ensure_account_ownership(
            knowledge_account_id=self.account_id,
            expected_account_id=account_id,
        )

    def is_terminal(self) -> bool:
        from .constants import TERMINAL_KNOWLEDGE_STATUSES

        return self.status in TERMINAL_KNOWLEDGE_STATUSES

    def is_eligible_for_context(self, *, strict: bool = False) -> bool:
        ensure_knowledge_item_status(self.status)
        return is_eligible_for_context(
            status=self.status,
            confidence_level=self.confidence_level,
            strict=strict,
        )

    def ensure_eligible_for_context(self, *, strict: bool = False) -> None:
        ensure_eligible_for_context(
            status=self.status,
            confidence_level=self.confidence_level,
            strict=strict,
        )

    def transition_status(
        self,
        new_status: KnowledgeStatus,
        *,
        reason: LifecycleReason | None = None,
        confidence_level: ConfidenceLevel | None = None,
        actor_user_id: UserId | None = None,
        source_id: SourceId | None = None,
        provenance_id: ProvenanceId | None = None,
    ) -> KnowledgeLifecycleRecord:
        previous_status = self.status

        ensure_lifecycle_transition_allowed(
            current_status=previous_status,
            new_status=new_status,
        )

        next_confidence = confidence_level or self.confidence_level
        ensure_status_confidence_compatible(
            status=new_status,
            confidence_level=next_confidence,
        )

        self.status = new_status
        self.confidence_level = next_confidence
        self.updated_at = utcnow()

        return KnowledgeLifecycleRecord.create_from_transition(
            knowledge=self,
            previous_status=previous_status,
            new_status=new_status,
            reason=reason or LifecycleReason("status_transition"),
            actor_user_id=actor_user_id,
            source_id=source_id,
            provenance_id=provenance_id,
        )

    def update_confidence(
        self,
        confidence_level: ConfidenceLevel,
        *,
        reason: ConfidenceReason | None = None,
        score: ConfidenceScore | None = None,
    ) -> None:
        if self.is_terminal():
            raise KnowledgeImmutable(
                f"Knowledge in status {self.status.value!r} cannot update confidence."
            )

        ensure_status_confidence_compatible(
            status=self.status,
            confidence_level=confidence_level,
        )

        self.confidence_level = confidence_level
        if reason is not None:
            self.confidence_reason = reason
        if score is not None:
            self.confidence_score = score
        self.updated_at = utcnow()

    def ensure_active(self) -> None:
        ensure_not_terminal_for_active_use(self.status)


@dataclass(slots=True)
class MemorySource:
    """Reference to an external source that may produce candidate knowledge.

    MemorySource is not Memory, not KnowledgeItem, and not CandidateKnowledge.
    It describes where candidate knowledge may come from without owning the
    lifecycle of the external source object.
    """

    account_id: AccountId
    source_type: SourceType
    external_reference: SourceReference
    id: SourceId = field(default_factory=new_source_id)
    created_at: datetime = field(default_factory=utcnow)
    updated_at: datetime = field(default_factory=utcnow)
    display_label: str | None = None
    source_timestamp: SourceTimestamp | None = None
    linked_by_user_id: UserId | None = None
    is_active: bool = True

    @classmethod
    def create(
        cls,
        *,
        account_id: AccountId,
        source_type: SourceType,
        external_reference: SourceReference,
        require_phase1_type: bool = True,
        source_id: SourceId | None = None,
        display_label: str | None = None,
        source_timestamp: SourceTimestamp | None = None,
        linked_by_user_id: UserId | None = None,
        created_at: datetime | None = None,
    ) -> MemorySource:
        ensure_memory_source_account_present(account_id=account_id)
        if require_phase1_type:
            ensure_phase1_source_type(source_type=source_type)
        else:
            from .policies import ensure_source_type_present

            ensure_source_type_present(source_type=source_type)
        ensure_external_source_reference_present(external_reference=external_reference)
        ensure_external_reference_matches_source_type(
            source_type=source_type,
            external_reference=external_reference,
        )

        timestamp = created_at or utcnow()
        return cls(
            id=source_id or new_source_id(),
            account_id=account_id,
            source_type=source_type,
            external_reference=external_reference,
            display_label=display_label,
            source_timestamp=source_timestamp,
            linked_by_user_id=linked_by_user_id,
            created_at=timestamp,
            updated_at=timestamp,
        )

    @classmethod
    def for_meeting(cls, *, account_id: AccountId, meeting_id: str) -> MemorySource:
        return cls.create(
            account_id=account_id,
            source_type=SourceType.MEETING,
            external_reference=SourceReference(f"meeting:{meeting_id}"),
        )

    @classmethod
    def for_document(cls, *, account_id: AccountId, document_id: str) -> MemorySource:
        return cls.create(
            account_id=account_id,
            source_type=SourceType.DOCUMENT,
            external_reference=SourceReference(f"document:{document_id}"),
        )

    @classmethod
    def for_research(cls, *, account_id: AccountId, research_id: str) -> MemorySource:
        return cls.create(
            account_id=account_id,
            source_type=SourceType.RESEARCH,
            external_reference=SourceReference(f"research:{research_id}"),
        )

    @classmethod
    def for_assistant_interaction(
        cls,
        *,
        account_id: AccountId,
        assistant_interaction_id: str,
    ) -> MemorySource:
        return cls.create(
            account_id=account_id,
            source_type=SourceType.ASSISTANT_INTERACTION,
            external_reference=SourceReference(f"assistant:{assistant_interaction_id}"),
        )

    @classmethod
    def for_integration(
        cls,
        *,
        account_id: AccountId,
        integration_reference: str,
    ) -> MemorySource:
        return cls.create(
            account_id=account_id,
            source_type=SourceType.INTEGRATION,
            external_reference=SourceReference(f"integration:{integration_reference}"),
        )

    def belongs_to_account(self, account_id: AccountId) -> bool:
        return self.account_id.value == account_id.value

    def ensure_belongs_to_account(self, account_id: AccountId) -> None:
        ensure_account_ownership(
            knowledge_account_id=self.account_id,
            expected_account_id=account_id,
        )

    def is_phase1_supported(self) -> bool:
        return is_phase1_source_type(self.source_type)

    def can_produce_candidate_knowledge(self) -> bool:
        return self.is_active

    def ensure_candidate_can_reference(self, candidate: CandidateKnowledge) -> None:
        ensure_candidate_references_memory_source(
            candidate_source_id=candidate.source_id,
            candidate_account_id=candidate.account_id,
            candidate_source_type=candidate.source_type,
            source_id=self.id,
            source_account_id=self.account_id,
            source_type=self.source_type,
        )

    def ensure_knowledge_can_reference(self, knowledge: KnowledgeItem) -> None:
        ensure_knowledge_references_memory_source(
            knowledge_source_id=knowledge.primary_source_id,
            knowledge_account_id=knowledge.account_id,
            source_id=self.id,
            source_account_id=self.account_id,
        )


@dataclass(slots=True)
class CandidateKnowledge:
    """Information that may become Memory but has not been accepted yet."""

    account_id: AccountId
    source_id: SourceId
    knowledge_type: KnowledgeType
    text: KnowledgeText
    status: CandidateKnowledgeStatus
    confidence_level: ConfidenceLevel
    provenance_type: ProvenanceType
    id: CandidateKnowledgeId = field(default_factory=new_candidate_knowledge_id)
    source_type: SourceType | None = None
    created_at: datetime = field(default_factory=utcnow)
    updated_at: datetime = field(default_factory=utcnow)
    confidence_score: ConfidenceScore | None = None
    confidence_reason: ConfidenceReason | None = None
    provenance_note: ProvenanceNote | None = None
    detected_by_user_id: UserId | None = None
    rejection_reason: CandidateRejectionReason | None = None
    accepted_knowledge_id: KnowledgeId | None = None
    merged_into_knowledge_id: KnowledgeId | None = None

    @classmethod
    def create_detected(
        cls,
        *,
        account_id: AccountId,
        source_id: SourceId,
        knowledge_type: KnowledgeType,
        text: KnowledgeText,
        confidence_level: ConfidenceLevel,
        provenance_type: ProvenanceType,
        source_type: SourceType | None = None,
        confidence_score: ConfidenceScore | None = None,
        confidence_reason: ConfidenceReason | None = None,
        provenance_note: ProvenanceNote | None = None,
        detected_by_user_id: UserId | None = None,
        candidate_id: CandidateKnowledgeId | None = None,
        created_at: datetime | None = None,
    ) -> CandidateKnowledge:
        ensure_source_reference_present(source_id=source_id)
        ensure_provenance_present(
            primary_source_id=source_id,
            primary_provenance_type=provenance_type,
        )
        ensure_candidate_confidence_present(confidence_level)
        ensure_candidate_confidence_valid(confidence_level)
        ensure_not_raw_source_dump(text)

        timestamp = created_at or utcnow()
        return cls(
            id=candidate_id or new_candidate_knowledge_id(),
            account_id=account_id,
            source_id=source_id,
            knowledge_type=knowledge_type,
            text=text,
            status=CandidateKnowledgeStatus.DETECTED,
            confidence_level=confidence_level,
            provenance_type=provenance_type,
            source_type=source_type,
            confidence_score=confidence_score,
            confidence_reason=confidence_reason,
            provenance_note=provenance_note,
            detected_by_user_id=detected_by_user_id,
            created_at=timestamp,
            updated_at=timestamp,
        )

    def belongs_to_account(self, account_id: AccountId) -> bool:
        return self.account_id.value == account_id.value

    def ensure_belongs_to_account(self, account_id: AccountId) -> None:
        ensure_account_ownership(
            knowledge_account_id=self.account_id,
            expected_account_id=account_id,
        )

    def is_terminal(self) -> bool:
        from .constants import TERMINAL_CANDIDATE_STATUSES

        return self.status in TERMINAL_CANDIDATE_STATUSES

    def is_eligible_for_acceptance(self) -> bool:
        return is_eligible_for_acceptance(
            status=self.status,
            confidence_level=self.confidence_level,
            source_id=self.source_id,
            provenance_type=self.provenance_type,
        )

    def ensure_eligible_for_acceptance(self) -> None:
        ensure_eligible_for_acceptance(
            status=self.status,
            confidence_level=self.confidence_level,
            source_id=self.source_id,
            provenance_type=self.provenance_type,
        )

    def is_memory_context_eligible(self) -> bool:
        return False

    def ensure_not_for_memory_context(self) -> None:
        ensure_candidate_not_for_memory_context()

    def _transition_to(self, new_status: CandidateKnowledgeStatus) -> None:
        ensure_candidate_transition_allowed(
            current_status=self.status,
            new_status=new_status,
        )
        self.status = new_status
        self.updated_at = utcnow()

    def mark_evaluated(self) -> None:
        self._transition_to(CandidateKnowledgeStatus.EVALUATED)

    def defer(self, *, reason: LifecycleReason | None = None) -> None:
        del reason
        self._transition_to(CandidateKnowledgeStatus.DEFERRED)

    def reject(self, *, reason: CandidateRejectionReason) -> None:
        if self.is_terminal():
            from .errors import CandidateAlreadyResolved

            raise CandidateAlreadyResolved("Candidate knowledge is already resolved.")

        ensure_candidate_transition_allowed(
            current_status=self.status,
            new_status=CandidateKnowledgeStatus.REJECTED,
        )
        self.status = CandidateKnowledgeStatus.REJECTED
        self.rejection_reason = reason
        self.updated_at = utcnow()

    def flag_contradiction(self) -> None:
        self._transition_to(CandidateKnowledgeStatus.CONTRADICTION)

    def mark_merged(self, *, merged_into_knowledge_id: KnowledgeId) -> None:
        ensure_merge_target_present(merged_into_knowledge_id=merged_into_knowledge_id)
        ensure_candidate_transition_allowed(
            current_status=self.status,
            new_status=CandidateKnowledgeStatus.MERGED,
        )
        self.status = CandidateKnowledgeStatus.MERGED
        self.merged_into_knowledge_id = merged_into_knowledge_id
        self.updated_at = utcnow()
        ensure_merged_candidate_has_target(
            status=self.status,
            merged_into_knowledge_id=self.merged_into_knowledge_id,
        )

    def accept(
        self,
        *,
        acceptance_status: KnowledgeStatus | None = None,
        actor_user_id: UserId | None = None,
    ) -> KnowledgeItem:
        self.ensure_eligible_for_acceptance()

        if acceptance_status is None:
            if self.confidence_level in {
                ConfidenceLevel.UNCONFIRMED,
                ConfidenceLevel.DOUBTFUL,
            }:
                acceptance_status = KnowledgeStatus.UNCONFIRMED
            else:
                acceptance_status = KnowledgeStatus.ACTIVE

        ensure_acceptance_initial_status(acceptance_status)
        ensure_status_confidence_compatible(
            status=acceptance_status,
            confidence_level=self.confidence_level,
        )

        knowledge = KnowledgeItem.create_from_accepted(
            account_id=self.account_id,
            knowledge_type=self.knowledge_type,
            text=self.text,
            status=acceptance_status,
            confidence_level=self.confidence_level,
            primary_source_id=self.source_id,
            primary_provenance_type=self.provenance_type,
            confidence_score=self.confidence_score,
            confidence_reason=self.confidence_reason,
            accepted_from_candidate_id=self.id,
            created_by_user_id=actor_user_id or self.detected_by_user_id,
        )

        ensure_candidate_transition_allowed(
            current_status=self.status,
            new_status=CandidateKnowledgeStatus.ACCEPTED,
        )
        self.status = CandidateKnowledgeStatus.ACCEPTED
        self.accepted_knowledge_id = knowledge.id
        self.updated_at = utcnow()
        return knowledge


@dataclass(frozen=True, slots=True)
class KnowledgeProvenance:
    """Append-only origin record explaining how knowledge became known to Memory."""

    knowledge_id: KnowledgeId
    account_id: AccountId
    event_type: ProvenanceEventType
    provenance_type: ProvenanceType
    source_id: SourceId
    id: ProvenanceId = field(default_factory=new_provenance_id)
    created_at: datetime = field(default_factory=utcnow)
    observed_at: datetime | None = None
    actor_user_id: UserId | None = None
    note: ProvenanceNote | None = None
    accepted_from_candidate_id: CandidateKnowledgeId | None = None
    related_lifecycle_record_id: LifecycleRecordId | None = None

    @classmethod
    def create(
        cls,
        *,
        knowledge_id: KnowledgeId,
        account_id: AccountId,
        event_type: ProvenanceEventType,
        provenance_type: ProvenanceType,
        source_id: SourceId,
        provenance_id: ProvenanceId | None = None,
        created_at: datetime | None = None,
        observed_at: datetime | None = None,
        actor_user_id: UserId | None = None,
        note: ProvenanceNote | None = None,
        accepted_from_candidate_id: CandidateKnowledgeId | None = None,
        related_lifecycle_record_id: LifecycleRecordId | None = None,
    ) -> KnowledgeProvenance:
        ensure_provenance_record_identity_present(
            knowledge_id=knowledge_id,
            account_id=account_id,
        )
        ensure_provenance_record_origin_present(
            source_id=source_id,
            provenance_type=provenance_type,
        )

        timestamp = created_at or utcnow()
        return cls(
            id=provenance_id or new_provenance_id(),
            knowledge_id=knowledge_id,
            account_id=account_id,
            event_type=event_type,
            provenance_type=provenance_type,
            source_id=source_id,
            created_at=timestamp,
            observed_at=observed_at,
            actor_user_id=actor_user_id,
            note=note,
            accepted_from_candidate_id=accepted_from_candidate_id,
            related_lifecycle_record_id=related_lifecycle_record_id,
        )

    @classmethod
    def create_origin_accepted(
        cls,
        *,
        knowledge: KnowledgeItem,
        actor_user_id: UserId | None = None,
        note: ProvenanceNote | None = None,
        accepted_from_candidate_id: CandidateKnowledgeId | None = None,
        observed_at: datetime | None = None,
        provenance_id: ProvenanceId | None = None,
        created_at: datetime | None = None,
    ) -> KnowledgeProvenance:
        record = cls.create(
            knowledge_id=knowledge.id,
            account_id=knowledge.account_id,
            event_type=ProvenanceEventType.ORIGIN_ACCEPTED,
            provenance_type=knowledge.primary_provenance_type,
            source_id=knowledge.primary_source_id,
            provenance_id=provenance_id,
            created_at=created_at,
            observed_at=observed_at,
            actor_user_id=actor_user_id or knowledge.created_by_user_id,
            note=note,
            accepted_from_candidate_id=(
                accepted_from_candidate_id or knowledge.accepted_from_candidate_id
            ),
        )
        ensure_provenance_record_matches_knowledge(
            expected_knowledge_id=knowledge.id,
            expected_account_id=knowledge.account_id,
            record_knowledge_id=record.knowledge_id,
            record_account_id=record.account_id,
        )
        return record

    @classmethod
    def create_from_candidate_acceptance(
        cls,
        *,
        knowledge: KnowledgeItem,
        candidate: CandidateKnowledge,
        actor_user_id: UserId | None = None,
        note: ProvenanceNote | None = None,
        observed_at: datetime | None = None,
        provenance_id: ProvenanceId | None = None,
        created_at: datetime | None = None,
    ) -> KnowledgeProvenance:
        if knowledge.account_id.value != candidate.account_id.value:
            from .errors import KnowledgeOwnershipMismatch

            raise KnowledgeOwnershipMismatch(
                "KnowledgeItem account does not match CandidateKnowledge account."
            )
        if knowledge.primary_source_id.value != candidate.source_id.value:
            from .errors import MemorySourceLinkMismatch

            raise MemorySourceLinkMismatch(
                "KnowledgeItem source does not match CandidateKnowledge source."
            )

        return cls.create_origin_accepted(
            knowledge=knowledge,
            actor_user_id=actor_user_id,
            note=note or candidate.provenance_note,
            accepted_from_candidate_id=candidate.id,
            observed_at=observed_at or candidate.created_at,
            provenance_id=provenance_id,
            created_at=created_at,
        )

    @classmethod
    def create_correction_record(
        cls,
        *,
        knowledge: KnowledgeItem,
        source_id: SourceId,
        provenance_type: ProvenanceType = ProvenanceType.USER_CORRECTED,
        actor_user_id: UserId | None = None,
        note: ProvenanceNote | None = None,
        related_lifecycle_record_id: LifecycleRecordId | None = None,
        observed_at: datetime | None = None,
        provenance_id: ProvenanceId | None = None,
        created_at: datetime | None = None,
    ) -> KnowledgeProvenance:
        record = cls.create(
            knowledge_id=knowledge.id,
            account_id=knowledge.account_id,
            event_type=ProvenanceEventType.CORRECTION_RECORDED,
            provenance_type=provenance_type,
            source_id=source_id,
            provenance_id=provenance_id,
            created_at=created_at,
            observed_at=observed_at,
            actor_user_id=actor_user_id,
            note=note,
            related_lifecycle_record_id=related_lifecycle_record_id,
        )
        ensure_provenance_record_matches_knowledge(
            expected_knowledge_id=knowledge.id,
            expected_account_id=knowledge.account_id,
            record_knowledge_id=record.knowledge_id,
            record_account_id=record.account_id,
        )
        return record

    @classmethod
    def create_reconfirmation_record(
        cls,
        *,
        knowledge: KnowledgeItem,
        source_id: SourceId | None = None,
        provenance_type: ProvenanceType = ProvenanceType.EXPLICITLY_STATED,
        actor_user_id: UserId | None = None,
        note: ProvenanceNote | None = None,
        related_lifecycle_record_id: LifecycleRecordId | None = None,
        observed_at: datetime | None = None,
        provenance_id: ProvenanceId | None = None,
        created_at: datetime | None = None,
    ) -> KnowledgeProvenance:
        record = cls.create(
            knowledge_id=knowledge.id,
            account_id=knowledge.account_id,
            event_type=ProvenanceEventType.RECONFIRMATION_RECORDED,
            provenance_type=provenance_type,
            source_id=source_id or knowledge.primary_source_id,
            provenance_id=provenance_id,
            created_at=created_at,
            observed_at=observed_at,
            actor_user_id=actor_user_id,
            note=note,
            related_lifecycle_record_id=related_lifecycle_record_id,
        )
        ensure_provenance_record_matches_knowledge(
            expected_knowledge_id=knowledge.id,
            expected_account_id=knowledge.account_id,
            record_knowledge_id=record.knowledge_id,
            record_account_id=record.account_id,
        )
        return record

    def belongs_to_knowledge(self, knowledge_id: KnowledgeId) -> bool:
        return self.knowledge_id.value == knowledge_id.value

    def belongs_to_account(self, account_id: AccountId) -> bool:
        return self.account_id.value == account_id.value


@dataclass(slots=True)
class KnowledgeProvenanceHistory:
    """In-memory append-only provenance history for a KnowledgeItem."""

    knowledge_id: KnowledgeId
    account_id: AccountId
    _records: list[KnowledgeProvenance] = field(default_factory=list)

    @classmethod
    def for_knowledge(cls, knowledge: KnowledgeItem) -> KnowledgeProvenanceHistory:
        return cls(
            knowledge_id=knowledge.id,
            account_id=knowledge.account_id,
        )

    def append(self, record: KnowledgeProvenance) -> None:
        ensure_provenance_record_matches_knowledge(
            expected_knowledge_id=self.knowledge_id,
            expected_account_id=self.account_id,
            record_knowledge_id=record.knowledge_id,
            record_account_id=record.account_id,
        )
        self._records.append(record)

    @property
    def records(self) -> tuple[KnowledgeProvenance, ...]:
        return tuple(self._records)

    @property
    def first_record(self) -> KnowledgeProvenance | None:
        if not self._records:
            return None
        return self._records[0]

    @property
    def latest_record(self) -> KnowledgeProvenance | None:
        if not self._records:
            return None
        return self._records[-1]


class KnowledgeConfidence:
    """Product-level trust signal for knowledge."""


@dataclass(frozen=True, slots=True)
class KnowledgeLifecycleRecord:
    """Append-only record of knowledge lifecycle movement over time."""

    knowledge_id: KnowledgeId
    account_id: AccountId
    previous_status: KnowledgeStatus
    new_status: KnowledgeStatus
    reason: LifecycleReason
    id: LifecycleRecordId = field(default_factory=new_lifecycle_record_id)
    actor_user_id: UserId | None = None
    created_at: datetime = field(default_factory=utcnow)
    source_id: SourceId | None = None
    provenance_id: ProvenanceId | None = None

    @classmethod
    def create(
        cls,
        *,
        knowledge_id: KnowledgeId,
        account_id: AccountId,
        previous_status: KnowledgeStatus,
        new_status: KnowledgeStatus,
        reason: LifecycleReason,
        record_id: LifecycleRecordId | None = None,
        actor_user_id: UserId | None = None,
        created_at: datetime | None = None,
        source_id: SourceId | None = None,
        provenance_id: ProvenanceId | None = None,
    ) -> KnowledgeLifecycleRecord:
        ensure_lifecycle_record_identity_present(
            knowledge_id=knowledge_id,
            account_id=account_id,
        )
        ensure_lifecycle_record_transition(
            previous_status=previous_status,
            new_status=new_status,
        )

        timestamp = created_at or utcnow()
        return cls(
            id=record_id or new_lifecycle_record_id(),
            knowledge_id=knowledge_id,
            account_id=account_id,
            previous_status=previous_status,
            new_status=new_status,
            reason=reason,
            actor_user_id=actor_user_id,
            created_at=timestamp,
            source_id=source_id,
            provenance_id=provenance_id,
        )

    @classmethod
    def create_from_transition(
        cls,
        *,
        knowledge: KnowledgeItem,
        previous_status: KnowledgeStatus,
        new_status: KnowledgeStatus,
        reason: LifecycleReason,
        actor_user_id: UserId | None = None,
        source_id: SourceId | None = None,
        provenance_id: ProvenanceId | None = None,
        record_id: LifecycleRecordId | None = None,
        created_at: datetime | None = None,
    ) -> KnowledgeLifecycleRecord:
        record = cls.create(
            knowledge_id=knowledge.id,
            account_id=knowledge.account_id,
            previous_status=previous_status,
            new_status=new_status,
            reason=reason,
            record_id=record_id,
            actor_user_id=actor_user_id,
            created_at=created_at,
            source_id=source_id,
            provenance_id=provenance_id,
        )
        ensure_lifecycle_record_matches_knowledge(
            expected_knowledge_id=knowledge.id,
            expected_account_id=knowledge.account_id,
            record_knowledge_id=record.knowledge_id,
            record_account_id=record.account_id,
        )
        return record

    def belongs_to_knowledge(self, knowledge_id: KnowledgeId) -> bool:
        return self.knowledge_id.value == knowledge_id.value

    def belongs_to_account(self, account_id: AccountId) -> bool:
        return self.account_id.value == account_id.value


@dataclass(slots=True)
class KnowledgeLifecycleHistory:
    """In-memory append-only lifecycle history for a KnowledgeItem."""

    knowledge_id: KnowledgeId
    account_id: AccountId
    _records: list[KnowledgeLifecycleRecord] = field(default_factory=list)

    def append(self, record: KnowledgeLifecycleRecord) -> None:
        ensure_lifecycle_record_matches_knowledge(
            expected_knowledge_id=self.knowledge_id,
            expected_account_id=self.account_id,
            record_knowledge_id=record.knowledge_id,
            record_account_id=record.account_id,
        )
        self._records.append(record)

    @property
    def records(self) -> tuple[KnowledgeLifecycleRecord, ...]:
        return tuple(self._records)


@dataclass(frozen=True, slots=True)
class KnowledgeRelation:
    """Append-only graph edge between two Account-owned knowledge items."""

    account_id: AccountId
    left_knowledge_id: KnowledgeId
    right_knowledge_id: KnowledgeId
    relation_type: RelationType
    reason: RelationReason
    id: RelationId = field(default_factory=new_relation_id)
    created_at: datetime = field(default_factory=utcnow)
    correction_id: CorrectionId | None = None
    contradiction_id: ContradictionId | None = None
    provenance_id: ProvenanceId | None = None

    @classmethod
    def create(
        cls,
        *,
        account_id: AccountId,
        left_knowledge_id: KnowledgeId,
        right_knowledge_id: KnowledgeId,
        relation_type: RelationType,
        reason: RelationReason,
        relation_id: RelationId | None = None,
        created_at: datetime | None = None,
        correction_id: CorrectionId | None = None,
        contradiction_id: ContradictionId | None = None,
        provenance_id: ProvenanceId | None = None,
    ) -> KnowledgeRelation:
        if reason is None:
            from .errors import KnowledgeRelationInvalid

            raise KnowledgeRelationInvalid("KnowledgeRelation requires reason.")
        ensure_relation_identity_present(
            left_knowledge_id=left_knowledge_id,
            right_knowledge_id=right_knowledge_id,
            account_id=account_id,
            relation_type=relation_type,
        )
        canonical_left, canonical_right = canonicalize_relation_pair(
            left_knowledge_id=left_knowledge_id,
            right_knowledge_id=right_knowledge_id,
            relation_type=relation_type,
        )

        return cls(
            id=relation_id or new_relation_id(),
            account_id=account_id,
            left_knowledge_id=canonical_left,
            right_knowledge_id=canonical_right,
            relation_type=relation_type,
            reason=reason,
            created_at=created_at or utcnow(),
            correction_id=correction_id,
            contradiction_id=contradiction_id,
            provenance_id=provenance_id,
        )

    @classmethod
    def create_between(
        cls,
        *,
        left_knowledge: KnowledgeItem,
        right_knowledge: KnowledgeItem,
        relation_type: RelationType,
        reason: RelationReason,
        relation_id: RelationId | None = None,
        correction_id: CorrectionId | None = None,
        contradiction_id: ContradictionId | None = None,
        provenance_id: ProvenanceId | None = None,
        created_at: datetime | None = None,
    ) -> KnowledgeRelation:
        relation = cls.create(
            account_id=left_knowledge.account_id,
            left_knowledge_id=left_knowledge.id,
            right_knowledge_id=right_knowledge.id,
            relation_type=relation_type,
            reason=reason,
            relation_id=relation_id,
            correction_id=correction_id,
            contradiction_id=contradiction_id,
            provenance_id=provenance_id,
            created_at=created_at,
        )
        relation.ensure_matches_knowledge_pair(
            left_knowledge=left_knowledge,
            right_knowledge=right_knowledge,
        )
        return relation

    def belongs_to_account(self, account_id: AccountId) -> bool:
        return self.account_id.value == account_id.value

    def involves_knowledge(self, knowledge_id: KnowledgeId) -> bool:
        return knowledge_id.value in {
            self.left_knowledge_id.value,
            self.right_knowledge_id.value,
        }

    def ensure_matches_knowledge_pair(
        self,
        *,
        left_knowledge: KnowledgeItem,
        right_knowledge: KnowledgeItem,
    ) -> None:
        ensure_relation_knowledge_pair_matches(
            relation_account_id=self.account_id,
            left_account_id=left_knowledge.account_id,
            right_account_id=right_knowledge.account_id,
            relation_left_knowledge_id=self.left_knowledge_id,
            relation_right_knowledge_id=self.right_knowledge_id,
            left_knowledge_id=left_knowledge.id,
            right_knowledge_id=right_knowledge.id,
            relation_type=self.relation_type,
        )


@dataclass(slots=True)
class KnowledgeRelationHistory:
    """In-memory append-only relation graph history for an Account."""

    account_id: AccountId
    _records: list[KnowledgeRelation] = field(default_factory=list)

    def append(self, record: KnowledgeRelation) -> None:
        if record.account_id.value != self.account_id.value:
            from .errors import KnowledgeRelationOwnershipMismatch

            raise KnowledgeRelationOwnershipMismatch(
                "KnowledgeRelation account_id does not match history."
            )
        existing_relation_keys = {
            (
                existing.relation_type.value,
                existing.left_knowledge_id.value,
                existing.right_knowledge_id.value,
            )
            for existing in self._records
        }
        ensure_no_duplicate_symmetric_relation(
            existing_relation_keys=existing_relation_keys,
            relation_type=record.relation_type,
            left_knowledge_id=record.left_knowledge_id,
            right_knowledge_id=record.right_knowledge_id,
        )
        self._records.append(record)

    @property
    def records(self) -> tuple[KnowledgeRelation, ...]:
        return tuple(self._records)

    @property
    def first_record(self) -> KnowledgeRelation | None:
        if not self._records:
            return None
        return self._records[0]

    @property
    def latest_record(self) -> KnowledgeRelation | None:
        if not self._records:
            return None
        return self._records[-1]


@dataclass(slots=True)
class MemoryCorrection:
    """Decision record that connects original knowledge to corrected knowledge."""

    account_id: AccountId
    original_knowledge_id: KnowledgeId
    status: CorrectionStatus
    reason: CorrectionReason
    id: CorrectionId = field(default_factory=new_correction_id)
    created_at: datetime = field(default_factory=utcnow)
    corrected_knowledge_id: KnowledgeId | None = None
    proposed_by_user_id: UserId | None = None
    accepted_by_user_id: UserId | None = None
    source_id: SourceId | None = None
    provenance_id: ProvenanceId | None = None
    lifecycle_record_id: LifecycleRecordId | None = None
    applied_at: datetime | None = None
    rejected_at: datetime | None = None

    @classmethod
    def create(
        cls,
        *,
        account_id: AccountId,
        original_knowledge_id: KnowledgeId,
        reason: CorrectionReason,
        status: CorrectionStatus = CorrectionStatus.PROPOSED,
        correction_id: CorrectionId | None = None,
        created_at: datetime | None = None,
        corrected_knowledge_id: KnowledgeId | None = None,
        proposed_by_user_id: UserId | None = None,
        accepted_by_user_id: UserId | None = None,
        source_id: SourceId | None = None,
        provenance_id: ProvenanceId | None = None,
        lifecycle_record_id: LifecycleRecordId | None = None,
        applied_at: datetime | None = None,
        rejected_at: datetime | None = None,
    ) -> MemoryCorrection:
        if reason is None:
            from .errors import MemoryCorrectionInvalid

            raise MemoryCorrectionInvalid("MemoryCorrection requires reason.")
        ensure_correction_identity_present(
            original_knowledge_id=original_knowledge_id,
            account_id=account_id,
        )
        ensure_correction_state_consistent(
            status=status,
            original_knowledge_id=original_knowledge_id,
            corrected_knowledge_id=corrected_knowledge_id,
            applied_at=applied_at,
            rejected_at=rejected_at,
        )

        return cls(
            id=correction_id or new_correction_id(),
            account_id=account_id,
            original_knowledge_id=original_knowledge_id,
            status=status,
            reason=reason,
            created_at=created_at or utcnow(),
            corrected_knowledge_id=corrected_knowledge_id,
            proposed_by_user_id=proposed_by_user_id,
            accepted_by_user_id=accepted_by_user_id,
            source_id=source_id,
            provenance_id=provenance_id,
            lifecycle_record_id=lifecycle_record_id,
            applied_at=applied_at,
            rejected_at=rejected_at,
        )

    @classmethod
    def propose_for_knowledge(
        cls,
        *,
        knowledge: KnowledgeItem,
        reason: CorrectionReason,
        proposed_by_user_id: UserId | None = None,
        source_id: SourceId | None = None,
        correction_id: CorrectionId | None = None,
        created_at: datetime | None = None,
    ) -> MemoryCorrection:
        return cls.create(
            correction_id=correction_id,
            account_id=knowledge.account_id,
            original_knowledge_id=knowledge.id,
            reason=reason,
            proposed_by_user_id=proposed_by_user_id,
            source_id=source_id,
            created_at=created_at,
        )

    def belongs_to_account(self, account_id: AccountId) -> bool:
        return self.account_id.value == account_id.value

    def belongs_to_original_knowledge(self, knowledge_id: KnowledgeId) -> bool:
        return self.original_knowledge_id.value == knowledge_id.value

    def ensure_original_matches(self, knowledge: KnowledgeItem) -> None:
        ensure_correction_matches_knowledge(
            correction_account_id=self.account_id,
            correction_knowledge_id=self.original_knowledge_id,
            knowledge_account_id=knowledge.account_id,
            knowledge_id=knowledge.id,
        )

    def accept(self, *, accepted_by_user_id: UserId | None = None) -> None:
        ensure_correction_transition_allowed(
            current_status=self.status,
            new_status=CorrectionStatus.ACCEPTED,
        )
        self.status = CorrectionStatus.ACCEPTED
        if accepted_by_user_id is not None:
            self.accepted_by_user_id = accepted_by_user_id

    def reject(self) -> None:
        ensure_correction_transition_allowed(
            current_status=self.status,
            new_status=CorrectionStatus.REJECTED,
        )
        self.status = CorrectionStatus.REJECTED
        self.rejected_at = utcnow()

    def apply(
        self,
        *,
        corrected_knowledge: KnowledgeItem,
        lifecycle_record_id: LifecycleRecordId | None = None,
        provenance_id: ProvenanceId | None = None,
    ) -> None:
        ensure_correction_transition_allowed(
            current_status=self.status,
            new_status=CorrectionStatus.APPLIED,
        )
        ensure_corrected_knowledge_matches_correction(
            correction_account_id=self.account_id,
            original_knowledge_id=self.original_knowledge_id,
            corrected_account_id=corrected_knowledge.account_id,
            corrected_knowledge_id=corrected_knowledge.id,
        )

        self.status = CorrectionStatus.APPLIED
        self.corrected_knowledge_id = corrected_knowledge.id
        self.lifecycle_record_id = lifecycle_record_id
        self.provenance_id = provenance_id
        self.applied_at = utcnow()
        ensure_correction_state_consistent(
            status=self.status,
            original_knowledge_id=self.original_knowledge_id,
            corrected_knowledge_id=self.corrected_knowledge_id,
            applied_at=self.applied_at,
            rejected_at=self.rejected_at,
        )


@dataclass(slots=True)
class MemoryCorrectionHistory:
    """In-memory append-only correction history for a KnowledgeItem."""

    original_knowledge_id: KnowledgeId
    account_id: AccountId
    _records: list[MemoryCorrection] = field(default_factory=list)

    @classmethod
    def for_knowledge(cls, knowledge: KnowledgeItem) -> MemoryCorrectionHistory:
        return cls(
            original_knowledge_id=knowledge.id,
            account_id=knowledge.account_id,
        )

    def append(self, record: MemoryCorrection) -> None:
        if record.original_knowledge_id.value != self.original_knowledge_id.value:
            from .errors import MemoryCorrectionOwnershipMismatch

            raise MemoryCorrectionOwnershipMismatch(
                "MemoryCorrection original_knowledge_id does not match history."
            )
        if record.account_id.value != self.account_id.value:
            from .errors import MemoryCorrectionOwnershipMismatch

            raise MemoryCorrectionOwnershipMismatch(
                "MemoryCorrection account_id does not match history."
            )
        self._records.append(record)

    @property
    def records(self) -> tuple[MemoryCorrection, ...]:
        return tuple(self._records)

    @property
    def first_record(self) -> MemoryCorrection | None:
        if not self._records:
            return None
        return self._records[0]

    @property
    def latest_record(self) -> MemoryCorrection | None:
        if not self._records:
            return None
        return self._records[-1]


@dataclass(slots=True)
class MemoryContradiction:
    """Domain record that captures two incompatible knowledge items."""

    account_id: AccountId
    left_knowledge_id: KnowledgeId
    right_knowledge_id: KnowledgeId
    status: ContradictionStatus
    reason: ContradictionReason
    id: ContradictionId = field(default_factory=new_contradiction_id)
    created_at: datetime = field(default_factory=utcnow)
    resolution_correction_id: CorrectionId | None = None
    source_id: SourceId | None = None
    provenance_id: ProvenanceId | None = None
    resolved_at: datetime | None = None
    dismissed_at: datetime | None = None

    @classmethod
    def create(
        cls,
        *,
        account_id: AccountId,
        left_knowledge_id: KnowledgeId,
        right_knowledge_id: KnowledgeId,
        reason: ContradictionReason,
        status: ContradictionStatus = ContradictionStatus.DETECTED,
        contradiction_id: ContradictionId | None = None,
        created_at: datetime | None = None,
        resolution_correction_id: CorrectionId | None = None,
        source_id: SourceId | None = None,
        provenance_id: ProvenanceId | None = None,
        resolved_at: datetime | None = None,
        dismissed_at: datetime | None = None,
    ) -> MemoryContradiction:
        if reason is None:
            from .errors import MemoryContradictionInvalid

            raise MemoryContradictionInvalid("MemoryContradiction requires reason.")
        ensure_contradiction_identity_present(
            left_knowledge_id=left_knowledge_id,
            right_knowledge_id=right_knowledge_id,
            account_id=account_id,
        )
        ensure_contradiction_state_consistent(
            status=status,
            left_knowledge_id=left_knowledge_id,
            right_knowledge_id=right_knowledge_id,
            resolved_at=resolved_at,
            dismissed_at=dismissed_at,
        )

        return cls(
            id=contradiction_id or new_contradiction_id(),
            account_id=account_id,
            left_knowledge_id=left_knowledge_id,
            right_knowledge_id=right_knowledge_id,
            status=status,
            reason=reason,
            created_at=created_at or utcnow(),
            resolution_correction_id=resolution_correction_id,
            source_id=source_id,
            provenance_id=provenance_id,
            resolved_at=resolved_at,
            dismissed_at=dismissed_at,
        )

    @classmethod
    def detect_between(
        cls,
        *,
        left_knowledge: KnowledgeItem,
        right_knowledge: KnowledgeItem,
        reason: ContradictionReason,
        contradiction_id: ContradictionId | None = None,
        source_id: SourceId | None = None,
        provenance_id: ProvenanceId | None = None,
        created_at: datetime | None = None,
    ) -> MemoryContradiction:
        if left_knowledge.account_id.value != right_knowledge.account_id.value:
            from .errors import MemoryContradictionOwnershipMismatch

            raise MemoryContradictionOwnershipMismatch(
                "Contradicting KnowledgeItems must belong to the same Account."
            )
        ensure_contradiction_pair_valid(
            left_knowledge_id=left_knowledge.id,
            right_knowledge_id=right_knowledge.id,
        )
        return cls.create(
            account_id=left_knowledge.account_id,
            left_knowledge_id=left_knowledge.id,
            right_knowledge_id=right_knowledge.id,
            reason=reason,
            contradiction_id=contradiction_id,
            source_id=source_id,
            provenance_id=provenance_id,
            created_at=created_at,
        )

    def belongs_to_account(self, account_id: AccountId) -> bool:
        return self.account_id.value == account_id.value

    def involves_knowledge(self, knowledge_id: KnowledgeId) -> bool:
        return knowledge_id.value in {
            self.left_knowledge_id.value,
            self.right_knowledge_id.value,
        }

    def ensure_matches_knowledge_pair(
        self,
        *,
        left_knowledge: KnowledgeItem,
        right_knowledge: KnowledgeItem,
    ) -> None:
        ensure_contradiction_knowledge_pair_matches(
            contradiction_account_id=self.account_id,
            left_account_id=left_knowledge.account_id,
            right_account_id=right_knowledge.account_id,
            contradiction_left_knowledge_id=self.left_knowledge_id,
            contradiction_right_knowledge_id=self.right_knowledge_id,
            left_knowledge_id=left_knowledge.id,
            right_knowledge_id=right_knowledge.id,
        )

    def mark_reviewed(self) -> None:
        ensure_contradiction_transition_allowed(
            current_status=self.status,
            new_status=ContradictionStatus.REVIEWED,
        )
        self.status = ContradictionStatus.REVIEWED

    def resolve(
        self,
        *,
        resolution_correction: MemoryCorrection | None = None,
    ) -> None:
        ensure_contradiction_transition_allowed(
            current_status=self.status,
            new_status=ContradictionStatus.RESOLVED,
        )
        if resolution_correction is not None:
            ensure_contradiction_resolution_correction_matches(
                contradiction_account_id=self.account_id,
                left_knowledge_id=self.left_knowledge_id,
                right_knowledge_id=self.right_knowledge_id,
                correction_account_id=resolution_correction.account_id,
                correction_original_knowledge_id=resolution_correction.original_knowledge_id,
            )
            self.resolution_correction_id = resolution_correction.id

        self.status = ContradictionStatus.RESOLVED
        self.resolved_at = utcnow()
        ensure_contradiction_state_consistent(
            status=self.status,
            left_knowledge_id=self.left_knowledge_id,
            right_knowledge_id=self.right_knowledge_id,
            resolved_at=self.resolved_at,
            dismissed_at=self.dismissed_at,
        )

    def dismiss(self) -> None:
        ensure_contradiction_transition_allowed(
            current_status=self.status,
            new_status=ContradictionStatus.DISMISSED,
        )
        self.status = ContradictionStatus.DISMISSED
        self.dismissed_at = utcnow()
        ensure_contradiction_state_consistent(
            status=self.status,
            left_knowledge_id=self.left_knowledge_id,
            right_knowledge_id=self.right_knowledge_id,
            resolved_at=self.resolved_at,
            dismissed_at=self.dismissed_at,
        )


@dataclass(slots=True)
class MemoryContradictionHistory:
    """In-memory append-only contradiction history for an Account."""

    account_id: AccountId
    _records: list[MemoryContradiction] = field(default_factory=list)

    def append(self, record: MemoryContradiction) -> None:
        if record.account_id.value != self.account_id.value:
            from .errors import MemoryContradictionOwnershipMismatch

            raise MemoryContradictionOwnershipMismatch(
                "MemoryContradiction account_id does not match history."
            )
        self._records.append(record)

    @property
    def records(self) -> tuple[MemoryContradiction, ...]:
        return tuple(self._records)

    @property
    def first_record(self) -> MemoryContradiction | None:
        if not self._records:
            return None
        return self._records[0]

    @property
    def latest_record(self) -> MemoryContradiction | None:
        if not self._records:
            return None
        return self._records[-1]


@dataclass(frozen=True, slots=True)
class MemoryContextItem:
    """Immutable eligibility snapshot for one knowledge item in context."""

    knowledge_id: KnowledgeId
    account_id: AccountId
    status: KnowledgeStatus
    confidence_level: ConfidenceLevel
    source_id: SourceId | None = None
    provenance_id: ProvenanceId | None = None
    included_reason: MemoryContextReason | None = None
    warning_flags: tuple[str, ...] = field(default_factory=tuple)

    @classmethod
    def from_knowledge(
        cls,
        knowledge: KnowledgeItem,
        *,
        strict: bool = False,
        included_reason: MemoryContextReason | None = None,
        provenance_id: ProvenanceId | None = None,
    ) -> MemoryContextItem:
        knowledge.ensure_eligible_for_context(strict=strict)
        warning_flags: list[str] = []
        if knowledge.status is KnowledgeStatus.UNCONFIRMED:
            warning_flags.append("unconfirmed_status")
        if knowledge.confidence_level in {
            ConfidenceLevel.UNCONFIRMED,
            ConfidenceLevel.DOUBTFUL,
        }:
            warning_flags.append("low_confidence")

        return cls(
            knowledge_id=knowledge.id,
            account_id=knowledge.account_id,
            status=knowledge.status,
            confidence_level=knowledge.confidence_level,
            source_id=knowledge.primary_source_id,
            provenance_id=provenance_id,
            included_reason=included_reason
            or MemoryContextReason("eligible_for_context"),
            warning_flags=tuple(warning_flags),
        )


@dataclass(frozen=True, slots=True)
class MemoryContext:
    """Immutable scenario-specific snapshot of eligible Memory knowledge."""

    account_id: AccountId
    purpose: MemoryContextPurpose
    items: tuple[MemoryContextItem, ...] = field(default_factory=tuple)
    created_at: datetime = field(default_factory=utcnow)
    strict: bool = False

    @classmethod
    def create(
        cls,
        *,
        account_id: AccountId,
        purpose: MemoryContextPurpose,
        items: tuple[MemoryContextItem, ...] = (),
        created_at: datetime | None = None,
        strict: bool = False,
    ) -> MemoryContext:
        if purpose is None:
            from .errors import MemoryContextInvalid

            raise MemoryContextInvalid("MemoryContext requires purpose.")
        ensure_memory_context_account_present(account_id=account_id)
        for item in items:
            ensure_memory_context_item_account(
                context_account_id=account_id,
                item_account_id=item.account_id,
            )
        ensure_memory_context_items_unique(
            knowledge_ids=tuple(item.knowledge_id for item in items),
        )

        return cls(
            account_id=account_id,
            purpose=purpose,
            items=tuple(items),
            created_at=created_at or utcnow(),
            strict=strict,
        )

    @classmethod
    def create_from_knowledge_items(
        cls,
        *,
        account_id: AccountId,
        purpose: MemoryContextPurpose,
        knowledge_items: list[KnowledgeItem] | tuple[KnowledgeItem, ...],
        strict: bool = False,
        created_at: datetime | None = None,
    ) -> MemoryContext:
        ensure_memory_context_account_present(account_id=account_id)
        items: list[MemoryContextItem] = []
        seen_knowledge_ids: set[str] = set()

        for knowledge in knowledge_items:
            if not isinstance(knowledge, KnowledgeItem):
                from .errors import MemoryContextInvalid

                raise MemoryContextInvalid(
                    "MemoryContext can only be created from KnowledgeItem instances."
                )
            ensure_memory_context_item_account(
                context_account_id=account_id,
                item_account_id=knowledge.account_id,
            )
            if knowledge.id.value in seen_knowledge_ids:
                continue
            if not knowledge.is_eligible_for_context(strict=strict):
                continue

            items.append(
                MemoryContextItem.from_knowledge(
                    knowledge,
                    strict=strict,
                )
            )
            seen_knowledge_ids.add(knowledge.id.value)

        return cls.create(
            account_id=account_id,
            purpose=purpose,
            items=tuple(items),
            created_at=created_at,
            strict=strict,
        )

    def is_empty(self) -> bool:
        return len(self.items) == 0

    def knowledge_ids(self) -> tuple[KnowledgeId, ...]:
        return tuple(item.knowledge_id for item in self.items)
