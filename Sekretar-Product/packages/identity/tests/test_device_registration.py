import unittest

from conftest import make_identity_repositories, make_identity_service
from sekretar_identity.enums import ClientType, IdentityEventType


class DeviceRegistrationTests(unittest.TestCase):
    def test_device_registers_with_supported_client_types(self):
        for client_type in ClientType:
            with self.subTest(client_type=client_type):
                repositories = make_identity_repositories()
                service = make_identity_service(repositories)
                device = service.register_device(
                    client_type=client_type,
                    display_name=f"{client_type.value} device",
                )

                self.assertTrue(device.id)
                self.assertIs(device.client_type, client_type)
                self.assertEqual(repositories["devices"].get(device.id), device)

    def test_android_recorder_is_normal_device_client_type(self):
        repositories = make_identity_repositories()
        service = make_identity_service(repositories)
        device = service.register_device(
            client_type=ClientType.ANDROID_RECORDER,
            display_name="Android Recorder",
        )

        self.assertIs(device.client_type, ClientType.ANDROID_RECORDER)

        events = list(repositories["events"].items.values())
        self.assertTrue(any(
            event.event_type is IdentityEventType.DEVICE_REGISTERED
            and event.device_id == device.id
            and event.metadata["client_type"] == "android_recorder"
            for event in events
        ))


if __name__ == "__main__":
    unittest.main()
