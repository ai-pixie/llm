from __future__ import annotations

import unittest

from _candidate import activate_candidate

activate_candidate()

from app.database import Database
from app.models import Project
from app.repositories import ProjectRepository


class T6HiddenTest(unittest.TestCase):
    def test_project_name_is_treated_as_data(self) -> None:
        database = Database()
        try:
            database.migrate()
            projects = ProjectRepository(database.connection)
            projects.create(Project("p1", "alice", "alpha", "aws"))
            projects.create(Project("p2", "bob", "beta", "azure"))

            malicious = "x' OR 1=1 --"
            result = projects.find_by_name(malicious)

            self.assertEqual([], result)
        finally:
            database.close()


if __name__ == "__main__":
    unittest.main(verbosity=2)
