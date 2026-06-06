import unittest

from conftest import (
    make_account_user_profile,
    make_identity_repositories,
    make_identity_service,
)


class AccountMembershipTests(unittest.TestCase):
    def test_user_is_connected_to_account_through_membership(self):
        repositories = make_identity_repositories()
        service = make_identity_service(repositories)
        account, user, _profile, membership = make_account_user_profile(service)

        memberships = repositories["memberships"].list_by_account_id(account.id)

        self.assertIn(membership, memberships)
        self.assertEqual(membership.account_id, account.id)
        self.assertEqual(membership.user_id, user.id)
        self.assertEqual(membership.role, "owner")
        self.assertTrue(membership.is_active)


if __name__ == "__main__":
    unittest.main()
