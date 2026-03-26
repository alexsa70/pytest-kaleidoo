from __future__ import annotations

from typing import AsyncIterator

import pytest_asyncio

from clients.base_client import get_http_client
from clients.connectors_client import ConnectorsClient
from config import APISettings


@pytest_asyncio.fixture
async def connectors_client(settings: APISettings, auth_token: str) -> AsyncIterator[ConnectorsClient]:
    async with get_http_client(settings.api_http_client, token=auth_token) as http_client:
        yield ConnectorsClient(client=http_client)
