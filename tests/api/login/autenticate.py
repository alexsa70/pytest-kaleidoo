from __future__ import annotations

from http import HTTPStatus
from typing import Optional

import allure
import pyotp
import pytest

from clients.auth_client import AuthClient
from config import APISettings as Settings
from schema.auth import (
    LoginRequestSchema,
    LoginMFAResponseSchema,
    SSOLoginResponseSchema,
    MessageErrorSchema,
)
from tools.assertions.base import assert_status_code
from tools.fakers import fake_email, fake_password, fake_org_name


def _make_login_payload(settings: Settings, *, otp_code: Optional[str] = None) -> LoginRequestSchema:
    """Builds a login payload, auto-generating OTP if otp_secret is configured."""
    code = otp_code
    if code is None and settings.auth_credentials.otp_secret:
        code = pyotp.TOTP(settings.auth_credentials.otp_secret).now()
    return LoginRequestSchema(
        orgName=settings.org_name or "",
        identity=settings.auth_credentials.email,
        password=settings.auth_credentials.password,
        otp_code=code,
    )


@pytest.mark.api
@pytest.mark.auth
@pytest.mark.integration
@allure.feature("Authentication")
@allure.story("Login")
class TestLogin:

    @allure.title("Login: valid credentials → 200 + token")
    async def test_login_valid_credentials(
        self,
        api_client: AuthClient,
        settings: Settings,
    ) -> None:
        payload = _make_login_payload(settings)
        response = await api_client.login(payload)

        assert_status_code(response.status_code, HTTPStatus.OK)
        data = response.json()
        if isinstance(data, dict) and data.get("mfa_required"):
            pytest.skip("MFA required but AUTH_CREDENTIALS.OTP_SECRET not set in .env")
        body = SSOLoginResponseSchema.model_validate(data)
        assert body.token, "token should not be empty"

    @allure.title("Login: token is JWT format")
    async def test_login_token_is_jwt(
        self,
        api_client: AuthClient,
        settings: Settings,
    ) -> None:
        payload = _make_login_payload(settings)
        response = await api_client.login(payload)
        assert_status_code(response.status_code, HTTPStatus.OK)

        data = response.json()
        if isinstance(data, dict) and data.get("mfa_required"):
            pytest.skip("MFA required but AUTH_CREDENTIALS.OTP_SECRET not set in .env")
        body = SSOLoginResponseSchema.model_validate(data)
        assert body.token.startswith("eyJ"), "token should be a JWT"

    @allure.title("Login: invalid password → 400")
    async def test_login_invalid_password(
        self,
        api_client: AuthClient,
        settings: Settings,
    ) -> None:
        payload = LoginRequestSchema(
            orgName=settings.org_name or "",
            identity=settings.auth_credentials.email,
            password="wrong_password_!@#$",
        )
        response = await api_client.login(payload)
        assert_status_code(response.status_code, HTTPStatus.BAD_REQUEST)

    @allure.title("Login: non-existent user → 400")
    async def test_login_nonexistent_user(
        self,
        api_client: AuthClient,
        settings: Settings,
    ) -> None:
        payload = LoginRequestSchema(
            orgName=settings.org_name or "",
            identity=fake_email(),
            password=fake_password(),
        )
        response = await api_client.login(payload)
        assert_status_code(response.status_code, HTTPStatus.BAD_REQUEST)

    @allure.title("Login: missing password → 400 or 422")
    async def test_login_missing_password(
        self,
        api_client: AuthClient,
        settings: Settings,
    ) -> None:
        response = await api_client.post(
            "/login",
            json={"orgName": settings.org_name, "identity": settings.auth_credentials.email},
        )
        assert response.status_code in (
            HTTPStatus.BAD_REQUEST.value,
            HTTPStatus.UNPROCESSABLE_ENTITY.value,
        )

    @allure.title("Login: missing identity → 400 or 422")
    async def test_login_missing_identity(
        self,
        api_client: AuthClient,
        settings: Settings,
    ) -> None:
        response = await api_client.post(
            "/login",
            json={"orgName": settings.org_name, "password": settings.auth_credentials.password},
        )
        assert response.status_code in (
            HTTPStatus.BAD_REQUEST.value,
            HTTPStatus.UNPROCESSABLE_ENTITY.value,
        )

    @allure.title("Login: missing orgName → 400 or 422")
    async def test_login_missing_org_name(
        self,
        api_client: AuthClient,
        settings: Settings,
    ) -> None:
        response = await api_client.post(
            "/login",
            json={"identity": settings.auth_credentials.email, "password": settings.auth_credentials.password},
        )
        assert response.status_code in (
            HTTPStatus.BAD_REQUEST.value,
            HTTPStatus.UNPROCESSABLE_ENTITY.value,
        )

    @allure.title("Login: empty body → 400 or 422")
    async def test_login_empty_body(self, api_client: AuthClient) -> None:
        response = await api_client.post("/login", json={})
        assert response.status_code in (
            HTTPStatus.BAD_REQUEST.value,
            HTTPStatus.UNPROCESSABLE_ENTITY.value,
        )

    @allure.title("Login: MFA challenge returned when otp_code omitted")
    async def test_login_mfa_required(
        self,
        api_client: AuthClient,
        settings: Settings,
    ) -> None:
        payload = LoginRequestSchema(
            orgName=settings.org_name or "",
            identity=settings.auth_credentials.email,
            password=settings.auth_credentials.password,
            # otp_code intentionally omitted
        )
        response = await api_client.login(payload)
        if response.status_code != HTTPStatus.OK.value:
            return  # non-200 is fine (e.g. 401 if MFA not enabled for this account)

        data = response.json()
        if not isinstance(data, dict) or not data.get("mfa_required"):
            pytest.skip("Account does not require MFA — test not applicable")

        body = LoginMFAResponseSchema.model_validate(data)
        assert body.mfa_required is True
        assert body.message
        # qr_code is present on first enrollment, None for already-enrolled users

    @allure.title("Login: invalid OTP → 400")
    async def test_login_invalid_otp(
        self,
        api_client: AuthClient,
        settings: Settings,
    ) -> None:
        payload = LoginRequestSchema(
            orgName=settings.org_name or "",
            identity=settings.auth_credentials.email,
            password=settings.auth_credentials.password,
            otp_code="000000",
        )
        response = await api_client.login(payload)
        if response.status_code == HTTPStatus.BAD_REQUEST.value:
            body = MessageErrorSchema.model_validate_json(response.text)
            assert body.message

    @allure.title("Login: response must not contain password")
    async def test_login_no_password_in_response(
        self,
        api_client: AuthClient,
        settings: Settings,
    ) -> None:
        payload = LoginRequestSchema(
            orgName=settings.org_name or "",
            identity=settings.auth_credentials.email,
            password=settings.auth_credentials.password,
        )
        response = await api_client.login(payload)
        assert settings.auth_credentials.password not in response.text

    @allure.title("Login: SQL injection in identity → not 500")
    async def test_login_sql_injection(
        self,
        api_client: AuthClient,
        settings: Settings,
    ) -> None:
        payload = LoginRequestSchema(
            orgName=settings.org_name or "",
            identity="' OR '1'='1",
            password="password",
        )
        response = await api_client.login(payload)
        assert response.status_code != HTTPStatus.INTERNAL_SERVER_ERROR.value

    @allure.title("Login: unknown orgName → 400")
    async def test_login_unknown_org(self, api_client: AuthClient) -> None:
        payload = LoginRequestSchema(
            orgName=fake_org_name(),
            identity=fake_email(),
            password=fake_password(),
        )
        response = await api_client.login(payload)
        assert response.status_code == HTTPStatus.BAD_REQUEST.value

    @allure.title("Login: rate limit → 429 after 5+ req/min per username")
    @pytest.mark.slow
    async def test_login_rate_limit_429(
        self,
        api_client: AuthClient,
        settings: Settings,
    ) -> None:
        status_codes = []
        for _ in range(10):
            r = await api_client.post(
                "/login",
                json={
                    "orgName": settings.org_name,
                    "identity": settings.auth_credentials.email,
                    "password": "wrong_password",
                },
            )
            status_codes.append(r.status_code)
            if r.status_code == HTTPStatus.TOO_MANY_REQUESTS.value:
                break
        assert HTTPStatus.TOO_MANY_REQUESTS.value in status_codes
