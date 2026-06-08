import unittest

from conftest import make_accepted_knowledge
from sekretar_memory.entities import KnowledgeItem
from sekretar_memory.enums import ConfidenceLevel, KnowledgeStatus, KnowledgeType, ProvenanceType
from sekretar_memory.errors import ConfidenceRequired, KnowledgeStatusMismatch
from sekretar_memory.value_objects import AccountId, KnowledgeText, SourceId


class ConfidenceTests(unittest.TestCase):
    def test_accepted_knowledge_requires_confidence(self):
        with self.assertRaises(ConfidenceRequired):
            KnowledgeItem.create_from_accepted(
                account_id=AccountId("account-1"),
                knowledge_type=KnowledgeType.FACT,
                text=KnowledgeText("Delivery timelines are sensitive for Company A."),
                status=KnowledgeStatus.ACTIVE,
                confidence_level=None,  # type: ignore[arg-type]
                primary_source_id=SourceId("source-1"),
                primary_provenance_type=ProvenanceType.EXPLICITLY_STATED,
            )

    def test_unconfirmed_knowledge_allows_unconfirmed_confidence(self):
        knowledge = make_accepted_knowledge(
            status=KnowledgeStatus.UNCONFIRMED,
            confidence_level=ConfidenceLevel.UNCONFIRMED,
        )

        self.assertIs(knowledge.status, KnowledgeStatus.UNCONFIRMED)
        self.assertIs(knowledge.confidence_level, ConfidenceLevel.UNCONFIRMED)

    def test_confirmed_status_requires_confirmed_confidence(self):
        knowledge = make_accepted_knowledge(
            status=KnowledgeStatus.ACTIVE,
            confidence_level=ConfidenceLevel.INFERRED,
        )

        with self.assertRaises(KnowledgeStatusMismatch):
            knowledge.transition_status(KnowledgeStatus.CONFIRMED)

    def test_update_confidence_must_remain_compatible_with_status(self):
        knowledge = make_accepted_knowledge(
            status=KnowledgeStatus.ACTIVE,
            confidence_level=ConfidenceLevel.INFERRED,
        )
        knowledge.transition_status(
            KnowledgeStatus.CONFIRMED,
            confidence_level=ConfidenceLevel.CONFIRMED,
        )

        with self.assertRaises(KnowledgeStatusMismatch):
            knowledge.update_confidence(ConfidenceLevel.INFERRED)


if __name__ == "__main__":
    unittest.main()
