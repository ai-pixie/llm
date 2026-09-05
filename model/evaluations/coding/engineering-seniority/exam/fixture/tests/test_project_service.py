from __future__ import annotations

import unittest

from app.auth import AuthorizationError, AuthorizationService
from app.database import Database
from app.models import Project, Resource
from app.providers import CloudOperations
from app.repositories import ProjectRepository, ResourceRepository
from app.services import ProjectNotFoundError, ProjectService


class ProjectServiceTest(unittest.TestCase):
    def setUp(self) -> None:
        self.database = Database()
        self.database.migrate()
        self.projects = ProjectRepository(self.database.connection)
        self.resources = ResourceRepository(self.database.connection)
        self.service = ProjectService(
            self.projects,
            self.resources,
            AuthorizationService(),
            CloudOperations(),
        )

    def tearDown(self) -> None:
        self.database.close()

    def test_delete_project_with_resource(self) -> None:
        self.projects.create(Project("p1", "alice", "demo", "aws"))
        self.resources.create(Resource("r1", "p1", "external-1"))

        self.service.delete_project("alice", "p1")

        self.assertIsNone(self.projects.get("p1"))
        self.assertIsNone(self.resources.find_by_project("p1"))

    def test_delete_missing_project_raises(self) -> None:
        with self.assertRaises(ProjectNotFoundError):
            self.service.delete_project("alice", "missing")

    def test_delete_project_requires_owner(self) -> None:
        self.projects.create(Project("p1", "alice", "demo", "aws"))
        self.resources.create(Resource("r1", "p1", "external-1"))

        with self.assertRaises(AuthorizationError):
            self.service.delete_project("bob", "p1")

        self.assertIsNotNone(self.projects.get("p1"))


if __name__ == "__main__":
    unittest.main()
