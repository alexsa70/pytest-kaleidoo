from __future__ import annotations

import allure
from httpx import Response

from clients.base_client import BaseClient
from schema.conversation import (
    ConversationCreateRequestSchema,
    ConversationDeleteRequestSchema,
    ConversationGetAllRequestSchema,
    ConversationGetRequestSchema,
    ConversationSearchRequestSchema,
)
from tools.routes import ConversationRoutes


class ConversationClient(BaseClient):
    """Клиент для User Conversation эндпоинтов Kaleidoo API."""

    @allure.step("Conversation: create")
    async def create(self, payload: ConversationCreateRequestSchema) -> Response:
        return await self.post(ConversationRoutes.CREATE, json=payload.model_dump(exclude_none=True))

    @allure.step("Conversation: get messages")
    async def get(self, payload: ConversationGetRequestSchema) -> Response:
        return await self.post(ConversationRoutes.GET, json=payload.model_dump(exclude_none=True))

    @allure.step("Conversation: get all")
    async def get_all(self, payload: ConversationGetAllRequestSchema | None = None) -> Response:
        body = payload.model_dump(exclude_none=True) if payload else {}
        return await self.post(ConversationRoutes.GET_ALL, json=body)

    @allure.step("Conversation: delete")
    async def delete(self, payload: ConversationDeleteRequestSchema) -> Response:
        return await self.post(ConversationRoutes.DELETE, json=payload.model_dump(exclude_none=True))

    @allure.step("Conversation: search")
    async def search(self, payload: ConversationSearchRequestSchema) -> Response:
        return await self.post(ConversationRoutes.SEARCH, json=payload.model_dump(exclude_none=True))
