from __future__ import annotations

import io
from typing import Optional

import allure
from httpx import Response

from clients.base_client import BaseClient
from schema.operations import (
    LoginRequestSchema,
    SSOLoginRequestSchema,
    ResetPasswordRequestSchema,
    SessionTokenRequestSchema,
    RefreshSessionTokenRequestSchema,
)
from schema.organizations import (
    CreateOrgRequestSchema,
    GetOrgRequestSchema,
    UpdateOrgRequestSchema,
    UpdateOrgCapabilitiesRequestSchema,
    UpdateOrgSSORequestSchema,
    CreateLicenseRequestSchema,
    UpdateLicenseRequestSchema,
    GetLicenseRequestSchema,
    SetPriorityTableRequestSchema,
)
from schema.users import UserRetrieveSchema
from schema.users import (
    UserCreateRequestSchema,
    UserDeleteRequestSchema,
    UserResetMFARequestSchema,
    UserRetrieveByIdSchema,
    UserUnlockRequestSchema,
    UserUpdateRequestSchema,
)
from tools.routes import AuthRoutes, OrgRoutes, UserRoutes


class APIClient(BaseClient):
    """Основной клиент Kaleidoo API."""

    # ── Authentication ─────────────────────────────────────────────────────

    @allure.step("Auth: login")
    async def login(self, payload: LoginRequestSchema) -> Response:
        return await self.post(
            AuthRoutes.LOGIN,
            json=payload.model_dump(exclude_none=True),
        )

    @allure.step("Auth: SSO login")
    async def sso_login(self, payload: SSOLoginRequestSchema) -> Response:
        return await self.post(
            AuthRoutes.SSO_LOGIN,
            json=payload.model_dump(exclude_none=True),
        )

    @allure.step("Auth: reset password")
    async def reset_password(self, payload: ResetPasswordRequestSchema) -> Response:
        return await self.post(
            AuthRoutes.RESET_PASSWORD,
            json=payload.model_dump(exclude_none=True),
        )

    @allure.step("Auth: create session token")
    async def create_session_token(self, payload: SessionTokenRequestSchema, token: str) -> Response:
        return await self.post(
            AuthRoutes.SESSION_TOKEN,
            json=payload.model_dump(exclude_none=True),
            headers={"Authorization": f"Bearer {token}"},
        )

    @allure.step("Auth: refresh session token")
    async def refresh_session_token(self, payload: RefreshSessionTokenRequestSchema) -> Response:
        return await self.post(
            AuthRoutes.REFRESH_SESSION_TOKEN,
            json=payload.model_dump(exclude_none=True),
        )

    # ── Organizations ──────────────────────────────────────────────────────

    @allure.step("Org: create organization")
    async def create_org(
        self,
        payload: CreateOrgRequestSchema,
        token: str,
        logo: Optional[bytes] = None,
        logo_filename: str = "logo.png",
        logo_content_type: str = "image/png",
    ) -> Response:
        """multipart/form-data. permissions сериализуется в JSON-строку."""
        data: dict = payload.model_dump(
            exclude_none=True,
            exclude={"permissions", "supported_languages"},
        )

        if payload.permissions is not None:
            data["permissions"] = payload.permissions.model_dump_json(
                exclude_none=True)

        if payload.supported_languages is not None:
            data["supported_languages"] = payload.supported_languages

        files = None
        if logo is not None:
            files = {"logo": (logo_filename, io.BytesIO(
                logo), logo_content_type)}

        return await self.post(
            OrgRoutes.ORG_CREATE,
            data=data,
            files=files,
            headers={"Authorization": f"Bearer {token}"},
        )
    @allure.step("Org: get organization")
    async def org_get(self, payload: GetOrgRequestSchema, token: str) -> Response:
        return await self.post(
            OrgRoutes.ORG_GET,
            json=payload.model_dump(exclude_none=True),
            headers={"Authorization": f"Bearer {token}"},
        )

    @allure.step("Org: get models")
    async def org_get_models(self, token: str) -> Response:
        return await self.post(
            OrgRoutes.ORG_GET_MODELS,
            json={},
            headers={"Authorization": f"Bearer {token}"},
        )

    @allure.step("Org: update organization")
    async def org_update(
        self,
        payload: UpdateOrgRequestSchema,
        token: str,
        logo: Optional[bytes] = None,
        logo_filename: str = "logo.png",
        logo_content_type: str = "image/png",
    ) -> Response:
        data = payload.model_dump(exclude_none=True, exclude={"supported_languages"})
        if payload.supported_languages is not None:
            data["supported_languages"] = payload.supported_languages
        files = None
        if logo is not None:
            files = {"logo": (logo_filename, io.BytesIO(logo), logo_content_type)}
        return await self.post(
            OrgRoutes.ORG_UPDATE,
            data=data,
            files=files,
            headers={"Authorization": f"Bearer {token}"},
        )

    @allure.step("Org: update capabilities")
    async def org_update_capabilities(
        self, payload: UpdateOrgCapabilitiesRequestSchema, token: str
    ) -> Response:
        return await self.post(
            OrgRoutes.ORG_UPDATE_CAPABILITIES,
            json=payload.model_dump(exclude_none=True),
            headers={"Authorization": f"Bearer {token}"},
        )

    @allure.step("Org: update SSO configuration")
    async def org_update_sso(self, payload: UpdateOrgSSORequestSchema, token: str) -> Response:
        return await self.post(
            OrgRoutes.ORG_UPDATE_SSO,
            json=payload.model_dump(exclude_none=True),
            headers={"Authorization": f"Bearer {token}"},
        )

    @allure.step("Org: delete organization")
    async def org_delete(self, token: str) -> Response:
        return await self.post(
            OrgRoutes.ORG_DELETE,
            json={},
            headers={"Authorization": f"Bearer {token}"},
        )

    @allure.step("Org: get all organizations")
    async def org_get_all(self, token: str) -> Response:
        return await self.post(
            OrgRoutes.ORG_GET_ALL,
            json={},
            headers={"Authorization": f"Bearer {token}"},
        )

    @allure.step("Org: create license")
    async def org_create_license(self, payload: CreateLicenseRequestSchema, token: str) -> Response:
        return await self.post(
            OrgRoutes.ORG_CREATE_LICENSE,
            json=payload.model_dump(),
            headers={"Authorization": f"Bearer {token}"},
        )

    @allure.step("Org: update license")
    async def org_update_license(self, payload: UpdateLicenseRequestSchema, token: str) -> Response:
        return await self.post(
            OrgRoutes.ORG_UPDATE_LICENSE,
            json=payload.model_dump(),
            headers={"Authorization": f"Bearer {token}"},
        )

    @allure.step("Org: get license")
    async def org_get_license(self, payload: GetLicenseRequestSchema, token: str) -> Response:
        return await self.post(
            OrgRoutes.ORG_GET_LICENSE,
            json=payload.model_dump(),
            headers={"Authorization": f"Bearer {token}"},
        )

    @allure.step("Org: set priority table")
    async def org_set_priority_table(
        self, payload: SetPriorityTableRequestSchema, token: str
    ) -> Response:
        return await self.post(
            OrgRoutes.ORG_SET_PRIORITY_TABLE,
            json=payload.model_dump(),
            headers={"Authorization": f"Bearer {token}"},
        )

    @allure.step("Org: balance organization priorities")
    async def org_balance_priorities(self, token: str) -> Response:
        return await self.post(
            OrgRoutes.ORG_BALANCE_PRIORITIES,
            json={},
            headers={"Authorization": f"Bearer {token}"},
        )

    # ── User ──────────────────────────────────────────────────────

    @allure.step("Users: retrieve user by name")
    async def user_retrieve(self, payload: UserRetrieveSchema, token: str) -> Response:
        return await self.post(
            UserRoutes.USER_RETRIEVE,
            json=payload.model_dump(exclude_none=True),
            headers={
                "Authorization": f"Bearer {token}"
            },
        )

    @allure.step("Users: retrieve user by id")
    async def user_get_by_id(self, payload: UserRetrieveByIdSchema, token: str) -> Response:
        return await self.post(
            UserRoutes.USER_GET_BY_ID,
            json=payload.model_dump(exclude_none=True),
            headers={"Authorization": f"Bearer {token}"},
        )

    @allure.step("Users: update user")
    async def user_update(
        self,
        payload: UserUpdateRequestSchema,
        token: str,
        user_image: Optional[bytes] = None,
        image_filename: str = "avatar.jpg",
        image_content_type: str = "image/jpeg",
    ) -> Response:
        data = payload.model_dump(exclude_none=True)
        files = None
        if user_image is not None:
            files = {"user_image": (image_filename, io.BytesIO(user_image), image_content_type)}
        return await self.post(
            UserRoutes.USER_UPDATE,
            data=data,
            files=files,
            headers={"Authorization": f"Bearer {token}"},
        )

    @allure.step("Users: create user")
    async def user_create(
        self,
        payload: UserCreateRequestSchema,
        token: str,
        user_image: Optional[bytes] = None,
        image_filename: str = "avatar.jpg",
        image_content_type: str = "image/jpeg",
    ) -> Response:
        data = payload.model_dump(exclude_none=True)
        if payload.is_ldap_sso_user is not None:
            data["is_ldap_sso_user"] = str(payload.is_ldap_sso_user).lower()

        files = None
        if user_image is not None:
            files = {"user_image": (image_filename, io.BytesIO(user_image), image_content_type)}
        return await self.post(
            UserRoutes.USER_CREATE,
            data=data,
            files=files,
            headers={"Authorization": f"Bearer {token}"},
        )

    @allure.step("Users: delete user")
    async def user_delete(self, payload: UserDeleteRequestSchema, token: str) -> Response:
        return await self.post(
            UserRoutes.USER_DELETE,
            json=payload.model_dump(exclude_none=True),
            headers={"Authorization": f"Bearer {token}"},
        )

    @allure.step("Users: get all users")
    async def user_get_all(self, token: str) -> Response:
        return await self.post(
            UserRoutes.USER_GET_ALL,
            json={},
            headers={"Authorization": f"Bearer {token}"},
        )

    @allure.step("Users: get available roles")
    async def user_get_roles(self, token: str) -> Response:
        return await self.post(
            UserRoutes.USER_GET_ROLES,
            json={},
            headers={"Authorization": f"Bearer {token}"},
        )

    @allure.step("Users: unlock user")
    async def user_unlock(self, payload: UserUnlockRequestSchema, token: str) -> Response:
        return await self.post(
            UserRoutes.USER_UNLOCK,
            json=payload.model_dump(exclude_none=True),
            headers={"Authorization": f"Bearer {token}"},
        )

    @allure.step("Users: reset MFA")
    async def user_reset_mfa(self, payload: UserResetMFARequestSchema, token: str) -> Response:
        return await self.post(
            UserRoutes.USER_RESET_MFA,
            json=payload.model_dump(exclude_none=True),
            headers={"Authorization": f"Bearer {token}"},
        )
