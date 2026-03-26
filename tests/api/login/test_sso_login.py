from http import HTTPStatus

import allure
import pytest

from clients.auth_client import AuthClient
from schema.auth import SSOLoginRequestSchema, MessageErrorSchema
from tools.assertions.base import assert_status_code


@pytest.mark.api
@pytest.mark.auth
@pytest.mark.integration
@allure.feature("Authentication")
@allure.story("SSO Login")
class TestSSOLogin:

    @allure.title("SSO: invalid code → 400 with message")
    async def test_sso_invalid_code_returns_400(self, api_client_no_auth: AuthClient) -> None:
        payload = SSOLoginRequestSchema(
            orgName="acme-corp",
            code="invalid_code_xyz",
            redirect_uri="https://app.kalsense.com/auth/callback",
            provider="google",
        )
        response = await api_client_no_auth.sso_login(payload)
        assert_status_code(response.status_code, HTTPStatus.BAD_REQUEST)
        body = MessageErrorSchema.model_validate_json(response.text)
        assert body.message

    @allure.title("SSO: missing orgName → 400 or 422")
    async def test_sso_missing_org_name(self, api_client_no_auth: AuthClient) -> None:
        response = await api_client_no_auth.post("/sso_login", json={
            "code": "some_code",
            "redirect_uri": "https://app.kalsense.com/auth/callback",
            "provider": "google",
        })
        assert response.status_code in (
            HTTPStatus.BAD_REQUEST.value,
            HTTPStatus.UNPROCESSABLE_ENTITY.value,
        )

    @allure.title("SSO: missing code → 400 or 422")
    async def test_sso_missing_code(self, api_client_no_auth: AuthClient) -> None:
        response = await api_client_no_auth.post("/sso_login", json={
            "orgName": "acme-corp",
            "redirect_uri": "https://app.kalsense.com/auth/callback",
            "provider": "google",
        })
        assert response.status_code in (
            HTTPStatus.BAD_REQUEST.value,
            HTTPStatus.UNPROCESSABLE_ENTITY.value,
        )

    @allure.title("SSO: missing redirect_uri → 400 or 422")
    async def test_sso_missing_redirect_uri(self, api_client_no_auth: AuthClient) -> None:
        response = await api_client_no_auth.post("/sso_login", json={
            "orgName": "acme-corp",
            "code": "some_code",
            "provider": "google",
        })
        assert response.status_code in (
            HTTPStatus.BAD_REQUEST.value,
            HTTPStatus.UNPROCESSABLE_ENTITY.value,
        )

    @allure.title("SSO: missing provider → 400 or 422")
    async def test_sso_missing_provider(self, api_client_no_auth: AuthClient) -> None:
        response = await api_client_no_auth.post("/sso_login", json={
            "orgName": "acme-corp",
            "code": "some_code",
            "redirect_uri": "https://app.kalsense.com/auth/callback",
        })
        assert response.status_code in (
            HTTPStatus.BAD_REQUEST.value,
            HTTPStatus.UNPROCESSABLE_ENTITY.value,
        )

    @allure.title("SSO: unknown provider → 400/422")
    async def test_sso_unknown_provider(self, api_client_no_auth: AuthClient) -> None:
        payload = SSOLoginRequestSchema(
            orgName="acme-corp",
            code="some_code",
            redirect_uri="https://app.kalsense.com/auth/callback",
            provider="unknown_provider_xyz",
        )
        response = await api_client_no_auth.sso_login(payload)
        assert response.status_code in (
            HTTPStatus.BAD_REQUEST.value,
            HTTPStatus.UNPROCESSABLE_ENTITY.value,
        )

    @allure.title("SSO: open redirect rejected → 400/422")
    async def test_sso_open_redirect_rejected(self, api_client_no_auth: AuthClient) -> None:
        payload = SSOLoginRequestSchema(
            orgName="acme-corp",
            code="some_code",
            redirect_uri="https://attacker.com/steal",
            provider="google",
        )
        response = await api_client_no_auth.sso_login(payload)
        assert response.status_code in (
            HTTPStatus.BAD_REQUEST.value,
            HTTPStatus.UNPROCESSABLE_ENTITY.value,
        )

    @allure.title("SSO: rate limit → 429 after 50+ req/min")
    @pytest.mark.slow
    async def test_sso_rate_limit_429(self, api_client_no_auth: AuthClient) -> None:
        status_codes = []
        for _ in range(55):
            r = await api_client_no_auth.post("/sso_login", json={
                "orgName": "acme-corp",
                "code": "some_code",
                "redirect_uri": "https://app.kalsense.com/auth/callback",
                "provider": "google",
            })
            status_codes.append(r.status_code)
            if r.status_code == HTTPStatus.TOO_MANY_REQUESTS.value:
                break
        assert HTTPStatus.TOO_MANY_REQUESTS.value in status_codes

    @allure.title("SSO: SQL injection in orgName → not 500")
    async def test_sso_sql_injection(self, api_client_no_auth: AuthClient) -> None:
        payload = SSOLoginRequestSchema(
            orgName="' OR '1'='1",
            code="some_code",
            redirect_uri="https://app.kalsense.com/auth/callback",
            provider="google",
        )
        response = await api_client_no_auth.sso_login(payload)
        assert response.status_code != HTTPStatus.INTERNAL_SERVER_ERROR.value

    @allure.title("SSO: JWT not leaked in error response")
    async def test_sso_no_token_in_error(self, api_client_no_auth: AuthClient) -> None:
        payload = SSOLoginRequestSchema(
            orgName="acme-corp",
            code="invalid_code",
            redirect_uri="https://app.kalsense.com/auth/callback",
            provider="google",
        )
        response = await api_client_no_auth.sso_login(payload)
        assert "eyJ" not in response.text
