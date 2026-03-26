from __future__ import annotations

import os
from typing import Any, Optional

import pytest
from httpx import Response

ROLE_ALIASES = {
    "regular": "user",
}


def get_env_or_skip(name: str) -> str:
    value = os.getenv(name)
    if not value:
        pytest.skip(f"{name} is not configured")
    return value


def get_optional_env(name: str) -> Optional[str]:
    return os.getenv(name)


def get_role_token(tokens_by_role: dict[str, str], role: str) -> str:
    resolved_role = ROLE_ALIASES.get(role, role)
    token = tokens_by_role.get(resolved_role)
    if not token:
        pytest.skip(f"No token configured for role: {resolved_role}")
    return token


def build_url(url_template: str, **params: Any) -> str:
    try:
        return url_template.format(**params)
    except KeyError:
        return url_template


async def request_as_role(
    *,
    api_client,
    tokens_by_role: dict[str, str],
    role: str,
    method: str,
    url: str,
    json_body: Any = None,
    data: Any = None,
    params: Any = None,
    files: Any = None,
) -> Response:
    token = get_role_token(tokens_by_role, role)
    return await api_client.client.request(
        method=method.upper(),
        url=url,
        json=json_body,
        data=data,
        params=params,
        files=files,
        headers={"Authorization": f"Bearer {token}"},
    )


def assert_status(response: Response, expected: int, message: str) -> None:
    assert response.status_code == expected, (
        f"{message}: expected {expected}, got {response.status_code}. "
        f"Response body: {response.text[:300]}"
    )
