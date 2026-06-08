import unittest

from conftest import make_accepted_knowledge
from sekretar_memory.entities import KnowledgeItem
from sekretar_memory.enums import ConfidenceLevel, KnowledgeStatus, KnowledgeType, ProvenanceType
from sekretar_memory.errors import InvalidKnowledgeContent, ProvenanceRequired
from sekretar_memory.value_objects import AccountId, KnowledgeText, SourceId


class ProvenanceTests(unittest.TestCase):
    def test_accepted_knowledge_requires_primary_source_and_provenance_type(self):
        knowledge = make_accepted_knowledge()

        self.assertEqual(knowledge.primary_source_id.value, "source-1")
        self.assertIs(
            knowledge.primary_provenance_type,
            ProvenanceType.MODEL_INFERRED,
        )

    def test_accepted_knowledge_rejects_missing_provenance(self):
        with self.assertRaises(ProvenanceRequired):
            KnowledgeItem.create_from_accepted(
                account_id=AccountId("account-1"),
                knowledge_type=KnowledgeType.FACT,
                text=KnowledgeText("Warehouse process belongs to Ivan."),
                status=KnowledgeStatus.ACTIVE,
                confidence_level=ConfidenceLevel.INFERRED,
                primary_source_id=None,  # type: ignore[arg-type]
                primary_provenance_type=ProvenanceType.EXPLICITLY_STATED,
            )

    def test_knowledge_text_rejects_raw_dump_markers(self):
        with self.assertRaises(InvalidKnowledgeContent):
            KnowledgeText("[TRANSCRIPT] full meeting dump")


if __name__ == "__main__":
    unittest.main()
