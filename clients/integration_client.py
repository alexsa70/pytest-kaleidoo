from __future__ import annotations

import allure
from httpx import Response

from clients.base_client import BaseClient
from schema.integration import ConversationEditingRequestSchema
from tools.routes import IntegrationRoutes


class IntegrationClient(BaseClient):
    """Клиент для Integration сервиса Kaleidoo API."""

    @allure.step("Integration: conversation editing")
    async def conversation_editing(self, payload: ConversationEditingRequestSchema) -> Response:
        return await self.post(IntegrationRoutes.CONVERSATION_EDITING, json=payload.model_dump(exclude_none=True))
