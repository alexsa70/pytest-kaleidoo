from __future__ import annotations

from http import HTTPStatus
from typing import Optional

import pyotp
import pytest
import pytest_asyncio

from clients.base_client import get_http_client
from clients.operations_client import APIClient
from config import APISettings
from schema.operations import LoginRequestSchema, SSOLoginResponseSchema
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
async def tokens_by_role(
    settings: APISettings,
    role_auth_payloads: dict[str, LoginRequestSchema],
) -> dict[str, str]:
    """Gets access tokens once per session for each configured role."""

    tokens: dict[str, str] = {}
    async with get_http_client(settings.api_http_client) as http_client:
        client = APIClient(client=http_client)
        for role, payload in role_auth_payloads.items():
            response = await client.login(payload)
            if response.status_code == HTTPStatus.TOO_MANY_REQUESTS.value:
                pytest.skip("Rate limited (429) on /login. Try again later.")
            assert_status_code(response.status_code, HTTPStatus.OK)
            data = response.json()
            if isinstance(data, dict) and data.get("mfa_required"):
                pytest.skip(
                    f"MFA required for role '{role}' but OTP_SECRET is not set in .env"
                )
            body = SSOLoginResponseSchema.model_validate(data)
            tokens[role] = body.token

    return tokens
