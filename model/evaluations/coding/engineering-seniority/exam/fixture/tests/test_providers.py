from __future__ import annotations

import unittest

from app.providers import CloudOperations


class CloudOperationsTest(unittest.TestCase):
    def test_existing_providers(self) -> None:
        cloud = CloudOperations()
        self.assertEqual("aws:ok", cloud.health_check("aws"))
        self.assertEqual("azure:ok", cloud.health_check("azure"))
        self.assertEqual("aws:deleted:x", cloud.delete_external_resource("aws", "x"))
        self.assertEqual("azure:deleted:x", cloud.delete_external_resource("azure", "x"))

    def test_unsupported_provider(self) -> None:
        with self.assertRaises(ValueError):
            CloudOperations().health_check("unknown")


if __name__ == "__main__":
    unittest.main()
