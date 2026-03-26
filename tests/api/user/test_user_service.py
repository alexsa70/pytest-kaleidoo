from __future__ import annotations

from http import HTTPStatus

import allure
import pytest
from pydantic import TypeAdapter

from clients.user_client import UserClient
from config import APISettings
from schema.users import (
    RoleSchema,
    UserCreateRequestSchema,
    UserCreateResponseSchema,
    UserDeleteRequestSchema,
    UserErrorSchema,
    UserResetMFARequestSchema,
    UserResponseSchema,
    UserRetrieveSchema,
    UserRetrieveByIdSchema,
    UserSummarySchema,
    UserUnlockRequestSchema,
    UserUpdateRequestSchema,
    UserUpdateResponseSchema,
)
from tools.fakers import fake_email, fake_first_name, fake_last_name, fake_username

@pytest.fixture
def current_user_id(logged_in_user) -> str:
    if not logged_in_user.id:
        pytest.skip("User_ID unavailable in API response")
    return logged_in_user.id    


@pytest.mark.user
@pytest.mark.api
@pytest.mark.integration
@allure.feature("User Service")
class TestUserService:
    @allure.title("Users: retrieve user by name")
    async def test_user_retrieve(
        self,
        user_client: UserClient,
        logged_in_user,
        #settings: APISettings,
    ) -> None:
        if not logged_in_user.user_name:
            pytest.skip("USER_NAME is not in response")

        payload = UserRetrieveSchema(user_name=logged_in_user.user_name)
        response = await user_client.user_retrieve(payload)

        assert response.status_code == HTTPStatus.OK
        user = UserResponseSchema.model_validate_json(response.text)
        assert user.user_name == logged_in_user.user_name

    @allure.title("User: get by id")
    async def test_user_get_by_id(
        self,
        user_client: UserClient,
        #settings: APISettings,
        logged_in_user,
    ) -> None:
        if not logged_in_user.id:
            pytest.skip("USER_ID is not configured in .env")

        payload = UserRetrieveByIdSchema(user_id=logged_in_user.id)
        response = await user_client.user_get_by_id(payload)

        assert response.status_code == HTTPStatus.OK
        body = UserResponseSchema.model_validate_json(response.text)
        assert body.id == logged_in_user.id

    @allure.title("User: get all users")
    async def test_user_get_all(self, user_client: UserClient) -> None:
        response = await user_client.user_get_all()

        assert response.status_code == HTTPStatus.OK
        users = TypeAdapter(list[UserSummarySchema]).validate_json(response.text)
        assert len(users) >= 0

    @allure.title("User: get roles")
    async def test_user_get_roles(self, user_client: UserClient) -> None:
        response = await user_client.user_get_roles()

        assert response.status_code == HTTPStatus.OK
        roles = TypeAdapter(list[RoleSchema]).validate_json(response.text)
        assert len(roles) > 0

    @allure.title("User: unlock non-existing user -> 400/404")
    async def test_user_unlock_non_existing(self, user_client: UserClient) -> None:
        payload = UserUnlockRequestSchema(username="nonexistent_user_qa_12345")
        response = await user_client.user_unlock(payload)

        assert response.status_code in {HTTPStatus.BAD_REQUEST, HTTPStatus.NOT_FOUND}
        body = UserErrorSchema.model_validate_json(response.text)
        assert body.message

    @allure.title("User: reset MFA non-existing user -> 400/404")
    async def test_user_reset_mfa_non_existing(self, user_client: UserClient) -> None:
        payload = UserResetMFARequestSchema(user_id="000000000000000000000000")
        response = await user_client.user_reset_mfa(payload)

        assert response.status_code in {HTTPStatus.BAD_REQUEST, HTTPStatus.NOT_FOUND}
        body = UserErrorSchema.model_validate_json(response.text)
        assert body.message

    # @allure.title("User: create and delete user")
    # async def test_user_create_and_delete(
    #     self,
    #     user_client: UserClient,
    #     settings: APISettings,
    # ) -> None:
    #     if not settings.org_name:
    #         pytest.skip("ORG_NAME is not configured in .env")

    #     role_id = settings.user_role_id or settings.org_role_id
    #     if not role_id:
    #         pytest.skip("USER_ROLE_ID/ORG_ROLE_ID is not configured in .env")

    #     payload = UserCreateRequestSchema(
    #         org_name=settings.org_name,
    #         user_name=f"qa-{fake_username()}",
    #         first_name=fake_first_name(),
    #         last_name=fake_last_name(),
    #         role_id=role_id,
    #         email=fake_email(),
    #         is_ldap_sso_user=False,
    #         base_url=settings.user_base_url,
    #     )
    #     create_response = await user_client.user_create(payload)
    #     if create_response.status_code in {HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN}:
    #         pytest.skip(
    #             f"Active role '{settings.active_role}' has no permission to create users "
    #             f"({create_response.status_code})"
    #         )
    #     assert create_response.status_code == HTTPStatus.OK

    #     create_body = UserCreateResponseSchema.model_validate_json(create_response.text)
    #     delete_response = await user_client.user_delete(
    #         UserDeleteRequestSchema(user_id=create_body.user_id)
    #     )
    #     assert delete_response.status_code == HTTPStatus.OK

    @allure.title("User: update user")
    async def test_user_update(
        self,
        user_client: UserClient,
        current_user_id: str,
    ) -> None:
        before_response = await user_client.user_get_by_id(
            UserRetrieveByIdSchema(user_id=current_user_id)
        )
        assert before_response.status_code == HTTPStatus.OK
        before_user = UserResponseSchema.model_validate_json(before_response.text)
        original_last_name = before_user.last_name

        new_last_name = f"QA{fake_first_name()}"
        payload = UserUpdateRequestSchema(
            user_id=current_user_id,
            last_name=new_last_name,
        )

        response = await user_client.user_update(payload)
        assert response.status_code == HTTPStatus.OK

        try:
            body = UserUpdateResponseSchema.model_validate_json(response.text)
            assert body.message

            get_by_id_response = await user_client.user_get_by_id(
                UserRetrieveByIdSchema(user_id=current_user_id)
            )
            assert get_by_id_response.status_code == HTTPStatus.OK

            updated_user = UserResponseSchema.model_validate_json(get_by_id_response.text)
            assert updated_user.last_name == new_last_name
        finally:
            rollback_response = await user_client.user_update(
                UserUpdateRequestSchema(
                    user_id=current_user_id,
                    last_name=original_last_name,
                )
            )
            assert rollback_response.status_code == HTTPStatus.OK

    @allure.title("User: delete non-existing user -> 400/404")
    async def test_user_delete_non_existing(self, user_client: UserClient) -> None:
        payload = UserDeleteRequestSchema(user_id="000000000000000000000000")

        response = await user_client.user_delete(payload)
        assert response.status_code in {HTTPStatus.BAD_REQUEST, HTTPStatus.NOT_FOUND}

    
