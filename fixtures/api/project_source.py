from __future__ import annotations

from typing import AsyncIterator

import pytest_asyncio

from clients.base_client import get_http_client
from clients.project_source_client import ProjectSourceClient
from config import APISettings


@pytest_asyncio.fixture
async def project_source_client(settings: APISettings, auth_token: str) -> AsyncIterator[ProjectSourceClient]:
    async with get_http_client(settings.api_http_client, token=auth_token) as http_client:
        yield ProjectSourceClient(client=http_client)
