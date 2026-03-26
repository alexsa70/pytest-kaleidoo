from __future__ import annotations

from typing import AsyncIterator

import pytest
import pytest_asyncio

from clients.base_client import get_http_client
from clients.auth_client import AuthClient
from config import APISettings


@pytest.fixture(scope="session")
def auth_token(tokens_by_role: dict[str, str], settings: APISettings) -> str:
    """Токен активной роли (ACTIVE_ROLE из .env, по умолчанию super_admin). Создаётся один раз на сессию."""
    token = tokens_by_role.get(settings.active_role)
    if token is None:
        available = list(tokens_by_role.keys())
        if not available:
            pytest.skip("No tokens available. Configure credentials in .env")
        token = tokens_by_role[available[0]]
    return token


@pytest_asyncio.fixture
async def api_client(settings: APISettings, auth_token: str) -> AsyncIterator[AuthClient]:
    """AuthClient с токеном активной роли. Токен встроен в заголовки клиента."""
    async with get_http_client(settings.api_http_client, token=auth_token) as http_client:
        yield AuthClient(client=http_client)


@pytest_asyncio.fixture
async def api_client_no_auth(settings: APISettings) -> AsyncIterator[AuthClient]:
    """AuthClient без токена — для тестов 401/403."""
    async with get_http_client(settings.api_http_client) as http_client:
        yield AuthClient(client=http_client)
