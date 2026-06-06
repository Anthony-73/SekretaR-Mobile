"""Repository interfaces for Memory persistence.

Concrete persistence is intentionally out of scope for this skeleton.
Implementations may later use PostgreSQL, another store, or test-only in-memory
repositories without changing Memory domain contracts.
"""

from __future__ import annotations

from typing import Protocol

from .entities import (
    CandidateKnowledge,
    KnowledgeItem,
    KnowledgeLifecycleRecord,
    KnowledgeProvenance,
    KnowledgeRelation,
    MemorySource,
)
from .events import MemoryEvent
from .value_objects import (
    AccountId,
    CandidateKnowledgeId,
    KnowledgeId,
    SourceId,
)


class KnowledgeRepository(Protocol):
    """Persistence contract for durable knowledge items."""

    def add(self, knowledge: KnowledgeItem) -> None: ...
    def get(self, knowledge_id: KnowledgeId) -> KnowledgeItem | None: ...
    def update(self, knowledge: KnowledgeItem) -> None: ...
    def list_by_account(self, account_id: AccountId) -> list[KnowledgeItem]: ...


class CandidateKnowledgeRepository(Protocol):
    """Persistence contract for candidate knowledge."""

    def add(self, candidate: CandidateKnowledge) -> None: ...
    def get(self, candidate_id: CandidateKnowledgeId) -> CandidateKnowledge | None: ...
    def update(self, candidate: CandidateKnowledge) -> None: ...
    def list_by_account(self, account_id: AccountId) -> list[CandidateKnowledge]: ...


class MemorySourceRepository(Protocol):
    """Persistence contract for source references."""

    def add(self, source: MemorySource) -> None: ...
    def get(self, source_id: SourceId) -> MemorySource | None: ...
    def list_by_account(self, account_id: AccountId) -> list[MemorySource]: ...


class ProvenanceRepository(Protocol):
    """Persistence contract for knowledge provenance."""

    def add(self, provenance: KnowledgeProvenance) -> None: ...
    def list_by_knowledge(self, knowledge_id: KnowledgeId) -> list[KnowledgeProvenance]: ...


class KnowledgeRelationRepository(Protocol):
    """Persistence contract for knowledge relations."""

    def add(self, relation: KnowledgeRelation) -> None: ...
    def list_by_knowledge(self, knowledge_id: KnowledgeId) -> list[KnowledgeRelation]: ...
    def list_by_account(self, account_id: AccountId) -> list[KnowledgeRelation]: ...


class KnowledgeLifecycleRepository(Protocol):
    """Persistence contract for knowledge lifecycle records."""

    def append(self, record: KnowledgeLifecycleRecord) -> None: ...
    def list_by_knowledge(
        self,
        knowledge_id: KnowledgeId,
    ) -> list[KnowledgeLifecycleRecord]: ...


class MemoryEventRepository(Protocol):
    """Persistence contract for Memory domain events."""

    def add(self, event: MemoryEvent) -> None: ...
    def list_by_account(self, account_id: AccountId) -> list[MemoryEvent]: ...
    def list_by_knowledge(self, knowledge_id: KnowledgeId) -> list[MemoryEvent]: ...
