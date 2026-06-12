"""Meaning domain entity skeletons.

These classes describe the approved Meaning domain surface. They intentionally
contain no business logic, policy behavior, or persistence implementation.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from .enums import (
    EntityKind,
    HypothesisStatus,
    HypothesisType,
    MeaningContextPurpose,
    MeaningDecisionState,
    MeaningEntityValidationState,
)
from .value_objects import (
    AccountId,
    InterpretiveDecisionScopeId,
    MeaningContextId,
    MeaningEntityId,
    MeaningEvidenceLink,
    MeaningHypothesisId,
    MeaningReferenceId,
    ReferenceObservation,
    ResponsibilityAttribution,
    RoleAttribution,
)


@dataclass(frozen=True, slots=True)
class MeaningReference:
    """Observed discourse or attribution referent."""

    id: MeaningReferenceId
    account_id: AccountId
    observation: ReferenceObservation


@dataclass(frozen=True, slots=True)
class MeaningHypothesis:
    """Proposed interpretation over one or more references."""

    id: MeaningHypothesisId
    account_id: AccountId
    hypothesis_type: HypothesisType
    status: HypothesisStatus
    subject_reference_id: MeaningReferenceId | None = None
    object_reference_id: MeaningReferenceId | None = None
    decision_scope_id: InterpretiveDecisionScopeId | None = None
    evidence_links: tuple[MeaningEvidenceLink, ...] = field(default_factory=tuple)


@dataclass(frozen=True, slots=True)
class MeaningHypothesisRecord:
    """Append-only history entry for a meaning hypothesis."""

    hypothesis_id: MeaningHypothesisId
    account_id: AccountId
    status: HypothesisStatus
    recorded_at: datetime


@dataclass(frozen=True, slots=True)
class MeaningHypothesisHistory:
    """Append-only history container for a meaning hypothesis."""

    hypothesis_id: MeaningHypothesisId
    account_id: AccountId
    records: tuple[MeaningHypothesisRecord, ...] = field(default_factory=tuple)


@dataclass(frozen=True, slots=True)
class InterpretiveDecisionScopeRecord:
    """State record for a bounded interpretive decision scope."""

    scope_id: InterpretiveDecisionScopeId
    account_id: AccountId
    hypothesis_type: HypothesisType
    decision_state: MeaningDecisionState
    question: str
    leading_hypothesis_id: MeaningHypothesisId | None = None


@dataclass(frozen=True, slots=True)
class MeaningEntityBinding:
    """Binding between a promoted entity and interpretive references."""

    entity_id: MeaningEntityId
    account_id: AccountId
    reference_id: MeaningReferenceId
    role_attribution: RoleAttribution | None = None
    responsibility_attribution: ResponsibilityAttribution | None = None


@dataclass(frozen=True, slots=True)
class MeaningEntity:
    """Promoted continuity object in the user's working world."""

    id: MeaningEntityId
    account_id: AccountId
    entity_kind: EntityKind
    validation_state: MeaningEntityValidationState
    display_label: str | None = None
    bindings: tuple[MeaningEntityBinding, ...] = field(default_factory=tuple)
    promoted_from_hypothesis_id: MeaningHypothesisId | None = None


@dataclass(frozen=True, slots=True)
class MeaningContextItem:
    """One interpretive item included in a meaning context snapshot."""

    account_id: AccountId
    reference_id: MeaningReferenceId | None = None
    hypothesis_id: MeaningHypothesisId | None = None
    scope_id: InterpretiveDecisionScopeId | None = None
    entity_id: MeaningEntityId | None = None
    decision_state: MeaningDecisionState | None = None
    validation_state: MeaningEntityValidationState | None = None


@dataclass(frozen=True, slots=True)
class MeaningContext:
    """Scenario-specific snapshot of meaning interpretation."""

    id: MeaningContextId
    account_id: AccountId
    purpose: MeaningContextPurpose
    items: tuple[MeaningContextItem, ...] = field(default_factory=tuple)
    created_at: datetime | None = None
    strict: bool = False
