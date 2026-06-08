"""Memory domain entities."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import uuid4

from .enums import (
    CandidateKnowledgeStatus,
    CandidateRejectionReason,
    ConfidenceLevel,
    KnowledgeStatus,
    KnowledgeType,
    ProvenanceType,
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
    ensure_eligible_for_acceptance,
    ensure_eligible_for_context,
    ensure_merge_target_present,
    ensure_merged_candidate_has_target,
    ensure_knowledge_item_status,
    ensure_lifecycle_record_identity_present,
    ensure_lifecycle_record_matches_knowledge,
    ensure_lifecycle_record_transition,
    ensure_lifecycle_transition_allowed,
    ensure_not_raw_source_dump,
    ensure_not_terminal_for_active_use,
    ensure_provenance_present,
    ensure_source_reference_present,
    ensure_status_confidence_compatible,
    is_eligible_for_acceptance,
    is_eligible_for_context,
)
from .value_objects import (
    AccountId,
    CandidateKnowledgeId,
    ConfidenceReason,
    ConfidenceScore,
    KnowledgeId,
    KnowledgeLanguage,
    KnowledgeSummary,
    KnowledgeTags,
    KnowledgeText,
    LifecycleReason,
    LifecycleRecordId,
    ProvenanceId,
    ProvenanceNote,
    SourceId,
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


class MemorySource:
    """Source reference that may produce candidate knowledge."""


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


class KnowledgeProvenance:
    """Explanation of where knowledge came from."""


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


class KnowledgeRelation:
    """Meaningful relation between knowledge and another reference."""


class MemoryCorrection:
    """User or system correction applied to knowledge."""


class MemoryContradiction:
    """Explicit conflict between knowledge items or candidates."""


class MemoryContext:
    """Scenario-specific subset of Memory for another block."""
