# Как добавлять новый endpoint

Алгоритм на примере нового endpoint `GET /users/{id}`.

---

## 1. `tools/routes/<domain>.py` — добавь маршрут

```python
from enum import Enum


class UsersRoutes(str, Enum):
    USERS_RETRIEVE = "/users/{id}"

    def __str__(self) -> str:
        return self.value
```

---

## 2. `schema/users.py` — создай схемы

```python
from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel, ConfigDict


class UserRetrieveSchema(BaseModel):
    """Параметры запроса GET /users/{id}."""

    id: int
    requestId: UUID


class UsersResponseSchema(BaseModel):
    """Ответ от users endpoint."""

    class UserDataSchema(BaseModel):
        id: int
        name: str

    data: UserDataSchema
    requestId: UUID

    model_config = ConfigDict(extra="ignore")  # API может вернуть лишние поля
```

---

## 3. `clients/operations_client.py` — добавь метод в `APIClient`

```python
from schema.users import UserRetrieveSchema
from tools.routes import UsersRoutes

@allure.step("Users: retrieve user by id")
async def users_retrieve(self, payload: UserRetrieveSchema, token: str) -> Response:
    return await self.get(
        UsersRoutes.USERS_RETRIEVE.format(id=payload.id),
        headers={
            "Authorization": f"Bearer {token}",
            "Request-ID": str(payload.requestId),
        },
    )
```

---

## 4. `pytest.ini` — зарегистрируй маркер

```ini
users: Тесты для users endpoint.
```

---

## 5. `config/settings.py` — добавь поле в `APISettings` (если нужен ID из `.env`)

Если тест требует ID или другой конфиг из `.env` (например, `USER_ID`), добавь поле в `Settings`:

```python
# config/settings.py
user_id: Optional[int] = None
```

И в `.env`:

```env
PROFILE=api
ENVIRONMENT=local
USER_ID=12345
```

> Не хардкодь ID прямо в тесте — выноси в `.env` через `Settings`.

---

## 6. `tests/test_users.py` — напиши тест

```python
from http import HTTPStatus
from uuid import uuid4

import allure
import pytest

from clients.operations_client import APIClient
from config import APISettings as Settings
from schema.users import UserRetrieveSchema, UsersResponseSchema


@pytest.mark.users
@pytest.mark.integration
class TestUsers:
    @allure.title("Users: retrieve user by id")
    async def test_users_retrieve(
        self,
        api_client: APIClient,
        auth_token: str,
        settings: Settings,
    ) -> None:
        payload = UserRetrieveSchema(
            id=settings.user_id,
            requestId=uuid4(),
        )
        response = await api_client.users_retrieve(payload, token=auth_token)

        assert response.status_code == HTTPStatus.OK

        user = UsersResponseSchema.model_validate_json(response.text)
        assert isinstance(user.data.id, int)
        assert isinstance(user.data.name, str)
```

---

## Чеклист

- [ ] `tools/routes.py` — маршрут добавлен
- [ ] `schema/<domain>.py` — схемы запроса и ответа созданы
- [ ] `clients/operations_client.py` — метод добавлен с `token: str` и `Authorization` заголовком
- [ ] `pytest.ini` — маркер зарегистрирован
- [ ] `config/settings.py` + `.env` — ID вынесен в конфиг (не хардкод в тесте)
- [ ] `tests/test_<domain>.py` — тест с `@pytest.mark.integration`, `settings`, `auth_token`
