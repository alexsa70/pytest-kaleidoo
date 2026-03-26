from __future__ import annotations

from typing import Optional

import allure
from httpx import Response

from clients.base_client import BaseClient
from schema.manual_loader import DeleteManualFilesRequestSchema
from tools.routes import ManualLoaderRoutes


class ManualLoaderClient(BaseClient):
    """Клиент для Manual Loader сервиса Kaleidoo API."""

    @allure.step("ManualLoader: upload file")
    async def upload_manual_file(
        self,
        file_content: bytes,
        filename: str,
        content_type: str = "application/octet-stream",
        folder_id: Optional[str] = None,
    ) -> Response:
        files = {"file": (filename, file_content, content_type)}
        data = {}
        if folder_id:
            data["folder_id"] = folder_id
        return await self.post(ManualLoaderRoutes.UPLOAD_MANUAL_FILE, files=files, data=data)

    @allure.step("ManualLoader: delete files")
    async def delete_manual_files(self, payload: DeleteManualFilesRequestSchema) -> Response:
        return await self.post(ManualLoaderRoutes.DELETE_MANUAL_FILES, json=payload.model_dump(exclude_none=True))
