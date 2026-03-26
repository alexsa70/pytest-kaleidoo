from __future__ import annotations

from typing import AsyncIterator

import pytest_asyncio

from clients.base_client import get_http_client
from clients.conversation_client import ConversationClient
from config import APISettings


@pytest_asyncio.fixture
async def conversation_client(settings: APISettings, auth_token: str) -> AsyncIterator[ConversationClient]:
    async with get_http_client(settings.api_http_client, token=auth_token) as http_client:
        yield ConversationClient(client=http_client)
