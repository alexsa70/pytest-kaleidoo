from __future__ import annotations

from contextlib import asynccontextmanager
from http import HTTPStatus
from typing import AsyncIterator, Optional

import pyotp
import pytest
import pytest_asyncio

from clients.base_client import get_http_client
from clients.auth_client import AuthClient
from config import APISettings
from schema.auth import LoginRequestSchema, SSOLoginResponseSchema
from tools.assertions.base import assert_status_code


def _build_payload(settings: APISettings, role: str) -> Optional[LoginRequestSchema]:
    if role == "super_admin":
        cfg = settings.auth_credentials_super_admin
    elif role == "admin":
        cfg = settings.auth_credentials_admin
    elif role == "user":
        cfg = settings.auth_credentials_user
    else:
        return None

    if cfg is None:
        return None

    otp_code = None
    if cfg.otp_secret:
        otp_code = pyotp.TOTP(cfg.otp_secret).now()

    return LoginRequestSchema(
        orgName=settings.org_name or "",
        identity=cfg.email,
        password=cfg.password,
        otp_code=otp_code,
    )


@pytest.fixture(scope="session")
def role_auth_payloads(settings: APISettings) -> dict[str, LoginRequestSchema]:
    """Builds auth payloads for roles configured in .env."""

    payloads: dict[str, LoginRequestSchema] = {}
    for role in ("super_admin", "admin", "user"):
        payload = _build_payload(settings, role)
        if payload is not None:
            payloads[role] = payload

    if not payloads:
        pytest.skip(
            "RBAC creds are not configured. Set AUTH_CREDENTIALS_{SUPER_ADMIN|ADMIN|USER}.* in .env"
        )

    return payloads


@pytest_asyncio.fixture(scope="session", loop_scope="session")
async def login_responses_by_role(
    settings: APISettings,
    role_auth_payloads: dict[str, LoginRequestSchema],
) -> dict[str, SSOLoginResponseSchema]:
    """Full /login response per role. Single login call — shared by all dependent fixtures."""

    responses: dict[str, SSOLoginResponseSchema] = {}
    async with get_http_client(settings.api_http_client) as http_client:
        client = AuthClient(client=http_client)
        for role, payload in role_auth_payloads.items():
            response = await client.login(payload)
            if response.status_code == HTTPStatus.TOO_MANY_REQUESTS.value:
                pytest.skip("Rate limited (429) on /login. Try again later.")
            if response.status_code != HTTPStatus.OK.value:
                print(f"[auth] Skipping role '{role}': login returned {response.status_code}")
                continue
            data = response.json()
            if isinstance(data, dict) and data.get("mfa_required"):
                print(f"[auth] Skipping role '{role}': MFA required but OTP_SECRET not set in .env")
                continue
            responses[role] = SSOLoginResponseSchema.model_validate(data)

    if not responses:
        pytest.skip("No roles could be authenticated. Check credentials in .env")

    return responses


@pytest.fixture(scope="session")
def tokens_by_role(login_responses_by_role: dict[str, SSOLoginResponseSchema]) -> dict[str, str]:
    """Access tokens per role, derived from login_responses_by_role."""
    return {role: body.token for role, body in login_responses_by_role.items()}


@pytest.fixture(scope="session")
def logged_in_user(
    login_responses_by_role: dict[str, SSOLoginResponseSchema],
    settings: APISettings,
):
    """User data for the active role from /login response. No .env IDs needed."""
    response = login_responses_by_role.get(settings.active_role)
    if response is None:
        available = list(login_responses_by_role.keys())
        if not available:
            pytest.skip("No login responses available")
        response = login_responses_by_role[available[0]]
    return response.user


@pytest.fixture(scope="session")
def api_client_for_role(settings: APISettings, tokens_by_role: dict[str, str]):
    """
    Фабрика: возвращает async context manager, создающий AuthClient для конкретной роли.

    Использование:
        async with api_client_for_role("admin") as client:
            response = await client.user_get_all()
    """
    @asynccontextmanager
    async def _factory(role: str) -> AsyncIterator[AuthClient]:
        token = tokens_by_role.get(role)
        if token is None:
            pytest.skip(f"No token configured for role: {role}")
        async with get_http_client(settings.api_http_client, token=token) as http_client:
            yield AuthClient(client=http_client)

    return _factory
