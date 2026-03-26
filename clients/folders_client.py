from __future__ import annotations

import allure
from httpx import Response

from clients.base_client import BaseClient
from schema.folders import (
    AssociateAgentsToFolderRequestSchema,
    AssociateAgentToFoldersRequestSchema,
    AssociateFilesRequestSchema,
    CreateFolderRequestSchema,
    DeleteFolderRequestSchema,
    DisassociateAgentsRequestSchema,
    DisassociateFilesRequestSchema,
    GetAgentsByFoldersRequestSchema,
    GetAllFoldersRequestSchema,
    GetFilesByFoldersRequestSchema,
    GetFolderRequestSchema,
    GetFoldersByAgentsRequestSchema,
    GetFoldersByFilesRequestSchema,
    GetFoldersRequestSchema,
    RemoveAutoSubfolderRequestSchema,
    UpdateFolderRequestSchema,
)
from tools.routes import FoldersRoutes


class FoldersClient(BaseClient):
    """Клиент для Folders сервиса Kaleidoo API."""

    @allure.step("Folders: get all")
    async def get_all(self, payload: GetAllFoldersRequestSchema | None = None) -> Response:
        body = payload.model_dump(exclude_none=True) if payload else {}
        return await self.post(FoldersRoutes.GET_ALL, json=body)

    @allure.step("Folders: get folders (paginated)")
    async def get_folders(self, payload: GetFoldersRequestSchema | None = None) -> Response:
        body = payload.model_dump(exclude_none=True) if payload else {}
        return await self.post(FoldersRoutes.GET_FOLDERS, json=body)

    @allure.step("Folders: get folder")
    async def get(self, payload: GetFolderRequestSchema) -> Response:
        return await self.post(FoldersRoutes.GET, json=payload.model_dump(exclude_none=True))

    @allure.step("Folders: create")
    async def create(self, payload: CreateFolderRequestSchema) -> Response:
        return await self.post(FoldersRoutes.CREATE, json=payload.model_dump(exclude_none=True))

    @allure.step("Folders: update")
    async def update(self, payload: UpdateFolderRequestSchema) -> Response:
        return await self.post(FoldersRoutes.UPDATE, json=payload.model_dump(exclude_none=True))

    @allure.step("Folders: delete")
    async def delete(self, payload: DeleteFolderRequestSchema) -> Response:
        return await self.post(FoldersRoutes.DELETE, json=payload.model_dump(exclude_none=True))

    @allure.step("Folders: associate files to folder")
    async def associate_files(self, payload: AssociateFilesRequestSchema) -> Response:
        return await self.post(FoldersRoutes.ASSOCIATE_FILES, json=payload.model_dump(exclude_none=True))

    @allure.step("Folders: disassociate files from folder")
    async def disassociate_files(self, payload: DisassociateFilesRequestSchema) -> Response:
        return await self.post(FoldersRoutes.DISASSOCIATE_FILES, json=payload.model_dump(exclude_none=True))

    @allure.step("Folders: get files by folders")
    async def get_files_by_folders(self, payload: GetFilesByFoldersRequestSchema) -> Response:
        return await self.post(FoldersRoutes.GET_FILES_BY_FOLDERS, json=payload.model_dump(exclude_none=True))

    @allure.step("Folders: get folders by files")
    async def get_folders_by_files(self, payload: GetFoldersByFilesRequestSchema) -> Response:
        return await self.post(FoldersRoutes.GET_FOLDERS_BY_FILES, json=payload.model_dump(exclude_none=True))

    @allure.step("Folders: associate agents to folder")
    async def associate_agents(self, payload: AssociateAgentsToFolderRequestSchema) -> Response:
        return await self.post(FoldersRoutes.ASSOCIATE_AGENTS, json=payload.model_dump(exclude_none=True))

    @allure.step("Folders: associate agent to folders")
    async def associate_agent_to_folders(self, payload: AssociateAgentToFoldersRequestSchema) -> Response:
        return await self.post(FoldersRoutes.ASSOCIATE_AGENT_TO_FOLDERS, json=payload.model_dump(exclude_none=True))

    @allure.step("Folders: disassociate agents from folder")
    async def disassociate_agents(self, payload: DisassociateAgentsRequestSchema) -> Response:
        return await self.post(FoldersRoutes.DISASSOCIATE_AGENTS, json=payload.model_dump(exclude_none=True))

    @allure.step("Folders: get agents by folders")
    async def get_agents_by_folders(self, payload: GetAgentsByFoldersRequestSchema) -> Response:
        return await self.post(FoldersRoutes.GET_AGENTS_BY_FOLDERS, json=payload.model_dump(exclude_none=True))

    @allure.step("Folders: get folders by agents")
    async def get_folders_by_agents(self, payload: GetFoldersByAgentsRequestSchema) -> Response:
        return await self.post(FoldersRoutes.GET_FOLDERS_BY_AGENTS, json=payload.model_dump(exclude_none=True))

    @allure.step("Folders: remove auto subfolder")
    async def remove_auto_subfolder(self, payload: RemoveAutoSubfolderRequestSchema) -> Response:
        return await self.post(FoldersRoutes.REMOVE_AUTO_SUBFOLDER, json=payload.model_dump(exclude_none=True))
