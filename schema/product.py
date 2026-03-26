from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict


# ── Product ────────────────────────────────────────────────────────────────────

class ProductSchema(BaseModel):
    id: Optional[str] = None
    name: str
    description: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    model_config = ConfigDict(extra="ignore", populate_by_name=True)


# ── Get Products ───────────────────────────────────────────────────────────────

class GetProductRequestSchema(BaseModel):
    product_id: str


# ── Project Type ───────────────────────────────────────────────────────────────

class ProjectTypeSchema(BaseModel):
    id: Optional[str] = None
    product_id: str
    type: str
    description: Optional[str] = None
    category: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    model_config = ConfigDict(extra="ignore", populate_by_name=True)


# ── Get Project Types ──────────────────────────────────────────────────────────

class GetProjectTypesRequestSchema(BaseModel):
    product_id: str
