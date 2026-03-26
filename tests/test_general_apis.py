from __future__ import annotations

from http import HTTPStatus

import allure
import pytest

from tests.kal_api_migration_helpers import assert_status, get_env_or_skip, request_as_role


@pytest.mark.api
@pytest.mark.integration
@allure.feature("General Queries")
class TestGeneralQueries:
    async def test_get_available_llms(self, api_client, tokens_by_role: dict[str, str]) -> None:
        response = await request_as_role(
            api_client=api_client,
            tokens_by_role=tokens_by_role,
            role="admin",
            method="POST",
            url=get_env_or_skip("KAL_GET_AVAILABLE_LLMS_ENDPOINT"),
            json_body={},
        )
        assert_status(response, HTTPStatus.OK, "get available llms")

    async def test_get_all_automations(self, api_client, tokens_by_role: dict[str, str]) -> None:
        response = await request_as_role(
            api_client=api_client,
            tokens_by_role=tokens_by_role,
            role="admin",
            method="POST",
            url=get_env_or_skip("KAL_GET_ALL_AUTOMATIONS_ENDPOINT"),
            json_body={},
        )
        assert_status(response, HTTPStatus.OK, "get all automations")

    async def test_get_tags(self, api_client, tokens_by_role: dict[str, str]) -> None:
        response = await request_as_role(
            api_client=api_client,
            tokens_by_role=tokens_by_role,
            role="admin",
            method="POST",
            url=get_env_or_skip("KAL_GET_TAGS_ENDPOINT"),
            json_body={},
        )
        assert_status(response, HTTPStatus.OK, "get tags")

    async def test_get_all_project_types(self, api_client, tokens_by_role: dict[str, str]) -> None:
        response = await request_as_role(
            api_client=api_client,
            tokens_by_role=tokens_by_role,
            role="admin",
            method="POST",
            url=get_env_or_skip("KAL_GET_ALL_PROJECT_TYPES_ENDPOINT"),
            json_body={},
        )
        assert_status(response, HTTPStatus.OK, "get all project types")

    async def test_get_roles(self, api_client, tokens_by_role: dict[str, str]) -> None:
        response = await request_as_role(
            api_client=api_client,
            tokens_by_role=tokens_by_role,
            role="admin",
            method="POST",
            url=get_env_or_skip("KAL_GET_ROLES_ENDPOINT"),
            json_body={},
        )
        assert_status(response, HTTPStatus.OK, "get roles")

    async def test_get_user_conversations(self, api_client, tokens_by_role: dict[str, str]) -> None:
        response = await request_as_role(
            api_client=api_client,
            tokens_by_role=tokens_by_role,
            role="admin",
            method="POST",
            url=get_env_or_skip("KAL_GET_USER_CONVERSATIONS_ENDPOINT"),
            json_body={},
        )
        assert_status(response, HTTPStatus.OK, "get user conversations")
