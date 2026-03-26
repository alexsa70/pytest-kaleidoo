from __future__ import annotations

import io
from typing import Optional

import allure
from httpx import Response

from clients.base_client import BaseClient
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
from tools.routes import OrgRoutes


class OrgClient(BaseClient):
    """Клиент для организационных эндпоинтов Kaleidoo API."""

    # ── Organizations ──────────────────────────────────────────────────────

    @allure.step("Org: create organization")
    async def create_org(
        self,
        payload: CreateOrgRequestSchema,
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

        return await self.post(OrgRoutes.ORG_CREATE, data=data, files=files)

    @allure.step("Org: get organization")
    async def org_get(self, payload: GetOrgRequestSchema) -> Response:
        return await self.post(OrgRoutes.ORG_GET, json=payload.model_dump(exclude_none=True))

    @allure.step("Org: get models")
    async def org_get_models(self) -> Response:
        return await self.post(OrgRoutes.ORG_GET_MODELS, json={})

    @allure.step("Org: update organization")
    async def org_update(
        self,
        payload: UpdateOrgRequestSchema,
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
        return await self.post(OrgRoutes.ORG_UPDATE, data=data, files=files)

    @allure.step("Org: update capabilities")
    async def org_update_capabilities(self, payload: UpdateOrgCapabilitiesRequestSchema) -> Response:
        return await self.post(OrgRoutes.ORG_UPDATE_CAPABILITIES, json=payload.model_dump(exclude_none=True))

    @allure.step("Org: update SSO configuration")
    async def org_update_sso(self, payload: UpdateOrgSSORequestSchema) -> Response:
        return await self.post(OrgRoutes.ORG_UPDATE_SSO, json=payload.model_dump(exclude_none=True))

    @allure.step("Org: delete organization")
    async def org_delete(self) -> Response:
        return await self.post(OrgRoutes.ORG_DELETE, json={})

    @allure.step("Org: get all organizations")
    async def org_get_all(self) -> Response:
        return await self.post(OrgRoutes.ORG_GET_ALL, json={})

    @allure.step("Org: create license")
    async def org_create_license(self, payload: CreateLicenseRequestSchema) -> Response:
        return await self.post(OrgRoutes.ORG_CREATE_LICENSE, json=payload.model_dump())

    @allure.step("Org: update license")
    async def org_update_license(self, payload: UpdateLicenseRequestSchema) -> Response:
        return await self.post(OrgRoutes.ORG_UPDATE_LICENSE, json=payload.model_dump())

    @allure.step("Org: get license")
    async def org_get_license(self, payload: GetLicenseRequestSchema) -> Response:
        return await self.post(OrgRoutes.ORG_GET_LICENSE, json=payload.model_dump())

    @allure.step("Org: set priority table")
    async def org_set_priority_table(self, payload: SetPriorityTableRequestSchema) -> Response:
        return await self.post(OrgRoutes.ORG_SET_PRIORITY_TABLE, json=payload.model_dump())

    @allure.step("Org: balance organization priorities")
    async def org_balance_priorities(self) -> Response:
        return await self.post(OrgRoutes.ORG_BALANCE_PRIORITIES, json={})
