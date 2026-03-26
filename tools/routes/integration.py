from enum import Enum


class IntegrationRoutes(str, Enum):
    """Integration service routes."""

    CONVERSATION_EDITING = "/api/integration/v1/conversation_editing"

    def __str__(self) -> str:
        return self.value
