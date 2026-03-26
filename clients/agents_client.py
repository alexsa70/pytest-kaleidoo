from __future__ import annotations

import allure
from httpx import Response

from clients.base_client import BaseClient
from schema.agents import (
    CreateAgentRequestSchema,
    DeleteAgentRequestSchema,
    GetAgentRequestSchema,
    GetAllAgentsRequestSchema,
    UpdateAgentRequestSchema,
)
from tools.routes import AgentsRoutes


class AgentsClient(BaseClient):
    """Клиент для Agents сервиса Kaleidoo API."""

    @allure.step("Agents: create")
    async def create(self, payload: CreateAgentRequestSchema) -> Response:
        return await self.post(AgentsRoutes.CREATE, json=payload.model_dump(exclude_none=True))

    @allure.step("Agents: get")
    async def get(self, payload: GetAgentRequestSchema) -> Response:
        return await self.post(AgentsRoutes.GET, json=payload.model_dump(exclude_none=True))

    @allure.step("Agents: get all")
    async def get_all(self, payload: GetAllAgentsRequestSchema | None = None) -> Response:
        body = payload.model_dump(exclude_none=True) if payload else {}
        return await self.post(AgentsRoutes.GET_ALL, json=body)

    @allure.step("Agents: update")
    async def update(self, payload: UpdateAgentRequestSchema) -> Response:
        return await self.post(AgentsRoutes.UPDATE, json=payload.model_dump(exclude_none=True))

    @allure.step("Agents: delete")
    async def delete(self, payload: DeleteAgentRequestSchema) -> Response:
        return await self.post(AgentsRoutes.DELETE, json=payload.model_dump(exclude_none=True))
