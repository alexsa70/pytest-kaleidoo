from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict


# ── Scan Task Schema ───────────────────────────────────────────────────────────

class ScanTaskSchema(BaseModel):
    id: str
    source_path: str
    sync_hour: Optional[str] = None
    source_id: str

    model_config = ConfigDict(extra="ignore")


# ── Get Scan Tasks ─────────────────────────────────────────────────────────────

class GetScanTasksRequestSchema(BaseModel):
    source_id: Optional[str] = None


class GetScanTasksResponseSchema(BaseModel):
    scan_tasks: list[ScanTaskSchema]

    model_config = ConfigDict(extra="ignore")
