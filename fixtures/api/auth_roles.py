from __future__ import annotations

from http import HTTPStatus

import pytest
import pytest_asyncio

from clients.base_client import get_http_client
from clients.operations_client import APIClient
from config import APISettings
from schema.operations import AuthenticateRequestSchema, AuthenticateResponseSchema
from tools.assertions.base import assert_status_code


def _build_payload(credentials: APISettings, role: str) -> AuthenticateRequestSchema | None:
    if role == "super_admin":
        cfg = credentials.auth_credentials_super_admin
    elif role == "admin":
        cfg = credentials.auth_credentials_admin
    elif role == "user":
        cfg = credentials.auth_credentials_user
    else:
        return None

    if cfg is None:
        return None

    return AuthenticateRequestSchema(email=cfg.email, password=cfg.password)


@pytest.fixture(scope="session")
def role_auth_payloads(settings: APISettings) -> dict[str, AuthenticateRequestSchema]:
    """Builds auth payloads for roles configured in .env."""

    payloads: dict[str, AuthenticateRequestSchema] = {}
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
    role_auth_payloads: dict[str, AuthenticateRequestSchema],
) -> dict[str, str]:
    """Gets access tokens once per session for each configured role."""

    tokens: dict[str, str] = {}
    async with get_http_client(settings.api_http_client) as http_client:
        client = APIClient(client=http_client)
        for role, payload in role_auth_payloads.items():
            response = await client.authenticate_api(payload)
            assert_status_code(response.status_code, HTTPStatus.OK)
            body = AuthenticateResponseSchema.model_validate_json(response.text)
            tokens[role] = body.data.token

    return tokens
