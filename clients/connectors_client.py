from __future__ import annotations

import allure
from httpx import Response

from clients.base_client import BaseClient
from schema.connectors import GetScanTasksRequestSchema
from tools.routes import (
    GmailConnectorRoutes,
    GoogleDriveConnectorRoutes,
    LeadspottingConnectorRoutes,
    SharepointConnectorRoutes,
)


class ConnectorsClient(BaseClient):
    """Клиент для Connector сервисов (Gmail, Google Drive, SharePoint, Leadspotting)."""

    # ── Gmail ──────────────────────────────────────────────────────────────────

    @allure.step("GmailConnector: get scan tasks")
    async def gmail_get_scan_tasks(self, payload: GetScanTasksRequestSchema | None = None) -> Response:
        body = payload.model_dump(exclude_none=True) if payload else {}
        return await self.post(GmailConnectorRoutes.GET_SCAN_TASKS, json=body)

    # ── Google Drive ───────────────────────────────────────────────────────────

    @allure.step("GoogleDriveConnector: get scan tasks")
    async def google_drive_get_scan_tasks(self, payload: GetScanTasksRequestSchema | None = None) -> Response:
        body = payload.model_dump(exclude_none=True) if payload else {}
        return await self.post(GoogleDriveConnectorRoutes.GET_SCAN_TASKS, json=body)

    # ── SharePoint ─────────────────────────────────────────────────────────────

    @allure.step("SharepointConnector: get scan tasks")
    async def sharepoint_get_scan_tasks(self, payload: GetScanTasksRequestSchema | None = None) -> Response:
        body = payload.model_dump(exclude_none=True) if payload else {}
        return await self.post(SharepointConnectorRoutes.GET_SCAN_TASKS, json=body)

    # ── Leadspotting ───────────────────────────────────────────────────────────

    @allure.step("LeadspottingConnector: get scan tasks")
    async def leadspotting_get_scan_tasks(self, payload: GetScanTasksRequestSchema | None = None) -> Response:
        body = payload.model_dump(exclude_none=True) if payload else {}
        return await self.post(LeadspottingConnectorRoutes.GET_SCAN_TASKS, json=body)
