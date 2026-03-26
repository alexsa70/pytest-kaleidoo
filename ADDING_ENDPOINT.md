# Добавление нового endpoint и тестов

Пошаговое руководство на примере:

```
Upload Manual File
POST /api/manual_loader/upload_manual_file
Roles: user, admin
Content-Type: multipart/form-data
```

---

## Шаг 1 — Добавить route

Создать **`tools/routes/manual_loader.py`**:
```python
from enum import Enum


class ManualLoaderRoutes(str, Enum):
    """Manual Loader routes."""

    UPLOAD_MANUAL_FILE = "/api/manual_loader/upload_manual_file"

    def __str__(self) -> str:
        return self.value
```

**`tools/routes/__init__.py`** — добавить импорт:
```python
from tools.routes.auth import AuthRoutes
from tools.routes.manual_loader import ManualLoaderRoutes  # добавить
from tools.routes.org import OrgRoutes
from tools.routes.users import UserRoutes

__all__ = [
    "AuthRoutes",
    "ManualLoaderRoutes",  # добавить
    "OrgRoutes",
    "UserRoutes",
]
```

---

## Шаг 2 — Добавить схемы

Создать **`schema/manual_loader.py`**:
```python
from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class UploadManualFileResponseSchema(BaseModel):
    """Успешный ответ от POST /api/manual_loader/upload_manual_file."""

    message: str
    file_id: str

    model_config = ConfigDict(extra="ignore")


class UploadManualFileErrorSchema(BaseModel):
    message: str
    status: str | None = None

    model_config = ConfigDict(extra="ignore")
```

> Схемы запроса не нужны если тело — только файл (multipart/form-data).
> Добавь `RequestSchema` только если есть JSON-поля помимо файла.

---

## Шаг 3 — Добавить клиент

Создать **`clients/manual_loader_client.py`**:
```python
from __future__ import annotations

import io

import allure
from httpx import Response

from clients.base_client import BaseClient
from tools.routes import ManualLoaderRoutes


class ManualLoaderClient(BaseClient):
    """Manual Loader Service client."""

    @allure.step("Manual Loader: upload manual file")
    async def upload_manual_file(
        self,
        file_content: bytes,
        filename: str,
        content_type: str = "application/pdf",
    ) -> Response:
        files = {"file": (filename, io.BytesIO(file_content), content_type)}
        return await self.post(ManualLoaderRoutes.UPLOAD_MANUAL_FILE, files=files)
```

> Если endpoint принимает дополнительные form-поля (например `org_id`), передай их через `data=`:
> ```python
> data = {"org_id": org_id}
> return await self.post(..., data=data, files=files)
> ```

---

## Шаг 4 — Добавить фикстуру

Создать **`fixtures/api/manual_loader.py`**:
```python
from __future__ import annotations

from typing import AsyncIterator

import pytest_asyncio

from clients.base_client import get_http_client
from clients.manual_loader_client import ManualLoaderClient
from config import APISettings


@pytest_asyncio.fixture
async def manual_loader_client(settings: APISettings, auth_token: str) -> AsyncIterator[ManualLoaderClient]:
    async with get_http_client(settings.api_http_client, token=auth_token) as http_client:
        yield ManualLoaderClient(client=http_client)
```

**`conftest.py`** — зарегистрировать фикстуру:
```python
pytest_plugins = (
    "fixtures.api.settings",
    "fixtures.api.auth",
    "fixtures.api.auth_roles",
    "fixtures.api.org",
    "fixtures.api.user",
    "fixtures.api.manual_loader",  # добавить
    "fixtures.e2e.settings",
)
```

---

## Шаг 5 — Написать тесты

Создать **`tests/api/manual_loader/test_upload_manual_file.py`**:
```python
from __future__ import annotations

from http import HTTPStatus

import allure
import pytest

from clients.auth_client import AuthClient
from clients.manual_loader_client import ManualLoaderClient
from schema.manual_loader import UploadManualFileResponseSchema
from tools.assertions.base import assert_status_code

# Минимальный валидный PDF
VALID_PDF = b"%PDF-1.0\n1 0 obj<</Type /Catalog>>endobj\nxref\n0 1\n0000000000 65535 f\ntrailer<</Size 1/Root 1 0 R>>\nstartxref\n9\n%%EOF"
VALID_DOCX = b"PK\x03\x04"  # ZIP-заголовок (DOCX = ZIP)
INVALID_BYTES = b"this is not a valid document"


@pytest.mark.api
@pytest.mark.manual_loader
@pytest.mark.integration
@allure.feature("Manual Loader")
@allure.story("Upload Manual File")
class TestUploadManualFilePositive:

    @allure.title("Upload: valid PDF → 200 + file_id")
    async def test_upload_pdf(self, manual_loader_client: ManualLoaderClient) -> None:
        response = await manual_loader_client.upload_manual_file(
            file_content=VALID_PDF,
            filename="test.pdf",
            content_type="application/pdf",
        )
        assert_status_code(response.status_code, HTTPStatus.OK)
        body = UploadManualFileResponseSchema.model_validate_json(response.text)
        assert body.file_id

    @allure.title("Upload: valid DOCX → 200")
    async def test_upload_docx(self, manual_loader_client: ManualLoaderClient) -> None:
        response = await manual_loader_client.upload_manual_file(
            file_content=VALID_DOCX,
            filename="test.docx",
            content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        )
        assert_status_code(response.status_code, HTTPStatus.OK)

    @allure.title("Upload: response schema is valid")
    async def test_upload_response_schema(self, manual_loader_client: ManualLoaderClient) -> None:
        response = await manual_loader_client.upload_manual_file(VALID_PDF, "manual.pdf")
        assert_status_code(response.status_code, HTTPStatus.OK)
        body = UploadManualFileResponseSchema.model_validate_json(response.text)
        assert body.message
        assert body.file_id


@pytest.mark.api
@pytest.mark.manual_loader
@pytest.mark.integration
@allure.feature("Manual Loader")
@allure.story("Upload Manual File – Validation")
class TestUploadManualFileValidation:

    @allure.title("Upload: invalid file format → 400")
    async def test_upload_invalid_format(self, manual_loader_client: ManualLoaderClient) -> None:
        response = await manual_loader_client.upload_manual_file(
            file_content=INVALID_BYTES,
            filename="bad.exe",
            content_type="application/octet-stream",
        )
        assert response.status_code == HTTPStatus.BAD_REQUEST.value

    @allure.title("Upload: empty file → 400 or 422")
    async def test_upload_empty_file(self, manual_loader_client: ManualLoaderClient) -> None:
        response = await manual_loader_client.upload_manual_file(
            file_content=b"",
            filename="empty.pdf",
            content_type="application/pdf",
        )
        assert response.status_code in (
            HTTPStatus.BAD_REQUEST.value,
            HTTPStatus.UNPROCESSABLE_ENTITY.value,
        )


@pytest.mark.api
@pytest.mark.manual_loader
@pytest.mark.integration
@allure.feature("Manual Loader")
@allure.story("Upload Manual File – Authorization")
class TestUploadManualFileAuthorization:

    @allure.title("Upload: no token → 401")
    async def test_upload_no_token(self, api_client_no_auth: AuthClient) -> None:
        response = await api_client_no_auth.post(
            "/api/manual_loader/upload_manual_file",
            files={"file": ("test.pdf", VALID_PDF, "application/pdf")},
        )
        assert response.status_code == HTTPStatus.UNAUTHORIZED.value
```

---

## Шаг 6 — Добавить RBAC-правило

Создать **`tests/api/rbac/policy/manual_loader.py`**:
```python
from __future__ import annotations

from schema.rbac import AccessRule

ACCESS_POLICY_MANUAL_LOADER: list[AccessRule] = [
    AccessRule(
        name="manual_loader:upload_manual_file — user allowed",
        method="POST",
        path="/api/manual_loader/upload_manual_file",
        allowed_roles=["user", "admin"],
        denied_roles=["super_admin"],
        expected_allowed_status=400,  # 400 т.к. файл не передан, но доступ разрешён
        expected_denied_status=403,
    ),
]
```

**`tests/api/rbac/policy/__init__.py`** — добавить:
```python
from tests.api.rbac.policy.auth import ACCESS_POLICY_AUTH
from tests.api.rbac.policy.manual_loader import ACCESS_POLICY_MANUAL_LOADER  # добавить
from tests.api.rbac.policy.org import ACCESS_POLICY_ORG
from tests.api.rbac.policy.user import ACCESS_POLICY_USER

ACCESS_POLICY = [
    *ACCESS_POLICY_AUTH,
    *ACCESS_POLICY_MANUAL_LOADER,  # добавить
    *ACCESS_POLICY_ORG,
    *ACCESS_POLICY_USER,
]
```

---

## Итого — какие файлы затронуты

| Действие | Файл |
|---|---|
| Создать | `tools/routes/manual_loader.py` |
| Изменить | `tools/routes/__init__.py` |
| Создать | `schema/manual_loader.py` |
| Создать | `clients/manual_loader_client.py` |
| Создать | `fixtures/api/manual_loader.py` |
| Изменить | `conftest.py` |
| Создать | `tests/api/manual_loader/test_upload_manual_file.py` |
| Создать | `tests/api/rbac/policy/manual_loader.py` |
| Изменить | `tests/api/rbac/policy/__init__.py` |

---

## Запуск

```bash
# Только тесты нового endpoint
python -m pytest tests/api/manual_loader/ -v

# С конкретной ролью
ACTIVE_ROLE=user python -m pytest tests/api/manual_loader/ -v

# RBAC матрица для нового endpoint
python -m pytest tests/api/rbac/ -k "manual_loader" -v

# Allure-отчёт
python -m pytest tests/api/manual_loader/ --alluredir=allure-results
allure serve allure-results
```
