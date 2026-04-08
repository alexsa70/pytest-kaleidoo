from __future__ import annotations

from http import HTTPStatus

import allure
import pytest

from clients.user_client import UserClient
from schema.users import (
    UserDeleteRequestSchema,
    UserErrorSchema,
    UserResetMFARequestSchema,
    UserUnlockRequestSchema,
)


@pytest.mark.user
@pytest.mark.api
@pytest.mark.integration
@allure.feature("User Service")
class TestUserNegative:
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

    @allure.title("User: delete non-existing user -> 400/404")
    async def test_user_delete_non_existing(self, user_client: UserClient) -> None:
        payload = UserDeleteRequestSchema(user_id="000000000000000000000000")
        response = await user_client.user_delete(payload)

        assert response.status_code in {HTTPStatus.BAD_REQUEST, HTTPStatus.NOT_FOUND}
