from __future__ import annotations

import allure
from httpx import Response

from clients.base_client import BaseClient
from schema.files import (
    EditFilesPermissionsRequestSchema,
    GetFileDetailsRequestSchema,
    GetFileMetadataRequestSchema,
    GetFilePermissionsRequestSchema,
    GetFilesByIdsRequestSchema,
    GetFilesRequestSchema,
    UpdateFileDetailsRequestSchema,
)
from tools.routes import FilesRoutes


class FilesClient(BaseClient):
    """Клиент для Files сервиса Kaleidoo API."""

    @allure.step("Files: get file metadata")
    async def get_file_metadata(self, payload: GetFileMetadataRequestSchema) -> Response:
        return await self.post(FilesRoutes.GET_FILE_METADATA, json=payload.model_dump(exclude_none=True))

    @allure.step("Files: get file details")
    async def get_file_details(self, payload: GetFileDetailsRequestSchema) -> Response:
        return await self.post(FilesRoutes.GET_FILE_DETAILS, json=payload.model_dump(exclude_none=True))

    @allure.step("Files: get files")
    async def get_files(self, payload: GetFilesRequestSchema | None = None) -> Response:
        body = payload.model_dump(exclude_none=True) if payload else {}
        return await self.post(FilesRoutes.GET_FILES, json=body)

    @allure.step("Files: get files by ids")
    async def get_files_by_ids(self, payload: GetFilesByIdsRequestSchema) -> Response:
        return await self.post(FilesRoutes.GET_FILES_BY_IDS, json=payload.model_dump(exclude_none=True))

    @allure.step("Files: update file details")
    async def update_file_details(self, payload: UpdateFileDetailsRequestSchema) -> Response:
        return await self.post(FilesRoutes.UPDATE_FILE_DETAILS, json=payload.model_dump(exclude_none=True))

    @allure.step("Files: edit files permissions")
    async def edit_files_permissions(self, payload: EditFilesPermissionsRequestSchema) -> Response:
        return await self.post(FilesRoutes.EDIT_FILES_PERMISSIONS, json=payload.model_dump(exclude_none=True))

    @allure.step("Files: get file permissions")
    async def get_file_permissions(self, payload: GetFilePermissionsRequestSchema) -> Response:
        return await self.post(FilesRoutes.GET_FILE_PERMISSIONS, json=payload.model_dump(exclude_none=True))
