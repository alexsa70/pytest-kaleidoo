from typing import AsyncIterator

import pytest
import pytest_asyncio

from clients.base_client import get_http_client
from clients.operations_client import ResourceClient
from config import Settings
from schema.operations import CreateResourceSchema


@pytest_asyncio.fixture
async def resource_client(settings: Settings) -> AsyncIterator[ResourceClient]:
    """Создает общий async HTTP-клиент и оборачивает его в ResourceClient."""

    async with get_http_client(settings.api_http_client) as http_client:
        yield ResourceClient(client=http_client)


@pytest.fixture
def sample_resource_payload() -> CreateResourceSchema:
    """Возвращает шаблонный payload для POST-запросов."""

    return CreateResourceSchema()
