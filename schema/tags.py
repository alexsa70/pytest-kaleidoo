from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict


# ── Tag Schema ─────────────────────────────────────────────────────────────────

class TagSchema(BaseModel):
    id: str
    name: str
    type: str
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    object_count: Optional[int] = None

    model_config = ConfigDict(extra="ignore")


# ── Create Tag ─────────────────────────────────────────────────────────────────

class CreateTagRequestSchema(BaseModel):
    tag_names: list[str]
    tag_type: Optional[str] = None


class CreateTagResponseSchema(BaseModel):
    message: str
    created_tags: list[TagSchema]
    total_created: int
    duplicates_skipped: Optional[int] = None

    model_config = ConfigDict(extra="ignore")


# ── Update Tag ─────────────────────────────────────────────────────────────────

class UpdateTagRequestSchema(BaseModel):
    tag_id: str
    name: str


# ── Delete Tag ─────────────────────────────────────────────────────────────────

class DeleteTagRequestSchema(BaseModel):
    tag_id: str


class DeleteTagResponseSchema(BaseModel):
    message: str
    deleted_associations: Optional[int] = None

    model_config = ConfigDict(extra="ignore")


# ── Get Tag ────────────────────────────────────────────────────────────────────

class GetTagRequestSchema(BaseModel):
    name: str
    type: Optional[str] = None


# ── Get Tags ───────────────────────────────────────────────────────────────────

class GetTagsRequestSchema(BaseModel):
    type: Optional[str] = None
    limit: Optional[int] = None
    cursor: Optional[str] = None


class GetTagsResponseSchema(BaseModel):
    tags: list[TagSchema]
    cursor: Optional[str] = None
    has_more: Optional[bool] = None
    total_count: Optional[int] = None

    model_config = ConfigDict(extra="ignore")


# ── Tag Files ──────────────────────────────────────────────────────────────────

class TagFilesRequestSchema(BaseModel):
    file_ids: list[str]
    tag_ids: Optional[list[str]] = None
    tag_names: Optional[list[str]] = None


class TagFilesResponseSchema(BaseModel):
    message: str
    linked_count: Optional[int] = None
    files_tagged: Optional[int] = None
    tags_used: Optional[int] = None

    model_config = ConfigDict(extra="ignore")


# ── Unlink Tag Files ───────────────────────────────────────────────────────────

class UnlinkTagFilesRequestSchema(BaseModel):
    file_ids: list[str]
    tag_ids: list[str]


# ── Tag Folders ────────────────────────────────────────────────────────────────

class TagFoldersRequestSchema(BaseModel):
    folder_ids: list[str]
    tag_ids: Optional[list[str]] = None
    tag_names: Optional[list[str]] = None


# ── Unlink Tag Folders ─────────────────────────────────────────────────────────

class UnlinkTagFoldersRequestSchema(BaseModel):
    folder_ids: list[str]
    tag_ids: list[str]


# ── Get Tags by Object ID ──────────────────────────────────────────────────────

class GetTagsByObjectIdRequestSchema(BaseModel):
    object_id: Optional[str] = None
    objects: Optional[list[str]] = None
    object_type: Optional[str] = None
    limit: Optional[int] = None
    limit_per_object: Optional[int] = None
    cursor: Optional[str] = None


# ── Get Objects by Tags ────────────────────────────────────────────────────────

class GetObjectsByTagsRequestSchema(BaseModel):
    tag_ids: list[str]
    object_type: Optional[str] = None
    limit: Optional[int] = None
    cursor: Optional[str] = None


# ── Get Objects by Tag Name ────────────────────────────────────────────────────

class GetObjectsByTagNameRequestSchema(BaseModel):
    tag_name: str
    tag_type: Optional[str] = None
    limit: Optional[int] = None
    cursor: Optional[str] = None


# ── Promote / Demote ───────────────────────────────────────────────────────────

class TagPromoteDemoteRequestSchema(BaseModel):
    tag_id: str
