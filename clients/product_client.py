from __future__ import annotations

import allure
from httpx import Response

from clients.base_client import BaseClient
from schema.product import GetProductRequestSchema, GetProjectTypesRequestSchema
from tools.routes import ProductRoutes


class ProductClient(BaseClient):
    """Клиент для Product сервиса Kaleidoo API."""

    @allure.step("Product: get products")
    async def get_products(self) -> Response:
        return await self.post(ProductRoutes.GET_PRODUCTS, json={})

    @allure.step("Product: get product by id")
    async def get_product(self, payload: GetProductRequestSchema) -> Response:
        return await self.post(ProductRoutes.GET_PRODUCT, json=payload.model_dump(exclude_none=True))

    @allure.step("Product: get project types")
    async def get_project_types(self, payload: GetProjectTypesRequestSchema) -> Response:
        return await self.post(ProductRoutes.GET_PROJECT_TYPES, json=payload.model_dump(exclude_none=True))

    @allure.step("Product: get all project types")
    async def get_all_project_types(self) -> Response:
        return await self.post(ProductRoutes.GET_ALL_PROJECT_TYPES, json={})
