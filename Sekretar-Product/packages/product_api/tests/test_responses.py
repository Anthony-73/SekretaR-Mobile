import unittest

import conftest  # noqa: F401
from sekretar_product_api.errors import ProductError, ProductErrorCode
from sekretar_product_api.responses import ProductResponse


class ProductResponseTests(unittest.TestCase):
    def test_success_response_has_data_and_no_error(self):
        response = ProductResponse.ok(
            {"status": "ok"},
            request_id="request-1",
            metadata={"source": "test"},
        )

        self.assertTrue(response.success)
        self.assertEqual(response.data, {"status": "ok"})
        self.assertIsNone(response.error)
        self.assertEqual(response.request_id, "request-1")

        serialized = response.to_dict()
        self.assertTrue(serialized["success"])
        self.assertEqual(serialized["data"], {"status": "ok"})
        self.assertIsNone(serialized["error"])

    def test_error_response_has_error_and_no_data(self):
        error = ProductError(
            code=ProductErrorCode.VALIDATION_ERROR,
            message="Invalid input",
            details={"field": "name"},
        )
        response = ProductResponse.fail(error, request_id="request-2")

        self.assertFalse(response.success)
        self.assertIsNone(response.data)
        self.assertEqual(response.error, error)

        serialized = response.to_dict()
        self.assertFalse(serialized["success"])
        self.assertIsNone(serialized["data"])
        self.assertEqual(serialized["error"]["code"], "validation_error")


if __name__ == "__main__":
    unittest.main()
