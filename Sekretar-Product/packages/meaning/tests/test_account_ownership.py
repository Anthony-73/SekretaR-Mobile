import unittest

from conftest import make_meaning_reference
from sekretar_meaning.value_objects import AccountId


class AccountOwnershipTests(unittest.TestCase):
    def test_meaning_reference_belongs_to_account(self):
        reference = make_meaning_reference(account_id="account-1")

        self.assertEqual(reference.account_id, AccountId("account-1"))
        self.assertNotEqual(reference.account_id, AccountId("account-2"))


if __name__ == "__main__":
    unittest.main()
