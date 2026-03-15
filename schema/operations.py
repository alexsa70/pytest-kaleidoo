from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field, RootModel
from typing import Optional

from tools.fakers import fake


class CreateResourceSchema(BaseModel):
    """Модель для создания сущности в API."""

    model_config = ConfigDict(populate_by_name=True)

    name: str = Field(default_factory=fake.word)
    description: str = Field(default_factory=fake.sentence)


class UpdateResourceSchema(BaseModel):
    """Модель для частичного обновления сущности."""

    model_config = ConfigDict(populate_by_name=True)

    name: str | None = None
    description: str | None = None


class ResourceSchema(CreateResourceSchema):
    """Модель сущности, возвращаемой API."""

    id: str | int


class ResourcesSchema(RootModel[list[ResourceSchema]]):
    """Контейнер для списка сущностей."""

# ── Login ──────────────────────────────────────────────────────────────────


class LoginRequestSchema(BaseModel):
    orgName: str
    identity: str
    password: str
    otp_code: Optional[str] = None


class LoginMFAResponseSchema(BaseModel):
    """Ответ когда MFA включён, но otp_code не передан."""
    message: str
    mfa_required: bool
    qr_code: Optional[str] = None

    model_config = ConfigDict(extra="ignore")


# ── SSO Login ──────────────────────────────────────────────────────────────

class SSOLoginRequestSchema(BaseModel):
    orgName: str
    code: str
    redirect_uri: str
    provider: str
    code_verifier: Optional[str] = None


class SSOUserSchema(BaseModel):
    id: str
    email: str
    first_name: str
    last_name: str
    role: str

    model_config = ConfigDict(extra="ignore")


class SSOOrgSchema(BaseModel):
    id: str
    name: str
    display_name: str

    model_config = ConfigDict(extra="ignore")


class SSOLoginResponseSchema(BaseModel):
    token: str
    refresh_token: str
    expires_in: int
    refresh_expires_in: int
    user: SSOUserSchema
    org: SSOOrgSchema

    model_config = ConfigDict(extra="ignore")


# ── Session Token ──────────────────────────────────────────────────────────


class SessionTokenRequestSchema(BaseModel):
    service: str  # "sse" or "websocket"
    org_name: Optional[str] = None


class SessionTokenResponseSchema(BaseModel):
    access_token: str
    refresh_token: str
    expires_in: int
    service: str
    session_client: Optional[str] = None

    model_config = ConfigDict(extra="ignore")


class RefreshSessionTokenRequestSchema(BaseModel):
    refresh_token: str
    service: str  # "sse", "websocket", or "kal-sense"


class RefreshSessionTokenResponseSchema(BaseModel):
    access_token: str
    refresh_token: str
    expires_in: int
    service: str

    model_config = ConfigDict(extra="ignore")


# ── Reset Password ─────────────────────────────────────────────────────────

class ResetPasswordRequestSchema(BaseModel):
    email: str
    org_name: Optional[str] = None


class ResetPasswordResponseSchema(BaseModel):
    message: str

    model_config = ConfigDict(extra="ignore")


# ── Error responses ────────────────────────────────────────────────────────

class ErrorSchema(BaseModel):
    error: str

    model_config = ConfigDict(extra="ignore")


class MessageErrorSchema(BaseModel):
    message: str

    model_config = ConfigDict(extra="ignore")
