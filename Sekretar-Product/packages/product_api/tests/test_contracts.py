import unittest

import conftest  # noqa: F401
from sekretar_product_api.contracts import ContractMetadata, Pagination


class ContractTests(unittest.TestCase):
    def test_pagination_defaults_are_valid(self):
        pagination = Pagination()

        self.assertEqual(pagination.limit, 50)
        self.assertEqual(pagination.offset, 0)

    def test_pagination_rejects_invalid_values(self):
        with self.assertRaises(ValueError):
            Pagination(limit=0)

        with self.assertRaises(ValueError):
            Pagination(offset=-1)

    def test_contract_metadata_carries_values(self):
        metadata = ContractMetadata(values={"key": "value"})

        self.assertEqual(metadata.values["key"], "value")


if __name__ == "__main__":
    unittest.main()
