from typing import AsyncIterator

import pyotp
import pytest
import pytest_asyncio
from http import HTTPStatus

from clients.base_client import get_http_client
from clients.operations_client import APIClient
from config import APISettings
from schema.operations import LoginRequestSchema, SSOLoginResponseSchema
from tools.assertions.base import assert_status_code


@pytest_asyncio.fixture
async def api_client(settings: APISettings) -> AsyncIterator[APIClient]:
    """Создает общий async HTTP-клиент и оборачивает его в APIClient."""

    async with get_http_client(settings.api_http_client) as http_client:
        yield APIClient(client=http_client)


@pytest.fixture(scope="session")
def auth_payload(settings: APISettings) -> LoginRequestSchema:
    """Формирует payload для POST /login из переменных окружения."""

    if settings.auth_credentials is None:
        pytest.skip("AUTH_CREDENTIALS не настроены в .env")

    otp_code = None
    if settings.auth_credentials.otp_secret:
        otp_code = pyotp.TOTP(settings.auth_credentials.otp_secret).now()

    return LoginRequestSchema(
        orgName=settings.org_name or "",
        identity=settings.auth_credentials.email,
        password=settings.auth_credentials.password,
        otp_code=otp_code,
    )


@pytest_asyncio.fixture(scope="session", loop_scope="session")
async def auth_token(
    settings: APISettings,
    auth_payload: LoginRequestSchema,
) -> str:
    """Получает token один раз на сессию тестов."""

    async with get_http_client(settings.api_http_client) as http_client:
        client = APIClient(client=http_client)
        response = await client.login(auth_payload)
        assert_status_code(response.status_code, HTTPStatus.OK)
        data = response.json()
        if isinstance(data, dict) and data.get("mfa_required"):
            pytest.skip("MFA required but AUTH_CREDENTIALS.OTP_SECRET is not set in .env")
        auth_response = SSOLoginResponseSchema.model_validate(data)
        return auth_response.token
