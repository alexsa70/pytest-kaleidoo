from enum import Enum


class AuthRoutes(str, Enum):
    """Authentication routes."""

    LOGIN = "/login"
    SSO_LOGIN = "/sso_login"
    RESET_PASSWORD = "/reset_password"
    SESSION_TOKEN = "/session_token"
    REFRESH_SESSION_TOKEN = "/refresh_session_token"

    def __str__(self) -> str:
        return self.value
