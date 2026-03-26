from enum import Enum


class ConversationRoutes(str, Enum):
    """User Conversation service routes."""

    CREATE = "/api/user_conversation/v1/create"
    GET = "/api/user_conversation/v1/get"
    GET_ALL = "/api/user_conversation/v1/get_all"
    DELETE = "/api/user_conversation/v1/delete"
    SEARCH = "/api/user_conversation/v1/search"

    def __str__(self) -> str:
        return self.value
