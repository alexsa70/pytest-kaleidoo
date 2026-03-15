from __future__ import annotations

from typing import Dict, List, Optional, Union
from pydantic import BaseModel, ConfigDict


# ── Shared ─────────────────────────────────────────────────────────────────

class OrgMessageResponseSchema(BaseModel):
    message: str

    model_config = ConfigDict(extra="ignore")


# ── Permissions (reused in Create and Update Capabilities) ─────────────────

class FilesAccessPermissionsSchema(BaseModel):
    manual_public: Optional[bool] = None


class CachePermissionsSchema(BaseModel):
    user_acl_ttl: Optional[int] = None            # min: 900
    user_acl_refresh_gap_ttl: Optional[int] = None  # min: 300, must be < user_acl_ttl


class PermissionsSchema(BaseModel):
    files_access: Optional[FilesAccessPermissionsSchema] = None
    cache: Optional[CachePermissionsSchema] = None


# ── Get Organization ────────────────────────────────────────────────────────

class GetOrgRequestSchema(BaseModel):
    fields: Optional[List[str]] = None


class OrgResponseSchema(BaseModel):
    id: str
    org_name: str
    domain: Optional[str] = None
    admin_email: Optional[str] = None
    org_description: Optional[str] = None
    org_color: Optional[str] = None
    default_language: Optional[str] = None
    supported_languages: Optional[List[str]] = None

    model_config = ConfigDict(extra="ignore")


# ── Create Organization ─────────────────────────────────────────────────────

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


# ── Update Organization ─────────────────────────────────────────────────────

class UpdateOrgRequestSchema(BaseModel):
    org_description: Optional[str] = None       # max 150 chars
    org_color: Optional[str] = None
    admin_email: Optional[str] = None
    callback_url: Optional[str] = None
    upload_image_action: Optional[str] = None   # "none" | "replace" | "delete"
    default_language: Optional[str] = None      # "english" | "hebrew"
    supported_languages: Optional[List[str]] = None
    prompt: Optional[str] = None


# ── Update Organization Capabilities ───────────────────────────────────────

class AgentSettingsSchema(BaseModel):
    activations_per_conversation: Optional[int] = None
    activation_interval_seconds: Optional[int] = None
    start: Optional[int] = None
    end: Optional[int] = None
    sections_type: Optional[str] = None


class UpdateOrgCapabilitiesRequestSchema(BaseModel):
    capabilities: Optional[dict] = None
    llm_preference: Optional[dict] = None
    internal_llm_id: Optional[str] = None
    prompt: Optional[str] = None
    auto_model_selection: Optional[bool] = None
    use_org_data: Optional[bool] = None
    agent_settings: Optional[AgentSettingsSchema] = None
    tags_settings: Optional[dict] = None
    ai_description_settings: Optional[dict] = None
    personal_connectors: Optional[dict] = None
    rerank: Optional[bool] = None
    query_allowed: Optional[bool] = None
    permissions: Optional[PermissionsSchema] = None


# ── Update Organization SSO ─────────────────────────────────────────────────

class UpdateOrgSSORequestSchema(BaseModel):
    google: Optional[Union[bool, str]] = None
    microsoft: Optional[Union[bool, str]] = None
    cyberark: Optional[Union[bool, str]] = None


# ── Get All Organizations ───────────────────────────────────────────────────

class OrgSummarySchema(BaseModel):
    id: str
    org_name: str
    domain: Optional[str] = None
    admin_email: Optional[str] = None
    org_description: Optional[str] = None
    org_color: Optional[str] = None
    created_at: Optional[str] = None
    products: Optional[List[str]] = None

    model_config = ConfigDict(extra="ignore")


class GetAllOrgsResponseSchema(BaseModel):
    organizations: List[OrgSummarySchema]
    total_count: int

    model_config = ConfigDict(extra="ignore")


# ── License ─────────────────────────────────────────────────────────────────

class CreateLicenseRequestSchema(BaseModel):
    product_id: str
    status: str  # "active" | "inactive" | "trial" | "expired"


class LicenseDataSchema(BaseModel):
    license_id: str


class CreateLicenseResponseSchema(BaseModel):
    message: str
    data: LicenseDataSchema

    model_config = ConfigDict(extra="ignore")


class UpdateLicenseRequestSchema(BaseModel):
    license_id: str
    status: str  # "active" | "inactive" | "trial" | "expired"


class GetLicenseRequestSchema(BaseModel):
    product_id: str


class GetLicenseResponseSchema(BaseModel):
    license_id: str
    product_id: str
    status: str
    created_at: Optional[str] = None
    expires_at: Optional[str] = None

    model_config = ConfigDict(extra="ignore")


# ── Priority Table ──────────────────────────────────────────────────────────

class SetPriorityTableRequestSchema(BaseModel):
    priorities: Dict[str, int]  # org_id → priority (1–100)


class BalanceOrgPrioritiesResponseSchema(BaseModel):
    message: str
    updated_count: int
    priorities: Optional[Dict[str, int]] = None

    model_config = ConfigDict(extra="ignore")
