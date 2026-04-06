from __future__ import annotations

from http import HTTPStatus

import allure
import pytest

from clients.auth_client import AuthClient
from config import APISettings as Settings
from schema.auth import LoginRequestSchema, MessageErrorSchema
from tools.assertions.base import assert_status_code
from tools.routes import AuthRoutes


def _require_auth_credentials(settings: Settings) -> None:
    if settings.auth_credentials is None:
        pytest.skip("AUTH_CREDENTIALS не настроены в .env")


@pytest.mark.api
@pytest.mark.auth
@pytest.mark.integration
@allure.feature("Authentication")
@allure.story("MFA Flow")
class TestLoginMFAFlowRefactored:

    @allure.title("MFA: OTP provided when MFA disabled → 400/422 + error message (if present)")
    async def test_otp_provided_when_mfa_disabled(
        self,
        api_client_no_auth: AuthClient,
        settings: Settings,
    ) -> None:
        _require_auth_credentials(settings)

        payload = LoginRequestSchema(
            orgName=settings.org_name or "",
            identity=settings.auth_credentials.email,
            password=settings.auth_credentials.password,
            otp_code="123456",
        )
        response = await api_client_no_auth.login(payload)

        assert response.status_code in {
            HTTPStatus.BAD_REQUEST.value,
            HTTPStatus.UNPROCESSABLE_ENTITY.value,
        }

        if response.status_code == HTTPStatus.BAD_REQUEST.value:
            body = MessageErrorSchema.model_validate_json(response.text)
            assert body.message

    @allure.title("MFA: extra fields in request → 400 or 422")
    async def test_extra_fields_in_request(
        self,
        api_client_no_auth: AuthClient,
        settings: Settings,
    ) -> None:
        _require_auth_credentials(settings)

        response = await api_client_no_auth.post(
            AuthRoutes.LOGIN,
            json={
                "orgName": settings.org_name or "",
                "identity": settings.auth_credentials.email,
                "password": settings.auth_credentials.password,
                "otp_code": "123456",
                "test": "extra_field",
            },
        )
        assert response.status_code in (
            HTTPStatus.BAD_REQUEST.value,
            HTTPStatus.UNPROCESSABLE_ENTITY.value,
        )

    @allure.title("MFA: OTP with 7 digits (too long) → 400 or 422")
    async def test_otp_too_long(
        self,
        api_client_no_auth: AuthClient,
        settings: Settings,
    ) -> None:
        _require_auth_credentials(settings)
        if not settings.auth_credentials.otp_secret:
            pytest.skip("Requires MFA-enabled account (OTP_SECRET not set)")

        payload = LoginRequestSchema(
            orgName=settings.org_name or "",
            identity=settings.auth_credentials.email,
            password=settings.auth_credentials.password,
            otp_code="1234567",
        )
        response = await api_client_no_auth.login(payload)
        assert response.status_code in (
            HTTPStatus.BAD_REQUEST.value,
            HTTPStatus.UNPROCESSABLE_ENTITY.value,
        )

    @allure.title("MFA: OTP with 5 digits (too short) → 400 or 422")
    async def test_otp_too_short(
        self,
        api_client_no_auth: AuthClient,
        settings: Settings,
    ) -> None:
        _require_auth_credentials(settings)
        if not settings.auth_credentials.otp_secret:
            pytest.skip("Requires MFA-enabled account (OTP_SECRET not set)")

        payload = LoginRequestSchema(
            orgName=settings.org_name or "",
            identity=settings.auth_credentials.email,
            password=settings.auth_credentials.password,
            otp_code="12345",
        )
        response = await api_client_no_auth.login(payload)
        assert response.status_code in (
            HTTPStatus.BAD_REQUEST.value,
            HTTPStatus.UNPROCESSABLE_ENTITY.value,
        )