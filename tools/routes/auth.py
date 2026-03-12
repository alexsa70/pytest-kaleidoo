from enum import Enum


class AuthRoutes(str, Enum):
    """Authentication routes."""

    AUTHENTICATE = "/authenticate"
    SSO_LOGIN = "/sso_login"
    RESET_PASSWORD = "/reset_password"

    def __str__(self) -> str:
        return self.value
