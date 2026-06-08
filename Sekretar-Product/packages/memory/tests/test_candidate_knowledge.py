import unittest

from conftest import make_candidate_knowledge
from sekretar_memory.entities import CandidateKnowledge, KnowledgeItem
from sekretar_memory.enums import (
    CandidateKnowledgeStatus,
    CandidateRejectionReason,
    ConfidenceLevel,
    KnowledgeStatus,
    KnowledgeType,
    ProvenanceType,
    SourceType,
)
from sekretar_memory.errors import (
    CandidateAlreadyResolved,
    CandidateNotEligibleForAcceptance,
    ConfidenceRequired,
    InvalidKnowledgeContent,
    InvalidMemorySource,
    KnowledgeNotEligibleForContext,
    KnowledgeOwnershipMismatch,
    ProvenanceRequired,
)
from sekretar_memory.value_objects import (
    AccountId,
    KnowledgeId,
    KnowledgeText,
    SourceId,
    UserId,
)


class CandidateKnowledgeTests(unittest.TestCase):
    def test_candidate_knowledge_is_created_with_required_fields(self):
        candidate = make_candidate_knowledge(
            account_id="account-1",
            source_id="source-meeting-1",
            text="Ivan is responsible for warehouse process design.",
            confidence_level=ConfidenceLevel.INFERRED,
            provenance_type=ProvenanceType.MODEL_INFERRED,
            source_type=SourceType.MEETING,
        )

        self.assertEqual(candidate.account_id.value, "account-1")
        self.assertEqual(candidate.source_id.value, "source-meeting-1")
        self.assertIs(candidate.status, CandidateKnowledgeStatus.DETECTED)
        self.assertIs(candidate.knowledge_type, KnowledgeType.RESPONSIBILITY)
        self.assertEqual(
            candidate.text.value,
            "Ivan is responsible for warehouse process design.",
        )
        self.assertIs(candidate.confidence_level, ConfidenceLevel.INFERRED)
        self.assertIs(candidate.provenance_type, ProvenanceType.MODEL_INFERRED)
        self.assertIs(candidate.source_type, SourceType.MEETING)
        self.assertIsNotNone(candidate.id.value)
        self.assertIsNotNone(candidate.created_at)

    def test_candidate_knowledge_requires_account_ownership(self):
        candidate = make_candidate_knowledge(account_id="account-1")

        self.assertTrue(candidate.belongs_to_account(AccountId("account-1")))
        self.assertFalse(candidate.belongs_to_account(AccountId("account-2")))

        with self.assertRaises(KnowledgeOwnershipMismatch):
            candidate.ensure_belongs_to_account(AccountId("account-2"))

    def test_candidate_knowledge_requires_provenance(self):
        with self.assertRaises(InvalidMemorySource):
            CandidateKnowledge.create_detected(
                account_id=AccountId("account-1"),
                source_id=None,  # type: ignore[arg-type]
                knowledge_type=KnowledgeType.FACT,
                text=KnowledgeText("Meaningful candidate fact."),
                confidence_level=ConfidenceLevel.INFERRED,
                provenance_type=ProvenanceType.EXPLICITLY_STATED,
            )

        with self.assertRaises(ProvenanceRequired):
            CandidateKnowledge.create_detected(
                account_id=AccountId("account-1"),
                source_id=SourceId("source-1"),
                knowledge_type=KnowledgeType.FACT,
                text=KnowledgeText("Meaningful candidate fact."),
                confidence_level=ConfidenceLevel.INFERRED,
                provenance_type=None,  # type: ignore[arg-type]
            )

    def test_candidate_knowledge_requires_confidence(self):
        with self.assertRaises(ConfidenceRequired):
            CandidateKnowledge.create_detected(
                account_id=AccountId("account-1"),
                source_id=SourceId("source-1"),
                knowledge_type=KnowledgeType.FACT,
                text=KnowledgeText("Meaningful candidate fact."),
                confidence_level=None,  # type: ignore[arg-type]
                provenance_type=ProvenanceType.MODEL_INFERRED,
            )

    def test_candidate_knowledge_rejects_raw_dump_content(self):
        with self.assertRaises(InvalidKnowledgeContent):
            CandidateKnowledge.create_detected(
                account_id=AccountId("account-1"),
                source_id=SourceId("source-1"),
                knowledge_type=KnowledgeType.FACT,
                text=KnowledgeText("[TRANSCRIPT] full meeting dump"),
                confidence_level=ConfidenceLevel.INFERRED,
                provenance_type=ProvenanceType.MODEL_INFERRED,
            )

    def test_detected_candidate_is_not_eligible_for_acceptance_until_evaluated(self):
        candidate = make_candidate_knowledge()

        self.assertFalse(candidate.is_eligible_for_acceptance())

        with self.assertRaises(CandidateNotEligibleForAcceptance):
            candidate.accept()

    def test_evaluated_candidate_can_be_accepted_into_knowledge_item(self):
        candidate = make_candidate_knowledge(
            confidence_level=ConfidenceLevel.INFERRED,
        )
        candidate.mark_evaluated()

        knowledge = candidate.accept(actor_user_id=UserId("user-1"))

        self.assertIsInstance(knowledge, KnowledgeItem)
        self.assertIs(candidate.status, CandidateKnowledgeStatus.ACCEPTED)
        self.assertIs(knowledge.status, KnowledgeStatus.ACTIVE)
        self.assertEqual(candidate.accepted_knowledge_id.value, knowledge.id.value)
        self.assertEqual(knowledge.accepted_from_candidate_id.value, candidate.id.value)
        self.assertEqual(knowledge.primary_source_id.value, candidate.source_id.value)
        self.assertEqual(knowledge.created_by_user_id.value, "user-1")

    def test_unconfirmed_candidate_acceptance_creates_unconfirmed_knowledge(self):
        candidate = make_candidate_knowledge(
            confidence_level=ConfidenceLevel.UNCONFIRMED,
        )
        candidate.mark_evaluated()

        knowledge = candidate.accept()

        self.assertIs(knowledge.status, KnowledgeStatus.UNCONFIRMED)
        self.assertIs(knowledge.confidence_level, ConfidenceLevel.UNCONFIRMED)

    def test_contradicted_confidence_blocks_acceptance(self):
        candidate = make_candidate_knowledge(
            confidence_level=ConfidenceLevel.CONTRADICTED,
        )
        candidate.mark_evaluated()

        self.assertFalse(candidate.is_eligible_for_acceptance())

        with self.assertRaises(CandidateNotEligibleForAcceptance):
            candidate.accept()

    def test_candidate_can_be_rejected_with_reason(self):
        candidate = make_candidate_knowledge()
        candidate.reject(reason=CandidateRejectionReason.LOW_VALUE)

        self.assertIs(candidate.status, CandidateKnowledgeStatus.REJECTED)
        self.assertIs(candidate.rejection_reason, CandidateRejectionReason.LOW_VALUE)
        self.assertTrue(candidate.is_terminal())

        with self.assertRaises(CandidateAlreadyResolved):
            candidate.accept()

    def test_rejection_reasons_cover_expected_scenarios(self):
        low_value = make_candidate_knowledge()
        low_value.reject(reason=CandidateRejectionReason.LOW_VALUE)

        duplicate = make_candidate_knowledge()
        duplicate.reject(reason=CandidateRejectionReason.DUPLICATE)

        raw_dump = make_candidate_knowledge()
        raw_dump.reject(reason=CandidateRejectionReason.RAW_SOURCE_DUMP)

        self.assertIs(low_value.rejection_reason, CandidateRejectionReason.LOW_VALUE)
        self.assertIs(duplicate.rejection_reason, CandidateRejectionReason.DUPLICATE)
        self.assertIs(raw_dump.rejection_reason, CandidateRejectionReason.RAW_SOURCE_DUMP)

    def test_candidate_cannot_be_used_in_memory_context(self):
        candidate = make_candidate_knowledge()

        self.assertFalse(candidate.is_memory_context_eligible())

        with self.assertRaises(KnowledgeNotEligibleForContext):
            candidate.ensure_not_for_memory_context()

    def test_contradiction_status_blocks_acceptance_until_resolved(self):
        candidate = make_candidate_knowledge()
        candidate.flag_contradiction()

        self.assertIs(candidate.status, CandidateKnowledgeStatus.CONTRADICTION)
        self.assertFalse(candidate.is_eligible_for_acceptance())

        with self.assertRaises(CandidateNotEligibleForAcceptance):
            candidate.accept()

    def test_deferred_candidate_must_be_re_evaluated_before_acceptance(self):
        candidate = make_candidate_knowledge()
        candidate.defer()
        candidate.mark_evaluated()

        knowledge = candidate.accept()

        self.assertIs(candidate.status, CandidateKnowledgeStatus.ACCEPTED)
        self.assertIsNotNone(knowledge.id.value)

    def test_evaluated_candidate_can_be_merged_without_becoming_knowledge(self):
        candidate = make_candidate_knowledge()
        candidate.mark_evaluated()
        candidate.mark_merged(into_knowledge_id=KnowledgeId("knowledge-existing"))

        self.assertIs(candidate.status, CandidateKnowledgeStatus.MERGED)
        self.assertEqual(candidate.merged_into_knowledge_id.value, "knowledge-existing")

        with self.assertRaises(CandidateAlreadyResolved):
            candidate.accept()


if __name__ == "__main__":
    unittest.main()
