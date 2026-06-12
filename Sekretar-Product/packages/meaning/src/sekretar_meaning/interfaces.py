"""External Meaning integration port contracts.

These interfaces describe how future blocks should interact with Meaning without
giving Meaning ownership of their lifecycles.
"""

from __future__ import annotations

from typing import Any, Protocol

from .value_objects import (
    ClarificationCandidatePayload,
    SpeakerAttributionEvidence,
    VoiceMatchEvidence,
)


class MemoryContextConsumerPort(Protocol):
    """Consumes Memory context and claim signals for interpretation input."""

    def consume_memory_context(self, memory_context: Any) -> None: ...


class MemoryReevaluationTriggerPort(Protocol):
    """Receives Memory domain events that may require Meaning re-evaluation."""

    def on_memory_change(self, memory_event: Any) -> None: ...


class SpeakerEvidenceIngressPort(Protocol):
    """Receives opaque speaker attribution and voice match evidence."""

    def ingest_speaker_attribution(
        self,
        evidence: SpeakerAttributionEvidence,
    ) -> None: ...

    def ingest_voice_match(self, evidence: VoiceMatchEvidence) -> None: ...


class ClarificationOutcomePort(Protocol):
    """Applies clarification outcomes back into Meaning interpretation."""

    def apply_clarification_outcome(self, outcome: Any) -> None: ...


class ClarificationCandidatePort(Protocol):
    """Emits clarification candidates to the future Clarification capability."""

    def emit_candidate(self, candidate: ClarificationCandidatePayload) -> None: ...


class StrictConsumerEligibilityPort(Protocol):
    """Exposes strict-use eligibility for downstream consumers."""

    def is_strict_eligible(
        self,
        *,
        scope_id: Any,
        entity_id: Any | None = None,
    ) -> bool: ...
