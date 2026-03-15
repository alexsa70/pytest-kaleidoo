from __future__ import annotations

from typing import Any

import pytest

from config import APISettings
from tests.api.rbac.policy import ACCESS_POLICY


def _resolve_placeholders(value: Any, settings: APISettings) -> Any:
    if isinstance(value, dict):
        return {k: _resolve_placeholders(v, settings) for k, v in value.items()}
    if isinstance(value, list):
        return [_resolve_placeholders(v, settings) for v in value]
    placeholder_map = {
        "$USER_NAME": settings.user_name,
        "$USER_ID": settings.user_id,
        "$ORG_NAME": settings.org_name,
        "$USER_ROLE_ID": settings.user_role_id or settings.org_role_id,
        "$USER_BASE_URL": settings.user_base_url,
    }
    if isinstance(value, str) and value in placeholder_map:
        resolved = placeholder_map[value]
        if not resolved:
            pytest.skip(f"{value[1:]} is not configured in .env")
        return resolved
    return value


@pytest.mark.api
@pytest.mark.rbac
@pytest.mark.integration
class TestRBACAccessMatrix:
    @pytest.mark.parametrize("rule", ACCESS_POLICY, ids=lambda rule: rule.name)
    async def test_access_by_role(
        self,
        api_client,
        tokens_by_role: dict[str, str],
        settings: APISettings,
        rule,
    ) -> None:
        json_body = _resolve_placeholders(rule.json_body, settings)
        data_body = _resolve_placeholders(rule.data, settings)
        params = _resolve_placeholders(rule.params, settings)

        for role in rule.allowed_roles:
            if role not in tokens_by_role:
                pytest.skip(f"No token configured for role: {role}")

            response = await api_client.client.request(
                method=rule.method,
                url=rule.path,
                json=json_body,
                data=data_body,
                params=params,
                headers={"Authorization": f"Bearer {tokens_by_role[role]}"},
            )
            assert response.status_code == rule.expected_allowed_status, (
                f"{rule.name}: role '{role}' expected {rule.expected_allowed_status}, "
                f"got {response.status_code}"
            )

        for role in rule.denied_roles:
            if role not in tokens_by_role:
                pytest.skip(f"No token configured for role: {role}")

            response = await api_client.client.request(
                method=rule.method,
                url=rule.path,
                json=json_body,
                data=data_body,
                params=params,
                headers={"Authorization": f"Bearer {tokens_by_role[role]}"},
            )
            assert response.status_code == rule.expected_denied_status, (
                f"{rule.name}: role '{role}' expected denied status {rule.expected_denied_status}, "
                f"got {response.status_code}"
            )
            assert (
                "access" in response.text.lower() or "forbidden" in response.text.lower()
            ), f"{rule.name}: denied response should contain access error details"
