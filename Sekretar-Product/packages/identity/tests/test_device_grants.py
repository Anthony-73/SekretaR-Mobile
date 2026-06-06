import unittest

from conftest import (
    make_account_user_profile,
    make_identity_repositories,
    make_identity_service,
)
from sekretar_identity.constants import MAX_ACTIVE_DEVICES_PER_ACCOUNT
from sekretar_identity.enums import ClientType, DeviceGrantStatus, IdentityEventType
from sekretar_identity.errors import ActiveDeviceLimitExceeded
from sekretar_identity.policies import count_active_device_grants


class DeviceGrantTests(unittest.TestCase):
    def test_device_grant_is_created_for_account_user_device(self):
        repositories = make_identity_repositories()
        service = make_identity_service(repositories)
        account, user, _profile, _membership = make_account_user_profile(service)
        device = service.register_device(client_type=ClientType.ANDROID_RECORDER)

        grant = service.create_device_grant(
            account_id=account.id,
            user_id=user.id,
            device_id=device.id,
        )

        self.assertEqual(grant.account_id, account.id)
        self.assertEqual(grant.user_id, user.id)
        self.assertEqual(grant.device_id, device.id)
        self.assertIs(grant.status, DeviceGrantStatus.ACTIVE)
        self.assertTrue(grant.is_active)
        self.assertEqual(repositories["device_grants"].get(grant.id), grant)

        events = repositories["events"].list_by_account_id(account.id)
        self.assertTrue(any(
            event.event_type is IdentityEventType.DEVICE_GRANT_CREATED
            for event in events
        ))

    def test_active_device_grant_limit_is_three(self):
        service = make_identity_service()
        account, user, _profile, _membership = make_account_user_profile(service)

        for _ in range(MAX_ACTIVE_DEVICES_PER_ACCOUNT):
            device = service.register_device(client_type=ClientType.WEB)
            service.create_device_grant(
                account_id=account.id,
                user_id=user.id,
                device_id=device.id,
            )

        extra_device = service.register_device(client_type=ClientType.ANDROID_RECORDER)

        with self.assertRaises(ActiveDeviceLimitExceeded):
            service.create_device_grant(
                account_id=account.id,
                user_id=user.id,
                device_id=extra_device.id,
            )

    def test_non_active_grants_do_not_occupy_active_slots(self):
        non_active_statuses = [
            DeviceGrantStatus.REVOKED,
            DeviceGrantStatus.LOST,
            DeviceGrantStatus.BLOCKED,
            DeviceGrantStatus.REPLACED,
            DeviceGrantStatus.EXPIRED,
        ]

        for status in non_active_statuses:
            with self.subTest(status=status):
                repositories = make_identity_repositories()
                service = make_identity_service(repositories)
                account, user, _profile, _membership = make_account_user_profile(service)

                for _ in range(MAX_ACTIVE_DEVICES_PER_ACCOUNT):
                    device = service.register_device(client_type=ClientType.WEB)
                    grant = service.create_device_grant(
                        account_id=account.id,
                        user_id=user.id,
                        device_id=device.id,
                    )
                    service.update_device_grant_status(grant_id=grant.id, status=status)

                grants = repositories["device_grants"].list_by_account_id(account.id)
                self.assertEqual(count_active_device_grants(grants), 0)

                replacement_device = service.register_device(
                    client_type=ClientType.ANDROID_RECORDER,
                )
                replacement_grant = service.create_device_grant(
                    account_id=account.id,
                    user_id=user.id,
                    device_id=replacement_device.id,
                )

                self.assertIs(replacement_grant.status, DeviceGrantStatus.ACTIVE)


if __name__ == "__main__":
    unittest.main()
