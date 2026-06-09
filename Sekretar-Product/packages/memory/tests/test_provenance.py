import unittest
from dataclasses import FrozenInstanceError

from conftest import make_accepted_knowledge, make_candidate_knowledge
from sekretar_memory.entities import (
    KnowledgeItem,
    KnowledgeProvenance,
    KnowledgeProvenanceHistory,
)
from sekretar_memory.enums import (
    ConfidenceLevel,
    KnowledgeStatus,
    KnowledgeType,
    ProvenanceEventType,
    ProvenanceType,
)
from sekretar_memory.errors import (
    InvalidKnowledgeContent,
    KnowledgeOwnershipMismatch,
    MemorySourceLinkMismatch,
    ProvenanceRecordInvalid,
    ProvenanceRecordOwnershipMismatch,
    ProvenanceRequired,
)
from sekretar_memory.value_objects import (
    AccountId,
    CandidateKnowledgeId,
    KnowledgeId,
    KnowledgeText,
    LifecycleRecordId,
    ProvenanceId,
    ProvenanceNote,
    SourceId,
    UserId,
)


class ProvenanceSnapshotTests(unittest.TestCase):
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


class KnowledgeProvenanceTests(unittest.TestCase):
    def test_provenance_record_is_created_with_required_fields(self):
        record = KnowledgeProvenance.create(
            knowledge_id=KnowledgeId("knowledge-1"),
            account_id=AccountId("account-1"),
            event_type=ProvenanceEventType.ORIGIN_ACCEPTED,
            provenance_type=ProvenanceType.MODEL_INFERRED,
            source_id=SourceId("source-1"),
            actor_user_id=UserId("user-1"),
            note=ProvenanceNote("Inferred from June planning meeting."),
            accepted_from_candidate_id=CandidateKnowledgeId("candidate-1"),
            related_lifecycle_record_id=LifecycleRecordId("lifecycle-1"),
        )

        self.assertEqual(record.knowledge_id.value, "knowledge-1")
        self.assertEqual(record.account_id.value, "account-1")
        self.assertIs(record.event_type, ProvenanceEventType.ORIGIN_ACCEPTED)
        self.assertIs(record.provenance_type, ProvenanceType.MODEL_INFERRED)
        self.assertEqual(record.source_id.value, "source-1")
        self.assertEqual(record.actor_user_id.value, "user-1")
        self.assertEqual(record.note.value, "Inferred from June planning meeting.")
        self.assertEqual(record.accepted_from_candidate_id.value, "candidate-1")
        self.assertEqual(record.related_lifecycle_record_id.value, "lifecycle-1")
        self.assertIsNotNone(record.id.value)
        self.assertIsNotNone(record.created_at)

    def test_provenance_record_rejects_missing_identity_fields(self):
        with self.assertRaises(ProvenanceRecordInvalid):
            KnowledgeProvenance.create(
                knowledge_id=None,  # type: ignore[arg-type]
                account_id=AccountId("account-1"),
                event_type=ProvenanceEventType.ORIGIN_ACCEPTED,
                provenance_type=ProvenanceType.MODEL_INFERRED,
                source_id=SourceId("source-1"),
            )

        with self.assertRaises(ProvenanceRecordInvalid):
            KnowledgeProvenance.create(
                knowledge_id=KnowledgeId("knowledge-1"),
                account_id=None,  # type: ignore[arg-type]
                event_type=ProvenanceEventType.ORIGIN_ACCEPTED,
                provenance_type=ProvenanceType.MODEL_INFERRED,
                source_id=SourceId("source-1"),
            )

    def test_provenance_record_rejects_missing_origin_fields(self):
        with self.assertRaises(ProvenanceRecordInvalid):
            KnowledgeProvenance.create(
                knowledge_id=KnowledgeId("knowledge-1"),
                account_id=AccountId("account-1"),
                event_type=ProvenanceEventType.ORIGIN_ACCEPTED,
                provenance_type=ProvenanceType.MODEL_INFERRED,
                source_id=None,  # type: ignore[arg-type]
            )

        with self.assertRaises(ProvenanceRecordInvalid):
            KnowledgeProvenance.create(
                knowledge_id=KnowledgeId("knowledge-1"),
                account_id=AccountId("account-1"),
                event_type=ProvenanceEventType.ORIGIN_ACCEPTED,
                provenance_type=None,  # type: ignore[arg-type]
                source_id=SourceId("source-1"),
            )

    def test_provenance_record_is_immutable(self):
        record = KnowledgeProvenance.create(
            knowledge_id=KnowledgeId("knowledge-1"),
            account_id=AccountId("account-1"),
            event_type=ProvenanceEventType.ORIGIN_ACCEPTED,
            provenance_type=ProvenanceType.MODEL_INFERRED,
            source_id=SourceId("source-1"),
        )

        with self.assertRaises(FrozenInstanceError):
            record.event_type = ProvenanceEventType.CORRECTION_RECORDED  # type: ignore[misc]

    def test_origin_accepted_record_matches_knowledge_snapshot(self):
        knowledge = make_accepted_knowledge(
            account_id="account-1",
            source_id="source-meeting-1",
            provenance_type=ProvenanceType.MODEL_INFERRED,
        )

        record = KnowledgeProvenance.create_origin_accepted(
            knowledge=knowledge,
            actor_user_id=UserId("user-1"),
            note=ProvenanceNote("Accepted from meeting inference."),
        )

        self.assertIs(record.event_type, ProvenanceEventType.ORIGIN_ACCEPTED)
        self.assertEqual(record.knowledge_id.value, knowledge.id.value)
        self.assertEqual(record.account_id.value, knowledge.account_id.value)
        self.assertEqual(record.source_id.value, knowledge.primary_source_id.value)
        self.assertIs(record.provenance_type, knowledge.primary_provenance_type)
        self.assertEqual(record.actor_user_id.value, "user-1")
        self.assertEqual(record.note.value, "Accepted from meeting inference.")

    def test_origin_accepted_from_candidate_preserves_candidate_link(self):
        candidate = make_candidate_knowledge(
            account_id="account-1",
            source_id="source-meeting-1",
            provenance_type=ProvenanceType.EXPLICITLY_STATED,
        )
        candidate.mark_evaluated()
        knowledge = candidate.accept(actor_user_id=UserId("user-1"))

        record = KnowledgeProvenance.create_from_candidate_acceptance(
            knowledge=knowledge,
            candidate=candidate,
        )

        self.assertIs(record.event_type, ProvenanceEventType.ORIGIN_ACCEPTED)
        self.assertEqual(record.accepted_from_candidate_id.value, candidate.id.value)
        self.assertEqual(record.source_id.value, candidate.source_id.value)
        self.assertIs(record.provenance_type, candidate.provenance_type)
        self.assertEqual(record.observed_at, candidate.created_at)

    def test_origin_accepted_from_candidate_rejects_account_mismatch(self):
        candidate = make_candidate_knowledge(account_id="account-1")
        candidate.mark_evaluated()
        knowledge = candidate.accept()
        knowledge = KnowledgeItem.create_from_accepted(
            account_id=AccountId("account-2"),
            knowledge_type=knowledge.knowledge_type,
            text=knowledge.text,
            status=knowledge.status,
            confidence_level=knowledge.confidence_level,
            primary_source_id=knowledge.primary_source_id,
            primary_provenance_type=knowledge.primary_provenance_type,
            knowledge_id=knowledge.id,
        )

        with self.assertRaises(KnowledgeOwnershipMismatch):
            KnowledgeProvenance.create_from_candidate_acceptance(
                knowledge=knowledge,
                candidate=candidate,
            )

    def test_origin_accepted_from_candidate_rejects_source_mismatch(self):
        candidate = make_candidate_knowledge(source_id="source-1")
        candidate.mark_evaluated()
        knowledge = candidate.accept()
        knowledge = KnowledgeItem.create_from_accepted(
            account_id=knowledge.account_id,
            knowledge_type=knowledge.knowledge_type,
            text=knowledge.text,
            status=knowledge.status,
            confidence_level=knowledge.confidence_level,
            primary_source_id=SourceId("source-2"),
            primary_provenance_type=knowledge.primary_provenance_type,
            knowledge_id=knowledge.id,
        )

        with self.assertRaises(MemorySourceLinkMismatch):
            KnowledgeProvenance.create_from_candidate_acceptance(
                knowledge=knowledge,
                candidate=candidate,
            )

    def test_correction_and_reconfirmation_records_extend_origin_history(self):
        knowledge = make_accepted_knowledge()
        lifecycle_record_id = LifecycleRecordId("lifecycle-confirm-1")

        correction = KnowledgeProvenance.create_correction_record(
            knowledge=knowledge,
            source_id=SourceId("assistant-source-1"),
            actor_user_id=UserId("user-1"),
            note=ProvenanceNote("User corrected during Assistant interaction."),
            related_lifecycle_record_id=lifecycle_record_id,
        )
        reconfirmation = KnowledgeProvenance.create_reconfirmation_record(
            knowledge=knowledge,
            actor_user_id=UserId("user-1"),
            note=ProvenanceNote("User reconfirmed the corrected fact."),
            related_lifecycle_record_id=lifecycle_record_id,
        )

        self.assertIs(correction.event_type, ProvenanceEventType.CORRECTION_RECORDED)
        self.assertIs(correction.provenance_type, ProvenanceType.USER_CORRECTED)
        self.assertEqual(correction.source_id.value, "assistant-source-1")
        self.assertEqual(correction.related_lifecycle_record_id.value, "lifecycle-confirm-1")

        self.assertIs(
            reconfirmation.event_type,
            ProvenanceEventType.RECONFIRMATION_RECORDED,
        )
        self.assertIs(reconfirmation.provenance_type, ProvenanceType.EXPLICITLY_STATED)
        self.assertEqual(
            reconfirmation.source_id.value,
            knowledge.primary_source_id.value,
        )

    def test_provenance_does_not_mutate_knowledge_item(self):
        knowledge = make_accepted_knowledge(
            status=KnowledgeStatus.ACTIVE,
            confidence_level=ConfidenceLevel.INFERRED,
        )
        before = (
            knowledge.status,
            knowledge.confidence_level,
            knowledge.primary_source_id.value,
            knowledge.primary_provenance_type,
            knowledge.updated_at,
        )

        KnowledgeProvenance.create_origin_accepted(knowledge=knowledge)
        KnowledgeProvenance.create_correction_record(
            knowledge=knowledge,
            source_id=SourceId("assistant-source-1"),
        )

        after = (
            knowledge.status,
            knowledge.confidence_level,
            knowledge.primary_source_id.value,
            knowledge.primary_provenance_type,
            knowledge.updated_at,
        )
        self.assertEqual(before, after)

    def test_provenance_history_supports_append_only_semantics(self):
        knowledge = make_accepted_knowledge()
        history = KnowledgeProvenanceHistory.for_knowledge(knowledge)

        origin = KnowledgeProvenance.create_origin_accepted(knowledge=knowledge)
        correction = KnowledgeProvenance.create_correction_record(
            knowledge=knowledge,
            source_id=SourceId("assistant-source-1"),
        )

        history.append(origin)
        history.append(correction)

        self.assertEqual(len(history.records), 2)
        self.assertIs(history.first_record, origin)
        self.assertIs(history.latest_record, correction)
        self.assertIs(history.records[0], origin)
        self.assertIs(history.records[1], correction)
        self.assertFalse(hasattr(history, "update"))
        self.assertFalse(hasattr(history, "delete"))
        self.assertFalse(hasattr(history, "clear"))

    def test_provenance_history_rejects_ownership_mismatch(self):
        knowledge = make_accepted_knowledge(account_id="account-1")
        history = KnowledgeProvenanceHistory.for_knowledge(knowledge)
        foreign_record = KnowledgeProvenance.create(
            knowledge_id=knowledge.id,
            account_id=AccountId("account-2"),
            event_type=ProvenanceEventType.ORIGIN_ACCEPTED,
            provenance_type=ProvenanceType.MODEL_INFERRED,
            source_id=SourceId("source-1"),
        )

        with self.assertRaises(ProvenanceRecordOwnershipMismatch):
            history.append(foreign_record)

    def test_provenance_history_rejects_foreign_knowledge_id(self):
        knowledge = make_accepted_knowledge()
        history = KnowledgeProvenanceHistory.for_knowledge(knowledge)
        foreign_record = KnowledgeProvenance.create(
            knowledge_id=KnowledgeId("foreign-knowledge"),
            account_id=knowledge.account_id,
            event_type=ProvenanceEventType.ORIGIN_ACCEPTED,
            provenance_type=ProvenanceType.MODEL_INFERRED,
            source_id=SourceId("source-1"),
        )

        with self.assertRaises(ProvenanceRecordOwnershipMismatch):
            history.append(foreign_record)

    def test_provenance_record_belongs_to_account_and_knowledge(self):
        record = KnowledgeProvenance.create(
            knowledge_id=KnowledgeId("knowledge-1"),
            account_id=AccountId("account-1"),
            event_type=ProvenanceEventType.ORIGIN_ACCEPTED,
            provenance_type=ProvenanceType.MODEL_INFERRED,
            source_id=SourceId("source-1"),
            provenance_id=ProvenanceId("provenance-1"),
        )

        self.assertTrue(record.belongs_to_account(AccountId("account-1")))
        self.assertFalse(record.belongs_to_account(AccountId("account-2")))
        self.assertTrue(record.belongs_to_knowledge(KnowledgeId("knowledge-1")))
        self.assertFalse(record.belongs_to_knowledge(KnowledgeId("knowledge-2")))


if __name__ == "__main__":
    unittest.main()
