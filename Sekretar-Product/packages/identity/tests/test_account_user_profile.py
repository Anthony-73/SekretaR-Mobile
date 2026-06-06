import unittest

from conftest import make_identity_repositories, make_identity_service
from sekretar_identity.enums import IdentityEventType


class AccountUserProfileTests(unittest.TestCase):
    def test_account_user_profile_are_created(self):
        repositories = make_identity_repositories()
        service = make_identity_service(repositories)

        account, user, profile, membership = service.create_account_with_user_profile(
            display_name="Alice",
            language="ru",
            timezone="Europe/Moscow",
        )

        self.assertTrue(account.id)
        self.assertTrue(user.id)
        self.assertEqual(user.account_id, account.id)
        self.assertEqual(profile.user_id, user.id)
        self.assertEqual(profile.display_name, "Alice")
        self.assertEqual(profile.language, "ru")
        self.assertEqual(profile.timezone, "Europe/Moscow")
        self.assertEqual(membership.account_id, account.id)
        self.assertEqual(membership.user_id, user.id)

        events = repositories["events"].list_by_account_id(account.id)
        event_types = {event.event_type for event in events}
        self.assertIn(IdentityEventType.ACCOUNT_CREATED, event_types)
        self.assertIn(IdentityEventType.USER_CREATED, event_types)


if __name__ == "__main__":
    unittest.main()
