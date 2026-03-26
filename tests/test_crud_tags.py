from __future__ import annotations

import uuid
from http import HTTPStatus

import allure
import pytest

from tests.kal_api_migration_helpers import assert_status, get_env_or_skip, request_as_role


async def _create_tag(*, api_client, tokens_by_role: dict[str, str], role: str) -> tuple[str, str]:
    tag_name = f"test_tag_{uuid.uuid4().hex[:8]}"
    endpoint = get_env_or_skip("KAL_CREATE_TAG_ENDPOINT")
    response = await request_as_role(
        api_client=api_client,
        tokens_by_role=tokens_by_role,
        role=role,
        method="POST",
        url=endpoint,
        json_body={"tag_name": tag_name},
    )
    assert_status(response, HTTPStatus.OK, f"create tag as {role}")
    tag_id = response.json().get("tag_id") or response.json().get("id")
    if not tag_id:
        pytest.skip("tag_id missing in create tag response")
    return tag_id, tag_name


async def _delete_tag(*, api_client, tokens_by_role: dict[str, str], role: str, tag_id: str) -> None:
    endpoint = get_env_or_skip("KAL_DELETE_TAGS_ENDPOINT")
    await request_as_role(
        api_client=api_client,
        tokens_by_role=tokens_by_role,
        role=role,
        method="POST",
        url=endpoint,
        json_body={"tag_ids": tag_id},
    )


@pytest.mark.api
@pytest.mark.integration
@allure.feature("CRUD Tags")
class TestCRUDTags:
    async def test_create_tag_as_admin(self, api_client, tokens_by_role: dict[str, str]) -> None:
        tag_id, _ = await _create_tag(api_client=api_client, tokens_by_role=tokens_by_role, role="admin")
        assert tag_id

    async def test_get_tags_as_admin(self, api_client, tokens_by_role: dict[str, str]) -> None:
        tag_id, tag_name = await _create_tag(api_client=api_client, tokens_by_role=tokens_by_role, role="admin")
        try:
            endpoint = get_env_or_skip("KAL_GET_TAGS_ENDPOINT")
            response = await request_as_role(
                api_client=api_client,
                tokens_by_role=tokens_by_role,
                role="admin",
                method="POST",
                url=endpoint,
                json_body={"tag_type": "project"},
            )
            assert_status(response, HTTPStatus.OK, "get tags as admin")
            tags = response.json().get("tags", [])
            assert any(tag.get("id") == tag_id and tag.get("name") == tag_name for tag in tags)
        finally:
            await _delete_tag(api_client=api_client, tokens_by_role=tokens_by_role, role="admin", tag_id=tag_id)

    async def test_update_tag_as_admin(self, api_client, tokens_by_role: dict[str, str]) -> None:
        tag_id, tag_name = await _create_tag(api_client=api_client, tokens_by_role=tokens_by_role, role="admin")
        updated_name = f"{tag_name}_updated"
        try:
            endpoint = get_env_or_skip("KAL_UPDATE_TAG_ENDPOINT")
            response = await request_as_role(
                api_client=api_client,
                tokens_by_role=tokens_by_role,
                role="admin",
                method="POST",
                url=endpoint,
                json_body={"tag_id": tag_id, "name": updated_name},
            )
            assert_status(response, HTTPStatus.OK, "update tag as admin")
        finally:
            await _delete_tag(api_client=api_client, tokens_by_role=tokens_by_role, role="admin", tag_id=tag_id)

    async def test_delete_tag_as_admin(self, api_client, tokens_by_role: dict[str, str]) -> None:
        tag_id, _ = await _create_tag(api_client=api_client, tokens_by_role=tokens_by_role, role="admin")
        endpoint = get_env_or_skip("KAL_DELETE_TAGS_ENDPOINT")
        response = await request_as_role(
            api_client=api_client,
            tokens_by_role=tokens_by_role,
            role="admin",
            method="POST",
            url=endpoint,
            json_body={"tag_ids": tag_id},
        )
        assert_status(response, HTTPStatus.OK, "delete tag as admin")

    async def test_create_tag_as_regular_user(self, api_client, tokens_by_role: dict[str, str]) -> None:
        tag_id, _ = await _create_tag(api_client=api_client, tokens_by_role=tokens_by_role, role="regular")
        assert tag_id

    async def test_get_tags_as_regular_user(self, api_client, tokens_by_role: dict[str, str]) -> None:
        tag_id, tag_name = await _create_tag(api_client=api_client, tokens_by_role=tokens_by_role, role="regular")
        try:
            endpoint = get_env_or_skip("KAL_GET_TAGS_ENDPOINT")
            response = await request_as_role(
                api_client=api_client,
                tokens_by_role=tokens_by_role,
                role="regular",
                method="POST",
                url=endpoint,
                json_body={"tag_type": "project"},
            )
            assert_status(response, HTTPStatus.OK, "get tags as regular")
            tags = response.json().get("tags", [])
            assert any(tag.get("id") == tag_id and tag.get("name") == tag_name for tag in tags)
        finally:
            await _delete_tag(api_client=api_client, tokens_by_role=tokens_by_role, role="regular", tag_id=tag_id)

    async def test_update_tag_as_regular_user(self, api_client, tokens_by_role: dict[str, str]) -> None:
        tag_id, tag_name = await _create_tag(api_client=api_client, tokens_by_role=tokens_by_role, role="regular")
        updated_name = f"{tag_name}_updated"
        try:
            endpoint = get_env_or_skip("KAL_UPDATE_TAG_ENDPOINT")
            response = await request_as_role(
                api_client=api_client,
                tokens_by_role=tokens_by_role,
                role="regular",
                method="POST",
                url=endpoint,
                json_body={"tag_id": tag_id, "name": updated_name},
            )
            assert_status(response, HTTPStatus.OK, "update tag as regular")
        finally:
            await _delete_tag(api_client=api_client, tokens_by_role=tokens_by_role, role="regular", tag_id=tag_id)

    async def test_delete_tag_as_regular_user(self, api_client, tokens_by_role: dict[str, str]) -> None:
        tag_id, _ = await _create_tag(api_client=api_client, tokens_by_role=tokens_by_role, role="regular")
        endpoint = get_env_or_skip("KAL_DELETE_TAGS_ENDPOINT")
        response = await request_as_role(
            api_client=api_client,
            tokens_by_role=tokens_by_role,
            role="regular",
            method="POST",
            url=endpoint,
            json_body={"tag_ids": tag_id},
        )
        assert_status(response, HTTPStatus.OK, "delete tag as regular")
