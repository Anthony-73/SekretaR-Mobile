"""Memory value objects."""

from __future__ import annotations

from dataclasses import dataclass

from .constants import MAX_KNOWLEDGE_TEXT_LENGTH, RAW_DUMP_MARKERS
from .errors import InvalidKnowledgeContent


def _normalize_required_text(value: str, *, field_name: str) -> str:
    normalized = (value or "").strip()
    if not normalized:
        raise InvalidKnowledgeContent(f"{field_name} must not be empty.")
    return normalized


@dataclass(frozen=True, slots=True)
class AccountId:
    """Identifier of the Account that owns Memory."""

    value: str

    def __post_init__(self) -> None:
        object.__setattr__(self, "value", _normalize_required_text(self.value, field_name="AccountId"))


@dataclass(frozen=True, slots=True)
class UserId:
    """Identifier of the user acting within Account-owned Memory."""

    value: str

    def __post_init__(self) -> None:
        object.__setattr__(self, "value", _normalize_required_text(self.value, field_name="UserId"))


@dataclass(frozen=True, slots=True)
class DeviceId:
    """Device identifier used as access metadata, not as Memory owner."""

    value: str

    def __post_init__(self) -> None:
        object.__setattr__(self, "value", _normalize_required_text(self.value, field_name="DeviceId"))


@dataclass(frozen=True, slots=True)
class SessionId:
    """Session identifier used as temporary access metadata."""

    value: str

    def __post_init__(self) -> None:
        object.__setattr__(self, "value", _normalize_required_text(self.value, field_name="SessionId"))


@dataclass(frozen=True, slots=True)
class KnowledgeId:
    """Identifier of a durable knowledge item."""

    value: str

    def __post_init__(self) -> None:
        object.__setattr__(self, "value", _normalize_required_text(self.value, field_name="KnowledgeId"))


@dataclass(frozen=True, slots=True)
class CandidateKnowledgeId:
    """Identifier of a candidate knowledge item."""

    value: str

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "value",
            _normalize_required_text(self.value, field_name="CandidateKnowledgeId"),
        )


@dataclass(frozen=True, slots=True)
class SourceId:
    """Identifier of a source that may produce candidate knowledge."""

    value: str

    def __post_init__(self) -> None:
        object.__setattr__(self, "value", _normalize_required_text(self.value, field_name="SourceId"))


@dataclass(frozen=True, slots=True)
class SourceReference:
    """Reference to an external source object without transferring ownership."""

    value: str

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "value",
            _normalize_required_text(self.value, field_name="SourceReference"),
        )


@dataclass(frozen=True, slots=True)
class SourceTimestamp:
    """Timestamp associated with source appearance or source evidence."""

    value: str

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "value",
            _normalize_required_text(self.value, field_name="SourceTimestamp"),
        )


@dataclass(frozen=True, slots=True)
class KnowledgeText:
    """Meaningful durable knowledge text, not a raw source dump."""

    value: str

    def __post_init__(self) -> None:
        normalized = _normalize_required_text(self.value, field_name="KnowledgeText")
        if len(normalized) > MAX_KNOWLEDGE_TEXT_LENGTH:
            raise InvalidKnowledgeContent(
                f"KnowledgeText exceeds maximum length of {MAX_KNOWLEDGE_TEXT_LENGTH}."
            )

        upper = normalized.upper()
        for marker in RAW_DUMP_MARKERS:
            if upper.startswith(marker):
                raise InvalidKnowledgeContent(
                    f"KnowledgeText must not begin with raw dump marker {marker!r}."
                )

        object.__setattr__(self, "value", normalized)


@dataclass(frozen=True, slots=True)
class KnowledgeSummary:
    """Short human-readable description of knowledge."""

    value: str

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "value",
            _normalize_required_text(self.value, field_name="KnowledgeSummary"),
        )


@dataclass(frozen=True, slots=True)
class KnowledgeLanguage:
    """Language marker for knowledge content."""

    value: str

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "value",
            _normalize_required_text(self.value, field_name="KnowledgeLanguage"),
        )


@dataclass(frozen=True, slots=True)
class KnowledgeTags:
    """Tags that may help classify knowledge without owning relationships."""

    values: tuple[str, ...]

    def __post_init__(self) -> None:
        normalized = tuple(
            _normalize_required_text(tag, field_name="KnowledgeTags")
            for tag in self.values
        )
        object.__setattr__(self, "values", normalized)


@dataclass(frozen=True, slots=True)
class ProvenanceNote:
    """Human-readable note explaining where knowledge came from."""

    value: str

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "value",
            _normalize_required_text(self.value, field_name="ProvenanceNote"),
        )


@dataclass(frozen=True, slots=True)
class ProvenanceTimestamp:
    """Timestamp of provenance creation or source observation."""

    value: str

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "value",
            _normalize_required_text(self.value, field_name="ProvenanceTimestamp"),
        )


@dataclass(frozen=True, slots=True)
class ConfidenceScore:
    """Optional product-level numeric confidence marker."""

    value: float

    def __post_init__(self) -> None:
        if self.value < 0.0 or self.value > 1.0:
            raise InvalidKnowledgeContent("ConfidenceScore must be between 0.0 and 1.0.")
        object.__setattr__(self, "value", float(self.value))


@dataclass(frozen=True, slots=True)
class ConfidenceReason:
    """Reason explaining a confidence level."""

    value: str

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "value",
            _normalize_required_text(self.value, field_name="ConfidenceReason"),
        )


@dataclass(frozen=True, slots=True)
class LifecycleRecordId:
    """Identifier of an append-only knowledge lifecycle record."""

    value: str

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "value",
            _normalize_required_text(self.value, field_name="LifecycleRecordId"),
        )


@dataclass(frozen=True, slots=True)
class ProvenanceId:
    """Identifier of a provenance record linked to knowledge."""

    value: str

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "value",
            _normalize_required_text(self.value, field_name="ProvenanceId"),
        )


@dataclass(frozen=True, slots=True)
class LifecycleReason:
    """Reason for a lifecycle transition."""

    value: str

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "value",
            _normalize_required_text(self.value, field_name="LifecycleReason"),
        )


@dataclass(frozen=True, slots=True)
class LifecycleTimestamp:
    """Timestamp of a lifecycle transition."""

    value: str

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "value",
            _normalize_required_text(self.value, field_name="LifecycleTimestamp"),
        )


@dataclass(frozen=True, slots=True)
class RelatedObjectReference:
    """Reference to related product object without transferring ownership."""

    value: str

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "value",
            _normalize_required_text(self.value, field_name="RelatedObjectReference"),
        )
