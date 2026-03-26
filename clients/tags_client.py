from __future__ import annotations

import allure
from httpx import Response

from clients.base_client import BaseClient
from schema.tags import (
    CreateTagRequestSchema,
    DeleteTagRequestSchema,
    GetObjectsByTagNameRequestSchema,
    GetObjectsByTagsRequestSchema,
    GetTagRequestSchema,
    GetTagsByObjectIdRequestSchema,
    GetTagsRequestSchema,
    TagFilesRequestSchema,
    TagFoldersRequestSchema,
    TagPromoteDemoteRequestSchema,
    UnlinkTagFilesRequestSchema,
    UnlinkTagFoldersRequestSchema,
    UpdateTagRequestSchema,
)
from tools.routes import TagIngestRoutes, TagQueryRoutes


class TagsClient(BaseClient):
    """Клиент для Tag сервиса Kaleidoo API."""

    # ── Ingest ─────────────────────────────────────────────────────────────────

    @allure.step("Tags: create")
    async def create(self, payload: CreateTagRequestSchema) -> Response:
        return await self.post(TagIngestRoutes.CREATE, json=payload.model_dump(exclude_none=True))

    @allure.step("Tags: update")
    async def update(self, payload: UpdateTagRequestSchema) -> Response:
        return await self.post(TagIngestRoutes.UPDATE, json=payload.model_dump(exclude_none=True))

    @allure.step("Tags: delete")
    async def delete(self, payload: DeleteTagRequestSchema) -> Response:
        return await self.post(TagIngestRoutes.DELETE, json=payload.model_dump(exclude_none=True))

    @allure.step("Tags: tag files")
    async def tag_files(self, payload: TagFilesRequestSchema) -> Response:
        return await self.post(TagIngestRoutes.TAG_FILES, json=payload.model_dump(exclude_none=True))

    @allure.step("Tags: unlink tag files")
    async def unlink_tag_files(self, payload: UnlinkTagFilesRequestSchema) -> Response:
        return await self.post(TagIngestRoutes.UNLINK_TAG_FILES, json=payload.model_dump(exclude_none=True))

    @allure.step("Tags: tag folders")
    async def tag_folders(self, payload: TagFoldersRequestSchema) -> Response:
        return await self.post(TagIngestRoutes.TAG_FOLDERS, json=payload.model_dump(exclude_none=True))

    @allure.step("Tags: unlink tag folders")
    async def unlink_tag_folders(self, payload: UnlinkTagFoldersRequestSchema) -> Response:
        return await self.post(TagIngestRoutes.UNLINK_TAG_FOLDERS, json=payload.model_dump(exclude_none=True))

    @allure.step("Tags: promote to album")
    async def promote_to_album(self, payload: TagPromoteDemoteRequestSchema) -> Response:
        return await self.post(TagIngestRoutes.PROMOTE_TO_ALBUM, json=payload.model_dump(exclude_none=True))

    @allure.step("Tags: demote to regular")
    async def demote_to_regular(self, payload: TagPromoteDemoteRequestSchema) -> Response:
        return await self.post(TagIngestRoutes.DEMOTE_TO_REGULAR, json=payload.model_dump(exclude_none=True))

    # ── Query ──────────────────────────────────────────────────────────────────

    @allure.step("Tags: get tag")
    async def get(self, payload: GetTagRequestSchema) -> Response:
        return await self.post(TagQueryRoutes.GET, json=payload.model_dump(exclude_none=True))

    @allure.step("Tags: get tags")
    async def get_tags(self, payload: GetTagsRequestSchema | None = None) -> Response:
        body = payload.model_dump(exclude_none=True) if payload else {}
        return await self.post(TagQueryRoutes.GET_TAGS, json=body)

    @allure.step("Tags: get tags by object id")
    async def get_tags_by_object_id(self, payload: GetTagsByObjectIdRequestSchema) -> Response:
        return await self.post(TagQueryRoutes.GET_TAGS_BY_OBJECT_ID, json=payload.model_dump(exclude_none=True))

    @allure.step("Tags: get objects by tags")
    async def get_objects_by_tags(self, payload: GetObjectsByTagsRequestSchema) -> Response:
        return await self.post(TagQueryRoutes.GET_OBJECTS_BY_TAGS, json=payload.model_dump(exclude_none=True))

    @allure.step("Tags: get objects by tag name")
    async def get_objects_by_tag_name(self, payload: GetObjectsByTagNameRequestSchema) -> Response:
        return await self.post(TagQueryRoutes.GET_OBJECTS_BY_TAG_NAME, json=payload.model_dump(exclude_none=True))
