import time
from http import HTTPStatus

import allure
import pytest

from clients.auth_client import AuthClient
from config import APISettings as Settings
from schema.auth import ResetPasswordRequestSchema
from tools.assertions.base import assert_status_code
from tools.fakers import fake_email

EXPECTED_MESSAGE = "Password reset request processed"


@pytest.mark.api
@pytest.mark.auth
@pytest.mark.integration
@allure.feature("Authentication")
@allure.story("Reset Password")
class TestResetPassword:

    @allure.title("Reset Password: valid email → 200 + expected message")
    async def test_reset_password_valid_email(self, api_client_no_auth: AuthClient) -> None:
        payload = ResetPasswordRequestSchema(email=fake_email())
        response = await api_client_no_auth.reset_password(payload)

        assert_status_code(response.status_code, HTTPStatus.OK)
        data = response.json()
        message = data.get("message", data) if isinstance(data, dict) else data
        assert message == EXPECTED_MESSAGE

    @allure.title("Reset Password: with org_name → 200")
    async def test_reset_password_with_org_name(
        self,
        api_client_no_auth: AuthClient,
        settings: Settings,
    ) -> None:
        payload = ResetPasswordRequestSchema(
            email=fake_email(),
            org_name=settings.org_name or "acme-corp",
        )
        response = await api_client_no_auth.reset_password(payload)
        assert_status_code(response.status_code, HTTPStatus.OK)

    @allure.title("Reset Password: non-existent email → 200 (anti-enumeration)")
    async def test_reset_password_nonexistent_email(self, api_client_no_auth: AuthClient) -> None:
        payload = ResetPasswordRequestSchema(email=fake_email())
        response = await api_client_no_auth.reset_password(payload)
        assert_status_code(response.status_code, HTTPStatus.OK)

    @allure.title("Reset Password: two different emails return identical response")
    async def test_reset_password_same_response(self, api_client_no_auth: AuthClient) -> None:
        first = await api_client_no_auth.reset_password(ResetPasswordRequestSchema(email=fake_email()))
        second = await api_client_no_auth.reset_password(ResetPasswordRequestSchema(email=fake_email()))

        assert first.status_code == second.status_code
        assert first.json() == second.json()

    @allure.title("Reset Password: timing difference < 500ms (anti-timing-attack)")
    @pytest.mark.security
    async def test_reset_password_no_timing_leak(self, api_client_no_auth: AuthClient) -> None:
        start = time.monotonic()
        await api_client_no_auth.reset_password(ResetPasswordRequestSchema(email=fake_email()))
        first_ms = time.monotonic() - start

        start = time.monotonic()
        await api_client_no_auth.reset_password(ResetPasswordRequestSchema(email=fake_email()))
        second_ms = time.monotonic() - start

        diff_ms = abs(first_ms - second_ms) * 1000
        assert diff_ms < 500, f"Timing difference {diff_ms:.0f}ms may reveal account existence"

    @allure.title("Reset Password: missing email → 400 or 422")
    async def test_reset_password_missing_email(self, api_client_no_auth: AuthClient) -> None:
        response = await api_client_no_auth.post("/reset_password", json={"org_name": "acme-corp"})
        assert response.status_code in (
            HTTPStatus.BAD_REQUEST.value,
            HTTPStatus.UNPROCESSABLE_ENTITY.value,
        )

    @allure.title("Reset Password: empty body → 400 or 422")
    async def test_reset_password_empty_body(self, api_client_no_auth: AuthClient) -> None:
        response = await api_client_no_auth.post("/reset_password", json={})
        assert response.status_code in (
            HTTPStatus.BAD_REQUEST.value,
            HTTPStatus.UNPROCESSABLE_ENTITY.value,
        )

    @allure.title("Reset Password: rate limit → 429 after repeated requests")
    @pytest.mark.slow
    async def test_reset_password_rate_limit_429(self, api_client_no_auth: AuthClient) -> None:
        email = fake_email()
        status_codes = []
        for _ in range(15):
            r = await api_client_no_auth.reset_password(ResetPasswordRequestSchema(email=email))
            status_codes.append(r.status_code)
            if r.status_code == HTTPStatus.TOO_MANY_REQUESTS.value:
                break
        assert HTTPStatus.TOO_MANY_REQUESTS.value in status_codes

    @allure.title("Reset Password: response must not leak user data")
    async def test_reset_password_no_user_data_leak(self, api_client_no_auth: AuthClient) -> None:
        response = await api_client_no_auth.reset_password(ResetPasswordRequestSchema(email=fake_email()))
        body = response.json()
        if isinstance(body, dict):
            sensitive_keys = {"token", "accessToken", "password", "id", "email"}
            assert not sensitive_keys.intersection(body.keys())
