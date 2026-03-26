from __future__ import annotations

import allure
from httpx import Response

from clients.base_client import BaseClient
from schema.temp_files import TempFileCleanupRequestSchema, TempFileGetRequestSchema
from tools.routes import TempFilesRoutes


class TempFilesClient(BaseClient):
    """Клиент для Temporary Files сервиса Kaleidoo API."""

    @allure.step("TempFiles: get file status")
    async def get_file(self, payload: TempFileGetRequestSchema) -> Response:
        return await self.post(TempFilesRoutes.GET_FILE, json=payload.model_dump(exclude_none=True))

    @allure.step("TempFiles: cleanup")
    async def cleanup(self, payload: TempFileCleanupRequestSchema) -> Response:
        return await self.post(TempFilesRoutes.CLEANUP, json=payload.model_dump(exclude_none=True))
