from __future__ import annotations

import io
from typing import Optional

import allure
from httpx import Response

from clients.base_client import BaseClient
from schema.users import (
    UserRetrieveSchema,
    UserRetrieveByIdSchema,
    UserUpdateRequestSchema,
    UserCreateRequestSchema,
    UserDeleteRequestSchema,
    UserUnlockRequestSchema,
    UserResetMFARequestSchema,
)
from tools.routes import UserRoutes


class UserClient(BaseClient):
    """Клиент для пользовательских эндпоинтов Kaleidoo API."""

    # ── User ──────────────────────────────────────────────────────

    @allure.step("Users: retrieve user by name")
    async def user_retrieve(self, payload: UserRetrieveSchema) -> Response:
        return await self.post(UserRoutes.USER_RETRIEVE, json=payload.model_dump(exclude_none=True))

    @allure.step("Users: retrieve user by id")
    async def user_get_by_id(self, payload: UserRetrieveByIdSchema) -> Response:
        return await self.post(UserRoutes.USER_GET_BY_ID, json=payload.model_dump(exclude_none=True))

    @allure.step("Users: update user")
    async def user_update(
        self,
        payload: UserUpdateRequestSchema,
        user_image: Optional[bytes] = None,
        image_filename: str = "avatar.jpg",
        image_content_type: str = "image/jpeg",
    ) -> Response:
        data = payload.model_dump(exclude_none=True)
        # Force multipart/form-data even without file upload.
        files = {key: (None, str(value)) for key, value in data.items()}
        if user_image is not None:
            files = {"user_image": (image_filename, io.BytesIO(user_image), image_content_type)}
            files.update({key: (None, str(value)) for key, value in data.items()})
        return await self.post(UserRoutes.USER_UPDATE, files=files)

    @allure.step("Users: create user")
    async def user_create(
        self,
        payload: UserCreateRequestSchema,
        user_image: Optional[bytes] = None,
        image_filename: str = "avatar.jpg",
        image_content_type: str = "image/jpeg",
    ) -> Response:
        data = payload.model_dump(exclude_none=True)
        if payload.is_ldap_sso_user is not None:
            data["is_ldap_sso_user"] = str(payload.is_ldap_sso_user).lower()

        # Force multipart/form-data even without file upload.
        files = {key: (None, str(value)) for key, value in data.items()}
        if user_image is not None:
            files = {"user_image": (image_filename, io.BytesIO(user_image), image_content_type)}
            files.update({key: (None, str(value)) for key, value in data.items()})
        return await self.post(UserRoutes.USER_CREATE, files=files)

    @allure.step("Users: delete user")
    async def user_delete(self, payload: UserDeleteRequestSchema) -> Response:
        return await self.post(UserRoutes.USER_DELETE, json=payload.model_dump(exclude_none=True))

    @allure.step("Users: get all users")
    async def user_get_all(self) -> Response:
        return await self.post(UserRoutes.USER_GET_ALL, json={})

    @allure.step("Users: get available roles")
    async def user_get_roles(self) -> Response:
        return await self.post(UserRoutes.USER_GET_ROLES, json={})

    @allure.step("Users: unlock user")
    async def user_unlock(self, payload: UserUnlockRequestSchema) -> Response:
        return await self.post(UserRoutes.USER_UNLOCK, json=payload.model_dump(exclude_none=True))

    @allure.step("Users: reset MFA")
    async def user_reset_mfa(self, payload: UserResetMFARequestSchema) -> Response:
        return await self.post(UserRoutes.USER_RESET_MFA, json=payload.model_dump(exclude_none=True))
