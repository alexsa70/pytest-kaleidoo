from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, ConfigDict


# ── File Metadata ──────────────────────────────────────────────────────────────

class FileMetadataSchema(BaseModel):
    id: str
    name: str
    mime_type: Optional[str] = None
    size: Optional[int] = None
    product: Optional[str] = None
    category: Optional[str] = None
    provider: Optional[str] = None
    folder_id: Optional[str] = None
    url: Optional[str] = None
    thumbnail_url: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    created_at_source: Optional[str] = None
    language: Optional[str] = None
    is_client_ready: Optional[bool] = None
    duration: Optional[float] = None

    model_config = ConfigDict(extra="ignore")


# ── Get File Metadata ──────────────────────────────────────────────────────────

class GetFileMetadataRequestSchema(BaseModel):
    file_id: Optional[str] = None
    external_id: Optional[str] = None


# ── Get File Details ───────────────────────────────────────────────────────────

class GetFileDetailsRequestSchema(BaseModel):
    file_id: Optional[str] = None
    external_id: Optional[str] = None
    fields: list[str]


class FileDetailsResponseSchema(BaseModel):
    file_id: str
    summary: Optional[str] = None
    topic: Optional[str] = None
    user_description: Optional[str] = None
    table_preview: Optional[Any] = None

    model_config = ConfigDict(extra="ignore")


# ── Get Files ──────────────────────────────────────────────────────────────────

class GetFilesRequestSchema(BaseModel):
    products: Optional[list[str]] = None
    category: Optional[str] = None
    provider: Optional[str] = None
    folder_id: Optional[str] = None
    folder_ids: Optional[list[str]] = None
    date_from: Optional[str] = None
    date_to: Optional[str] = None
    show_only_ready: Optional[bool] = None
    limit: Optional[int] = None
    cursor: Optional[str] = None
    data_fields: Optional[list[str]] = None


class GetFilesResponseSchema(BaseModel):
    files: list[FileMetadataSchema]
    cursor: Optional[str] = None
    has_more: Optional[bool] = None
    total_count: Optional[int] = None

    model_config = ConfigDict(extra="ignore")


# ── Get Files by IDs ───────────────────────────────────────────────────────────

class GetFilesByIdsRequestSchema(BaseModel):
    files: Optional[list[str]] = None
    external_ids: Optional[list[str]] = None
    fields: Optional[list[str]] = None
    sign_url: Optional[bool] = None


# ── Update File Details ────────────────────────────────────────────────────────

class UpdateFileDetailsRequestSchema(BaseModel):
    file_id: str
    user_description: Optional[str] = None


class UpdateFileDetailsResponseSchema(BaseModel):
    message: str
    file_id: str
    user_description: Optional[str] = None
    updated_at: Optional[str] = None

    model_config = ConfigDict(extra="ignore")


# ── Edit Files Permissions ─────────────────────────────────────────────────────

class EditFilesPermissionsRequestSchema(BaseModel):
    files: Optional[list[str]] = None
    external_ids: Optional[list[str]] = None
    principals: list[str]


# ── Get File Permissions ───────────────────────────────────────────────────────

class GetFilePermissionsRequestSchema(BaseModel):
    file_id: Optional[str] = None
    external_id: Optional[str] = None


class PrincipalSchema(BaseModel):
    type: str
    id: Optional[str] = None
    name: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None

    model_config = ConfigDict(extra="ignore")


class FilePermissionsResponseSchema(BaseModel):
    file_id: str
    external_id: Optional[str] = None
    principals: list[PrincipalSchema]

    model_config = ConfigDict(extra="ignore")
