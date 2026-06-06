import unittest

import conftest  # noqa: F401
from sekretar_product_api.versioning import ApiVersion


class ApiVersionTests(unittest.TestCase):
    def test_parse_major_minor_version(self):
        version = ApiVersion.parse("1.2")

        self.assertEqual(version.major, 1)
        self.assertEqual(version.minor, 2)
        self.assertEqual(str(version), "1.2")

    def test_parse_major_only_version(self):
        version = ApiVersion.parse("2")

        self.assertEqual(version.major, 2)
        self.assertEqual(version.minor, 0)
        self.assertEqual(str(version), "2.0")

    def test_rejects_negative_versions(self):
        with self.assertRaises(ValueError):
            ApiVersion(major=-1)


if __name__ == "__main__":
    unittest.main()
