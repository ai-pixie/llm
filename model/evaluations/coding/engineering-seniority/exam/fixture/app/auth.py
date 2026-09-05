from __future__ import annotations

from app.models import Project


class AuthorizationError(PermissionError):
    pass


class AuthorizationService:
    def assert_project_owner(self, actor_id: str, project: Project) -> None:
        if project.owner_id != actor_id:
            raise AuthorizationError("project access denied")
