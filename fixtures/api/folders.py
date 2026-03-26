from __future__ import annotations

from typing import AsyncIterator

import pytest_asyncio

from clients.base_client import get_http_client
from clients.folders_client import FoldersClient
from config import APISettings


@pytest_asyncio.fixture
async def folders_client(settings: APISettings, auth_token: str) -> AsyncIterator[FoldersClient]:
    async with get_http_client(settings.api_http_client, token=auth_token) as http_client:
        yield FoldersClient(client=http_client)
