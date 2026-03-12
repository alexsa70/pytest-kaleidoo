from typing import AsyncIterator

import pytest
import pytest_asyncio
from http import HTTPStatus

from clients.base_client import get_http_client
from clients.operations_client import APIClient
from config import APISettings
from schema.operations import AuthenticateRequestSchema, AuthenticateResponseSchema
from tools.assertions.base import assert_status_code


@pytest_asyncio.fixture
async def api_client(settings: APISettings) -> AsyncIterator[APIClient]:
    """Создает общий async HTTP-клиент и оборачивает его в APIClient."""

    async with get_http_client(settings.api_http_client) as http_client:
        yield APIClient(client=http_client)


@pytest.fixture(scope="session")
def auth_payload(settings: APISettings) -> AuthenticateRequestSchema:
    """Формирует payload для POST /authenticate из переменных окружения."""

    if settings.auth_credentials is None:
        pytest.skip("AUTH_CREDENTIALS не настроены в .env")

    return AuthenticateRequestSchema(
        email=settings.auth_credentials.email,
        password=settings.auth_credentials.password,
    )


@pytest_asyncio.fixture(scope="session", loop_scope="session")
async def auth_token(
    settings: APISettings,
    auth_payload: AuthenticateRequestSchema,
) -> str:
    """Получает token один раз на сессию тестов."""

    async with get_http_client(settings.api_http_client) as http_client:
        client = APIClient(client=http_client)
        response = await client.authenticate_api(auth_payload)
        assert_status_code(response.status_code, HTTPStatus.OK)
        auth_response = AuthenticateResponseSchema.model_validate_json(response.text)
        return auth_response.data.token
