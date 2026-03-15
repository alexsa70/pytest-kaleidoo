from __future__ import annotations

from http import HTTPStatus

import allure
import pytest

from clients.operations_client import APIClient
from config import APISettings
from schema.users import (
    UserCreateRequestSchema,
    UserCreateResponseSchema,
    UserDeleteRequestSchema,
    UserErrorSchema,
    UserGetAllResponseSchema,
    UserGetRolesResponseSchema,
    UserResetMFARequestSchema,
    UserResponseSchema,
    UserRetrieveSchema,
    UserRetrieveByIdSchema,
    UserUnlockRequestSchema,
    UserUpdateRequestSchema,
    UserUpdateResponseSchema,
)
from tools.fakers import fake_email, fake_first_name, fake_last_name, fake_username


def _token_for_roles(tokens_by_role: dict[str, str], roles: tuple[str, ...]) -> str:
    for role in roles:
        if role in tokens_by_role:
            return tokens_by_role[role]
    pytest.skip(f"None of required roles is configured: {', '.join(roles)}")


@pytest.mark.user
@pytest.mark.api
@pytest.mark.integration
@allure.feature("User Service")
class TestUserService:
    @allure.title("Users: retrieve user by name")
    async def test_user_retrieve(
        self,
        api_client: APIClient,
        tokens_by_role: dict[str, str],
        settings: APISettings,
    ) -> None:
        if not settings.user_name:
            pytest.skip("USER_NAME is not configured in .env")

        token = _token_for_roles(tokens_by_role, ("admin", "user"))
        payload = UserRetrieveSchema(user_name=settings.user_name)
        response = await api_client.user_retrieve(payload, token=token)

        assert response.status_code == HTTPStatus.OK
        user = UserResponseSchema.model_validate_json(response.text)
        assert user.user_name == settings.user_name

    @allure.title("User: get by id")
    async def test_user_get_by_id(
        self,
        api_client: APIClient,
        tokens_by_role: dict[str, str],
        settings: APISettings,
    ) -> None:
        if not settings.user_id:
            pytest.skip("USER_ID is not configured in .env")

        token = _token_for_roles(tokens_by_role, ("admin", "user"))
        payload = UserRetrieveByIdSchema(user_id=settings.user_id)
        response = await api_client.user_get_by_id(payload, token=token)

        assert response.status_code == HTTPStatus.OK
        body = UserResponseSchema.model_validate_json(response.text)
        assert body.id == settings.user_id

    @allure.title("User: get all users")
    async def test_user_get_all(
        self,
        api_client: APIClient,
        tokens_by_role: dict[str, str],
    ) -> None:
        token = _token_for_roles(tokens_by_role, ("admin", "super_admin"))
        response = await api_client.user_get_all(token=token)

        assert response.status_code == HTTPStatus.OK
        body = UserGetAllResponseSchema.model_validate_json(response.text)
        assert body.total_count >= 0

    @allure.title("User: get roles")
    async def test_user_get_roles(
        self,
        api_client: APIClient,
        tokens_by_role: dict[str, str],
    ) -> None:
        token = _token_for_roles(tokens_by_role, ("admin", "user"))
        response = await api_client.user_get_roles(token=token)

        assert response.status_code == HTTPStatus.OK
        body = UserGetRolesResponseSchema.model_validate_json(response.text)
        assert len(body.roles) > 0

    @allure.title("User: unlock non-existing user -> 404")
    async def test_user_unlock_non_existing(
        self,
        api_client: APIClient,
        tokens_by_role: dict[str, str],
    ) -> None:
        token = _token_for_roles(tokens_by_role, ("admin", "super_admin"))
        payload = UserUnlockRequestSchema(username="nonexistent_user_qa_12345")
        response = await api_client.user_unlock(payload, token=token)

        assert response.status_code == HTTPStatus.NOT_FOUND
        body = UserErrorSchema.model_validate_json(response.text)
        assert body.message

    @allure.title("User: reset MFA non-existing user -> 404")
    async def test_user_reset_mfa_non_existing(
        self,
        api_client: APIClient,
        tokens_by_role: dict[str, str],
    ) -> None:
        token = _token_for_roles(tokens_by_role, ("admin", "super_admin"))
        payload = UserResetMFARequestSchema(user_id="000000000000000000000000")
        response = await api_client.user_reset_mfa(payload, token=token)

        assert response.status_code == HTTPStatus.NOT_FOUND
        body = UserErrorSchema.model_validate_json(response.text)
        assert body.message

    @allure.title("User: create and delete user")
    async def test_user_create_and_delete(
        self,
        api_client: APIClient,
        tokens_by_role: dict[str, str],
        settings: APISettings,
    ) -> None:
        if not settings.org_name:
            pytest.skip("ORG_NAME is not configured in .env")

        role_id = settings.user_role_id or settings.org_role_id
        if not role_id:
            pytest.skip("USER_ROLE_ID/ORG_ROLE_ID is not configured in .env")

        token = _token_for_roles(tokens_by_role, ("admin", "super_admin"))

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
        create_response = await api_client.user_create(payload, token=token)
        assert create_response.status_code == HTTPStatus.OK

        create_body = UserCreateResponseSchema.model_validate_json(
            create_response.text)
        delete_response = await api_client.user_delete(
            UserDeleteRequestSchema(user_id=create_body.user_id), token=token
        )
        assert delete_response.status_code == HTTPStatus.OK

    @allure.title("User: update user")
    async def test_user_update(
        self,
        api_client: APIClient,
        tokens_by_role: dict[str, str],
        settings: APISettings,
    ) -> None:
        if not settings.user_id:
            pytest.skip("USER_ID is not configured in .env")

        token = _token_for_roles(tokens_by_role, ("admin",))
        payload = UserUpdateRequestSchema(
            user_id=settings.user_id,
            first_name=f"QA{fake_first_name()}",
        )

        response = await api_client.user_update(payload, token=token)
        assert response.status_code == HTTPStatus.OK

        body = UserUpdateResponseSchema.model_validate_json(response.text)
        assert body.id == settings.user_id

    @allure.title("User: delete non-existing user -> 404")
    async def test_user_delete_non_existing(
        self,
        api_client: APIClient,
        tokens_by_role: dict[str, str],
    ) -> None:
        token = _token_for_roles(tokens_by_role, ("admin", "super_admin"))
        payload = UserDeleteRequestSchema(user_id="000000000000000000000000")

        response = await api_client.user_delete(payload, token=token)
        assert response.status_code == HTTPStatus.NOT_FOUND
