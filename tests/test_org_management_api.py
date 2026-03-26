from __future__ import annotations

from http import HTTPStatus

import allure
import pytest

from tests.kal_api_migration_helpers import assert_status, get_env_or_skip, request_as_role


@pytest.mark.api
@pytest.mark.integration
@allure.feature("Organization Management")
class TestSenseOrgApi:
    async def test_admin_get_all_organizations(self, api_client, tokens_by_role: dict[str, str]) -> None:
        response = await request_as_role(
            api_client=api_client,
            tokens_by_role=tokens_by_role,
            role="super_admin",
            method="POST",
            url=get_env_or_skip("KAL_GET_ALL_ORGANIZATIONS_ENDPOINT"),
            json_body={},
        )
        assert_status(response, HTTPStatus.OK, "get all organizations as super admin")

    async def test_user_get_all_organizations(self, api_client, tokens_by_role: dict[str, str]) -> None:
        response = await request_as_role(
            api_client=api_client,
            tokens_by_role=tokens_by_role,
            role="admin",
            method="POST",
            url=get_env_or_skip("KAL_GET_ALL_ORGANIZATIONS_ENDPOINT"),
            json_body={},
        )
        assert_status(response, HTTPStatus.FORBIDDEN, "get all organizations as admin")

    async def test_user_get_all_organizations_without_auth_token(self, api_client_no_auth) -> None:
        response = await api_client_no_auth.client.request(
            method="POST",
            url=get_env_or_skip("KAL_GET_ALL_ORGANIZATIONS_ENDPOINT"),
            json={},
        )
        assert_status(response, HTTPStatus.UNAUTHORIZED, "get all organizations without auth")
