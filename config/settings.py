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


class Environment(str, Enum):
    local = "local"
    staging = "staging"
    prod = "prod"


class Profile(str, Enum):
    api = "api"
    e2e = "e2e"


class ProjectSettings(BaseSettings):
    """Базовые настройки проекта, загружаются из `.env`."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter=".",
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

    # Org-specific config (вынесено из тестов)
    org_role_id: Optional[str] = None


class E2ESettings(ProjectSettings):
    profile: Literal["e2e"] = "e2e"
    e2e_base_url: Optional[HttpUrl] = None
