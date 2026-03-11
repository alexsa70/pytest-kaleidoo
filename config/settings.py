from pydantic import BaseModel, HttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class HTTPClientConfig(BaseModel):
    """Настройки HTTP-клиента."""

    url: HttpUrl
    timeout: float

    @property
    def client_url(self) -> str:
        return str(self.url)


class Settings(BaseSettings):
    """Настройки проекта, загружаются из `.env`."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter=".",
    )

    api_http_client: HTTPClientConfig
