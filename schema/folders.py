from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, ConfigDict


# ── Folder Schema ──────────────────────────────────────────────────────────────

class FolderSchema(BaseModel):
    id: str
    org_id: Optional[str] = None
    name: str
    type: str
    parent_id: Optional[str] = None
    source_url: Optional[str] = None
    source_type: Optional[str] = None
    scan_task_id: Optional[str] = None
    pid: Optional[str] = None
    settings: Optional[dict[str, Any]] = None
    internal: Optional[bool] = None
    parent_id_with_settings: Optional[str] = None
    is_deleted: Optional[bool] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    created_by: Optional[str] = None
    user_folder: Optional[bool] = None
    sub_folders: Optional[list[Any]] = None
    image_url: Optional[str] = None

    model_config = ConfigDict(extra="ignore")


# ── Get All Folders ────────────────────────────────────────────────────────────

class GetAllFoldersRequestSchema(BaseModel):
    type: Optional[str] = None
    parent_id: Optional[str] = None
    scan_task_id: Optional[str] = None
    source_type: Optional[str] = None
    include_subfolders: Optional[bool] = None
    subfolders_depth: Optional[int] = None
    folder_ids: Optional[list[str]] = None
    include_all: Optional[bool] = None


class GetAllFoldersResponseSchema(BaseModel):
    folders: list[FolderSchema]
    total: Optional[int] = None

    model_config = ConfigDict(extra="ignore")


# ── Get Folders (Paginated) ────────────────────────────────────────────────────

class GetFoldersRequestSchema(BaseModel):
    parent_id: Optional[str] = None
    limit: Optional[int] = None
    cursor: Optional[str] = None
    type: Optional[str] = None
    source_type: Optional[str] = None
    scan_task_id: Optional[str] = None


class PaginationSchema(BaseModel):
    next_cursor: Optional[str] = None
    has_more: bool
    count: int
    limit: int

    model_config = ConfigDict(extra="ignore")


class GetFoldersResponseSchema(BaseModel):
    folders: list[FolderSchema]
    pagination: PaginationSchema

    model_config = ConfigDict(extra="ignore")


# ── Get Folder ─────────────────────────────────────────────────────────────────

class GetFolderRequestSchema(BaseModel):
    folder_id: Optional[str] = None
    folder_name: Optional[str] = None
    source_url: Optional[str] = None
    include_subfolders: Optional[bool] = None


# ── Create Folder ──────────────────────────────────────────────────────────────

class CreateFolderRequestSchema(BaseModel):
    name: str
    type: str
    parent_id: Optional[str] = None
    permissions: Optional[list[Any]] = None
    agents_ids: Optional[list[str]] = None
    settings: Optional[dict[str, Any]] = None
    image_id: Optional[str] = None


class CreateFolderResponseSchema(BaseModel):
    id: str

    model_config = ConfigDict(extra="ignore")


# ── Update Folder ──────────────────────────────────────────────────────────────

class UpdateFolderRequestSchema(BaseModel):
    folder_id: str
    name: Optional[str] = None
    permissions: Optional[list[Any]] = None
    settings: Optional[dict[str, Any]] = None
    delete_settings: Optional[bool] = None
    agents_ids_add: Optional[list[str]] = None
    agents_ids_delete: Optional[list[str]] = None
    tags_ids_add: Optional[list[str]] = None
    tags_ids_delete: Optional[list[str]] = None
    parent_id: Optional[str] = None
    image_id: Optional[str] = None
    delete_image: Optional[bool] = None


# ── Delete Folder ──────────────────────────────────────────────────────────────

class DeleteFolderRequestSchema(BaseModel):
    folder_id: str
    cascade: Optional[bool] = None


# ── Associate / Disassociate Files ─────────────────────────────────────────────

class AssociateFilesRequestSchema(BaseModel):
    folder_id: str
    file_ids: list[str]


class DisassociateFilesRequestSchema(BaseModel):
    folder_id: str
    file_ids: list[str]


# ── Get Files by Folders ───────────────────────────────────────────────────────

class GetFilesByFoldersRequestSchema(BaseModel):
    folder_ids: list[str]
    cursor: Optional[str] = None


# ── Get Folders by Files ───────────────────────────────────────────────────────

class GetFoldersByFilesRequestSchema(BaseModel):
    file_ids: list[str]


# ── Associate / Disassociate Agents ───────────────────────────────────────────

class AssociateAgentsToFolderRequestSchema(BaseModel):
    folder_id: str
    agent_ids: list[str]


class AssociateAgentToFoldersRequestSchema(BaseModel):
    agent_id: str
    folder_ids: list[str]


class DisassociateAgentsRequestSchema(BaseModel):
    folder_id: str
    agent_ids: list[str]


# ── Get Agents by Folders ──────────────────────────────────────────────────────

class GetAgentsByFoldersRequestSchema(BaseModel):
    folder_ids: Optional[list[str]] = None
    scan_task_id: Optional[str] = None
    ids_only: Optional[bool] = None


# ── Get Folders by Agents ──────────────────────────────────────────────────────

class GetFoldersByAgentsRequestSchema(BaseModel):
    agent_ids: list[str]


# ── Remove Auto Subfolder ──────────────────────────────────────────────────────

class RemoveAutoSubfolderRequestSchema(BaseModel):
    folder_id: str
