"""Meaning domain event skeletons."""


class MeaningEvent:
    """Base domain event marker for Meaning events."""


class MeaningReferenceObserved(MeaningEvent):
    """Emitted when a discourse or attribution reference is observed."""


class HypothesisCreated(MeaningEvent):
    """Emitted when a new meaning hypothesis is created."""


class EvidenceAdded(MeaningEvent):
    """Emitted when evidence is linked to a hypothesis or decision scope."""


class DecisionResolved(MeaningEvent):
    """Emitted when an interpretive decision scope becomes resolved."""


class DecisionConflicted(MeaningEvent):
    """Emitted when an interpretive decision scope becomes conflicted."""


class DecisionReopened(MeaningEvent):
    """Emitted when a previously resolved decision scope is reopened."""


class EntityPromoted(MeaningEvent):
    """Emitted when a meaning entity is promoted."""


class EntityValidated(MeaningEvent):
    """Emitted when a meaning entity becomes validated."""


class EntityCorrected(MeaningEvent):
    """Emitted when a meaning entity or binding is corrected."""


class EntityContradicted(MeaningEvent):
    """Emitted when a meaning entity enters contradicted validation state."""


class MeaningContextPrepared(MeaningEvent):
    """Emitted when Meaning prepares a scenario-specific context snapshot."""


class ClarificationCandidateEmitted(MeaningEvent):
    """Emitted when Meaning proposes a clarification candidate."""
