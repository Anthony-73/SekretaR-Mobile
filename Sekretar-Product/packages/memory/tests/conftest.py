from __future__ import annotations

import sys
from pathlib import Path

PACKAGE_SRC = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(PACKAGE_SRC))

from sekretar_memory.entities import KnowledgeItem  # noqa: E402
from sekretar_memory.enums import (  # noqa: E402
    ConfidenceLevel,
    KnowledgeStatus,
    KnowledgeType,
    ProvenanceType,
)
from sekretar_memory.value_objects import (  # noqa: E402
    AccountId,
    KnowledgeText,
    SourceId,
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
