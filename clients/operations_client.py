from __future__ import annotations

import io
from typing import Optional

import allure
from httpx import Response

from clients.base_client import BaseClient
from schema.operations import (
    AuthenticateRequestSchema,
    SSOLoginRequestSchema,
    ResetPasswordRequestSchema,
)
from schema.organizations import CreateOrgRequestSchema
from tools.routes import AuthRoutes, OrgRoutes


class APIClient(BaseClient):
    """Основной клиент Kaleidoo API."""

    # ── Authentication ─────────────────────────────────────────────────────

    @allure.step("Auth: authenticate")
    async def authenticate_api(self, payload: AuthenticateRequestSchema) -> Response:
        return await self.post(
            AuthRoutes.AUTHENTICATE,
            json=payload.model_dump(exclude_none=True),
        )

    @allure.step("Auth: SSO login via {payload.provider}")
    async def sso_login(self, payload: SSOLoginRequestSchema) -> Response:
        return await self.post(
            AuthRoutes.SSO_LOGIN,
            json=payload.model_dump(exclude_none=True),
        )

    @allure.step("Auth: reset password for {payload.email}")
    async def reset_password(self, payload: ResetPasswordRequestSchema) -> Response:
        return await self.post(
            AuthRoutes.RESET_PASSWORD,
            json=payload.model_dump(exclude_none=True),
        )

    # ── Organizations ──────────────────────────────────────────────────────

    @allure.step("Org: create organization '{payload.org_name}'")
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
            data["permissions"] = payload.permissions.model_dump_json(exclude_none=True)

        if payload.supported_languages is not None:
            data["supported_languages"] = payload.supported_languages

        files = None
        if logo is not None:
            files = {"logo": (logo_filename, io.BytesIO(logo), logo_content_type)}

        return await self.post(
            OrgRoutes.ORG_CREATE,
            data=data,
            files=files,
            headers={"Authorization": f"Bearer {token}"},
        )
