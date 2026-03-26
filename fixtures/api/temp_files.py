from __future__ import annotations

from typing import AsyncIterator

import pytest_asyncio

from clients.base_client import get_http_client
from clients.temp_files_client import TempFilesClient
from config import APISettings


@pytest_asyncio.fixture
async def temp_files_client(settings: APISettings, auth_token: str) -> AsyncIterator[TempFilesClient]:
    async with get_http_client(settings.api_http_client, token=auth_token) as http_client:
        yield TempFilesClient(client=http_client)
