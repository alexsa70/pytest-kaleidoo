from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, ConfigDict


# ── Create Auth URL ────────────────────────────────────────────────────────────

class CreateAuthUrlRequestSchema(BaseModel):
    provider: str
    redirect_uri: str


class CreateAuthUrlResponseSchema(BaseModel):
    auth_url: str

    model_config = ConfigDict(extra="ignore")


# ── Create Connector ───────────────────────────────────────────────────────────

class CreateConnectorRequestSchema(BaseModel):
    provider: str
    code: Optional[str] = None
    redirect_uri: Optional[str] = None
    events_filter: Optional[str] = None


class CreateConnectorResponseSchema(BaseModel):
    message: str
    source_id: str

    model_config = ConfigDict(extra="ignore")


# ── Create Scan Tasks ──────────────────────────────────────────────────────────

class CreateScanTasksRequestSchema(BaseModel):
    source_id: str
    source_paths: dict[str, Any]
    sync_hour: Optional[str] = None
    initial_page_limit: Optional[int] = None


class CreateScanTasksResponseSchema(BaseModel):
    successful: int
    failed: int
    total: int
    scan_task_ids: list[str]
    errors: Optional[dict[str, str]] = None

    model_config = ConfigDict(extra="ignore")


# ── List by Org ────────────────────────────────────────────────────────────────

class ListByOrgRequestSchema(BaseModel):
    provider: Optional[str] = None


class ConnectorSchema(BaseModel):
    id: str
    provider: str
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    sync_status: Optional[str] = None
    last_sync: Optional[str] = None
    scan_tasks_count: Optional[int] = None

    model_config = ConfigDict(extra="ignore")


# ── Delete Source ──────────────────────────────────────────────────────────────

class DeleteSourceRequestSchema(BaseModel):
    source_id: str
    scan_task_ids: Optional[list[str]] = None


# ── Connect / Disconnect Sync ──────────────────────────────────────────────────

class ConnectSyncRequestSchema(BaseModel):
    source_id: str
    scan_task_id: Optional[str] = None


class ConnectSyncResponseSchema(BaseModel):
    message: str
    scan_task_id: Optional[str] = None

    model_config = ConfigDict(extra="ignore")


class DisconnectSyncRequestSchema(BaseModel):
    source_id: str
    scan_task_id: Optional[str] = None


# ── Update Sync Hour ───────────────────────────────────────────────────────────

class UpdateSyncHourRequestSchema(BaseModel):
    source_id: str
    scan_task_id: str
    sync_hour: str


class UpdateSyncHourResponseSchema(BaseModel):
    message: str
    scan_task_id: str
    sync_hour: str

    model_config = ConfigDict(extra="ignore")


# ── Validate Source Path ───────────────────────────────────────────────────────

class ValidateSourcePathRequestSchema(BaseModel):
    source_id: str
    source_path: str


class ValidateSourcePathResponseSchema(BaseModel):
    valid: bool
    folder_name: Optional[str] = None
    folder_path: Optional[str] = None
    error: Optional[str] = None

    model_config = ConfigDict(extra="ignore")
