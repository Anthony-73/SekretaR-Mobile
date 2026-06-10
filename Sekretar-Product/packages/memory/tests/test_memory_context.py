import unittest
from dataclasses import FrozenInstanceError

from conftest import make_accepted_knowledge, make_candidate_knowledge
from sekretar_memory.entities import MemoryContext, MemoryContextItem
from sekretar_memory.enums import (
    ConfidenceLevel,
    KnowledgeStatus,
    MemoryContextPurpose,
)
from sekretar_memory.errors import MemoryContextInvalid, MemoryContextOwnershipMismatch
from sekretar_memory.value_objects import (
    AccountId,
    KnowledgeId,
    LifecycleReason,
    MemoryContextReason,
    ProvenanceId,
)


class MemoryContextTests(unittest.TestCase):
    def test_create_empty_context(self):
        context = MemoryContext.create(
            account_id=AccountId("account-1"),
            purpose=MemoryContextPurpose.MEMORY_REVIEW,
            strict=True,
        )

        self.assertEqual(context.account_id.value, "account-1")
        self.assertIs(context.purpose, MemoryContextPurpose.MEMORY_REVIEW)
        self.assertTrue(context.strict)
        self.assertEqual(context.items, ())
        self.assertTrue(context.is_empty())
        self.assertIsNotNone(context.created_at)

    def test_include_active_and_confirmed_eligible_knowledge(self):
        active = make_accepted_knowledge(
            account_id="account-1",
            source_id="source-active",
        )
        confirmed = make_accepted_knowledge(
            account_id="account-1",
            source_id="source-confirmed",
        )
        confirmed.transition_status(
            KnowledgeStatus.CONFIRMED,
            confidence_level=ConfidenceLevel.CONFIRMED,
            reason=LifecycleReason("user_confirmed"),
        )

        context = MemoryContext.create_from_knowledge_items(
            account_id=AccountId("account-1"),
            purpose=MemoryContextPurpose.ASSISTANT_RESPONSE,
            knowledge_items=[active, confirmed],
            strict=True,
        )

        self.assertEqual(len(context.items), 2)
        self.assertEqual(
            {item.knowledge_id.value for item in context.items},
            {active.id.value, confirmed.id.value},
        )
        self.assertFalse(context.is_empty())

    def test_exclude_terminal_deleted_forgotten_archived_knowledge(self):
        archived = make_accepted_knowledge(account_id="account-1", source_id="source-a")
        deleted = make_accepted_knowledge(account_id="account-1", source_id="source-d")
        forgotten = make_accepted_knowledge(account_id="account-1", source_id="source-f")
        archived.transition_status(KnowledgeStatus.ARCHIVED)
        deleted.transition_status(KnowledgeStatus.DELETED)
        forgotten.transition_status(KnowledgeStatus.FORGOTTEN)

        context = MemoryContext.create_from_knowledge_items(
            account_id=AccountId("account-1"),
            purpose=MemoryContextPurpose.MEMORY_REVIEW,
            knowledge_items=[archived, deleted, forgotten],
        )

        self.assertEqual(context.items, ())

    def test_exclude_outdated_contradicted_and_corrected_knowledge(self):
        outdated = make_accepted_knowledge(account_id="account-1", source_id="source-o")
        contradicted = make_accepted_knowledge(account_id="account-1", source_id="source-c")
        corrected = make_accepted_knowledge(account_id="account-1", source_id="source-r")
        outdated.transition_status(KnowledgeStatus.OUTDATED)
        contradicted.transition_status(
            KnowledgeStatus.CONTRADICTED,
            confidence_level=ConfidenceLevel.CONTRADICTED,
        )
        corrected.transition_status(KnowledgeStatus.CORRECTED)

        context = MemoryContext.create_from_knowledge_items(
            account_id=AccountId("account-1"),
            purpose=MemoryContextPurpose.MEMORY_REVIEW,
            knowledge_items=[outdated, contradicted, corrected],
        )

        self.assertEqual(context.items, ())

    def test_strict_mode_excludes_unconfirmed_and_doubtful_knowledge(self):
        unconfirmed = make_accepted_knowledge(
            account_id="account-1",
            status=KnowledgeStatus.UNCONFIRMED,
            confidence_level=ConfidenceLevel.UNCONFIRMED,
        )
        doubtful = make_accepted_knowledge(
            account_id="account-1",
            confidence_level=ConfidenceLevel.DOUBTFUL,
            source_id="source-doubtful",
        )

        context = MemoryContext.create_from_knowledge_items(
            account_id=AccountId("account-1"),
            purpose=MemoryContextPurpose.ASSISTANT_RESPONSE,
            knowledge_items=[unconfirmed, doubtful],
            strict=True,
        )

        self.assertEqual(context.items, ())

    def test_permissive_mode_can_include_allowed_unconfirmed_knowledge(self):
        unconfirmed = make_accepted_knowledge(
            account_id="account-1",
            status=KnowledgeStatus.UNCONFIRMED,
            confidence_level=ConfidenceLevel.UNCONFIRMED,
        )

        context = MemoryContext.create_from_knowledge_items(
            account_id=AccountId("account-1"),
            purpose=MemoryContextPurpose.MEMORY_REVIEW,
            knowledge_items=[unconfirmed],
            strict=False,
        )

        self.assertEqual(len(context.items), 1)
        self.assertEqual(context.items[0].knowledge_id.value, unconfirmed.id.value)
        self.assertEqual(context.items[0].warning_flags, ("unconfirmed_status", "low_confidence"))

    def test_account_mismatch_is_rejected(self):
        knowledge = make_accepted_knowledge(account_id="account-2")

        with self.assertRaises(MemoryContextOwnershipMismatch):
            MemoryContext.create_from_knowledge_items(
                account_id=AccountId("account-1"),
                purpose=MemoryContextPurpose.MEMORY_REVIEW,
                knowledge_items=[knowledge],
            )

    def test_candidate_knowledge_is_rejected(self):
        candidate = make_candidate_knowledge(account_id="account-1")

        with self.assertRaises(MemoryContextInvalid):
            MemoryContext.create_from_knowledge_items(
                account_id=AccountId("account-1"),
                purpose=MemoryContextPurpose.MEMORY_REVIEW,
                knowledge_items=[candidate],  # type: ignore[list-item]
            )

    def test_duplicate_knowledge_is_deduplicated(self):
        knowledge = make_accepted_knowledge(account_id="account-1")

        context = MemoryContext.create_from_knowledge_items(
            account_id=AccountId("account-1"),
            purpose=MemoryContextPurpose.RESEARCH_INPUT,
            knowledge_items=[knowledge, knowledge],
        )

        self.assertEqual(len(context.items), 1)
        self.assertEqual(context.knowledge_ids(), (knowledge.id,))

    def test_context_item_stores_eligibility_snapshot(self):
        knowledge = make_accepted_knowledge(account_id="account-1")

        item = MemoryContextItem.from_knowledge(
            knowledge,
            included_reason=MemoryContextReason("included_for_review"),
            provenance_id=ProvenanceId("provenance-1"),
        )

        self.assertEqual(item.account_id.value, "account-1")
        self.assertEqual(item.knowledge_id.value, knowledge.id.value)
        self.assertIs(item.status, knowledge.status)
        self.assertIs(item.confidence_level, knowledge.confidence_level)
        self.assertEqual(item.source_id.value, knowledge.primary_source_id.value)
        self.assertEqual(item.provenance_id.value, "provenance-1")
        self.assertEqual(item.included_reason.value, "included_for_review")

    def test_context_items_must_be_unique_when_created_directly(self):
        item = MemoryContextItem(
            account_id=AccountId("account-1"),
            knowledge_id=KnowledgeId("knowledge-1"),
            status=KnowledgeStatus.ACTIVE,
            confidence_level=ConfidenceLevel.INFERRED,
        )

        with self.assertRaises(MemoryContextInvalid):
            MemoryContext.create(
                account_id=AccountId("account-1"),
                purpose=MemoryContextPurpose.MEMORY_REVIEW,
                items=(item, item),
            )

    def test_context_does_not_mutate_knowledge_item(self):
        knowledge = make_accepted_knowledge(
            status=KnowledgeStatus.ACTIVE,
            confidence_level=ConfidenceLevel.INFERRED,
        )
        before = (
            knowledge.text.value,
            knowledge.status,
            knowledge.confidence_level,
            knowledge.updated_at,
        )

        MemoryContext.create_from_knowledge_items(
            account_id=knowledge.account_id,
            purpose=MemoryContextPurpose.ASSISTANT_RESPONSE,
            knowledge_items=[knowledge],
            strict=True,
        )

        after = (
            knowledge.text.value,
            knowledge.status,
            knowledge.confidence_level,
            knowledge.updated_at,
        )
        self.assertEqual(before, after)

    def test_context_does_not_create_correction_contradiction_or_relation(self):
        context = MemoryContext.create_from_knowledge_items(
            account_id=AccountId("account-1"),
            purpose=MemoryContextPurpose.MEMORY_REVIEW,
            knowledge_items=[make_accepted_knowledge(account_id="account-1")],
        )

        self.assertFalse(hasattr(context, "correction_id"))
        self.assertFalse(hasattr(context, "contradiction_id"))
        self.assertFalse(hasattr(context, "relation_id"))

    def test_context_is_immutable_snapshot(self):
        context = MemoryContext.create(
            account_id=AccountId("account-1"),
            purpose=MemoryContextPurpose.MEMORY_REVIEW,
        )

        with self.assertRaises(FrozenInstanceError):
            context.strict = True  # type: ignore[misc]

    def test_purpose_is_stored_correctly(self):
        for purpose in MemoryContextPurpose:
            context = MemoryContext.create(
                account_id=AccountId("account-1"),
                purpose=purpose,
            )

            self.assertIs(context.purpose, purpose)


if __name__ == "__main__":
    unittest.main()
