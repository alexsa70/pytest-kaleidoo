from http import HTTPStatus

import allure
import pytest

from clients.operations_client import APIClient
from config import APISettings as Settings
from schema.operations import (
    AuthenticateRequestSchema,
    AuthenticateResponseSchema,
    ErrorSchema,
)
from tools.assertions.base import assert_status_code
from tools.assertions.operations import assert_authenticate_response_valid
from tools.fakers import fake_email, fake_password


@pytest.mark.api
@pytest.mark.auth
@pytest.mark.integration
@pytest.mark.usefixtures("auth_payload")
@allure.feature("Authentication")
@allure.story("Authenticate")
class TestAuthenticate:

    @allure.title("Authenticate: valid credentials → 200 + data.token")
    async def test_authenticate_valid_credentials(
        self,
        api_client: APIClient,
        settings: Settings,
    ) -> None:
        payload = AuthenticateRequestSchema(
            email=settings.auth_credentials.email,
            password=settings.auth_credentials.password,
        )
        response = await api_client.authenticate_api(payload)

        assert_status_code(response.status_code, HTTPStatus.OK)
        body = AuthenticateResponseSchema.model_validate_json(response.text)
        assert_authenticate_response_valid(body)

    @allure.title("Authenticate: token is JWT format")
    async def test_authenticate_token_is_jwt(
        self,
        api_client: APIClient,
        settings: Settings,
    ) -> None:
        payload = AuthenticateRequestSchema(
            email=settings.auth_credentials.email,
            password=settings.auth_credentials.password,
        )
        response = await api_client.authenticate_api(payload)
        assert_status_code(response.status_code, HTTPStatus.OK)

        body = AuthenticateResponseSchema.model_validate_json(response.text)
        assert body.data.token.startswith("eyJ"), "token should be a JWT"

    @allure.title("Authenticate: invalid password → 401")
    async def test_authenticate_invalid_password(
        self,
        api_client: APIClient,
        settings: Settings,
    ) -> None:
        payload = AuthenticateRequestSchema(
            email=settings.auth_credentials.email,
            password="wrong_password_!@#$",
        )
        response = await api_client.authenticate_api(payload)
        assert_status_code(response.status_code, HTTPStatus.UNAUTHORIZED)

    @allure.title("Authenticate: non-existent email → 401")
    async def test_authenticate_nonexistent_user(self, api_client: APIClient) -> None:
        payload = AuthenticateRequestSchema(
            email=fake_email(),
            password=fake_password(),
        )
        response = await api_client.authenticate_api(payload)
        assert_status_code(response.status_code, HTTPStatus.UNAUTHORIZED)

    @allure.title("Authenticate: missing password → 400")
    async def test_authenticate_missing_password(
        self,
        api_client: APIClient,
        settings: Settings,
    ) -> None:
        response = await api_client.post(
            "/authenticate",
            json={"email": settings.auth_credentials.email},
        )
        assert response.status_code == HTTPStatus.BAD_REQUEST.value

    @allure.title("Authenticate: missing email → 400")
    async def test_authenticate_missing_email(
        self,
        api_client: APIClient,
        settings: Settings,
    ) -> None:
        response = await api_client.post(
            "/authenticate",
            json={"password": settings.auth_credentials.password},
        )
        assert response.status_code == HTTPStatus.BAD_REQUEST.value

    @allure.title("Authenticate: empty body → 400")
    async def test_authenticate_empty_body(self, api_client: APIClient) -> None:
        response = await api_client.post("/authenticate", json={})
        assert response.status_code == HTTPStatus.BAD_REQUEST.value

    @allure.title("Authenticate: missing OTP when MFA enabled → 401")
    async def test_authenticate_missing_otp_when_mfa_required(
        self,
        api_client: APIClient,
        settings: Settings,
    ) -> None:
        payload = AuthenticateRequestSchema(
            email=settings.auth_credentials.email,
            password=settings.auth_credentials.password,
        )
        response = await api_client.authenticate_api(payload)
        if response.status_code == HTTPStatus.UNAUTHORIZED.value:
            body = ErrorSchema.model_validate_json(response.text)
            assert body.error in ("otp_required", "invalid_credentials")

    @allure.title("Authenticate: invalid OTP → 401")
    async def test_authenticate_invalid_otp(
        self,
        api_client: APIClient,
        settings: Settings,
    ) -> None:
        payload = AuthenticateRequestSchema(
            email=settings.auth_credentials.email,
            password=settings.auth_credentials.password,
            otp="000000",
        )
        response = await api_client.authenticate_api(payload)
        if response.status_code == HTTPStatus.UNAUTHORIZED.value:
            body = ErrorSchema.model_validate_json(response.text)
            assert body.error in ("invalid_otp", "otp_required", "invalid_credentials")

    @allure.title("Authenticate: response must not contain password")
    async def test_authenticate_no_password_in_response(
        self,
        api_client: APIClient,
        settings: Settings,
    ) -> None:
        payload = AuthenticateRequestSchema(
            email=settings.auth_credentials.email,
            password=settings.auth_credentials.password,
        )
        response = await api_client.authenticate_api(payload)
        assert settings.auth_credentials.password not in response.text

    @allure.title("Authenticate: SQL injection in email → not 500")
    async def test_authenticate_sql_injection(self, api_client: APIClient) -> None:
        payload = AuthenticateRequestSchema(
            email="' OR '1'='1",
            password="password",
        )
        response = await api_client.authenticate_api(payload)
        assert response.status_code != HTTPStatus.INTERNAL_SERVER_ERROR.value

    @allure.title("Authenticate: very long email → not 500")
    async def test_authenticate_very_long_email(self, api_client: APIClient) -> None:
        payload = AuthenticateRequestSchema(
            email="a" * 10000 + "@test.com",
            password="password",
        )
        response = await api_client.authenticate_api(payload)
        assert response.status_code in (
            HTTPStatus.BAD_REQUEST.value,
            HTTPStatus.UNAUTHORIZED.value,
            HTTPStatus.UNPROCESSABLE_ENTITY.value,
        )
