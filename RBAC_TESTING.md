# RBAC Testing Guide (super_admin / admin / user)

Этот документ описывает, как проверять права доступа (`RBAC`) в текущей структуре проекта.

## Цель

Проверять для каждого endpoint:
- роль **может** выполнить запрос (ожидаемый `2xx`/`4xx` по контракту),
- роль **не может** выполнить запрос (ожидаемый `403 Access Denied` или `401`).

## Идея

Используется матрица:

`role x endpoint x expected_status`

Вместо ручного написания десятков тестов создается единый параметризованный тест, который прогоняет все правила доступа.

## 1. Конфиг в `.env`

Добавь креды для каждой роли (реальные значения подставишь позже):

```env
AUTH_CREDENTIALS_SUPER_ADMIN.EMAIL=super_admin@example.com
AUTH_CREDENTIALS_SUPER_ADMIN.PASSWORD=super_secret

AUTH_CREDENTIALS_ADMIN.EMAIL=admin@example.com
AUTH_CREDENTIALS_ADMIN.PASSWORD=admin_secret

AUTH_CREDENTIALS_USER.EMAIL=user@example.com
AUTH_CREDENTIALS_USER.PASSWORD=user_secret
```

Если твой endpoint логина поддерживает одинаковый payload для всех ролей, этого достаточно.

## 2. Где хранить RBAC тесты

Рекомендуемая структура:

```text
tests/api/rbac/
  policy/
    __init__.py
    auth.py
    org.py
    users.py
  test_access_matrix.py
fixtures/api/
  auth_roles.py
schema/
  rbac.py
```

## 3. Модель правила доступа

Создай `schema/rbac.py`:

```python
from pydantic import BaseModel


class AccessRule(BaseModel):
    name: str
    method: str
    path: str
    allowed_roles: list[str]
    denied_roles: list[str]
    expected_allowed_status: int = 200
    expected_denied_status: int = 403
```

## 4. Policy-матрица

Создай доменные policy-файлы в `tests/api/rbac/policy/` и агрегатор `__init__.py`:

```python
# tests/api/rbac/policy/users.py
from schema.rbac import AccessRule

ACCESS_POLICY_USERS = [
    AccessRule(
        name="List users",
        method="GET",
        path="/api/users",
        allowed_roles=["super_admin", "admin"],
        denied_roles=["user"],
        expected_allowed_status=200,
        expected_denied_status=403,
    ),
]

# tests/api/rbac/policy/__init__.py
from tests.api.rbac.policy.auth import ACCESS_POLICY_AUTH
from tests.api.rbac.policy.org import ACCESS_POLICY_ORG
from tests.api.rbac.policy.users import ACCESS_POLICY_USERS

ACCESS_POLICY = [
    *ACCESS_POLICY_AUTH,
    *ACCESS_POLICY_ORG,
    *ACCESS_POLICY_USERS,
]
```

## 5. Фикстура токенов по ролям

Создай `fixtures/api/auth_roles.py`:

```python
import pytest_asyncio
from clients.base_client import get_http_client
from clients.operations_client import APIClient


@pytest_asyncio.fixture(scope="session", loop_scope="session")
async def tokens_by_role(settings) -> dict[str, str]:
    # здесь логин по 3 парам credentials из .env
    # вернуть: {"super_admin": "...", "admin": "...", "user": "..."}
    ...
```

Важно:
- токены получать **1 раз на сессию**;
- не делать логин в каждом тесте, чтобы не упираться в rate-limit.

## 6. Параметризованный тест матрицы

Создай `tests/api/rbac/test_access_matrix.py`:

```python
from http import HTTPStatus
import pytest
from tests.api.rbac.policy import ACCESS_POLICY


@pytest.mark.api
@pytest.mark.integration
class TestAccessMatrix:
    @pytest.mark.parametrize("rule", ACCESS_POLICY, ids=lambda r: r.name)
    async def test_access_by_role(self, api_client, tokens_by_role, rule):
        for role in rule.allowed_roles:
            response = await api_client.client.request(
                rule.method,
                rule.path,
                headers={"Authorization": f"Bearer {tokens_by_role[role]}"},
            )
            assert response.status_code == rule.expected_allowed_status

        for role in rule.denied_roles:
            response = await api_client.client.request(
                rule.method,
                rule.path,
                headers={"Authorization": f"Bearer {tokens_by_role[role]}"},
            )
            assert response.status_code == rule.expected_denied_status
            assert "access" in response.text.lower() or "forbidden" in response.text.lower()
```

## 7. Запуск

```bash
PROFILE=api python -m pytest tests/api/rbac -m "api and integration"
```

## 8. Практические правила

- Для защищенных endpoint всегда используй Bearer token.
- Исключения: тесты endpoint получения токена и негативные проверки `no token` / `invalid token`.
- Для ownership-сценариев добавляй отдельные правила:
  - `user_own_resource` (доступ разрешен),
  - `user_foreign_resource` (доступ запрещен).
- Если для deny возвращается `401` (а не `403`), фиксируй это в `expected_denied_status`.
- Для чувствительных endpoint добавь проверку тела ошибки (стабильный код/сообщение).

## 9. Минимальный rollout

1. Сначала 5-10 самых критичных endpoint.
2. Затем покрыть все admin-only и super-admin-only методы.
3. Добавить тесты ownership.
4. Подключить в CI как отдельный job `rbac`.
