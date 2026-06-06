import unittest

from conftest import make_account_user_profile, make_identity_service
from sekretar_identity.enums import BetaAccessStatus, IdentityEventType
from sekretar_identity.errors import BetaAccessInvalid


class BetaAccessTests(unittest.TestCase):
    def test_beta_access_is_bound_to_account_and_user(self):
        service = make_identity_service()
        account, user, _profile, _membership = make_account_user_profile(service)
        beta_access = service.create_beta_access_code(code="SR-TEST-CODE")

        activated = service.activate_beta_access(
            code=beta_access.code,
            account_id=account.id,
            user_id=user.id,
        )

        self.assertEqual(activated.account_id, account.id)
        self.assertEqual(activated.user_id, user.id)
        self.assertIs(activated.status, BetaAccessStatus.ACTIVATED)
        self.assertIsNotNone(activated.activated_at)

        events = service.events.list_by_account_id(account.id)
        self.assertTrue(any(
            event.event_type is IdentityEventType.BETA_ACCESS_ACTIVATED
            for event in events
        ))

    def test_beta_access_cannot_be_activated_twice(self):
        service = make_identity_service()
        account, user, _profile, _membership = make_account_user_profile(service)
        beta_access = service.create_beta_access_code(code="SR-ONE-TIME")

        service.activate_beta_access(
            code=beta_access.code,
            account_id=account.id,
            user_id=user.id,
        )

        with self.assertRaises(BetaAccessInvalid):
            service.activate_beta_access(
                code=beta_access.code,
                account_id=account.id,
                user_id=user.id,
            )


if __name__ == "__main__":
    unittest.main()
