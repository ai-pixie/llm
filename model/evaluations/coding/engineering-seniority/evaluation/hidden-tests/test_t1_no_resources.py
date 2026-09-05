from __future__ import annotations

import unittest

from _candidate import activate_candidate

activate_candidate()

from app.auth import AuthorizationService
from app.database import Database
from app.models import Project
from app.providers import CloudOperations
from app.repositories import ProjectRepository, ResourceRepository
from app.services import ProjectService


class T1HiddenTest(unittest.TestCase):
    def test_delete_project_with_no_resources(self) -> None:
        database = Database()
        try:
            database.migrate()
            projects = ProjectRepository(database.connection)
            resources = ResourceRepository(database.connection)
            service = ProjectService(
                projects,
                resources,
                AuthorizationService(),
                CloudOperations(),
            )
            projects.create(Project("p-empty", "alice", "empty", "aws"))

            service.delete_project("alice", "p-empty")

            self.assertIsNone(projects.get("p-empty"))
        finally:
            database.close()


if __name__ == "__main__":
    unittest.main(verbosity=2)
