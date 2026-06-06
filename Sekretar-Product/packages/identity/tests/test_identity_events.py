import unittest

from conftest import make_identity_repositories, make_identity_service
from sekretar_identity.enums import ClientType, DeviceGrantStatus, IdentityEventType


class IdentityEventTests(unittest.TestCase):
    def test_identity_events_are_created_for_key_actions(self):
        repositories = make_identity_repositories()
        service = make_identity_service(repositories)

        account, user, _profile, _membership = service.create_account_with_user_profile(
            display_name="Event User",
        )
        device = service.register_device(client_type=ClientType.ANDROID_RECORDER)
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
        service.logout_session(session.id)
        expired_session = service.create_session(account_id=account.id, user_id=user.id)
        service.expire_session(expired_session.id)

        beta_access = service.create_beta_access_code(code="SR-EVENTS")
        service.activate_beta_access(
            code=beta_access.code,
            account_id=account.id,
            user_id=user.id,
        )
        service.update_device_grant_status(
            grant_id=grant.id,
            status=DeviceGrantStatus.REVOKED,
        )

        events = repositories["events"].list_by_account_id(account.id)
        event_types = {event.event_type for event in events}

        self.assertIn(IdentityEventType.ACCOUNT_CREATED, event_types)
        self.assertIn(IdentityEventType.USER_CREATED, event_types)
        self.assertIn(IdentityEventType.DEVICE_GRANT_CREATED, event_types)
        self.assertIn(IdentityEventType.SESSION_CREATED, event_types)
        self.assertIn(IdentityEventType.USER_LOGGED_IN, event_types)
        self.assertIn(IdentityEventType.USER_LOGGED_OUT, event_types)
        self.assertIn(IdentityEventType.SESSION_EXPIRED, event_types)
        self.assertIn(IdentityEventType.BETA_ACCESS_ACTIVATED, event_types)
        self.assertIn(IdentityEventType.DEVICE_GRANT_REVOKED, event_types)

        all_events = list(repositories["events"].items.values())
        self.assertTrue(any(
            event.event_type is IdentityEventType.DEVICE_REGISTERED
            and event.device_id == device.id
            for event in all_events
        ))


if __name__ == "__main__":
    unittest.main()
