from __future__ import annotations

from http import HTTPStatus

import allure
import pytest

from clients.auth_client import AuthClient
from config import APISettings as Settings
from schema.auth import LoginRequestSchema, MessageErrorSchema
from tools.fakers import fake_email, fake_org_name, fake_password
from tools.routes import AuthRoutes

def _require_auth_credentials(settings: Settings) -> None:
    if settings.auth_credentials is None:
        pytest.skip("AUTH_CREDENTIALS не настроены в .env")


@pytest.mark.api
@pytest.mark.auth
@pytest.mark.integration
@pytest.mark.security
@allure.feature("Authentication")
@allure.story("Login – Security")
class TestLoginSecurity:

    @allure.title("Security: unknown orgName → 400/401/403")
    async def test_unknown_org_name(self, api_client_no_auth: AuthClient) -> None:
        payload = LoginRequestSchema(
            orgName=fake_org_name(),
            identity=fake_email(),
            password=fake_password(),
        )
        response = await api_client_no_auth.login(payload)
        assert response.status_code in (
            HTTPStatus.BAD_REQUEST.value,
            HTTPStatus.UNAUTHORIZED.value,
            HTTPStatus.FORBIDDEN.value,
            HTTPStatus.TOO_MANY_REQUESTS.value,
        )

    @allure.title("Security: password not returned in response body")
    async def test_password_not_in_response(
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
        assert settings.auth_credentials.password not in response.text

    @allure.title("Security: SQL injection in identity field → not 500")
    async def test_sql_injection_in_identity(
        self,
        api_client_no_auth: AuthClient,
        settings: Settings,
    ) -> None:
        payload = LoginRequestSchema(
            orgName=settings.org_name or "",
            identity="' OR '1'='1",
            password="password",
        )
        response = await api_client_no_auth.login(payload)
        assert response.status_code != HTTPStatus.INTERNAL_SERVER_ERROR.value

    @allure.title("Security: brute force protection → 429 after N failed attempts")
    @pytest.mark.slow
    async def test_brute_force_lockout(
        self,
        api_client_no_auth: AuthClient,
        settings: Settings,
    ) -> None:
        status_codes = []
        for _ in range(10):
            response = await api_client_no_auth.post(
                AuthRoutes.LOGIN,
                json={
                    "orgName": settings.org_name,
                    "identity": fake_email(),
                    "password": "wrong_password",
                },
            )
            status_codes.append(response.status_code)
            if response.status_code == HTTPStatus.TOO_MANY_REQUESTS.value:
                break
        assert HTTPStatus.TOO_MANY_REQUESTS.value in status_codes

    @allure.title("Security: error message does not reveal if username exists")
    async def test_error_message_does_not_reveal_username(
        self,
        api_client_no_auth: AuthClient,
        settings: Settings,
    ) -> None:
        _require_auth_credentials(settings)

        # Request 1: non-existent user
        non_existent_response = await api_client_no_auth.login(
            LoginRequestSchema(
                orgName=settings.org_name or "",
                identity=fake_email(),
                password=fake_password(),
            )
        )

        # Request 2: real user + wrong password
        wrong_password_response = await api_client_no_auth.login(
            LoginRequestSchema(
                orgName=settings.org_name or "",
                identity=settings.auth_credentials.email,
                password="wrong_password_!@#$",
            )
        )

        if (
            non_existent_response.status_code == HTTPStatus.TOO_MANY_REQUESTS.value
            or wrong_password_response.status_code == HTTPStatus.TOO_MANY_REQUESTS.value
        ):
            pytest.skip("Rate limit hit — skipping message comparison")

        assert non_existent_response.status_code == HTTPStatus.BAD_REQUEST.value
        assert wrong_password_response.status_code == HTTPStatus.BAD_REQUEST.value

        body1 = MessageErrorSchema.model_validate_json(non_existent_response.text)
        body2 = MessageErrorSchema.model_validate_json(wrong_password_response.text)
        assert body1.message == body2.message

    @allure.title("Security: existing user with wrong org credentials → 400")
    async def test_existing_user_wrong_org_credentials(
        self,
        api_client_no_auth: AuthClient,
        settings: Settings,
    ) -> None:
        _require_auth_credentials(settings)

        payload = LoginRequestSchema(
            orgName=settings.org_name or "",
            identity="AutomationUser",
            password=settings.auth_credentials.password,
        )
        response = await api_client_no_auth.login(payload)
        if response.status_code == HTTPStatus.TOO_MANY_REQUESTS.value:
            pytest.skip("Rate limit hit")
        assert response.status_code == HTTPStatus.BAD_REQUEST.value
