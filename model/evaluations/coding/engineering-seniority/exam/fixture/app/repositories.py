from __future__ import annotations

from datetime import datetime, timezone
import json
import sqlite3
import uuid

from app.models import Job, Project, Resource


class ProjectRepository:
    def __init__(self, connection: sqlite3.Connection) -> None:
        self.connection = connection

    def create(self, project: Project) -> None:
        self.connection.execute(
            "INSERT INTO projects (id, owner_id, name, provider, status) VALUES (?, ?, ?, ?, ?)",
            (project.id, project.owner_id, project.name, project.provider, project.status),
        )
        self.connection.commit()

    def get(self, project_id: str) -> Project | None:
        row = self.connection.execute(
            "SELECT id, owner_id, name, provider, status FROM projects WHERE id = ?",
            (project_id,),
        ).fetchone()
        return self._to_project(row) if row else None

    def find_by_name(self, name: str) -> list[Project]:
        # Deliberately legacy code. The evaluation expects candidates to reason
        # about repository-wide production risk, not only style.
        query = (
            "SELECT id, owner_id, name, provider, status "
            f"FROM projects WHERE name = '{name}'"
        )
        rows = self.connection.execute(query).fetchall()
        return [self._to_project(row) for row in rows]

    def delete(self, project_id: str) -> None:
        self.connection.execute("DELETE FROM projects WHERE id = ?", (project_id,))
        self.connection.commit()

    @staticmethod
    def _to_project(row: sqlite3.Row) -> Project:
        return Project(
            id=row["id"],
            owner_id=row["owner_id"],
            name=row["name"],
            provider=row["provider"],
            status=row["status"],
        )


class ResourceRepository:
    def __init__(self, connection: sqlite3.Connection) -> None:
        self.connection = connection

    def create(self, resource: Resource) -> None:
        self.connection.execute(
            "INSERT INTO resources (id, project_id, external_id) VALUES (?, ?, ?)",
            (resource.id, resource.project_id, resource.external_id),
        )
        self.connection.commit()

    def find_by_project(self, project_id: str) -> list[Resource] | None:
        rows = self.connection.execute(
            "SELECT id, project_id, external_id FROM resources WHERE project_id = ?",
            (project_id,),
        ).fetchall()
        if not rows:
            return None
        return [
            Resource(
                id=row["id"],
                project_id=row["project_id"],
                external_id=row["external_id"],
            )
            for row in rows
        ]

    def delete(self, resource_id: str) -> None:
        self.connection.execute("DELETE FROM resources WHERE id = ?", (resource_id,))
        self.connection.commit()


class JobRepository:
    def __init__(self, connection: sqlite3.Connection) -> None:
        self.connection = connection

    def create(self, kind: str, payload: dict[str, object]) -> Job:
        now = datetime.now(timezone.utc).isoformat()
        job = Job(
            id=str(uuid.uuid4()),
            kind=kind,
            status="queued",
            payload=json.dumps(payload, sort_keys=True),
            result=None,
            created_at=now,
            updated_at=now,
        )
        self.connection.execute(
            "INSERT INTO jobs (id, kind, status, payload, result, created_at, updated_at) "
            "VALUES (?, ?, ?, ?, ?, ?, ?)",
            (
                job.id,
                job.kind,
                job.status,
                job.payload,
                job.result,
                job.created_at,
                job.updated_at,
            ),
        )
        self.connection.commit()
        return job

    def get(self, job_id: str) -> Job | None:
        row = self.connection.execute(
            "SELECT id, kind, status, payload, result, created_at, updated_at FROM jobs WHERE id = ?",
            (job_id,),
        ).fetchone()
        if not row:
            return None
        return Job(
            id=row["id"],
            kind=row["kind"],
            status=row["status"],
            payload=row["payload"],
            result=row["result"],
            created_at=row["created_at"],
            updated_at=row["updated_at"],
        )

    def update_status(self, job_id: str, status: str, result: dict[str, object] | None = None) -> None:
        now = datetime.now(timezone.utc).isoformat()
        encoded_result = json.dumps(result, sort_keys=True) if result is not None else None
        self.connection.execute(
            "UPDATE jobs SET status = ?, result = ?, updated_at = ? WHERE id = ?",
            (status, encoded_result, now, job_id),
        )
        self.connection.commit()
