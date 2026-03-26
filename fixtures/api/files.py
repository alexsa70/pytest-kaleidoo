from __future__ import annotations

from typing import AsyncIterator

import pytest_asyncio

from clients.base_client import get_http_client
from clients.files_client import FilesClient
from config import APISettings


@pytest_asyncio.fixture
async def files_client(settings: APISettings, auth_token: str) -> AsyncIterator[FilesClient]:
    async with get_http_client(settings.api_http_client, token=auth_token) as http_client:
        yield FilesClient(client=http_client)
