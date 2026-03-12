from __future__ import annotations

from typing import Optional, List
from pydantic import BaseModel, ConfigDict


class FilesAccessPermissionsSchema(BaseModel):
    manual_public: Optional[bool] = None


class CachePermissionsSchema(BaseModel):
    user_acl_ttl: Optional[int] = None           # min: 900
    user_acl_refresh_gap_ttl: Optional[int] = None  # min: 300, must be < user_acl_ttl


class PermissionsSchema(BaseModel):
    files_access: Optional[FilesAccessPermissionsSchema] = None
    cache: Optional[CachePermissionsSchema] = None


class CreateOrgRequestSchema(BaseModel):
    org_name: str
    domain: str
    admin_email: str
    user_name: str
    first_name: str
    last_name: str
    role_id: str
    org_description: Optional[str] = None       # max 150 chars
    org_color: Optional[str] = None
    default_language: Optional[str] = None      # "english" | "hebrew"
    supported_languages: Optional[List[str]] = None
    permissions: Optional[PermissionsSchema] = None


class CreateOrgResponseSchema(BaseModel):
    message: str
    org_id: str

    model_config = ConfigDict(extra="ignore")


class CreateOrgValidationErrorSchema(BaseModel):
    message: str
    validation_errors: List[str]

    model_config = ConfigDict(extra="ignore")
