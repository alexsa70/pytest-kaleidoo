from __future__ import annotations

import uuid
from http import HTTPStatus
from typing import Optional

import allure
import pytest

from config import APISettings
from tests.kal_api_migration_helpers import assert_status, request_as_role
from tools.routes import UserRoutes


def _require_user_create_data(settings: APISettings) -> tuple[str, str, str]:
    if not settings.org_name:
        pytest.skip("ORG_NAME is not configured")
    role_id = settings.user_role_id or settings.org_role_id
    if not role_id:
        pytest.skip("USER_ROLE_ID/ORG_ROLE_ID is not configured")
    base_url = settings.user_base_url or str(settings.api_http_client.url)
    return settings.org_name, role_id, base_url


async def _create_user(
    *,
    api_client,
    tokens_by_role: dict[str, str],
    role: str,
    settings: APISettings,
) -> str:
    org_name, role_id, base_url = _require_user_create_data(settings)
    suffix = uuid.uuid4().hex[:8]
    payload = {
        "org_name": org_name,
        "user_name": f"qa-user-{suffix}",
        "first_name": "QA",
        "last_name": f"Auto{suffix}",
        "role_id": role_id,
        "email": f"qa-{suffix}@example.com",
        "is_ldap_sso_user": "false",
        "base_url": base_url,
    }

    response = await request_as_role(
        api_client=api_client,
        tokens_by_role=tokens_by_role,
        role=role,
        method="POST",
        url=str(UserRoutes.USER_CREATE),
        data=payload,
    )
    assert_status(response, HTTPStatus.OK, f"create user as {role}")
    user_id = response.json().get("user_id")
    if not user_id:
        pytest.skip("user_id missing in create user response")
    return user_id


async def _delete_user(
    *,
    api_client,
    tokens_by_role: dict[str, str],
    role: str,
    user_id: Optional[str],
) -> None:
    if not user_id:
        return
    await request_as_role(
        api_client=api_client,
        tokens_by_role=tokens_by_role,
        role=role,
        method="POST",
        url=str(UserRoutes.USER_DELETE),
        json_body={"user_id": user_id},
    )


@pytest.mark.api
@pytest.mark.integration
@allure.feature("CRUD Users")
class TestCRUDUsers:
    async def test_admin_create_user(self, api_client, tokens_by_role: dict[str, str], settings: APISettings) -> None:
        user_id = await _create_user(
            api_client=api_client,
            tokens_by_role=tokens_by_role,
            role="admin",
            settings=settings,
        )
        await _delete_user(api_client=api_client, tokens_by_role=tokens_by_role, role="admin", user_id=user_id)
        assert user_id

    async def test_admin_get_user_by_id(self, api_client, tokens_by_role: dict[str, str], settings: APISettings) -> None:
        user_id = await _create_user(
            api_client=api_client,
            tokens_by_role=tokens_by_role,
            role="admin",
            settings=settings,
        )
        try:
            response = await request_as_role(
                api_client=api_client,
                tokens_by_role=tokens_by_role,
                role="admin",
                method="POST",
                url=str(UserRoutes.USER_GET_BY_ID),
                json_body={"user_id": user_id},
            )
            assert_status(response, HTTPStatus.OK, "admin get user by id")
        finally:
            await _delete_user(api_client=api_client, tokens_by_role=tokens_by_role, role="admin", user_id=user_id)

    async def test_admin_update_user(self, api_client, tokens_by_role: dict[str, str], settings: APISettings) -> None:
        user_id = await _create_user(
            api_client=api_client,
            tokens_by_role=tokens_by_role,
            role="admin",
            settings=settings,
        )
        try:
            response = await request_as_role(
                api_client=api_client,
                tokens_by_role=tokens_by_role,
                role="admin",
                method="POST",
                url=str(UserRoutes.USER_UPDATE),
                data={"user_id": user_id, "last_name": "UpdatedByAdmin"},
            )
            assert_status(response, HTTPStatus.OK, "admin update user")
        finally:
            await _delete_user(api_client=api_client, tokens_by_role=tokens_by_role, role="admin", user_id=user_id)

    async def test_admin_delete_user(self, api_client, tokens_by_role: dict[str, str], settings: APISettings) -> None:
        user_id = await _create_user(
            api_client=api_client,
            tokens_by_role=tokens_by_role,
            role="admin",
            settings=settings,
        )
        response = await request_as_role(
            api_client=api_client,
            tokens_by_role=tokens_by_role,
            role="admin",
            method="POST",
            url=str(UserRoutes.USER_DELETE),
            json_body={"user_id": user_id},
        )
        assert_status(response, HTTPStatus.OK, "admin delete user")

    async def test_regular_create_user(self, api_client, tokens_by_role: dict[str, str], settings: APISettings) -> None:
        user_id = await _create_user(
            api_client=api_client,
            tokens_by_role=tokens_by_role,
            role="regular",
            settings=settings,
        )
        await _delete_user(api_client=api_client, tokens_by_role=tokens_by_role, role="regular", user_id=user_id)
        assert user_id

    async def test_regular_get_user_by_id(self, api_client, tokens_by_role: dict[str, str], settings: APISettings) -> None:
        user_id = await _create_user(
            api_client=api_client,
            tokens_by_role=tokens_by_role,
            role="regular",
            settings=settings,
        )
        try:
            response = await request_as_role(
                api_client=api_client,
                tokens_by_role=tokens_by_role,
                role="regular",
                method="POST",
                url=str(UserRoutes.USER_GET_BY_ID),
                json_body={"user_id": user_id},
            )
            assert_status(response, HTTPStatus.OK, "regular get user by id")
        finally:
            await _delete_user(api_client=api_client, tokens_by_role=tokens_by_role, role="regular", user_id=user_id)

    async def test_regular_update_user(self, api_client, tokens_by_role: dict[str, str], settings: APISettings) -> None:
        user_id = await _create_user(
            api_client=api_client,
            tokens_by_role=tokens_by_role,
            role="regular",
            settings=settings,
        )
        try:
            response = await request_as_role(
                api_client=api_client,
                tokens_by_role=tokens_by_role,
                role="regular",
                method="POST",
                url=str(UserRoutes.USER_UPDATE),
                data={"user_id": user_id, "last_name": "UpdatedByRegular"},
            )
            assert_status(response, HTTPStatus.OK, "regular update user")
        finally:
            await _delete_user(api_client=api_client, tokens_by_role=tokens_by_role, role="regular", user_id=user_id)

    async def test_regular_delete_user(self, api_client, tokens_by_role: dict[str, str], settings: APISettings) -> None:
        user_id = await _create_user(
            api_client=api_client,
            tokens_by_role=tokens_by_role,
            role="regular",
            settings=settings,
        )
        response = await request_as_role(
            api_client=api_client,
            tokens_by_role=tokens_by_role,
            role="regular",
            method="POST",
            url=str(UserRoutes.USER_DELETE),
            json_body={"user_id": user_id},
        )
        assert_status(response, HTTPStatus.OK, "regular delete user")
