from __future__ import annotations

import uuid
from http import HTTPStatus
from typing import AsyncIterator

import allure
import pytest
import pytest_asyncio

from tests.kal_api_migration_helpers import (
    assert_status,
    build_url,
    get_env_or_skip,
    request_as_role,
)


@pytest_asyncio.fixture(scope="session")
async def created_project(api_client, tokens_by_role: dict[str, str]) -> AsyncIterator[str]:
    create_project_endpoint = get_env_or_skip("KAL_CREATE_PROJECT_ENDPOINT")
    delete_project_endpoint = get_env_or_skip("KAL_DELETE_PROJECT_ENDPOINT")

    response = await request_as_role(
        api_client=api_client,
        tokens_by_role=tokens_by_role,
        role="admin",
        method="POST",
        url=create_project_endpoint,
        json_body={"project_type_name": "KalDocs"},
    )
    assert_status(response, HTTPStatus.OK, "create project")
    body = response.json()
    project_id = body.get("project_id") or body.get("id")
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


async def _upload_file(
    *,
    api_client,
    tokens_by_role: dict[str, str],
    role: str,
    project_id: str,
    filename: str,
) -> str:
    endpoint = get_env_or_skip("KAL_CREATE_FILE_ENDPOINT")
    org_id = get_env_or_skip("KAL_ORG_ID")

    response = await request_as_role(
        api_client=api_client,
        tokens_by_role=tokens_by_role,
        role=role,
        method="POST",
        url=endpoint,
        data={"org_id": org_id, "project_id": project_id, "file_name": filename, "product": "KalDocs"},
        files={"file": (filename, b"file-content", "application/octet-stream")},
    )
    assert_status(response, HTTPStatus.OK, f"upload file as {role}")
    file_id = response.json().get("file_id")
    if not file_id:
        pytest.skip("file_id missing in upload response")
    return file_id


@pytest.mark.api
@pytest.mark.integration
@allure.feature("CRUD Files")
class TestSenseCrudFilesAdmin:
    @pytest_asyncio.fixture
    async def uploaded_file_id(self, api_client, tokens_by_role: dict[str, str], created_project: str) -> str:
        return await _upload_file(
            api_client=api_client,
            tokens_by_role=tokens_by_role,
            role="admin",
            project_id=created_project,
            filename=f"admin-{uuid.uuid4().hex[:8]}.pdf",
        )

    async def test_upload_file_as_admin(self, uploaded_file_id: str) -> None:
        assert uploaded_file_id

    async def test_get_file(self, api_client, tokens_by_role: dict[str, str], created_project: str, uploaded_file_id: str) -> None:
        endpoint = build_url(
            get_env_or_skip("KAL_GET_FILE_ENDPOINT"),
            org_id=get_env_or_skip("KAL_ORG_ID"),
            project_id=created_project,
            file_id=uploaded_file_id,
        )
        response = await request_as_role(
            api_client=api_client,
            tokens_by_role=tokens_by_role,
            role="admin",
            method="POST",
            url=endpoint,
            json_body={"org_id": get_env_or_skip("KAL_ORG_ID"), "project_id": created_project, "file_id": uploaded_file_id},
        )
        assert_status(response, HTTPStatus.OK, "get file as admin")

    async def test_get_all_files_as_admin(self, api_client, tokens_by_role: dict[str, str], created_project: str) -> None:
        endpoint = get_env_or_skip("KAL_GET_ALL_FILES_ENDPOINT")
        response = await request_as_role(
            api_client=api_client,
            tokens_by_role=tokens_by_role,
            role="admin",
            method="POST",
            url=endpoint,
            json_body={"org_id": get_env_or_skip("KAL_ORG_ID"), "project_ids": [created_project]},
        )
        assert_status(response, HTTPStatus.OK, "get all files as admin")

    async def test_get_all_files_v2_as_admin(self, api_client, tokens_by_role: dict[str, str], created_project: str) -> None:
        endpoint = get_env_or_skip("KAL_GET_ALL_FILES_V2_ENDPOINT")
        response = await request_as_role(
            api_client=api_client,
            tokens_by_role=tokens_by_role,
            role="admin",
            method="POST",
            url=endpoint,
            json_body={"org_id": get_env_or_skip("KAL_ORG_ID"), "project_ids": [created_project]},
        )
        assert_status(response, HTTPStatus.OK, "get all files v2 as admin")

    async def test_delete_file_as_admin(
        self,
        api_client,
        tokens_by_role: dict[str, str],
        created_project: str,
        uploaded_file_id: str,
    ) -> None:
        endpoint = get_env_or_skip("KAL_DELETE_FILE_ENDPOINT")
        response = await request_as_role(
            api_client=api_client,
            tokens_by_role=tokens_by_role,
            role="admin",
            method="POST",
            url=endpoint,
            json_body={"org_id": get_env_or_skip("KAL_ORG_ID"), "project_id": created_project, "file_id": uploaded_file_id},
        )
        assert_status(response, HTTPStatus.OK, "delete file as admin")


@pytest.mark.api
@pytest.mark.integration
@allure.feature("CRUD Files")
class TestSenseCrudFilesRegular:
    @pytest_asyncio.fixture
    async def uploaded_file_id(self, api_client, tokens_by_role: dict[str, str], created_project: str) -> str:
        return await _upload_file(
            api_client=api_client,
            tokens_by_role=tokens_by_role,
            role="regular",
            project_id=created_project,
            filename=f"regular-{uuid.uuid4().hex[:8]}.pdf",
        )

    async def test_upload_file_as_regular(self, uploaded_file_id: str) -> None:
        assert uploaded_file_id

    async def test_get_file(self, api_client, tokens_by_role: dict[str, str], created_project: str, uploaded_file_id: str) -> None:
        endpoint = build_url(
            get_env_or_skip("KAL_GET_FILE_ENDPOINT"),
            org_id=get_env_or_skip("KAL_ORG_ID"),
            project_id=created_project,
            file_id=uploaded_file_id,
        )
        response = await request_as_role(
            api_client=api_client,
            tokens_by_role=tokens_by_role,
            role="regular",
            method="POST",
            url=endpoint,
            json_body={"org_id": get_env_or_skip("KAL_ORG_ID"), "project_id": created_project, "file_id": uploaded_file_id},
        )
        assert_status(response, HTTPStatus.OK, "get file as regular")

    async def test_get_all_files_as_regular(self, api_client, tokens_by_role: dict[str, str], created_project: str) -> None:
        endpoint = get_env_or_skip("KAL_GET_ALL_FILES_ENDPOINT")
        response = await request_as_role(
            api_client=api_client,
            tokens_by_role=tokens_by_role,
            role="regular",
            method="POST",
            url=endpoint,
            json_body={"org_id": get_env_or_skip("KAL_ORG_ID"), "project_ids": [created_project]},
        )
        assert_status(response, HTTPStatus.OK, "get all files as regular")

    async def test_get_all_files_v2_as_regular(self, api_client, tokens_by_role: dict[str, str], created_project: str) -> None:
        endpoint = get_env_or_skip("KAL_GET_ALL_FILES_V2_ENDPOINT")
        response = await request_as_role(
            api_client=api_client,
            tokens_by_role=tokens_by_role,
            role="regular",
            method="POST",
            url=endpoint,
            json_body={"org_id": get_env_or_skip("KAL_ORG_ID"), "project_ids": [created_project]},
        )
        assert_status(response, HTTPStatus.OK, "get all files v2 as regular")

    async def test_delete_file_as_regular(
        self,
        api_client,
        tokens_by_role: dict[str, str],
        created_project: str,
        uploaded_file_id: str,
    ) -> None:
        endpoint = get_env_or_skip("KAL_DELETE_FILE_ENDPOINT")
        response = await request_as_role(
            api_client=api_client,
            tokens_by_role=tokens_by_role,
            role="regular",
            method="POST",
            url=endpoint,
            json_body={"org_id": get_env_or_skip("KAL_ORG_ID"), "project_id": created_project, "file_id": uploaded_file_id},
        )
        assert_status(response, HTTPStatus.OK, "delete file as regular")
