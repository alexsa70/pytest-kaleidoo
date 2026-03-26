from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict


# ── Upload Manual File ─────────────────────────────────────────────────────────

class UploadManualFileResponseSchema(BaseModel):
    message: str
    external_id: str

    model_config = ConfigDict(extra="ignore")


# ── Delete Manual Files ────────────────────────────────────────────────────────

class DeleteManualFilesRequestSchema(BaseModel):
    file_ids: list[str]


class DeleteManualFilesResponseSchema(BaseModel):
    message: str
    valid_file_ids: Optional[list[str]] = None
    ignored_file_ids: Optional[list[str]] = None

    model_config = ConfigDict(extra="ignore")
