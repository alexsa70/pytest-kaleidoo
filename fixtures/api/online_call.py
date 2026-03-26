from __future__ import annotations

from typing import AsyncIterator

import pytest_asyncio

from clients.base_client import get_http_client
from clients.online_call_client import OnlineCallClient
from config import APISettings


@pytest_asyncio.fixture
async def online_call_client(settings: APISettings, auth_token: str) -> AsyncIterator[OnlineCallClient]:
    async with get_http_client(settings.api_http_client, token=auth_token) as http_client:
        yield OnlineCallClient(client=http_client)
