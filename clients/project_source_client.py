from __future__ import annotations

import allure
from httpx import Response

from clients.base_client import BaseClient
from schema.project_source import (
    ConnectSyncRequestSchema,
    CreateAuthUrlRequestSchema,
    CreateConnectorRequestSchema,
    CreateScanTasksRequestSchema,
    DeleteSourceRequestSchema,
    DisconnectSyncRequestSchema,
    ListByOrgRequestSchema,
    UpdateSyncHourRequestSchema,
    ValidateSourcePathRequestSchema,
)
from tools.routes import ProjectSourceRoutes


class ProjectSourceClient(BaseClient):
    """Клиент для Connectors - Project Source сервиса Kaleidoo API."""

    @allure.step("ProjectSource: create auth URL")
    async def create_auth_url(self, payload: CreateAuthUrlRequestSchema) -> Response:
        return await self.post(ProjectSourceRoutes.CREATE_AUTH_URL, json=payload.model_dump(exclude_none=True))

    @allure.step("ProjectSource: create connector")
    async def create_connector(self, payload: CreateConnectorRequestSchema) -> Response:
        return await self.post(ProjectSourceRoutes.CREATE_CONNECTOR, json=payload.model_dump(exclude_none=True))

    @allure.step("ProjectSource: create scan tasks")
    async def create_scan_tasks(self, payload: CreateScanTasksRequestSchema) -> Response:
        return await self.post(ProjectSourceRoutes.CREATE_SCAN_TASKS, json=payload.model_dump(exclude_none=True))

    @allure.step("ProjectSource: list by org")
    async def list_by_org(self, payload: ListByOrgRequestSchema | None = None) -> Response:
        body = payload.model_dump(exclude_none=True) if payload else {}
        return await self.post(ProjectSourceRoutes.LIST_BY_ORG, json=body)

    @allure.step("ProjectSource: delete source")
    async def delete(self, payload: DeleteSourceRequestSchema) -> Response:
        return await self.post(ProjectSourceRoutes.DELETE, json=payload.model_dump(exclude_none=True))

    @allure.step("ProjectSource: connect sync")
    async def connect_sync(self, payload: ConnectSyncRequestSchema) -> Response:
        return await self.post(ProjectSourceRoutes.CONNECT_SYNC, json=payload.model_dump(exclude_none=True))

    @allure.step("ProjectSource: disconnect sync")
    async def disconnect_sync(self, payload: DisconnectSyncRequestSchema) -> Response:
        return await self.post(ProjectSourceRoutes.DISCONNECT_SYNC, json=payload.model_dump(exclude_none=True))

    @allure.step("ProjectSource: update sync hour")
    async def update_sync_hour(self, payload: UpdateSyncHourRequestSchema) -> Response:
        return await self.post(ProjectSourceRoutes.UPDATE_SYNC_HOUR, json=payload.model_dump(exclude_none=True))

    @allure.step("ProjectSource: validate source path")
    async def validate_source_path(self, payload: ValidateSourcePathRequestSchema) -> Response:
        return await self.post(ProjectSourceRoutes.VALIDATE_SOURCE_PATH, json=payload.model_dump(exclude_none=True))

    @allure.step("ProjectSource: get supported file types")
    async def get_supported_file_types(self) -> Response:
        return await self.post(ProjectSourceRoutes.GET_SUPPORTED_FILE_TYPES, json={})
