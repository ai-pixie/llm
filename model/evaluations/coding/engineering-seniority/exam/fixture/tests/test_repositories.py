from __future__ import annotations

import unittest

from app.database import Database
from app.models import Project
from app.repositories import JobRepository, ProjectRepository


class RepositoryTest(unittest.TestCase):
    def setUp(self) -> None:
        self.database = Database()
        self.database.migrate()
        self.projects = ProjectRepository(self.database.connection)
        self.jobs = JobRepository(self.database.connection)

    def tearDown(self) -> None:
        self.database.close()

    def test_find_project_by_name(self) -> None:
        self.projects.create(Project("p1", "alice", "demo", "aws"))
        self.assertEqual(["p1"], [project.id for project in self.projects.find_by_name("demo")])

    def test_create_job(self) -> None:
        job = self.jobs.create("example", {"project_id": "p1"})
        loaded = self.jobs.get(job.id)
        self.assertIsNotNone(loaded)
        self.assertEqual("queued", loaded.status)


if __name__ == "__main__":
    unittest.main()
