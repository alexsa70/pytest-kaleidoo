from __future__ import annotations

from http import HTTPStatus

import allure
import pytest

from clients.auth_client import AuthClient
from config import APISettings as Settings
from schema.auth import LoginRequestSchema, SSOLoginResponseSchema

EXPIRES_IN_EXPECTED = 36000


def _require_auth_credentials(settings: Settings) -> None:
    if settings.auth_credentials is None:
        pytest.skip("AUTH_CREDENTIALS не настроены в .env")


@pytest.mark.api
@pytest.mark.auth
@pytest.mark.integration
@allure.feature("Authentication")
@allure.story("Login – Positive")
class TestLoginPositive:

    @allure.title("Login: valid credentials ({label}) → 200 + token")
    @pytest.mark.smoke
    @pytest.mark.regression
    @pytest.mark.parametrize("label,creds_attr", [
        ("Admin", "auth_credentials_admin"),
        ("User",  "auth_credentials_user"),
    ])
    async def test_login_valid_credentials_by_role(
        self,
        api_client_no_auth: AuthClient,
        settings: Settings,
        label: str,
        creds_attr: str,
    ) -> None:
        creds = getattr(settings, creds_attr)
        if creds is None:
            pytest.skip(f"{label} credentials not set in .env")

        payload = LoginRequestSchema(
            orgName=settings.org_name or "",
            identity=creds.email,
            password=creds.password,
        )
        response = await api_client_no_auth.login(payload)

        assert response.status_code == HTTPStatus.OK.value
        SSOLoginResponseSchema.model_validate_json(response.text)

    @allure.title("Login: otp_code='' when MFA disabled → 200")
    async def test_login_otp_empty_string_mfa_disabled(
        self,
        api_client_no_auth: AuthClient,
        settings: Settings,
    ) -> None:
        _require_auth_credentials(settings)

        payload = LoginRequestSchema(
            orgName=settings.org_name or "",
            identity=settings.auth_credentials.email,
            password=settings.auth_credentials.password,
            otp_code="",
        )
        response = await api_client_no_auth.login(payload)

        assert response.status_code == HTTPStatus.OK.value
        data = response.json()

        if isinstance(data, dict) and data.get("mfa_required"):
            if not settings.auth_credentials.otp_secret:
                pytest.skip("MFA required but AUTH_CREDENTIALS.OTP_SECRET not set in .env")
        else:
            SSOLoginResponseSchema.model_validate(data)

    @allure.title("Login: username is case-insensitive (if supported) → 200")
    async def test_login_username_case_insensitive(
        self,
        api_client_no_auth: AuthClient,
        settings: Settings,
    ) -> None:
        _require_auth_credentials(settings)

        payload = LoginRequestSchema(
            orgName=settings.org_name or "",
            identity="ALEX",
            password=settings.auth_credentials.password,
        )
        response = await api_client_no_auth.login(payload)

        assert response.status_code == HTTPStatus.OK.value
        SSOLoginResponseSchema.model_validate_json(response.text)

    @allure.title("Login: identity in email format → 200")
    async def test_login_identity_as_email(
        self,
        api_client_no_auth: AuthClient,
        settings: Settings,
    ) -> None:
        _require_auth_credentials(settings)

        payload = LoginRequestSchema(
            orgName=settings.org_name or "",
            identity="alexsa70@gmail.com",
            password=settings.auth_credentials.password,
        )
        response = await api_client_no_auth.login(payload)

        assert response.status_code == HTTPStatus.OK.value
        SSOLoginResponseSchema.model_validate_json(response.text)

    @allure.title(f"Login: response contains refresh_token and expires_in={EXPIRES_IN_EXPECTED}")
    async def test_login_verify_response_values(
        self,
        api_client_no_auth: AuthClient,
        settings: Settings,
    ) -> None:
        _require_auth_credentials(settings)

        payload = LoginRequestSchema(
            orgName=settings.org_name or "",
            identity=settings.auth_credentials.email,
            password=settings.auth_credentials.password,
        )
        response = await api_client_no_auth.login(payload)

        assert response.status_code == HTTPStatus.OK.value
        body = SSOLoginResponseSchema.model_validate_json(response.text)
        assert body.refresh_token
        assert body.expires_in == EXPIRES_IN_EXPECTED
