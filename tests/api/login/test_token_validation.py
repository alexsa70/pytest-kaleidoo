from __future__ import annotations

import base64
import json
from http import HTTPStatus

import allure
import pytest

from clients.auth_client import AuthClient
from config import APISettings as Settings
from schema.auth import LoginRequestSchema, SSOLoginResponseSchema


def _decode_jwt_payload(token: str) -> dict:
    """Декодирует payload JWT без проверки подписи."""
    payload_b64 = token.split(".")[1]
    # base64url → base64 (добавить padding)
    padding = 4 - len(payload_b64) % 4
    payload_b64 += "=" * (padding % 4)
    return json.loads(base64.urlsafe_b64decode(payload_b64))


@pytest.mark.api
@pytest.mark.auth
@pytest.mark.integration
@allure.feature("Authentication")
@allure.story("Login – Token Validation")
class TestLoginTokenValidation:

    @allure.title("Token: accessToken has valid JWT 3-part structure")
    async def test_access_token_jwt_structure(
        self,
        api_client_no_auth: AuthClient,
        settings: Settings,
    ) -> None:
        if settings.auth_credentials is None:
            pytest.skip("AUTH_CREDENTIALS не настроены в .env")

        payload = LoginRequestSchema(
            orgName=settings.org_name or "",
            identity=settings.auth_credentials.email,
            password=settings.auth_credentials.password,
        )
        response = await api_client_no_auth.login(payload)
        if response.status_code == HTTPStatus.TOO_MANY_REQUESTS.value:
            pytest.skip("Rate limit hit")
        assert response.status_code == HTTPStatus.OK.value

        body = SSOLoginResponseSchema.model_validate_json(response.text)
        parts = body.token.split(".")
        assert len(parts) == 3
        assert parts[0].startswith("eyJ")

    @allure.title("Token: JWT payload contains required claims (sub, exp, iat)")
    async def test_jwt_payload_required_claims(
        self,
        api_client_no_auth: AuthClient,
        settings: Settings,
    ) -> None:
        if settings.auth_credentials is None:
            pytest.skip("AUTH_CREDENTIALS не настроены в .env")

        payload = LoginRequestSchema(
            orgName=settings.org_name or "",
            identity=settings.auth_credentials.email,
            password=settings.auth_credentials.password,
        )
        response = await api_client_no_auth.login(payload)
        if response.status_code == HTTPStatus.TOO_MANY_REQUESTS.value:
            pytest.skip("Rate limit hit")
        assert response.status_code == HTTPStatus.OK.value

        body = SSOLoginResponseSchema.model_validate_json(response.text)
        jwt_payload = _decode_jwt_payload(body.token)

        assert "sub" in jwt_payload
        assert "exp" in jwt_payload
        assert "iat" in jwt_payload
        assert isinstance(jwt_payload["exp"], int)
        assert isinstance(jwt_payload["iat"], int)
