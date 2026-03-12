from __future__ import annotations

import pytest

from tests.api.rbac.policy import ACCESS_POLICY


@pytest.mark.api
@pytest.mark.rbac
@pytest.mark.integration
class TestRBACAccessMatrix:
    @pytest.mark.parametrize("rule", ACCESS_POLICY, ids=lambda rule: rule.name)
    async def test_access_by_role(self, api_client, tokens_by_role: dict[str, str], rule) -> None:
        for role in rule.allowed_roles:
            if role not in tokens_by_role:
                pytest.skip(f"No token configured for role: {role}")

            response = await api_client.client.request(
                method=rule.method,
                url=rule.path,
                json=rule.json_body,
                data=rule.data,
                params=rule.params,
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
                json=rule.json_body,
                data=rule.data,
                params=rule.params,
                headers={"Authorization": f"Bearer {tokens_by_role[role]}"},
            )
            assert response.status_code == rule.expected_denied_status, (
                f"{rule.name}: role '{role}' expected denied status {rule.expected_denied_status}, "
                f"got {response.status_code}"
            )
            assert (
                "access" in response.text.lower() or "forbidden" in response.text.lower()
            ), f"{rule.name}: denied response should contain access error details"
