from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Project:
    id: str
    owner_id: str
    name: str
    provider: str
    status: str = "active"


@dataclass(frozen=True)
class Resource:
    id: str
    project_id: str
    external_id: str


@dataclass(frozen=True)
class Job:
    id: str
    kind: str
    status: str
    payload: str
    result: str | None
    created_at: str
    updated_at: str
