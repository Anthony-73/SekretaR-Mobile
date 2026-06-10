import unittest

from conftest import make_accepted_knowledge
from sekretar_memory.entities import (
    KnowledgeItem,
    MemoryCorrection,
    MemoryCorrectionHistory,
)
from sekretar_memory.enums import (
    ConfidenceLevel,
    CorrectionStatus,
    KnowledgeStatus,
    KnowledgeType,
    ProvenanceType,
)
from sekretar_memory.errors import (
    InvalidCorrectionTransition,
    InvalidKnowledgeContent,
    MemoryCorrectionInvalid,
    MemoryCorrectionOwnershipMismatch,
)
from sekretar_memory.value_objects import (
    AccountId,
    CorrectionId,
    CorrectionReason,
    KnowledgeId,
    KnowledgeText,
    LifecycleRecordId,
    ProvenanceId,
    SourceId,
    UserId,
)


def make_corrected_knowledge(
    *,
    original: KnowledgeItem,
    account_id: str | None = None,
    knowledge_id: str = "corrected-knowledge-1",
) -> KnowledgeItem:
    return KnowledgeItem.create_from_accepted(
        account_id=AccountId(account_id or original.account_id.value),
        knowledge_type=KnowledgeType.CORRECTION,
        text=KnowledgeText("Client A prefers detailed commercial proposals."),
        status=KnowledgeStatus.ACTIVE,
        confidence_level=ConfidenceLevel.INFERRED,
        primary_source_id=SourceId("source-correction-1"),
        primary_provenance_type=ProvenanceType.USER_CORRECTED,
        supersedes_knowledge_id=original.id,
        knowledge_id=KnowledgeId(knowledge_id),
    )


class MemoryCorrectionTests(unittest.TestCase):
    def test_proposed_correction_is_created_with_required_fields(self):
        knowledge = make_accepted_knowledge(account_id="account-1")

        correction = MemoryCorrection.propose_for_knowledge(
            knowledge=knowledge,
            reason=CorrectionReason("User corrected the proposal preference."),
            proposed_by_user_id=UserId("user-1"),
            source_id=SourceId("source-1"),
            correction_id=CorrectionId("correction-1"),
        )

        self.assertEqual(correction.id.value, "correction-1")
        self.assertEqual(correction.account_id.value, "account-1")
        self.assertEqual(correction.original_knowledge_id.value, knowledge.id.value)
        self.assertIs(correction.status, CorrectionStatus.PROPOSED)
        self.assertEqual(correction.reason.value, "User corrected the proposal preference.")
        self.assertEqual(correction.proposed_by_user_id.value, "user-1")
        self.assertEqual(correction.source_id.value, "source-1")
        self.assertIsNone(correction.corrected_knowledge_id)
        self.assertIsNotNone(correction.created_at)

    def test_accept_correction_records_allowed_transition(self):
        correction = MemoryCorrection.propose_for_knowledge(
            knowledge=make_accepted_knowledge(),
            reason=CorrectionReason("User supplied a corrected statement."),
        )

        correction.accept(accepted_by_user_id=UserId("user-1"))

        self.assertIs(correction.status, CorrectionStatus.ACCEPTED)
        self.assertEqual(correction.accepted_by_user_id.value, "user-1")

    def test_reject_correction_records_rejected_timestamp(self):
        correction = MemoryCorrection.propose_for_knowledge(
            knowledge=make_accepted_knowledge(),
            reason=CorrectionReason("Later review rejected this correction."),
        )

        correction.reject()

        self.assertIs(correction.status, CorrectionStatus.REJECTED)
        self.assertIsNotNone(correction.rejected_at)
        self.assertIsNone(correction.applied_at)

    def test_apply_accepted_correction_links_corrected_knowledge(self):
        original = make_accepted_knowledge(account_id="account-1")
        corrected = make_corrected_knowledge(original=original)
        correction = MemoryCorrection.propose_for_knowledge(
            knowledge=original,
            reason=CorrectionReason("User corrected the old preference."),
        )
        correction.accept(accepted_by_user_id=UserId("user-1"))

        correction.apply(
            corrected_knowledge=corrected,
            lifecycle_record_id=LifecycleRecordId("lifecycle-1"),
            provenance_id=ProvenanceId("provenance-1"),
        )

        self.assertIs(correction.status, CorrectionStatus.APPLIED)
        self.assertEqual(correction.corrected_knowledge_id.value, corrected.id.value)
        self.assertEqual(correction.lifecycle_record_id.value, "lifecycle-1")
        self.assertEqual(correction.provenance_id.value, "provenance-1")
        self.assertIsNotNone(correction.applied_at)

    def test_applied_correction_requires_corrected_knowledge_id(self):
        original = make_accepted_knowledge()

        with self.assertRaises(MemoryCorrectionInvalid):
            MemoryCorrection.create(
                account_id=original.account_id,
                original_knowledge_id=original.id,
                reason=CorrectionReason("Correction was already applied."),
                status=CorrectionStatus.APPLIED,
                applied_at=original.created_at,
            )

    def test_original_and_corrected_knowledge_ids_cannot_be_equal(self):
        original = make_accepted_knowledge()

        with self.assertRaises(MemoryCorrectionInvalid):
            MemoryCorrection.create(
                account_id=original.account_id,
                original_knowledge_id=original.id,
                reason=CorrectionReason("Correction cannot replace itself."),
                corrected_knowledge_id=original.id,
            )

    def test_rejected_correction_cannot_be_applied(self):
        original = make_accepted_knowledge()
        corrected = make_corrected_knowledge(original=original)
        correction = MemoryCorrection.propose_for_knowledge(
            knowledge=original,
            reason=CorrectionReason("User correction was rejected."),
        )
        correction.reject()

        with self.assertRaises(InvalidCorrectionTransition):
            correction.apply(corrected_knowledge=corrected)

    def test_applied_correction_cannot_be_rejected(self):
        original = make_accepted_knowledge()
        corrected = make_corrected_knowledge(original=original)
        correction = MemoryCorrection.propose_for_knowledge(
            knowledge=original,
            reason=CorrectionReason("User correction was accepted."),
        )
        correction.accept()
        correction.apply(corrected_knowledge=corrected)

        with self.assertRaises(InvalidCorrectionTransition):
            correction.reject()

    def test_accepted_correction_cannot_be_rejected(self):
        correction = MemoryCorrection.propose_for_knowledge(
            knowledge=make_accepted_knowledge(),
            reason=CorrectionReason("Accepted correction must apply or stay accepted."),
        )
        correction.accept()

        with self.assertRaises(InvalidCorrectionTransition):
            correction.reject()

    def test_correction_reason_cannot_be_empty_or_raw_source_content(self):
        with self.assertRaises(InvalidKnowledgeContent):
            CorrectionReason(" ")

        with self.assertRaises(InvalidKnowledgeContent):
            CorrectionReason("[TRANSCRIPT] full meeting dump")

    def test_account_mismatch_is_rejected_for_corrected_knowledge(self):
        original = make_accepted_knowledge(account_id="account-1")
        corrected = make_corrected_knowledge(
            original=original,
            account_id="account-2",
        )
        correction = MemoryCorrection.propose_for_knowledge(
            knowledge=original,
            reason=CorrectionReason("Corrected knowledge must stay in account."),
        )
        correction.accept()

        with self.assertRaises(MemoryCorrectionOwnershipMismatch):
            correction.apply(corrected_knowledge=corrected)

    def test_history_is_append_only_and_preserves_first_latest_records(self):
        knowledge = make_accepted_knowledge()
        history = MemoryCorrectionHistory.for_knowledge(knowledge)
        first = MemoryCorrection.propose_for_knowledge(
            knowledge=knowledge,
            reason=CorrectionReason("First correction proposal."),
            correction_id=CorrectionId("correction-1"),
        )
        second = MemoryCorrection.propose_for_knowledge(
            knowledge=knowledge,
            reason=CorrectionReason("Second correction proposal."),
            correction_id=CorrectionId("correction-2"),
        )

        history.append(first)
        history.append(second)

        self.assertEqual(len(history.records), 2)
        self.assertIs(history.first_record, first)
        self.assertIs(history.latest_record, second)
        self.assertIs(history.records[0], first)
        self.assertIs(history.records[1], second)
        self.assertFalse(hasattr(history, "update"))
        self.assertFalse(hasattr(history, "delete"))
        self.assertFalse(hasattr(history, "clear"))

    def test_history_rejects_correction_from_another_account(self):
        knowledge = make_accepted_knowledge(account_id="account-1")
        history = MemoryCorrectionHistory.for_knowledge(knowledge)
        foreign_correction = MemoryCorrection.create(
            account_id=AccountId("account-2"),
            original_knowledge_id=knowledge.id,
            reason=CorrectionReason("Foreign account correction."),
        )

        with self.assertRaises(MemoryCorrectionOwnershipMismatch):
            history.append(foreign_correction)

    def test_history_rejects_correction_for_another_knowledge_item(self):
        knowledge = make_accepted_knowledge()
        history = MemoryCorrectionHistory.for_knowledge(knowledge)
        foreign_correction = MemoryCorrection.create(
            account_id=knowledge.account_id,
            original_knowledge_id=KnowledgeId("foreign-knowledge"),
            reason=CorrectionReason("Foreign knowledge correction."),
        )

        with self.assertRaises(MemoryCorrectionOwnershipMismatch):
            history.append(foreign_correction)

    def test_correction_does_not_mutate_original_knowledge_item(self):
        original = make_accepted_knowledge(
            status=KnowledgeStatus.ACTIVE,
            confidence_level=ConfidenceLevel.INFERRED,
        )
        corrected = make_corrected_knowledge(original=original)
        before = (
            original.text.value,
            original.status,
            original.confidence_level,
            original.updated_at,
        )
        correction = MemoryCorrection.propose_for_knowledge(
            knowledge=original,
            reason=CorrectionReason("User corrected the original knowledge."),
        )
        correction.accept()

        correction.apply(corrected_knowledge=corrected)

        after = (
            original.text.value,
            original.status,
            original.confidence_level,
            original.updated_at,
        )
        self.assertEqual(before, after)


if __name__ == "__main__":
    unittest.main()
