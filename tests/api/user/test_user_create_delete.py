from __future__ import annotations

from http import HTTPStatus
from typing import Any

import allure
import pytest
import pytest_asyncio

from clients.base_client import get_http_client
from clients.user_client import UserClient
from config import APISettings
from schema.users import (
    UserCreateRequestSchema,
    UserCreateResponseSchema,
    UserResponseSchema,
    UserDeleteRequestSchema,
    UserRetrieveByIdSchema,
)
from tools.fakers import fake_email, fake_first_name, fake_last_name, fake_username


@pytest.mark.user
@pytest.mark.api
@pytest.mark.integration
@allure.feature("User Service")
class TestUserCreateDelete:
    @staticmethod
    async def _retry_create_with_valid_role(
        user_client: UserClient,
        payload: UserCreateRequestSchema,
        failed_response_message: str,
    ):
        if "role id not exist" not in failed_response_message.lower():
            return None

        roles_response = await user_client.user_get_roles()
        if roles_response.status_code != HTTPStatus.OK:
            pytest.skip(
                "Unable to auto-resolve valid role_id: /api/user/get_roles "
                f"returned {roles_response.status_code}"
            )

        roles_data = roles_response.json()
        roles = roles_data if isinstance(roles_data, list) else roles_data.get("roles", [])
        fallback_role_id = next((role.get("id") for role in roles if isinstance(role, dict) and role.get("id")), None)
        if not fallback_role_id:
            pytest.skip("Unable to auto-resolve valid role_id: no roles with id in /api/user/get_roles response")

        retry_payload = payload.model_copy(update={"role_id": fallback_role_id})
        return await user_client.user_create(retry_payload)

    @pytest_asyncio.fixture(scope="class", loop_scope="class")
    async def created_user_data(
        self,
        settings: APISettings,
        auth_token: str,
    ) -> dict[str, Any]:
        if not settings.org_name:
            pytest.skip("ORG_NAME is not configured in .env")

        role_id = settings.user_role_id or settings.org_role_id
        if not role_id:
            pytest.skip("USER_ROLE_ID/ORG_ROLE_ID is not configured in .env")

        payload = UserCreateRequestSchema(
            org_name=settings.org_name,
            user_name=f"qa-{fake_username()}",
            first_name=fake_first_name(),
            last_name=fake_last_name(),
            role_id=role_id,
            email=fake_email(),
            is_ldap_sso_user=False,
            base_url=settings.user_base_url,
        )
        async with get_http_client(settings.api_http_client, token=auth_token) as http_client:
            user_client = UserClient(client=http_client)
            create_response = await user_client.user_create(payload)
            if create_response.status_code == HTTPStatus.BAD_REQUEST:
                failed_message = str(create_response.json().get("message", ""))
                retried_response = await self._retry_create_with_valid_role(
                    user_client=user_client,
                    payload=payload,
                    failed_response_message=failed_message,
                )
                if retried_response is not None:
                    create_response = retried_response
        if create_response.status_code in {HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN}:
            pytest.skip(
                f"Active role '{settings.active_role}' has no permission to create users "
                f"({create_response.status_code})"
            )
        assert create_response.status_code == HTTPStatus.OK, (
            f"User create failed with status {create_response.status_code}: {create_response.text}"
        )

        create_body = UserCreateResponseSchema.model_validate_json(create_response.text)
        print(f"Created user_id: {create_body.user_id}")
        allure.attach(
            create_response.text,
            name="Create User Response",
            attachment_type=allure.attachment_type.JSON,
        )
        return {
            "create_status_code": create_response.status_code,
            "create_json": create_response.json(),
            "create_body": create_body,
        }

    @allure.title("User: create user")
    async def test_user_create(
        self,
        created_user_data: dict[str, Any],
    ) -> None:
        assert created_user_data["create_status_code"] == HTTPStatus.OK
        assert created_user_data["create_body"].user_id
        assert created_user_data["create_json"]

    @allure.title("User: delete created user")
    async def test_user_delete_created_user(
        self,
        settings: APISettings,
        auth_token: str,
        created_user_data: dict[str, Any],
    ) -> None:
        create_body: UserCreateResponseSchema = created_user_data["create_body"]
        async with get_http_client(settings.api_http_client, token=auth_token) as http_client:
            user_client = UserClient(client=http_client)
            delete_response = await user_client.user_delete(
                UserDeleteRequestSchema(user_id=create_body.user_id)
            )
        assert delete_response.status_code == HTTPStatus.OK
        print(f"Deleted user_id: {create_body.user_id}")
        allure.attach(
            delete_response.text,
            name="Delete User Response",
            attachment_type=allure.attachment_type.JSON,
        )

    @allure.title("User: verify user state after delete")
    async def test_user_state_after_delete(
        self,
        settings: APISettings,
        auth_token: str,
        created_user_data: dict[str, Any],
    ) -> None:
        create_body: UserCreateResponseSchema = created_user_data["create_body"]
        async with get_http_client(settings.api_http_client, token=auth_token) as http_client:
            user_client = UserClient(client=http_client)
            get_response = await user_client.user_get_by_id(
                UserRetrieveByIdSchema(user_id=create_body.user_id)
            )

        if get_response.status_code in {HTTPStatus.BAD_REQUEST, HTTPStatus.NOT_FOUND}:
            return

        assert get_response.status_code == HTTPStatus.OK, (
            "Unexpected status from get_by_id after delete: "
            f"{get_response.status_code}, body: {get_response.text}"
        )
        body = UserResponseSchema.model_validate_json(get_response.text)
        assert body.status in {"On Hold", "Deleted", "Disabled"}, (
            "User is still active after delete. "
            f"Expected soft-delete status, got '{body.status}'. Response: {get_response.text}"
        )
        allure.attach(
            get_response.text,
            name="Get User After Delete Response",
            attachment_type=allure.attachment_type.JSON,
        )
