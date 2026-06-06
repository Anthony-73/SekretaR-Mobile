import unittest

from conftest import (
    make_account_user_profile,
    make_identity_repositories,
    make_identity_service,
)
from sekretar_identity.enums import ClientType, IdentityEventType, SessionStatus


class SessionTests(unittest.TestCase):
    def test_session_is_created_but_does_not_own_data(self):
        repositories = make_identity_repositories()
        service = make_identity_service(repositories)
        account, user, _profile, _membership = make_account_user_profile(service)
        device = service.register_device(client_type=ClientType.WEB)
        grant = service.create_device_grant(
            account_id=account.id,
            user_id=user.id,
            device_id=device.id,
        )

        session = service.create_session(
            account_id=account.id,
            user_id=user.id,
            device_id=device.id,
            device_grant_id=grant.id,
        )

        self.assertEqual(session.account_id, account.id)
        self.assertEqual(session.user_id, user.id)
        self.assertEqual(session.device_id, device.id)
        self.assertEqual(session.device_grant_id, grant.id)
        self.assertIs(session.status, SessionStatus.ACTIVE)
        self.assertFalse(hasattr(session, "owns_data"))

        events = repositories["events"].list_by_account_id(account.id)
        event_types = {event.event_type for event in events}
        self.assertIn(IdentityEventType.SESSION_CREATED, event_types)
        self.assertIn(IdentityEventType.USER_LOGGED_IN, event_types)

    def test_session_can_be_logged_out_and_expired(self):
        repositories = make_identity_repositories()
        service = make_identity_service(repositories)
        account, user, _profile, _membership = make_account_user_profile(service)

        logout_session = service.create_session(account_id=account.id, user_id=user.id)
        expired_session = service.create_session(account_id=account.id, user_id=user.id)

        service.logout_session(logout_session.id)
        service.expire_session(expired_session.id)

        self.assertIs(logout_session.status, SessionStatus.LOGGED_OUT)
        self.assertIs(expired_session.status, SessionStatus.EXPIRED)

        events = repositories["events"].list_by_account_id(account.id)
        event_types = {event.event_type for event in events}
        self.assertIn(IdentityEventType.USER_LOGGED_OUT, event_types)
        self.assertIn(IdentityEventType.SESSION_EXPIRED, event_types)


if __name__ == "__main__":
    unittest.main()
