from enum import Enum
from typing import Optional, Literal

from pydantic import BaseModel, HttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class HTTPClientConfig(BaseModel):
    """Настройки HTTP-клиента."""

    url: HttpUrl
    timeout: float

    @property
    def client_url(self) -> str:
        return str(self.url)


class AuthCredentialsConfig(BaseModel):
    email: str
    password: str
    otp_secret: Optional[str] = None


class Environment(str, Enum):
    local = "local"
    qa = "qa"
    staging = "staging"
    prod = "prod"
    on_premise = "on_premise"


class Profile(str, Enum):
    api = "api"
    e2e = "e2e"


class ProjectSettings(BaseSettings):
    """Базовые настройки проекта, загружаются из `.env`."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter=".",
        extra="ignore",
    )

    profile: Profile = Profile.api
    environment: Environment = Environment.local


class APISettings(ProjectSettings):
    profile: Literal["api"] = "api"
    api_http_client: HTTPClientConfig
    auth_credentials: Optional[AuthCredentialsConfig] = None
    auth_credentials_super_admin: Optional[AuthCredentialsConfig] = None
    auth_credentials_admin: Optional[AuthCredentialsConfig] = None
    auth_credentials_user: Optional[AuthCredentialsConfig] = None
    user_name: Optional[str] = None
    user_id: Optional[str] = None
    user_role_id: Optional[str] = None
    user_base_url: Optional[str] = None
    org_name: Optional[str] = None

    # Org-specific config (вынесено из тестов)
    org_role_id: Optional[str] = None

    # Активная роль для запуска тестов. Переопределяется через ACTIVE_ROLE=admin pytest ...
    active_role: Literal["super_admin", "admin", "user"] = "admin"


class E2ESettings(ProjectSettings):
    profile: Literal["e2e"] = "e2e"
    e2e_base_url: Optional[HttpUrl] = None
