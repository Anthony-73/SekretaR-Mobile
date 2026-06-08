import unittest

from conftest import make_accepted_knowledge
from sekretar_memory.errors import KnowledgeOwnershipMismatch
from sekretar_memory.value_objects import AccountId


class AccountOwnershipTests(unittest.TestCase):
    def test_knowledge_item_belongs_to_account(self):
        knowledge = make_accepted_knowledge(account_id="account-1")

        self.assertTrue(knowledge.belongs_to_account(AccountId("account-1")))
        self.assertFalse(knowledge.belongs_to_account(AccountId("account-2")))

    def test_knowledge_item_rejects_foreign_account_access(self):
        knowledge = make_accepted_knowledge(account_id="account-1")

        with self.assertRaises(KnowledgeOwnershipMismatch):
            knowledge.ensure_belongs_to_account(AccountId("account-2"))


if __name__ == "__main__":
    unittest.main()
