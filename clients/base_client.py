from __future__ import annotations

from typing import Any, AsyncIterator

import allure
from httpx import AsyncClient, URL, Response, QueryParams
from httpx._types import RequestData, RequestFiles

from clients.event_hooks import log_request_event_hook, log_response_event_hook
from config import HTTPClientConfig


class BaseClient:
    """
    Базовый асинхронный клиент для выполнения HTTP-запросов.
    """

    def __init__(self, client: AsyncClient):
        self.client = client

    @allure.step("Make GET request to {url}")
    async def get(self, url: URL | str, params: QueryParams | None = None, headers: dict | None = None) -> Response:
        return await self.client.get(url, params=params, headers=headers)

    @allure.step("Make POST request to {url}")
    async def post(
            self,
            url: URL | str,
            json: Any | None = None,
            data: RequestData | None = None,
            files: RequestFiles | None = None,
            headers: dict | None = None
    ) -> Response:
        return await self.client.post(url, json=json, data=data, files=files, headers=headers)

    @allure.step("Make PATCH request to {url}")
    async def patch(self, url: URL | str, json: Any | None = None) -> Response:
        return await self.client.patch(url, json=json)

    @allure.step("Make DELETE request to {url}")
    async def delete(self, url: URL | str) -> Response:
        return await self.client.delete(url)

    async def stream_sse(self, url: URL | str, json: Any | None = None, headers: dict | None = None) -> AsyncIterator[str]:
        """Стримит SSE события. Yields raw data-line содержимое."""
        _headers = {"Accept": "text/event-stream"}
        if headers:
            _headers.update(headers)
        async with self.client.stream("POST", url, json=json, headers=_headers) as response:
            async for line in response.aiter_lines():
                if line.startswith("data:"):
                    yield line[len("data:"):].strip()


def get_http_client(config: HTTPClientConfig) -> AsyncClient:
    """
    Создаёт экземпляр AsyncClient.
    Используй как async context manager в фикстурах:
        async with get_http_client(config) as client: ...
    """
    return AsyncClient(
        timeout=config.timeout,
        base_url=config.client_url,
        event_hooks={
            "request": [log_request_event_hook],
            "response": [log_response_event_hook]
        }
    )
