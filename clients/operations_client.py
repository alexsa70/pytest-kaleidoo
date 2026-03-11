from __future__ import annotations

import allure
from httpx import Response

from clients.base_client import BaseClient
from schema.operations import CreateResourceSchema, ResourceSchema, UpdateResourceSchema
from tools.routes import APIRoutes


class ResourceClient(BaseClient):
    """Шаблонный асинхронный клиент для CRUD-операций с ресурсом."""

    @allure.step("Get resources list")
    async def list_resources_api(self) -> Response:
        return await self.get(APIRoutes.RESOURCES)

    @allure.step("Get resource by id {resource_id}")
    async def get_resource_api(self, resource_id: str | int) -> Response:
        return await self.get(f"{APIRoutes.RESOURCES}/{resource_id}")

    @allure.step("Create resource")
    async def create_resource_api(self, payload: CreateResourceSchema) -> Response:
        return await self.post(
            APIRoutes.RESOURCES,
            json=payload.model_dump(mode="json", by_alias=True),
        )

    @allure.step("Update resource by id {resource_id}")
    async def update_resource_api(
        self,
        resource_id: str | int,
        payload: UpdateResourceSchema,
    ) -> Response:
        return await self.patch(
            f"{APIRoutes.RESOURCES}/{resource_id}",
            json=payload.model_dump(mode="json", by_alias=True, exclude_none=True),
        )

    @allure.step("Delete resource by id {resource_id}")
    async def delete_resource_api(self, resource_id: str | int) -> Response:
        return await self.delete(f"{APIRoutes.RESOURCES}/{resource_id}")

    async def create_resource(self) -> ResourceSchema:
        """Вспомогательный метод для создания сущности из дефолтного payload."""

        payload = CreateResourceSchema()
        response = await self.create_resource_api(payload)
        return ResourceSchema.model_validate_json(response.text)
