from __future__ import annotations

import uuid
from http import HTTPStatus
from typing import AsyncIterator

import allure
import pytest
import pytest_asyncio

from tests.kal_api_migration_helpers import assert_status, get_env_or_skip, request_as_role


@pytest_asyncio.fixture(scope="session")
async def created_media_project(api_client, tokens_by_role: dict[str, str]) -> AsyncIterator[str]:
    create_project_endpoint = get_env_or_skip("KAL_CREATE_PROJECT_ENDPOINT")
    delete_project_endpoint = get_env_or_skip("KAL_DELETE_PROJECT_ENDPOINT")

    response = await request_as_role(
        api_client=api_client,
        tokens_by_role=tokens_by_role,
        role="admin",
        method="POST",
        url=create_project_endpoint,
        json_body={"project_type_name": "KalMedia"},
    )
    assert_status(response, HTTPStatus.OK, "create media project")
    project_id = response.json().get("project_id") or response.json().get("id")
    if not project_id:
        pytest.skip("project_id is missing in create project response")

    yield project_id

    await request_as_role(
        api_client=api_client,
        tokens_by_role=tokens_by_role,
        role="admin",
        method="POST",
        url=delete_project_endpoint,
        json_body={"project_id": project_id},
    )


async def _upload_image(
    *,
    api_client,
    tokens_by_role: dict[str, str],
    role: str,
    project_id: str,
    image_name: str,
) -> str:
    endpoint = get_env_or_skip("KAL_CREATE_FILE_ENDPOINT")
    org_id = get_env_or_skip("KAL_ORG_ID")

    response = await request_as_role(
        api_client=api_client,
        tokens_by_role=tokens_by_role,
        role=role,
        method="POST",
        url=endpoint,
        data={"org_id": org_id, "project_id": project_id, "file_name": image_name, "product": "KalMedia"},
        files={"file": (image_name, b"\x89PNG\r\n\x1a\n", "image/png")},
    )
    assert_status(response, HTTPStatus.OK, f"upload image as {role}")
    image_id = response.json().get("file_id")
    if not image_id:
        pytest.skip("file_id missing in upload image response")
    return image_id


@pytest.mark.api
@pytest.mark.integration
@allure.feature("CRUD Media")
class TestSenseCrudMediaAdmin:
    @pytest_asyncio.fixture
    async def uploaded_image_id(self, api_client, tokens_by_role: dict[str, str], created_media_project: str) -> str:
        return await _upload_image(
            api_client=api_client,
            tokens_by_role=tokens_by_role,
            role="admin",
            project_id=created_media_project,
            image_name=f"admin-{uuid.uuid4().hex[:8]}.png",
        )

    async def test_upload_image_as_admin(self, uploaded_image_id: str) -> None:
        assert uploaded_image_id

    async def test_get_image(self, api_client, tokens_by_role: dict[str, str], created_media_project: str, uploaded_image_id: str) -> None:
        endpoint = get_env_or_skip("KAL_GET_FILE_ENDPOINT")
        response = await request_as_role(
            api_client=api_client,
            tokens_by_role=tokens_by_role,
            role="admin",
            method="POST",
            url=endpoint,
            json_body={
                "org_id": get_env_or_skip("KAL_ORG_ID"),
                "project_id": created_media_project,
                "file_id": uploaded_image_id,
            },
        )
        assert_status(response, HTTPStatus.OK, "get image as admin")

    async def test_get_all_images_as_admin(self, api_client, tokens_by_role: dict[str, str], created_media_project: str) -> None:
        endpoint = get_env_or_skip("KAL_GET_ALL_FILES_ENDPOINT")
        response = await request_as_role(
            api_client=api_client,
            tokens_by_role=tokens_by_role,
            role="admin",
            method="POST",
            url=endpoint,
            json_body={"org_id": get_env_or_skip("KAL_ORG_ID"), "project_ids": [created_media_project]},
        )
        assert_status(response, HTTPStatus.OK, "get all images as admin")

    async def test_delete_image_as_admin(
        self,
        api_client,
        tokens_by_role: dict[str, str],
        created_media_project: str,
        uploaded_image_id: str,
    ) -> None:
        endpoint = get_env_or_skip("KAL_DELETE_FILE_ENDPOINT")
        response = await request_as_role(
            api_client=api_client,
            tokens_by_role=tokens_by_role,
            role="admin",
            method="POST",
            url=endpoint,
            json_body={
                "org_id": get_env_or_skip("KAL_ORG_ID"),
                "project_id": created_media_project,
                "file_id": uploaded_image_id,
            },
        )
        assert_status(response, HTTPStatus.OK, "delete image as admin")


@pytest.mark.api
@pytest.mark.integration
@allure.feature("CRUD Media")
class TestSenseCrudImagesRegular:
    @pytest_asyncio.fixture
    async def uploaded_image_id(self, api_client, tokens_by_role: dict[str, str], created_media_project: str) -> str:
        return await _upload_image(
            api_client=api_client,
            tokens_by_role=tokens_by_role,
            role="regular",
            project_id=created_media_project,
            image_name=f"regular-{uuid.uuid4().hex[:8]}.png",
        )

    async def test_upload_image_as_regular(self, uploaded_image_id: str) -> None:
        assert uploaded_image_id

    async def test_get_image(self, api_client, tokens_by_role: dict[str, str], created_media_project: str, uploaded_image_id: str) -> None:
        endpoint = get_env_or_skip("KAL_GET_FILE_ENDPOINT")
        response = await request_as_role(
            api_client=api_client,
            tokens_by_role=tokens_by_role,
            role="regular",
            method="POST",
            url=endpoint,
            json_body={
                "org_id": get_env_or_skip("KAL_ORG_ID"),
                "project_id": created_media_project,
                "file_id": uploaded_image_id,
            },
        )
        assert_status(response, HTTPStatus.OK, "get image as regular")

    async def test_get_all_images_as_regular(self, api_client, tokens_by_role: dict[str, str], created_media_project: str) -> None:
        endpoint = get_env_or_skip("KAL_GET_ALL_FILES_ENDPOINT")
        response = await request_as_role(
            api_client=api_client,
            tokens_by_role=tokens_by_role,
            role="regular",
            method="POST",
            url=endpoint,
            json_body={"org_id": get_env_or_skip("KAL_ORG_ID"), "project_ids": [created_media_project]},
        )
        assert_status(response, HTTPStatus.OK, "get all images as regular")

    async def test_delete_image_as_regular(
        self,
        api_client,
        tokens_by_role: dict[str, str],
        created_media_project: str,
        uploaded_image_id: str,
    ) -> None:
        endpoint = get_env_or_skip("KAL_DELETE_FILE_ENDPOINT")
        response = await request_as_role(
            api_client=api_client,
            tokens_by_role=tokens_by_role,
            role="regular",
            method="POST",
            url=endpoint,
            json_body={
                "org_id": get_env_or_skip("KAL_ORG_ID"),
                "project_id": created_media_project,
                "file_id": uploaded_image_id,
            },
        )
        assert_status(response, HTTPStatus.OK, "delete image as regular")
