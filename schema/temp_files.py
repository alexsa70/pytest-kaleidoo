from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict


# ── Get File ───────────────────────────────────────────────────────────────────

class TempFileGetRequestSchema(BaseModel):
    file_id: str


class TempFileGetResponseSchema(BaseModel):
    signed_url: Optional[str] = None
    message: str
    file_size: Optional[int] = None
    expires_at: Optional[str] = None

    model_config = ConfigDict(extra="ignore")


# ── Cleanup ────────────────────────────────────────────────────────────────────

class TempFileCleanupRequestSchema(BaseModel):
    file_id: str


class TempFileCleanupResponseSchema(BaseModel):
    status: str
    file_id: str

    model_config = ConfigDict(extra="ignore")
