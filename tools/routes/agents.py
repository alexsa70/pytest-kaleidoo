from enum import Enum


class AgentsRoutes(str, Enum):
    """Agents service routes."""

    CREATE = "/api/agents/create"
    GET = "/api/agents/get"
    GET_ALL = "/api/agents/get_all"
    UPDATE = "/api/agents/update"
    DELETE = "/api/agents/delete"

    def __str__(self) -> str:
        return self.value
