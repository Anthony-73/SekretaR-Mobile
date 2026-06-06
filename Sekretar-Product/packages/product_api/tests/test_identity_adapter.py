import unittest

import conftest  # noqa: F401
from sekretar_identity.errors import (
    AccountNotFound,
    ActiveDeviceLimitExceeded,
    BetaAccessInvalid,
    DeviceNotFound,
    GrantNotValid,
    IdentityError,
    SessionInvalid,
    UserNotFound,
)
from sekretar_product_api.errors import ProductErrorCode
from sekretar_product_api.identity_adapter import map_identity_error


class IdentityErrorMappingTests(unittest.TestCase):
    def test_maps_account_and_user_not_found_to_identity_not_found(self):
        for error in [AccountNotFound("missing account"), UserNotFound("missing user")]:
            mapped = map_identity_error(error)

            self.assertEqual(mapped.code, ProductErrorCode.IDENTITY_NOT_FOUND)
            self.assertEqual(mapped.category, "identity")

    def test_maps_device_not_found(self):
        mapped = map_identity_error(DeviceNotFound("missing device"))

        self.assertEqual(mapped.code, ProductErrorCode.DEVICE_NOT_REGISTERED)

    def test_maps_invalid_grant(self):
        mapped = map_identity_error(GrantNotValid("invalid grant"))

        self.assertEqual(mapped.code, ProductErrorCode.DEVICE_GRANT_INVALID)

    def test_maps_device_limit(self):
        mapped = map_identity_error(ActiveDeviceLimitExceeded("limit exceeded"))

        self.assertEqual(mapped.code, ProductErrorCode.DEVICE_LIMIT_EXCEEDED)

    def test_maps_invalid_session(self):
        mapped = map_identity_error(SessionInvalid("invalid session"))

        self.assertEqual(mapped.code, ProductErrorCode.SESSION_INVALID)

    def test_maps_beta_access_invalid_to_access_denied(self):
        mapped = map_identity_error(BetaAccessInvalid("beta denied"))

        self.assertEqual(mapped.code, ProductErrorCode.ACCESS_DENIED)

    def test_maps_unknown_identity_error_to_internal_error(self):
        mapped = map_identity_error(IdentityError("unexpected identity error"))

        self.assertEqual(mapped.code, ProductErrorCode.INTERNAL_ERROR)
        self.assertEqual(mapped.category, "identity")


if __name__ == "__main__":
    unittest.main()
