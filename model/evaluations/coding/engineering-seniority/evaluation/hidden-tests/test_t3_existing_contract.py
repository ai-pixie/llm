from __future__ import annotations

import unittest

from _candidate import activate_candidate

activate_candidate()

from app.providers import CloudOperations


class T3HiddenTest(unittest.TestCase):
    def test_existing_provider_behavior_is_preserved(self) -> None:
        cloud = CloudOperations()
        self.assertEqual("aws:ok", cloud.health_check("aws"))
        self.assertEqual("azure:ok", cloud.health_check("azure"))
        self.assertEqual("aws:deleted:x", cloud.delete_external_resource("aws", "x"))
        self.assertEqual("azure:deleted:x", cloud.delete_external_resource("azure", "x"))

    def test_unknown_provider_remains_predictable(self) -> None:
        with self.assertRaises(ValueError):
            CloudOperations().health_check("unknown")


if __name__ == "__main__":
    unittest.main(verbosity=2)
