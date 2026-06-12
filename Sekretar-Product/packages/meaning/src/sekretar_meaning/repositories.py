"""Repository interfaces for Meaning persistence.

Concrete persistence is intentionally out of scope for this skeleton.
Implementations may later use PostgreSQL, another store, or test-only in-memory
repositories without changing Meaning domain contracts.
"""

from __future__ import annotations

from typing import Protocol

from .entities import (
    InterpretiveDecisionScopeRecord,
    MeaningContext,
    MeaningEntity,
    MeaningHypothesis,
    MeaningHypothesisHistory,
    MeaningReference,
)
from .events import MeaningEvent
from .value_objects import (
    AccountId,
    InterpretiveDecisionScopeId,
    MeaningContextId,
    MeaningEntityId,
    MeaningHypothesisId,
    MeaningReferenceId,
)


class MeaningReferenceRepository(Protocol):
    """Persistence contract for observed meaning references."""

    def add(self, reference: MeaningReference) -> None: ...
    def get(self, reference_id: MeaningReferenceId) -> MeaningReference | None: ...
    def list_by_account(self, account_id: AccountId) -> list[MeaningReference]: ...


class MeaningHypothesisRepository(Protocol):
    """Persistence contract for meaning hypotheses."""

    def add(self, hypothesis: MeaningHypothesis) -> None: ...
    def get(self, hypothesis_id: MeaningHypothesisId) -> MeaningHypothesis | None: ...
    def update(self, hypothesis: MeaningHypothesis) -> None: ...
    def list_by_account(self, account_id: AccountId) -> list[MeaningHypothesis]: ...


class MeaningHypothesisHistoryRepository(Protocol):
    """Persistence contract for append-only hypothesis history."""

    def append(self, history: MeaningHypothesisHistory) -> None: ...
    def get(
        self,
        hypothesis_id: MeaningHypothesisId,
    ) -> MeaningHypothesisHistory | None: ...


class InterpretiveDecisionScopeRepository(Protocol):
    """Persistence contract for interpretive decision scopes."""

    def add(self, scope: InterpretiveDecisionScopeRecord) -> None: ...
    def get(
        self,
        scope_id: InterpretiveDecisionScopeId,
    ) -> InterpretiveDecisionScopeRecord | None: ...
    def update(self, scope: InterpretiveDecisionScopeRecord) -> None: ...
    def list_by_account(
        self,
        account_id: AccountId,
    ) -> list[InterpretiveDecisionScopeRecord]: ...


class MeaningEntityRepository(Protocol):
    """Persistence contract for promoted meaning entities."""

    def add(self, entity: MeaningEntity) -> None: ...
    def get(self, entity_id: MeaningEntityId) -> MeaningEntity | None: ...
    def update(self, entity: MeaningEntity) -> None: ...
    def list_by_account(self, account_id: AccountId) -> list[MeaningEntity]: ...


class MeaningContextRepository(Protocol):
    """Persistence contract for meaning context snapshots."""

    def add(self, context: MeaningContext) -> None: ...
    def get(self, context_id: MeaningContextId) -> MeaningContext | None: ...
    def list_by_account(self, account_id: AccountId) -> list[MeaningContext]: ...


class MeaningEventRepository(Protocol):
    """Persistence contract for emitted meaning domain events."""

    def append(self, event: MeaningEvent) -> None: ...
    def list_by_account(self, account_id: AccountId) -> list[MeaningEvent]: ...
