"""Meaning domain enumerations.

These enums define the architectural surface of the Meaning block. They do not
implement storage, retrieval, inference, promotion, or validation logic.
"""

from enum import Enum


class ReferenceKind(str, Enum):
    """Phase 1 observed referent kinds in discourse or attribution."""

    PERSON_MENTION = "person_mention"
    ROLE_MENTION = "role_mention"
    RESPONSIBILITY_MENTION = "responsibility_mention"
    SPEAKER_REF = "speaker_ref"
    GROUP_MENTION = "group_mention"


class HypothesisType(str, Enum):
    """Phase 1 interpretive hypothesis types."""

    CO_REFERENCE = "co_reference"
    ROLE_ATTRIBUTION = "role_attribution"
    RESPONSIBILITY = "responsibility"
    SPEAKER_IDENTITY = "speaker_identity"
    DECISION_INTERPRETATION = "decision_interpretation"


class HypothesisStatus(str, Enum):
    """Lifecycle states for a meaning hypothesis."""

    PROPOSED = "proposed"
    SUPPORTED = "supported"
    CONFIRMED = "confirmed"
    REJECTED = "rejected"
    SUPERSEDED = "superseded"


class MeaningDecisionState(str, Enum):
    """State of an interpretive decision scope."""

    RESOLVED = "resolved"
    UNRESOLVED = "unresolved"
    CONFLICTED = "conflicted"


class MeaningEntityValidationState(str, Enum):
    """Validation state of a promoted meaning entity."""

    NOT_APPLICABLE = "not_applicable"
    UNVALIDATED = "unvalidated"
    VALIDATED = "validated"
    CORRECTED = "corrected"
    CONTRADICTED = "contradicted"


class EvidenceStrength(str, Enum):
    """Phase 1 evidence strength taxonomy."""

    DIRECT = "direct"
    STRONG = "strong"
    WEAK = "weak"


class EvidenceRole(str, Enum):
    """How evidence affects an interpretive hypothesis."""

    SUPPORTS = "supports"
    WEAKENS = "weakens"
    CONFLICTS = "conflicts"


class EntityKind(str, Enum):
    """Phase 1 promoted meaning entity kinds."""

    PERSON = "person"
    RESPONSIBILITY_SCOPE = "responsibility_scope"


class MeaningContextPurpose(str, Enum):
    """Phase 1 scenarios for preparing a meaning context snapshot."""

    MEETING_INTERPRETATION = "meeting_interpretation"
    TASK_ASSIGNMENT = "task_assignment"


class ClarificationCandidateIntent(str, Enum):
    """Recommended clarification intent emitted by Meaning."""

    CONFIRM = "confirm"
    DISAMBIGUATE = "disambiguate"
    REJECT = "reject"
    CORRECT = "correct"
    DEFER = "defer"


class MeaningEventType(str, Enum):
    """Domain events emitted by the Meaning block."""

    MEANING_REFERENCE_OBSERVED = "meaning_reference_observed"
    HYPOTHESIS_CREATED = "hypothesis_created"
    EVIDENCE_ADDED = "evidence_added"
    DECISION_RESOLVED = "decision_resolved"
    DECISION_CONFLICTED = "decision_conflicted"
    DECISION_REOPENED = "decision_reopened"
    ENTITY_PROMOTED = "entity_promoted"
    ENTITY_VALIDATED = "entity_validated"
    ENTITY_CORRECTED = "entity_corrected"
    ENTITY_CONTRADICTED = "entity_contradicted"
    MEANING_CONTEXT_PREPARED = "meaning_context_prepared"
    CLARIFICATION_CANDIDATE_EMITTED = "clarification_candidate_emitted"
