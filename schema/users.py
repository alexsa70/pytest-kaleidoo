from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class UserRetrieveSchema(BaseModel):
    """Параметры запроса POST /api/user/get."""

    user_name: str


class UserRetrieveByIdSchema(BaseModel):
    user_id: str


class UserUpdateRequestSchema(BaseModel):
    user_id: str
    first_name: str | None = None
    last_name: str | None = None
    user_name: str | None = None
    role_id: str | None = None
    status: str | None = None
    upload_image_action: str | None = None


class UserCreateRequestSchema(BaseModel):
    org_name: str
    user_name: str
    first_name: str
    last_name: str
    role_id: str
    email: str
    is_ldap_sso_user: bool | None = None
    base_url: str | None = None


class UserDeleteRequestSchema(BaseModel):
    user_id: str


class UserUnlockRequestSchema(BaseModel):
    username: str


class UserResetMFARequestSchema(BaseModel):
    user_id: str


class UserResponseSchema(BaseModel):
    """Успешный ответ от user endpoint."""

    id: str
    user_name: str
    email: str
    first_name: str
    last_name: str
    user_type: str
    status: str
    user_image: str | None = None
    color: str | None = None
    created_at: str
    updated_at: str
    created_by: str

    model_config = ConfigDict(extra="ignore")  # API может вернуть лишние поля


class UserSummarySchema(BaseModel):
    id: str
    user_name: str
    email: str
    first_name: str
    last_name: str
    user_type: str
    status: str
    user_image: str | None = None
    color: str | None = None
    created_at: str | None = None

    model_config = ConfigDict(extra="ignore")


class UserGetAllResponseSchema(BaseModel):
    users: list[UserSummarySchema]
    total_count: int

    model_config = ConfigDict(extra="ignore")


class RoleSchema(BaseModel):
    id: str
    name: str
    description: str

    model_config = ConfigDict(extra="ignore")


class UserGetRolesResponseSchema(BaseModel):
    roles: list[RoleSchema]

    model_config = ConfigDict(extra="ignore")


class UserCreateResponseSchema(BaseModel):
    message: str
    user_id: str

    model_config = ConfigDict(extra="ignore")


class UserUpdateResponseSchema(BaseModel):
    message: str
    id: str
    user_name: str
    first_name: str
    last_name: str
    updated_at: str

    model_config = ConfigDict(extra="ignore")


class UserErrorSchema(BaseModel):
    message: str
    status: str | None = None

    model_config = ConfigDict(extra="ignore")
