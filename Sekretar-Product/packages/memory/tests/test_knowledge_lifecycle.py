import unittest

from conftest import make_accepted_knowledge
from sekretar_memory.entities import KnowledgeItem
from sekretar_memory.enums import ConfidenceLevel, KnowledgeStatus, KnowledgeType, ProvenanceType
from sekretar_memory.errors import (
    InvalidKnowledgeContent,
    InvalidKnowledgeLifecycleTransition,
    KnowledgeAlreadyDeleted,
    KnowledgeImmutable,
    KnowledgeNotEligibleForContext,
)
from sekretar_memory.value_objects import AccountId, KnowledgeText, SourceId


class KnowledgeLifecycleTests(unittest.TestCase):
    def test_knowledge_item_cannot_be_created_with_candidate_status(self):
        with self.assertRaises(InvalidKnowledgeLifecycleTransition):
            KnowledgeItem.create_from_accepted(
                account_id=AccountId("account-1"),
                knowledge_type=KnowledgeType.FACT,
                text=KnowledgeText("Candidate status must not create KnowledgeItem."),
                status=KnowledgeStatus.CANDIDATE,
                confidence_level=ConfidenceLevel.UNCONFIRMED,
                primary_source_id=SourceId("source-1"),
                primary_provenance_type=ProvenanceType.MODEL_INFERRED,
            )

    def test_active_knowledge_can_be_confirmed(self):
        knowledge = make_accepted_knowledge(
            status=KnowledgeStatus.ACTIVE,
            confidence_level=ConfidenceLevel.INFERRED,
        )

        knowledge.transition_status(
            KnowledgeStatus.CONFIRMED,
            confidence_level=ConfidenceLevel.CONFIRMED,
        )

        self.assertIs(knowledge.status, KnowledgeStatus.CONFIRMED)
        self.assertIs(knowledge.confidence_level, ConfidenceLevel.CONFIRMED)
        self.assertTrue(knowledge.is_eligible_for_context())

    def test_archived_knowledge_is_terminal_in_phase_1(self):
        knowledge = make_accepted_knowledge(
            status=KnowledgeStatus.ACTIVE,
            confidence_level=ConfidenceLevel.CONFIRMED,
        )
        knowledge.transition_status(
            KnowledgeStatus.CONFIRMED,
            confidence_level=ConfidenceLevel.CONFIRMED,
        )
        knowledge.transition_status(KnowledgeStatus.ARCHIVED)

        self.assertTrue(knowledge.is_terminal())

        with self.assertRaises(KnowledgeImmutable):
            knowledge.transition_status(KnowledgeStatus.ACTIVE)

        with self.assertRaises(KnowledgeImmutable):
            knowledge.transition_status(KnowledgeStatus.DELETED)

    def test_deleted_and_forgotten_remain_distinct_terminal_states(self):
        deleted = make_accepted_knowledge()
        deleted.transition_status(KnowledgeStatus.DELETED)

        forgotten = make_accepted_knowledge()
        forgotten.transition_status(KnowledgeStatus.FORGOTTEN)

        self.assertIs(deleted.status, KnowledgeStatus.DELETED)
        self.assertIs(forgotten.status, KnowledgeStatus.FORGOTTEN)
        self.assertTrue(deleted.is_terminal())
        self.assertTrue(forgotten.is_terminal())

    def test_deleted_knowledge_cannot_be_used_as_active_memory(self):
        knowledge = make_accepted_knowledge()
        knowledge.transition_status(KnowledgeStatus.DELETED)

        with self.assertRaises(KnowledgeAlreadyDeleted):
            knowledge.ensure_active()

    def test_contradicted_knowledge_is_not_context_eligible(self):
        knowledge = make_accepted_knowledge(
            status=KnowledgeStatus.ACTIVE,
            confidence_level=ConfidenceLevel.INFERRED,
        )
        knowledge.transition_status(
            KnowledgeStatus.CONTRADICTED,
            confidence_level=ConfidenceLevel.CONTRADICTED,
        )

        self.assertFalse(knowledge.is_eligible_for_context())

        with self.assertRaises(KnowledgeNotEligibleForContext):
            knowledge.ensure_eligible_for_context()

    def test_empty_knowledge_text_is_rejected(self):
        with self.assertRaises(InvalidKnowledgeContent):
            KnowledgeText("   ")


if __name__ == "__main__":
    unittest.main()
