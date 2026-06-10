import unittest

from sekretar_memory.entities import KnowledgeItem, KnowledgeRelation, KnowledgeRelationHistory
from sekretar_memory.enums import ConfidenceLevel, KnowledgeStatus, KnowledgeType, ProvenanceType, RelationType
from sekretar_memory.errors import (
    DuplicateKnowledgeRelation,
    InvalidKnowledgeContent,
    KnowledgeRelationInvalid,
    KnowledgeRelationOwnershipMismatch,
)
from sekretar_memory.value_objects import (
    AccountId,
    ContradictionId,
    CorrectionId,
    KnowledgeId,
    KnowledgeText,
    ProvenanceId,
    RelationId,
    RelationReason,
    SourceId,
)


def make_knowledge(
    *,
    knowledge_id: str,
    account_id: str = "account-1",
    text: str = "Knowledge item text.",
    source_id: str = "source-1",
) -> KnowledgeItem:
    return KnowledgeItem.create_from_accepted(
        account_id=AccountId(account_id),
        knowledge_type=KnowledgeType.FACT,
        text=KnowledgeText(text),
        status=KnowledgeStatus.ACTIVE,
        confidence_level=ConfidenceLevel.INFERRED,
        primary_source_id=SourceId(source_id),
        primary_provenance_type=ProvenanceType.MODEL_INFERRED,
        knowledge_id=KnowledgeId(knowledge_id),
    )


class KnowledgeRelationTests(unittest.TestCase):
    def test_replaces_relation_can_link_correction(self):
        corrected = make_knowledge(knowledge_id="knowledge-b", text="Corrected fact.")
        original = make_knowledge(knowledge_id="knowledge-a", text="Original fact.")

        relation = KnowledgeRelation.create_between(
            left_knowledge=corrected,
            right_knowledge=original,
            relation_type=RelationType.REPLACES,
            reason=RelationReason("Corrected knowledge replaces the original."),
            correction_id=CorrectionId("correction-1"),
            relation_id=RelationId("relation-1"),
        )

        self.assertEqual(relation.id.value, "relation-1")
        self.assertIs(relation.relation_type, RelationType.REPLACES)
        self.assertEqual(relation.left_knowledge_id.value, "knowledge-b")
        self.assertEqual(relation.right_knowledge_id.value, "knowledge-a")
        self.assertEqual(relation.correction_id.value, "correction-1")
        self.assertIsNone(relation.contradiction_id)

    def test_contradicts_relation_can_link_contradiction(self):
        left = make_knowledge(knowledge_id="knowledge-a")
        right = make_knowledge(knowledge_id="knowledge-b", source_id="source-2")

        relation = KnowledgeRelation.create_between(
            left_knowledge=left,
            right_knowledge=right,
            relation_type=RelationType.CONTRADICTS,
            reason=RelationReason("Both facts cannot be true as stated."),
            contradiction_id=ContradictionId("contradiction-1"),
        )

        self.assertIs(relation.relation_type, RelationType.CONTRADICTS)
        self.assertEqual(relation.left_knowledge_id.value, "knowledge-a")
        self.assertEqual(relation.right_knowledge_id.value, "knowledge-b")
        self.assertEqual(relation.contradiction_id.value, "contradiction-1")
        self.assertIsNone(relation.correction_id)

    def test_supports_relation_is_created(self):
        supporting = make_knowledge(knowledge_id="knowledge-a")
        supported = make_knowledge(knowledge_id="knowledge-b", source_id="source-2")

        relation = KnowledgeRelation.create_between(
            left_knowledge=supporting,
            right_knowledge=supported,
            relation_type=RelationType.SUPPORTS,
            reason=RelationReason("First fact supports the second fact."),
        )

        self.assertIs(relation.relation_type, RelationType.SUPPORTS)
        self.assertEqual(relation.left_knowledge_id.value, "knowledge-a")
        self.assertEqual(relation.right_knowledge_id.value, "knowledge-b")

    def test_derived_from_relation_can_link_provenance(self):
        derived = make_knowledge(knowledge_id="knowledge-a")
        source = make_knowledge(knowledge_id="knowledge-b", source_id="source-2")

        relation = KnowledgeRelation.create_between(
            left_knowledge=derived,
            right_knowledge=source,
            relation_type=RelationType.DERIVED_FROM,
            reason=RelationReason("Derived fact uses the source knowledge item."),
            provenance_id=ProvenanceId("provenance-1"),
        )

        self.assertIs(relation.relation_type, RelationType.DERIVED_FROM)
        self.assertEqual(relation.left_knowledge_id.value, "knowledge-a")
        self.assertEqual(relation.right_knowledge_id.value, "knowledge-b")
        self.assertEqual(relation.provenance_id.value, "provenance-1")

    def test_duplicates_relation_is_created_with_canonical_ordering(self):
        left = make_knowledge(knowledge_id="knowledge-z")
        right = make_knowledge(knowledge_id="knowledge-a", source_id="source-2")

        relation = KnowledgeRelation.create_between(
            left_knowledge=left,
            right_knowledge=right,
            relation_type=RelationType.DUPLICATES,
            reason=RelationReason("These knowledge items duplicate each other."),
        )

        self.assertIs(relation.relation_type, RelationType.DUPLICATES)
        self.assertEqual(relation.left_knowledge_id.value, "knowledge-a")
        self.assertEqual(relation.right_knowledge_id.value, "knowledge-z")

    def test_relation_requires_account_ownership(self):
        left = make_knowledge(knowledge_id="knowledge-a", account_id="account-1")
        right = make_knowledge(knowledge_id="knowledge-b", account_id="account-2")

        with self.assertRaises(KnowledgeRelationOwnershipMismatch):
            KnowledgeRelation.create_between(
                left_knowledge=left,
                right_knowledge=right,
                relation_type=RelationType.SUPPORTS,
                reason=RelationReason("Cross-account relation is forbidden."),
            )

    def test_relation_rejects_same_knowledge_id(self):
        with self.assertRaises(KnowledgeRelationInvalid):
            KnowledgeRelation.create(
                account_id=AccountId("account-1"),
                left_knowledge_id=KnowledgeId("knowledge-a"),
                right_knowledge_id=KnowledgeId("knowledge-a"),
                relation_type=RelationType.SUPPORTS,
                reason=RelationReason("Knowledge cannot relate to itself."),
            )

    def test_relation_reason_cannot_be_empty_or_raw_source_content(self):
        with self.assertRaises(InvalidKnowledgeContent):
            RelationReason(" ")

        with self.assertRaises(InvalidKnowledgeContent):
            RelationReason("[TRANSCRIPT] full meeting dump")

    def test_directional_relation_preserves_order(self):
        left = make_knowledge(knowledge_id="knowledge-z")
        right = make_knowledge(knowledge_id="knowledge-a", source_id="source-2")

        relation = KnowledgeRelation.create_between(
            left_knowledge=left,
            right_knowledge=right,
            relation_type=RelationType.REPLACES,
            reason=RelationReason("Directional relation preserves left to right."),
        )

        self.assertEqual(relation.left_knowledge_id.value, "knowledge-z")
        self.assertEqual(relation.right_knowledge_id.value, "knowledge-a")

    def test_duplicate_symmetric_reverse_relation_is_rejected(self):
        history = KnowledgeRelationHistory(account_id=AccountId("account-1"))
        first = KnowledgeRelation.create(
            account_id=AccountId("account-1"),
            left_knowledge_id=KnowledgeId("knowledge-a"),
            right_knowledge_id=KnowledgeId("knowledge-b"),
            relation_type=RelationType.CONTRADICTS,
            reason=RelationReason("First conflict relation."),
        )
        reverse = KnowledgeRelation.create(
            account_id=AccountId("account-1"),
            left_knowledge_id=KnowledgeId("knowledge-b"),
            right_knowledge_id=KnowledgeId("knowledge-a"),
            relation_type=RelationType.CONTRADICTS,
            reason=RelationReason("Reverse conflict relation."),
        )

        history.append(first)

        with self.assertRaises(DuplicateKnowledgeRelation):
            history.append(reverse)

    def test_relation_history_is_append_only_and_preserves_first_latest_records(self):
        history = KnowledgeRelationHistory(account_id=AccountId("account-1"))
        first = KnowledgeRelation.create(
            account_id=AccountId("account-1"),
            left_knowledge_id=KnowledgeId("knowledge-a"),
            right_knowledge_id=KnowledgeId("knowledge-b"),
            relation_type=RelationType.SUPPORTS,
            reason=RelationReason("First relation."),
        )
        second = KnowledgeRelation.create(
            account_id=AccountId("account-1"),
            left_knowledge_id=KnowledgeId("knowledge-c"),
            right_knowledge_id=KnowledgeId("knowledge-d"),
            relation_type=RelationType.DERIVED_FROM,
            reason=RelationReason("Second relation."),
        )

        history.append(first)
        history.append(second)

        self.assertEqual(len(history.records), 2)
        self.assertIs(history.first_record, first)
        self.assertIs(history.latest_record, second)
        self.assertFalse(hasattr(history, "update"))
        self.assertFalse(hasattr(history, "delete"))
        self.assertFalse(hasattr(history, "clear"))

    def test_relation_history_rejects_other_account(self):
        history = KnowledgeRelationHistory(account_id=AccountId("account-1"))
        foreign = KnowledgeRelation.create(
            account_id=AccountId("account-2"),
            left_knowledge_id=KnowledgeId("knowledge-a"),
            right_knowledge_id=KnowledgeId("knowledge-b"),
            relation_type=RelationType.SUPPORTS,
            reason=RelationReason("Foreign account relation."),
        )

        with self.assertRaises(KnowledgeRelationOwnershipMismatch):
            history.append(foreign)

    def test_relation_does_not_mutate_knowledge_item(self):
        left = make_knowledge(knowledge_id="knowledge-a")
        right = make_knowledge(knowledge_id="knowledge-b", source_id="source-2")
        before_left = (left.text.value, left.status, left.updated_at)
        before_right = (right.text.value, right.status, right.updated_at)

        KnowledgeRelation.create_between(
            left_knowledge=left,
            right_knowledge=right,
            relation_type=RelationType.SUPPORTS,
            reason=RelationReason("Relation should not mutate knowledge."),
        )

        self.assertEqual(before_left, (left.text.value, left.status, left.updated_at))
        self.assertEqual(before_right, (right.text.value, right.status, right.updated_at))

    def test_relation_does_not_create_correction_or_contradiction_automatically(self):
        left = make_knowledge(knowledge_id="knowledge-a")
        right = make_knowledge(knowledge_id="knowledge-b", source_id="source-2")

        relation = KnowledgeRelation.create_between(
            left_knowledge=left,
            right_knowledge=right,
            relation_type=RelationType.CONTRADICTS,
            reason=RelationReason("Relation edge does not create conflict record."),
        )

        self.assertIsNone(relation.correction_id)
        self.assertIsNone(relation.contradiction_id)

    def test_related_to_is_not_implemented_in_phase1(self):
        self.assertFalse(hasattr(RelationType, "RELATED_TO"))


if __name__ == "__main__":
    unittest.main()
