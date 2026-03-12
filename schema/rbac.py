from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field


RoleName = Literal["super_admin", "admin", "user"]


class AccessRule(BaseModel):
    """Rule for role-based access checks."""

    name: str
    method: str
    path: str
    allowed_roles: list[RoleName] = Field(default_factory=list)
    denied_roles: list[RoleName] = Field(default_factory=list)
    expected_allowed_status: int = 200
    expected_denied_status: int = 403
    json_body: dict[str, Any] | None = None
    data: dict[str, Any] | None = None
    params: dict[str, Any] | None = None
