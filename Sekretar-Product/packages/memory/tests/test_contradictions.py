import unittest

from conftest import make_accepted_knowledge
from sekretar_memory.entities import (
    MemoryContradiction,
    MemoryContradictionHistory,
    MemoryCorrection,
)
from sekretar_memory.enums import ContradictionStatus
from sekretar_memory.errors import (
    InvalidContradictionTransition,
    InvalidKnowledgeContent,
    MemoryContradictionInvalid,
    MemoryContradictionOwnershipMismatch,
)
from sekretar_memory.value_objects import (
    AccountId,
    ContradictionId,
    ContradictionReason,
    CorrectionReason,
    KnowledgeId,
    ProvenanceId,
    SourceId,
)


class MemoryContradictionTests(unittest.TestCase):
    def test_contradiction_is_created_between_two_knowledge_items(self):
        left = make_accepted_knowledge(
            account_id="account-1",
            text="Ivan leads the project.",
        )
        right = make_accepted_knowledge(
            account_id="account-1",
            text="Sergey leads the project.",
            source_id="source-2",
        )

        contradiction = MemoryContradiction.detect_between(
            left_knowledge=left,
            right_knowledge=right,
            reason=ContradictionReason("Both people cannot lead the same project as stated."),
            contradiction_id=ContradictionId("contradiction-1"),
            source_id=SourceId("source-2"),
            provenance_id=ProvenanceId("provenance-1"),
        )

        self.assertEqual(contradiction.id.value, "contradiction-1")
        self.assertEqual(contradiction.account_id.value, "account-1")
        self.assertEqual(contradiction.left_knowledge_id.value, left.id.value)
        self.assertEqual(contradiction.right_knowledge_id.value, right.id.value)
        self.assertIs(contradiction.status, ContradictionStatus.DETECTED)
        self.assertEqual(
            contradiction.reason.value,
            "Both people cannot lead the same project as stated.",
        )
        self.assertEqual(contradiction.source_id.value, "source-2")
        self.assertEqual(contradiction.provenance_id.value, "provenance-1")
        self.assertIsNone(contradiction.resolution_correction_id)
        self.assertIsNotNone(contradiction.created_at)

    def test_contradiction_requires_same_account_for_knowledge_items(self):
        left = make_accepted_knowledge(account_id="account-1")
        right = make_accepted_knowledge(account_id="account-2", source_id="source-2")

        with self.assertRaises(MemoryContradictionOwnershipMismatch):
            MemoryContradiction.detect_between(
                left_knowledge=left,
                right_knowledge=right,
                reason=ContradictionReason("Accounts must not be mixed."),
            )

    def test_contradiction_rejects_same_knowledge_id(self):
        knowledge = make_accepted_knowledge()

        with self.assertRaises(MemoryContradictionInvalid):
            MemoryContradiction.create(
                account_id=knowledge.account_id,
                left_knowledge_id=knowledge.id,
                right_knowledge_id=knowledge.id,
                reason=ContradictionReason("Knowledge cannot contradict itself."),
            )

    def test_contradiction_reason_cannot_be_empty_or_raw_source_content(self):
        with self.assertRaises(InvalidKnowledgeContent):
            ContradictionReason(" ")

        with self.assertRaises(InvalidKnowledgeContent):
            ContradictionReason("[TRANSCRIPT] full meeting dump")

    def test_status_transitions_follow_allowed_path_to_resolved(self):
        contradiction = MemoryContradiction.detect_between(
            left_knowledge=make_accepted_knowledge(),
            right_knowledge=make_accepted_knowledge(source_id="source-2"),
            reason=ContradictionReason("Two facts conflict."),
        )

        contradiction.mark_reviewed()
        contradiction.resolve()

        self.assertIs(contradiction.status, ContradictionStatus.RESOLVED)
        self.assertIsNotNone(contradiction.resolved_at)

    def test_status_transitions_follow_allowed_path_to_dismissed(self):
        contradiction = MemoryContradiction.detect_between(
            left_knowledge=make_accepted_knowledge(),
            right_knowledge=make_accepted_knowledge(source_id="source-2"),
            reason=ContradictionReason("Conflict was reviewed as noise."),
        )

        contradiction.mark_reviewed()
        contradiction.dismiss()

        self.assertIs(contradiction.status, ContradictionStatus.DISMISSED)
        self.assertIsNotNone(contradiction.dismissed_at)

    def test_resolved_contradiction_requires_resolved_at(self):
        left = make_accepted_knowledge()
        right = make_accepted_knowledge(source_id="source-2")

        with self.assertRaises(MemoryContradictionInvalid):
            MemoryContradiction.create(
                account_id=left.account_id,
                left_knowledge_id=left.id,
                right_knowledge_id=right.id,
                reason=ContradictionReason("Resolved contradiction needs timestamp."),
                status=ContradictionStatus.RESOLVED,
            )

    def test_dismissed_contradiction_requires_dismissed_at(self):
        left = make_accepted_knowledge()
        right = make_accepted_knowledge(source_id="source-2")

        with self.assertRaises(MemoryContradictionInvalid):
            MemoryContradiction.create(
                account_id=left.account_id,
                left_knowledge_id=left.id,
                right_knowledge_id=right.id,
                reason=ContradictionReason("Dismissed contradiction needs timestamp."),
                status=ContradictionStatus.DISMISSED,
            )

    def test_backward_or_skipped_transitions_are_forbidden(self):
        contradiction = MemoryContradiction.detect_between(
            left_knowledge=make_accepted_knowledge(),
            right_knowledge=make_accepted_knowledge(source_id="source-2"),
            reason=ContradictionReason("Conflict must be reviewed before resolution."),
        )

        with self.assertRaises(InvalidContradictionTransition):
            contradiction.resolve()

        contradiction.mark_reviewed()
        contradiction.resolve()

        with self.assertRaises(InvalidContradictionTransition):
            contradiction.mark_reviewed()

        with self.assertRaises(InvalidContradictionTransition):
            contradiction.dismiss()

    def test_contradiction_history_is_append_only(self):
        account_id = AccountId("account-1")
        history = MemoryContradictionHistory(account_id=account_id)
        first = MemoryContradiction.create(
            account_id=account_id,
            left_knowledge_id=KnowledgeId("knowledge-1"),
            right_knowledge_id=KnowledgeId("knowledge-2"),
            reason=ContradictionReason("First contradiction."),
            contradiction_id=ContradictionId("contradiction-1"),
        )
        second = MemoryContradiction.create(
            account_id=account_id,
            left_knowledge_id=KnowledgeId("knowledge-3"),
            right_knowledge_id=KnowledgeId("knowledge-4"),
            reason=ContradictionReason("Second contradiction."),
            contradiction_id=ContradictionId("contradiction-2"),
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

    def test_contradiction_history_rejects_other_account(self):
        history = MemoryContradictionHistory(account_id=AccountId("account-1"))
        foreign = MemoryContradiction.create(
            account_id=AccountId("account-2"),
            left_knowledge_id=KnowledgeId("knowledge-1"),
            right_knowledge_id=KnowledgeId("knowledge-2"),
            reason=ContradictionReason("Foreign account contradiction."),
        )

        with self.assertRaises(MemoryContradictionOwnershipMismatch):
            history.append(foreign)

    def test_contradiction_does_not_mutate_knowledge_item(self):
        left = make_accepted_knowledge(text="Meeting starts at 09:00.")
        right = make_accepted_knowledge(
            text="Meeting starts at 10:00.",
            source_id="source-2",
        )
        before_left = (left.text.value, left.status, left.updated_at)
        before_right = (right.text.value, right.status, right.updated_at)

        contradiction = MemoryContradiction.detect_between(
            left_knowledge=left,
            right_knowledge=right,
            reason=ContradictionReason("Meeting cannot start at both times."),
        )
        contradiction.mark_reviewed()
        contradiction.dismiss()

        self.assertEqual(before_left, (left.text.value, left.status, left.updated_at))
        self.assertEqual(before_right, (right.text.value, right.status, right.updated_at))

    def test_contradiction_does_not_create_correction_automatically(self):
        contradiction = MemoryContradiction.detect_between(
            left_knowledge=make_accepted_knowledge(),
            right_knowledge=make_accepted_knowledge(source_id="source-2"),
            reason=ContradictionReason("Contradiction is not a correction."),
        )
        contradiction.mark_reviewed()
        contradiction.resolve()

        self.assertIsNone(contradiction.resolution_correction_id)

    def test_contradiction_can_reference_correction_after_resolution(self):
        left = make_accepted_knowledge()
        right = make_accepted_knowledge(source_id="source-2")
        correction = MemoryCorrection.propose_for_knowledge(
            knowledge=left,
            reason=CorrectionReason("Left knowledge was corrected after conflict."),
        )
        contradiction = MemoryContradiction.detect_between(
            left_knowledge=left,
            right_knowledge=right,
            reason=ContradictionReason("Conflict resolved by correcting left side."),
        )

        contradiction.mark_reviewed()
        contradiction.resolve(resolution_correction=correction)

        self.assertIs(contradiction.status, ContradictionStatus.RESOLVED)
        self.assertEqual(
            contradiction.resolution_correction_id.value,
            correction.id.value,
        )

    def test_resolution_correction_must_belong_to_contradiction_account(self):
        left = make_accepted_knowledge(account_id="account-1")
        right = make_accepted_knowledge(account_id="account-1", source_id="source-2")
        foreign = make_accepted_knowledge(account_id="account-2", source_id="source-3")
        correction = MemoryCorrection.propose_for_knowledge(
            knowledge=foreign,
            reason=CorrectionReason("Foreign correction must not resolve conflict."),
        )
        contradiction = MemoryContradiction.detect_between(
            left_knowledge=left,
            right_knowledge=right,
            reason=ContradictionReason("Conflict cannot resolve from another account."),
        )
        contradiction.mark_reviewed()

        with self.assertRaises(MemoryContradictionOwnershipMismatch):
            contradiction.resolve(resolution_correction=correction)


if __name__ == "__main__":
    unittest.main()
