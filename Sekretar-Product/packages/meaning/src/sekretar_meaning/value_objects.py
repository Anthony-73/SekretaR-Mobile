"""Meaning immutable value objects."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from .enums import (
    ClarificationCandidateIntent,
    EvidenceRole,
    EvidenceStrength,
    HypothesisType,
    MeaningDecisionState,
    ReferenceKind,
)


@dataclass(frozen=True, slots=True)
class AccountId:
    """Identifier of the Account that owns Meaning interpretation."""

    value: str


@dataclass(frozen=True, slots=True)
class MeaningReferenceId:
    """Identifier of an observed meaning reference."""

    value: str


@dataclass(frozen=True, slots=True)
class MeaningHypothesisId:
    """Identifier of a meaning hypothesis."""

    value: str


@dataclass(frozen=True, slots=True)
class InterpretiveDecisionScopeId:
    """Identifier of a bounded interpretive decision scope."""

    value: str


@dataclass(frozen=True, slots=True)
class MeaningEntityId:
    """Identifier of a promoted meaning entity."""

    value: str


@dataclass(frozen=True, slots=True)
class MeaningContextId:
    """Identifier of a meaning context snapshot."""

    value: str


@dataclass(frozen=True, slots=True)
class KnowledgeId:
    """Opaque Memory knowledge identifier referenced by Meaning evidence."""

    value: str


@dataclass(frozen=True, slots=True)
class MeetingRef:
    """Opaque meeting identifier for reference or evidence context."""

    value: str


@dataclass(frozen=True, slots=True)
class SurfaceForm:
    """Observed surface form from discourse."""

    value: str


@dataclass(frozen=True, slots=True)
class SpeakerRef:
    """Opaque speaker label or speaker_ref from attribution."""

    value: str


@dataclass(frozen=True, slots=True)
class VoiceProfileRef:
    """Opaque voice profile reference owned by Speaker Intelligence."""

    value: str


@dataclass(frozen=True, slots=True)
class SegmentRef:
    """Opaque transcript segment reference."""

    value: str


@dataclass(frozen=True, slots=True)
class InterpretiveDecisionScope:
    """Descriptor of a bounded interpretive question."""

    scope_id: InterpretiveDecisionScopeId
    account_id: AccountId
    hypothesis_type: HypothesisType
    question: str


@dataclass(frozen=True, slots=True)
class MeaningEvidence:
    """Evidence payload used to justify interpretation."""

    strength: EvidenceStrength
    role: EvidenceRole
    summary: str | None = None


@dataclass(frozen=True, slots=True)
class MeaningEvidenceLink:
    """Attachment of evidence to a hypothesis or decision scope."""

    evidence: MeaningEvidence
    knowledge_id: KnowledgeId | None = None
    speaker_ref: SpeakerRef | None = None
    voice_profile_ref: VoiceProfileRef | None = None
    meeting_ref: MeetingRef | None = None
    segment_ref: SegmentRef | None = None


@dataclass(frozen=True, slots=True)
class RoleAttribution:
    """Interpretive binding between a person reference and a role mention."""

    person_reference_id: MeaningReferenceId
    role_reference_id: MeaningReferenceId
    summary: str | None = None


@dataclass(frozen=True, slots=True)
class ResponsibilityAttribution:
    """Interpretive binding between a person and a responsibility scope."""

    person_reference_id: MeaningReferenceId | None
    responsibility_reference_id: MeaningReferenceId
    summary: str | None = None


@dataclass(frozen=True, slots=True)
class SpeakerAttributionEvidence:
    """Speaker attribution evidence from Speaker Intelligence."""

    speaker_ref: SpeakerRef
    meeting_ref: MeetingRef
    segment_refs: tuple[SegmentRef, ...] = field(default_factory=tuple)


@dataclass(frozen=True, slots=True)
class VoiceMatchEvidence:
    """Voice match metadata used as interpretive evidence only."""

    voice_profile_ref: VoiceProfileRef
    match_strength: EvidenceStrength
    matched_speaker_ref: SpeakerRef | None = None


@dataclass(frozen=True, slots=True)
class ClarificationCandidatePayload:
    """Data Meaning emits to the future Clarification capability."""

    scope_id: InterpretiveDecisionScopeId
    account_id: AccountId
    decision_state: MeaningDecisionState
    hypothesis_ids: tuple[MeaningHypothesisId, ...]
    reference_ids: tuple[MeaningReferenceId, ...]
    knowledge_ids: tuple[KnowledgeId, ...]
    intent: ClarificationCandidateIntent
    expected_value: str | None = None


@dataclass(frozen=True, slots=True)
class ReferenceObservation:
    """Observed referent details for a meaning reference."""

    kind: ReferenceKind
    surface_form: SurfaceForm | None = None
    meeting_ref: MeetingRef | None = None
    speaker_ref: SpeakerRef | None = None
