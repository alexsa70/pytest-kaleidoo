from enum import Enum


class OrgRoutes(str, Enum):
    """Organization routes."""

    ORG_CREATE = "/api/org/create"

    def __str__(self) -> str:
        return self.value
