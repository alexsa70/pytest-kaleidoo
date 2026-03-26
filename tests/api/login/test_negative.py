from __future__ import annotations

from http import HTTPStatus

import allure
import pytest

from clients.auth_client import AuthClient
from config import APISettings as Settings
from schema.auth import LoginRequestSchema, MessageErrorSchema
from tools.fakers import fake_email, fake_password

EXPECTED_ERROR_MESSAGE = "User name or password incorrect."


@pytest.mark.api
@pytest.mark.auth
@pytest.mark.integration
@allure.feature("Authentication")
@allure.story("Login – Negative")
class TestLoginNegative:

    @allure.title("Login: invalid password → 400 + error message")
    async def test_invalid_password(
        self,
        api_client_no_auth: AuthClient,
        settings: Settings,
    ) -> None:
        if settings.auth_credentials is None:
            pytest.skip("AUTH_CREDENTIALS не настроены в .env")

        payload = LoginRequestSchema(
            orgName=settings.org_name or "",
            identity=settings.auth_credentials.email,
            password="wrong_password_!@#$",
        )
        response = await api_client_no_auth.login(payload)

        assert response.status_code == HTTPStatus.BAD_REQUEST.value
        body = MessageErrorSchema.model_validate_json(response.text)
        assert body.message == EXPECTED_ERROR_MESSAGE

    @allure.title("Login: invalid username → 400 + error message")
    async def test_invalid_username(
        self,
        api_client_no_auth: AuthClient,
        settings: Settings,
    ) -> None:
        payload = LoginRequestSchema(
            orgName=settings.org_name or "",
            identity=fake_email(),
            password=fake_password(),
        )
        response = await api_client_no_auth.login(payload)

        assert response.status_code == HTTPStatus.BAD_REQUEST.value
        body = MessageErrorSchema.model_validate_json(response.text)
        assert body.message == EXPECTED_ERROR_MESSAGE

    @allure.title("Login: missing password field → 400 or 422")
    async def test_missing_password(
        self,
        api_client_no_auth: AuthClient,
        settings: Settings,
    ) -> None:
        response = await api_client_no_auth.post(
            "/login",
            json={"orgName": settings.org_name, "identity": fake_email()},
        )
        assert response.status_code in (
            HTTPStatus.BAD_REQUEST.value,
            HTTPStatus.UNPROCESSABLE_ENTITY.value,
        )

    @allure.title("Login: missing username field → 400 or 422")
    async def test_missing_username(
        self,
        api_client_no_auth: AuthClient,
        settings: Settings,
    ) -> None:
        response = await api_client_no_auth.post(
            "/login",
            json={"orgName": settings.org_name, "password": fake_password()},
        )
        assert response.status_code in (
            HTTPStatus.BAD_REQUEST.value,
            HTTPStatus.UNPROCESSABLE_ENTITY.value,
        )

    @allure.title("Login: missing orgName field → 400 or 422")
    async def test_missing_org_name(self, api_client_no_auth: AuthClient) -> None:
        response = await api_client_no_auth.post(
            "/login",
            json={"identity": fake_email(), "password": fake_password()},
        )
        assert response.status_code in (
            HTTPStatus.BAD_REQUEST.value,
            HTTPStatus.UNPROCESSABLE_ENTITY.value,
        )

    @allure.title("Login: empty body → 400 or 422")
    async def test_empty_body(self, api_client_no_auth: AuthClient) -> None:
        response = await api_client_no_auth.post("/login", json={})
        assert response.status_code in (
            HTTPStatus.BAD_REQUEST.value,
            HTTPStatus.UNPROCESSABLE_ENTITY.value,
        )
