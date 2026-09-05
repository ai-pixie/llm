from __future__ import annotations

from app.auth import AuthorizationService
from app.providers import CloudOperations
from app.repositories import ProjectRepository, ResourceRepository


class ProjectNotFoundError(LookupError):
    pass


class ProjectService:
    def __init__(
        self,
        projects: ProjectRepository,
        resources: ResourceRepository,
        authorization: AuthorizationService,
        cloud: CloudOperations,
    ) -> None:
        self.projects = projects
        self.resources = resources
        self.authorization = authorization
        self.cloud = cloud

    def delete_project(self, actor_id: str, project_id: str) -> None:
        project = self.projects.get(project_id)
        if project is None:
            raise ProjectNotFoundError(project_id)

        self.authorization.assert_project_owner(actor_id, project)

        resources = self.resources.find_by_project(project_id)
        for resource in resources:
            self.cloud.delete_external_resource(project.provider, resource.external_id)
            self.resources.delete(resource.id)

        self.projects.delete(project_id)
