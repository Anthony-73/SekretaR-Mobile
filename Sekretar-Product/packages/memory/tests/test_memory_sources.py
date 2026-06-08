import unittest

from conftest import make_accepted_knowledge, make_candidate_knowledge, make_memory_source
from sekretar_memory.constants import PHASE_1_SOURCE_TYPES
from sekretar_memory.entities import MemorySource
from sekretar_memory.enums import SourceType
from sekretar_memory.errors import (
    InvalidSourceReference,
    InvalidSourceType,
    KnowledgeOwnershipMismatch,
    MemorySourceInvalid,
    MemorySourceLinkMismatch,
)
from sekretar_memory.policies import is_phase1_source_type
from sekretar_memory.value_objects import AccountId, SourceId, SourceReference


class MemorySourceTests(unittest.TestCase):
    def test_memory_source_is_created_with_required_fields(self):
        source = make_memory_source(
            account_id="account-1",
            source_type=SourceType.MEETING,
            external_reference="meeting:planning-june",
        )

        self.assertEqual(source.account_id.value, "account-1")
        self.assertIs(source.source_type, SourceType.MEETING)
        self.assertEqual(source.external_reference.value, "meeting:planning-june")
        self.assertIsNotNone(source.id.value)
        self.assertTrue(source.is_phase1_supported())
        self.assertTrue(source.can_produce_candidate_knowledge())

    def test_memory_source_requires_account_id(self):
        with self.assertRaises(MemorySourceInvalid):
            MemorySource.create(
                account_id=None,  # type: ignore[arg-type]
                source_type=SourceType.MEETING,
                external_reference=SourceReference("meeting:1"),
            )

    def test_memory_source_requires_source_type(self):
        with self.assertRaises(InvalidSourceType):
            MemorySource.create(
                account_id=AccountId("account-1"),
                source_type=None,  # type: ignore[arg-type]
                external_reference=SourceReference("meeting:1"),
            )

    def test_memory_source_requires_external_reference(self):
        with self.assertRaises(InvalidSourceReference):
            MemorySource.create(
                account_id=AccountId("account-1"),
                source_type=SourceType.MEETING,
                external_reference=None,  # type: ignore[arg-type]
            )

    def test_memory_source_rejects_invalid_external_reference_prefix(self):
        with self.assertRaises(InvalidSourceReference):
            MemorySource.create(
                account_id=AccountId("account-1"),
                source_type=SourceType.MEETING,
                external_reference=SourceReference("document:wrong-prefix"),
            )

    def test_memory_source_enforces_account_ownership(self):
        source = make_memory_source(account_id="account-1")

        self.assertTrue(source.belongs_to_account(AccountId("account-1")))
        self.assertFalse(source.belongs_to_account(AccountId("account-2")))

        with self.assertRaises(KnowledgeOwnershipMismatch):
            source.ensure_belongs_to_account(AccountId("account-2"))

    def test_phase1_source_types_are_supported(self):
        phase1_examples = {
            SourceType.MEETING: "meeting:1",
            SourceType.DOCUMENT: "document:1",
            SourceType.VOICE_NOTE: "voice-note-1",
            SourceType.MANUAL_NOTE: "manual-note-1",
            SourceType.RESEARCH: "research:1",
            SourceType.ASSISTANT_INTERACTION: "assistant:1",
            SourceType.INTEGRATION: "integration:crm-1",
            SourceType.CONFIRMED_TASK: "task:1",
        }

        for source_type, external_reference in phase1_examples.items():
            source = MemorySource.create(
                account_id=AccountId("account-1"),
                source_type=source_type,
                external_reference=SourceReference(external_reference),
            )
            self.assertIn(source.source_type, PHASE_1_SOURCE_TYPES)
            self.assertTrue(source.is_phase1_supported())

    def test_reserved_unknown_source_type_is_rejected_in_phase1(self):
        with self.assertRaises(InvalidSourceType):
            MemorySource.create(
                account_id=AccountId("account-1"),
                source_type=SourceType.UNKNOWN,
                external_reference=SourceReference("unknown:1"),
            )

    def test_non_phase1_source_type_can_be_modeled_when_explicitly_allowed(self):
        source = MemorySource.create(
            account_id=AccountId("account-1"),
            source_type=SourceType.UNKNOWN,
            external_reference=SourceReference("unknown:future-source"),
            require_phase1_type=False,
        )

        self.assertFalse(source.is_phase1_supported())
        self.assertFalse(is_phase1_source_type(SourceType.UNKNOWN))

    def test_external_reference_factories_for_future_blocks(self):
        meeting = MemorySource.for_meeting(
            account_id=AccountId("account-1"),
            meeting_id="june-planning",
        )
        document = MemorySource.for_document(
            account_id=AccountId("account-1"),
            document_id="brief-42",
        )
        research = MemorySource.for_research(
            account_id=AccountId("account-1"),
            research_id="market-scan",
        )
        assistant = MemorySource.for_assistant_interaction(
            account_id=AccountId("account-1"),
            assistant_interaction_id="chat-9",
        )
        integration = MemorySource.for_integration(
            account_id=AccountId("account-1"),
            integration_reference="crm:client-a",
        )

        self.assertEqual(meeting.external_reference.value, "meeting:june-planning")
        self.assertEqual(document.external_reference.value, "document:brief-42")
        self.assertEqual(research.external_reference.value, "research:market-scan")
        self.assertEqual(assistant.external_reference.value, "assistant:chat-9")
        self.assertEqual(integration.external_reference.value, "integration:crm:client-a")

    def test_candidate_knowledge_can_reference_memory_source(self):
        source = make_memory_source(
            source_type=SourceType.MEETING,
            external_reference="meeting:planning-june",
        )
        candidate = make_candidate_knowledge(
            account_id=source.account_id.value,
            source_id=source.id.value,
            source_type=SourceType.MEETING,
        )

        source.ensure_candidate_can_reference(candidate)

    def test_candidate_knowledge_rejects_mismatched_memory_source(self):
        source = make_memory_source(source_id="source-1")
        candidate = make_candidate_knowledge(source_id="source-2")

        with self.assertRaises(MemorySourceLinkMismatch):
            source.ensure_candidate_can_reference(candidate)

    def test_knowledge_item_can_reference_memory_source(self):
        source = make_memory_source(source_id="source-1")
        knowledge = make_accepted_knowledge(
            account_id=source.account_id.value,
            source_id=source.id.value,
        )

        source.ensure_knowledge_can_reference(knowledge)

    def test_knowledge_item_rejects_mismatched_memory_source(self):
        source = make_memory_source(source_id="source-1")
        knowledge = make_accepted_knowledge(source_id="source-2")

        with self.assertRaises(MemorySourceLinkMismatch):
            source.ensure_knowledge_can_reference(knowledge)


if __name__ == "__main__":
    unittest.main()
