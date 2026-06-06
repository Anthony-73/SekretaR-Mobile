import unittest

import conftest  # noqa: F401
from sekretar_product_api.context import (
    ProductActor,
    ProductClient,
    ProductDeviceContext,
    ProductRequestContext,
    ProductSessionContext,
)
from sekretar_product_api.metadata import RequestMetadata
from sekretar_product_api.versioning import ApiVersion


class ProductRequestContextTests(unittest.TestCase):
    def test_context_carries_validated_identity_values(self):
        context = ProductRequestContext(
            actor=ProductActor(account_id="account-1", user_id="user-1"),
            client=ProductClient(client_type="android_recorder", client_version="1.0.0"),
            api_version=ApiVersion(major=1, minor=0),
            metadata=RequestMetadata(request_id="request-1", timezone="UTC"),
            device=ProductDeviceContext(
                device_id="device-1",
                device_grant_id="grant-1",
            ),
            session=ProductSessionContext(session_id="session-1"),
        )

        self.assertEqual(context.request_id, "request-1")
        self.assertEqual(context.account_id, "account-1")
        self.assertEqual(context.user_id, "user-1")
        self.assertEqual(context.device_id, "device-1")
        self.assertEqual(context.device_grant_id, "grant-1")
        self.assertEqual(context.session_id, "session-1")
        self.assertEqual(str(context.api_version), "1.0")


if __name__ == "__main__":
    unittest.main()
