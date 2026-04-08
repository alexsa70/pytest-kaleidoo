from __future__ import annotations

from http import HTTPStatus

import allure
import pytest
from pydantic import TypeAdapter

from clients.user_client import UserClient
from schema.users import (
    RoleSchema,
    UserResponseSchema,
    UserRetrieveSchema,
    UserRetrieveByIdSchema,
    UserSummarySchema,
    UserUpdateRequestSchema,
    UserUpdateResponseSchema,
)
from tools.fakers import fake_first_name

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

    
