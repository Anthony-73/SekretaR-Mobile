import unittest
from dataclasses import FrozenInstanceError

from conftest import make_accepted_knowledge
from sekretar_memory.entities import KnowledgeLifecycleHistory, KnowledgeLifecycleRecord
from sekretar_memory.enums import ConfidenceLevel, KnowledgeStatus
from sekretar_memory.errors import (
    KnowledgeImmutable,
    LifecycleRecordInvalid,
    LifecycleRecordOwnershipMismatch,
)
from sekretar_memory.value_objects import (
    AccountId,
    KnowledgeId,
    LifecycleReason,
    LifecycleRecordId,
    ProvenanceId,
    SourceId,
    UserId,
)


class KnowledgeLifecycleRecordTests(unittest.TestCase):
    def test_lifecycle_record_is_created_with_required_fields(self):
        record = KnowledgeLifecycleRecord.create(
            knowledge_id=KnowledgeId("knowledge-1"),
            account_id=AccountId("account-1"),
            previous_status=KnowledgeStatus.ACTIVE,
            new_status=KnowledgeStatus.CONFIRMED,
            reason=LifecycleReason("user_confirmed"),
            actor_user_id=UserId("user-1"),
            source_id=SourceId("source-1"),
            provenance_id=ProvenanceId("provenance-1"),
        )

        self.assertEqual(record.knowledge_id.value, "knowledge-1")
        self.assertEqual(record.account_id.value, "account-1")
        self.assertIs(record.previous_status, KnowledgeStatus.ACTIVE)
        self.assertIs(record.new_status, KnowledgeStatus.CONFIRMED)
        self.assertEqual(record.reason.value, "user_confirmed")
        self.assertEqual(record.actor_user_id.value, "user-1")
        self.assertEqual(record.source_id.value, "source-1")
        self.assertEqual(record.provenance_id.value, "provenance-1")
        self.assertIsNotNone(record.id.value)
        self.assertIsNotNone(record.created_at)

    def test_lifecycle_record_rejects_missing_identity_fields(self):
        with self.assertRaises(LifecycleRecordInvalid):
            KnowledgeLifecycleRecord.create(
                knowledge_id=None,  # type: ignore[arg-type]
                account_id=AccountId("account-1"),
                previous_status=KnowledgeStatus.ACTIVE,
                new_status=KnowledgeStatus.CONFIRMED,
                reason=LifecycleReason("user_confirmed"),
            )

        with self.assertRaises(LifecycleRecordInvalid):
            KnowledgeLifecycleRecord.create(
                knowledge_id=KnowledgeId("knowledge-1"),
                account_id=None,  # type: ignore[arg-type]
                previous_status=KnowledgeStatus.ACTIVE,
                new_status=KnowledgeStatus.CONFIRMED,
                reason=LifecycleReason("user_confirmed"),
            )

    def test_lifecycle_record_is_append_only_at_entity_level(self):
        record = KnowledgeLifecycleRecord.create(
            knowledge_id=KnowledgeId("knowledge-1"),
            account_id=AccountId("account-1"),
            previous_status=KnowledgeStatus.ACTIVE,
            new_status=KnowledgeStatus.CONFIRMED,
            reason=LifecycleReason("user_confirmed"),
        )

        with self.assertRaises(FrozenInstanceError):
            record.new_status = KnowledgeStatus.OUTDATED  # type: ignore[misc]

    def test_lifecycle_history_supports_append_only_semantics(self):
        history = KnowledgeLifecycleHistory(
            knowledge_id=KnowledgeId("knowledge-1"),
            account_id=AccountId("account-1"),
        )
        first = KnowledgeLifecycleRecord.create(
            knowledge_id=KnowledgeId("knowledge-1"),
            account_id=AccountId("account-1"),
            previous_status=KnowledgeStatus.ACTIVE,
            new_status=KnowledgeStatus.CONFIRMED,
            reason=LifecycleReason("user_confirmed"),
        )
        second = KnowledgeLifecycleRecord.create(
            knowledge_id=KnowledgeId("knowledge-1"),
            account_id=AccountId("account-1"),
            previous_status=KnowledgeStatus.CONFIRMED,
            new_status=KnowledgeStatus.OUTDATED,
            reason=LifecycleReason("context_changed"),
        )

        history.append(first)
        history.append(second)

        self.assertEqual(len(history.records), 2)
        self.assertIs(history.records[0], first)
        self.assertIs(history.records[1], second)
        self.assertFalse(hasattr(history, "update"))
        self.assertFalse(hasattr(history, "delete"))
        self.assertFalse(hasattr(history, "clear"))

    def test_transition_active_to_confirmed_records_lifecycle(self):
        knowledge = make_accepted_knowledge(
            account_id="account-1",
            status=KnowledgeStatus.ACTIVE,
            confidence_level=ConfidenceLevel.INFERRED,
        )
        history = KnowledgeLifecycleHistory(
            knowledge_id=knowledge.id,
            account_id=knowledge.account_id,
        )

        record = knowledge.transition_status(
            KnowledgeStatus.CONFIRMED,
            confidence_level=ConfidenceLevel.CONFIRMED,
            reason=LifecycleReason("user_confirmed"),
            actor_user_id=UserId("user-1"),
        )
        history.append(record)

        self.assertIs(knowledge.status, KnowledgeStatus.CONFIRMED)
        self.assertIs(record.previous_status, KnowledgeStatus.ACTIVE)
        self.assertIs(record.new_status, KnowledgeStatus.CONFIRMED)
        self.assertEqual(record.knowledge_id.value, knowledge.id.value)
        self.assertEqual(record.account_id.value, knowledge.account_id.value)
        self.assertEqual(record.reason.value, "user_confirmed")
        self.assertEqual(len(history.records), 1)

    def test_transition_confirmed_to_outdated_records_lifecycle(self):
        knowledge = make_accepted_knowledge(
            status=KnowledgeStatus.ACTIVE,
            confidence_level=ConfidenceLevel.INFERRED,
        )
        knowledge.transition_status(
            KnowledgeStatus.CONFIRMED,
            confidence_level=ConfidenceLevel.CONFIRMED,
            reason=LifecycleReason("user_confirmed"),
        )

        record = knowledge.transition_status(
            KnowledgeStatus.OUTDATED,
            reason=LifecycleReason("context_changed"),
        )

        self.assertIs(knowledge.status, KnowledgeStatus.OUTDATED)
        self.assertIs(record.previous_status, KnowledgeStatus.CONFIRMED)
        self.assertIs(record.new_status, KnowledgeStatus.OUTDATED)
        self.assertEqual(record.reason.value, "context_changed")

    def test_terminal_transition_records_history_then_blocks_further_records(self):
        knowledge = make_accepted_knowledge(
            status=KnowledgeStatus.ACTIVE,
            confidence_level=ConfidenceLevel.CONFIRMED,
        )
        knowledge.transition_status(
            KnowledgeStatus.CONFIRMED,
            confidence_level=ConfidenceLevel.CONFIRMED,
        )
        history = KnowledgeLifecycleHistory(
            knowledge_id=knowledge.id,
            account_id=knowledge.account_id,
        )

        archived_record = knowledge.transition_status(
            KnowledgeStatus.ARCHIVED,
            reason=LifecycleReason("manual_archive"),
        )
        history.append(archived_record)

        self.assertTrue(knowledge.is_terminal())
        self.assertEqual(len(history.records), 1)

        with self.assertRaises(KnowledgeImmutable):
            knowledge.transition_status(
                KnowledgeStatus.DELETED,
                reason=LifecycleReason("should_not_apply"),
            )

        self.assertEqual(len(history.records), 1)

    def test_lifecycle_history_rejects_ownership_mismatch(self):
        knowledge = make_accepted_knowledge(account_id="account-1")
        history = KnowledgeLifecycleHistory(
            knowledge_id=knowledge.id,
            account_id=knowledge.account_id,
        )
        foreign_record = KnowledgeLifecycleRecord.create(
            knowledge_id=knowledge.id,
            account_id=AccountId("account-2"),
            previous_status=KnowledgeStatus.ACTIVE,
            new_status=KnowledgeStatus.CONFIRMED,
            reason=LifecycleReason("foreign_account"),
        )

        with self.assertRaises(LifecycleRecordOwnershipMismatch):
            history.append(foreign_record)

    def test_lifecycle_record_rejects_no_op_transition(self):
        with self.assertRaises(LifecycleRecordInvalid):
            KnowledgeLifecycleRecord.create(
                knowledge_id=KnowledgeId("knowledge-1"),
                account_id=AccountId("account-1"),
                previous_status=KnowledgeStatus.ACTIVE,
                new_status=KnowledgeStatus.ACTIVE,
                reason=LifecycleReason("noop"),
            )


if __name__ == "__main__":
    unittest.main()
