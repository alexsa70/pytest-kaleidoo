from __future__ import annotations

import allure
from httpx import Response

from clients.base_client import BaseClient
from schema.auth import (
    LoginRequestSchema,
    SSOLoginRequestSchema,
    ResetPasswordRequestSchema,
    SessionTokenRequestSchema,
    RefreshSessionTokenRequestSchema,
)
from tools.routes import AuthRoutes


class AuthClient(BaseClient):
    """Клиент для аутентификационных эндпоинтов Kaleidoo API."""

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
        # token передаётся явно: это exchange-операция, требующая конкретного токена
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
