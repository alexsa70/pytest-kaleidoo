from enum import Enum


class UserRoutes(str, Enum):
    """User service routes."""

    USER_RETRIEVE = "/api/user/get"
    USER_GET_BY_ID = "/api/user/get_by_id"
    USER_UPDATE = "/api/user/update"
    USER_CREATE = "/api/user/create"
    USER_DELETE = "/api/user/delete"
    USER_GET_ALL = "/api/user/get_all"
    USER_GET_ROLES = "/api/user/get_roles"
    USER_UNLOCK = "/api/user/unlock_user"
    USER_RESET_MFA = "/api/user/reset_user_mfa"

    def __str__(self) -> str:
        return self.value
