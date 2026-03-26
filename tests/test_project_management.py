from __future__ import annotations

from http import HTTPStatus
from typing import AsyncIterator

import allure
import pytest
import pytest_asyncio

from tests.kal_api_migration_helpers import assert_status, get_env_or_skip, request_as_role


@pytest_asyncio.fixture
async def created_project(api_client, tokens_by_role: dict[str, str]) -> AsyncIterator[str]:
    endpoint = get_env_or_skip("KAL_CREATE_PROJECT_ENDPOINT")
    response = await request_as_role(
        api_client=api_client,
        tokens_by_role=tokens_by_role,
        role="admin",
        method="POST",
        url=endpoint,
        json_body={},
    )
    assert_status(response, HTTPStatus.OK, "create project")
    project_id = response.json().get("project_id") or response.json().get("id")
    if not project_id:
        pytest.skip("project_id missing in create project response")

    yield project_id

    await request_as_role(
        api_client=api_client,
        tokens_by_role=tokens_by_role,
        role="admin",
        method="POST",
        url=get_env_or_skip("KAL_DELETE_PROJECT_ENDPOINT"),
        json_body={"project_id": project_id},
    )


@pytest.mark.api
@pytest.mark.integration
@allure.feature("CRUD Project")
class TestSenseCrudProjectApi:
    async def test_create_project(self, created_project: str) -> None:
        assert created_project

    async def test_create_project_without_auth_token(self, api_client_no_auth) -> None:
        response = await api_client_no_auth.client.request(
            method="POST",
            url=get_env_or_skip("KAL_CREATE_PROJECT_ENDPOINT"),
            json={},
        )
        assert_status(response, HTTPStatus.UNAUTHORIZED, "create project without auth")

    async def test_create_project_with_invalid_inputs(self, api_client, tokens_by_role: dict[str, str]) -> None:
        response = await request_as_role(
            api_client=api_client,
            tokens_by_role=tokens_by_role,
            role="admin",
            method="POST",
            url=get_env_or_skip("KAL_CREATE_PROJECT_ENDPOINT"),
            json_body={"org_id": "", "product_id": ""},
        )
        assert response.status_code in {HTTPStatus.BAD_REQUEST, HTTPStatus.UNPROCESSABLE_ENTITY, HTTPStatus.FORBIDDEN}

    async def test_get_project(self, api_client, tokens_by_role: dict[str, str], created_project: str) -> None:
        response = await request_as_role(
            api_client=api_client,
            tokens_by_role=tokens_by_role,
            role="admin",
            method="POST",
            url=get_env_or_skip("KAL_GET_PROJECT_ENDPOINT"),
            json_body={"project_id": created_project},
        )
        assert_status(response, HTTPStatus.OK, "get project")

    async def test_get_project_with_invalid_id(self, api_client, tokens_by_role: dict[str, str]) -> None:
        response = await request_as_role(
            api_client=api_client,
            tokens_by_role=tokens_by_role,
            role="admin",
            method="POST",
            url=get_env_or_skip("KAL_GET_PROJECT_ENDPOINT"),
            json_body={"project_id": "invalid"},
        )
        assert response.status_code in {HTTPStatus.BAD_REQUEST, HTTPStatus.UNPROCESSABLE_ENTITY, HTTPStatus.FORBIDDEN}

    @pytest.mark.parametrize("action_endpoint", ["KAL_GET_PROJECT_ENDPOINT"])
    async def test_project_actions_without_auth_token(self, api_client_no_auth, created_project: str, action_endpoint: str) -> None:
        response = await api_client_no_auth.client.request(
            method="POST",
            url=get_env_or_skip(action_endpoint),
            json={"project_id": created_project},
        )
        assert_status(response, HTTPStatus.UNAUTHORIZED, f"project action without auth: {action_endpoint}")

    async def test_get_all_projects_as_admin(self, api_client, tokens_by_role: dict[str, str]) -> None:
        response = await request_as_role(
            api_client=api_client,
            tokens_by_role=tokens_by_role,
            role="admin",
            method="POST",
            url=get_env_or_skip("KAL_GET_ALL_PROJECTS_ENDPOINT"),
            json_body={},
        )
        assert_status(response, HTTPStatus.OK, "get all projects as admin")

    async def test_get_all_projects_as_user(self, api_client, tokens_by_role: dict[str, str]) -> None:
        response = await request_as_role(
            api_client=api_client,
            tokens_by_role=tokens_by_role,
            role="regular",
            method="POST",
            url=get_env_or_skip("KAL_GET_ALL_PROJECTS_ENDPOINT"),
            json_body={},
        )
        assert_status(response, HTTPStatus.OK, "get all projects as regular")
