"""Meaning domain errors."""


class MeaningError(Exception):
    """Base error for Meaning domain failures."""


class MeaningReferenceNotFound(MeaningError):
    """Raised when a meaning reference cannot be found."""


class MeaningHypothesisNotFound(MeaningError):
    """Raised when a meaning hypothesis cannot be found."""


class InterpretiveDecisionScopeNotFound(MeaningError):
    """Raised when an interpretive decision scope cannot be found."""


class MeaningEntityNotFound(MeaningError):
    """Raised when a meaning entity cannot be found."""


class MeaningOwnershipMismatch(MeaningError):
    """Raised when meaning data does not belong to the expected Account."""


class MeaningContextInvalid(MeaningError):
    """Raised when a meaning context snapshot violates domain shape rules."""


class MeaningEvidenceInvalid(MeaningError):
    """Raised when evidence attachment violates domain shape rules."""


class MeaningPromotionInvalid(MeaningError):
    """Raised when entity promotion violates domain rules."""


class MeaningValidationInvalid(MeaningError):
    """Raised when entity validation state violates domain rules."""


class StrictConsumerRequirementNotMet(MeaningError):
    """Raised when strict consumer eligibility requirements are not met."""
