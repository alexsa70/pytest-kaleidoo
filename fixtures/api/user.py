from __future__ import annotations

from typing import AsyncIterator

import pytest_asyncio

from clients.base_client import get_http_client
from clients.user_client import UserClient
from config import APISettings


@pytest_asyncio.fixture
async def user_client(settings: APISettings, auth_token: str) -> AsyncIterator[UserClient]:
    async with get_http_client(settings.api_http_client, token=auth_token) as http_client:
        yield UserClient(client=http_client)
