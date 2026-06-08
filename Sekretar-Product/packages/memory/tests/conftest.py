from __future__ import annotations

import sys
from pathlib import Path

PACKAGE_SRC = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(PACKAGE_SRC))

from sekretar_memory.entities import CandidateKnowledge, KnowledgeItem, MemorySource  # noqa: E402
from sekretar_memory.enums import (  # noqa: E402
    ConfidenceLevel,
    KnowledgeStatus,
    KnowledgeType,
    ProvenanceType,
    SourceType,
)
from sekretar_memory.value_objects import (  # noqa: E402
    AccountId,
    KnowledgeText,
    SourceId,
    SourceReference,
)


def make_accepted_knowledge(
    *,
    account_id: str = "account-1",
    text: str = "Client A prefers short commercial proposals.",
    status: KnowledgeStatus = KnowledgeStatus.ACTIVE,
    confidence_level: ConfidenceLevel = ConfidenceLevel.INFERRED,
    knowledge_type: KnowledgeType = KnowledgeType.PREFERENCE,
    source_id: str = "source-1",
    provenance_type: ProvenanceType = ProvenanceType.MODEL_INFERRED,
) -> KnowledgeItem:
    return KnowledgeItem.create_from_accepted(
        account_id=AccountId(account_id),
        knowledge_type=knowledge_type,
        text=KnowledgeText(text),
        status=status,
        confidence_level=confidence_level,
        primary_source_id=SourceId(source_id),
        primary_provenance_type=provenance_type,
    )


def make_candidate_knowledge(
    *,
    account_id: str = "account-1",
    source_id: str = "source-1",
    text: str = "Ivan is responsible for warehouse process design.",
    confidence_level: ConfidenceLevel = ConfidenceLevel.INFERRED,
    knowledge_type: KnowledgeType = KnowledgeType.RESPONSIBILITY,
    provenance_type: ProvenanceType = ProvenanceType.MODEL_INFERRED,
    source_type: SourceType | None = SourceType.MEETING,
) -> CandidateKnowledge:
    return CandidateKnowledge.create_detected(
        account_id=AccountId(account_id),
        source_id=SourceId(source_id),
        knowledge_type=knowledge_type,
        text=KnowledgeText(text),
        confidence_level=confidence_level,
        provenance_type=provenance_type,
        source_type=source_type,
    )


def make_memory_source(
    *,
    account_id: str = "account-1",
    source_type: SourceType = SourceType.MEETING,
    external_reference: str = "meeting:planning-june",
    source_id: str | None = None,
) -> MemorySource:
    return MemorySource.create(
        account_id=AccountId(account_id),
        source_type=source_type,
        external_reference=SourceReference(external_reference),
        source_id=SourceId(source_id) if source_id is not None else None,
    )
