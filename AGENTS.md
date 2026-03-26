# AGENTS.md

This file contains instructions and conventions for AI agents working in this repository.

## Project Overview

This is a pytest-based async API test framework using `pytest-asyncio` + `httpx.AsyncClient` for testing a REST API (Kaleidoo).

**Architecture flow:**
```
Test → Fixture → DomainClient → BaseClient → httpx.AsyncClient → API
```

## Build/Lint/Test Commands

### Running Tests

```bash
# All tests
python -m pytest tests/

# Single test file
python -m pytest tests/api/login/test_positive.py

# Single test class
python -m pytest tests/api/login/test_positive.py::TestLoginPositive

# Single test function (most specific)
python -m pytest tests/api/login/test_positive.py::TestLoginPositive::test_login_valid_credentials_by_role

# By marker
python -m pytest tests/ -m smoke
python -m pytest tests/ -m regression
python -m pytest tests/ -m "api and integration"
python -m pytest tests/ -m "not slow"  # exclude slow tests

# By profile
PROFILE=api python -m pytest tests/api -m "api and integration"
PROFILE=e2e python -m pytest tests/e2e -m e2e

# With Allure reporting
python -m pytest tests/ --alluredir=allure-results
allure serve allure-results
```

### Linting

```bash
# Flake8 (max-line-length: 120)
flake8 .
```

### Environment Setup

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

## Code Style Guidelines

### Imports

- Always include `from __future__ import annotations` at the top
- Group imports: stdlib → third-party → local (enforced by editor)
- Use type hints with `typing` module for complex types
- Example:
```python
from __future__ import annotations

from typing import Any, AsyncIterator, Optional

import allure
import pytest
import pytest_asyncio

from clients.auth_client import AuthClient
from config import APISettings
```

### Formatting

- Max line length: **120 characters** (configured in `.flake8`)
- Use soft lines (hug related content, split at logical points)
- Section separators: `# ── Title ──────────────────────`
- Docstrings: Google style for functions, simple summaries for classes

### Type Hints

- Use `Optional[X]` instead of `X | None` for broader compatibility
- Use `Literal["value1", "value2"]` for constrained string types
- Always type-hint fixture returns:
```python
@pytest_asyncio.fixture
async def api_client(settings: APISettings, auth_token: str) -> AsyncIterator[AuthClient]:
    ...
```

### Naming Conventions

| Element | Convention | Example |
|---------|-----------|---------|
| Classes | PascalCase | `AuthClient`, `LoginRequestSchema` |
| Functions/methods | snake_case | `test_login_valid_credentials` |
| Constants | SCREAMING_SNAKE_CASE | `EXPIRES_IN_EXPECTED` |
| Modules | snake_case | `test_positive.py` |
| Test files | `test_*.py` or `*_tests.py` | `test_login.py`, `auth_tests.py` |
| Test classes | `Test*` | `TestLoginPositive` |
| Test functions | `test_*` | `test_login_with_mfa` |
| Fixtures | snake_case | `api_client`, `auth_token` |
| Routes (enum values) | SCREAMING_SNAKE_CASE | `AuthRoutes.LOGIN` |

### Error Handling

- Use `pytest.skip()` for conditional test skipping (missing credentials, etc.)
- Never swallow exceptions silently
- Use assertion messages for clarity:
```python
assert response.status_code == HTTPStatus.OK, f"Expected 200, got {response.status_code}"
```

### Pydantic Schemas

- Use `model_dump(exclude_none=True)` when serializing for API requests
- Use `model_config = ConfigDict(extra="ignore")` for response schemas
- Organize schemas by domain in `schema/` directory

### HTTP Testing

- Use `HTTPStatus` from `http` module for status codes:
```python
from http import HTTPStatus
assert response.status_code == HTTPStatus.OK
```
- Validate response bodies with Pydantic schemas:
```python
SSOLoginResponseSchema.model_validate_json(response.text)
```

### Allure Reporting

- Use `@allure.feature`, `@allure.story`, `@allure.title` for test classes/functions
- Use `@allure.step` decorator for custom test steps
- Steps appear in Allure report for better debugging

### Test Markers (from pytest.ini)

| Marker | Purpose |
|--------|---------|
| `smoke` | Critical path tests |
| `regression` | Full regression suite |
| `api` | API tests |
| `auth` | Authentication tests |
| `org` | Organization endpoint tests |
| `rbac` | Role-based access control tests |
| `user` | User endpoint tests |
| `integration` | Tests requiring live API |
| `e2e` | End-to-end tests |
| `slow` | Rate limit or heavy request tests |
| `security` | Security-focused tests |
| `live` | Tests requiring real OAuth tokens |
| `template` | Template/example tests |
| `only` | Run only explicitly marked tests |

## Project Structure

```
├── clients/           # HTTP clients
│   ├── base_client.py      # Generic httpx wrapper
│   ├── auth_client.py      # Authentication domain client
│   ├── org_client.py       # Organization domain client
│   └── user_client.py      # User domain client
├── config/            # Configuration
│   └── settings.py         # Pydantic settings from .env
├── fixtures/          # Pytest fixtures
│   ├── api/               # API test fixtures
│   │   ├── settings.py         # settings fixture
│   │   ├── auth.py             # auth fixtures
│   │   └── ...
│   └── e2e/               # E2E fixtures
├── schema/            # Pydantic request/response models
│   ├── auth.py
│   ├── organizations.py
│   └── users.py
├── tests/            # Test suite
│   ├── api/
│   │   ├── login/
│   │   ├── org/
│   │   ├── rbac/
│   │   └── user/
│   └── e2e/
├── tools/            # Utilities
│   ├── routes/           # API route constants (StringEnums)
│   ├── assertions/       # Custom assertion helpers
│   ├── fakers.py         # Test data generators
│   └── logger.py         # Logging utility
└── conftest.py       # Root pytest plugins
```

## Key Conventions

### Client Architecture

1. **BaseClient** (`clients/base_client.py`): Generic HTTP wrapper, no business logic
2. **Domain Clients** (`clients/*_client.py`): Inherit from BaseClient, contain business methods
3. All client methods use `@allure.step` for step reporting

### Fixture Lifecycle

- `settings`: Session-scoped, loads from `.env`
- `tokens_by_role`: Session-scoped, pre-created auth tokens
- `api_client`: Function-scoped, authenticated client
- `api_client_no_auth`: Function-scoped, no auth (for 401/403 tests)

### Route Definitions

Define routes as `StringEnum` in `tools/routes/`:
```python
class AuthRoutes(str, Enum):
    LOGIN = "/login"
    
    def __str__(self) -> str:
        return self.value
```

### Test Organization

- Group tests by feature (login, org, user, rbac)
- Use `Test<Feature><Scenario>` naming (e.g., `TestLoginPositive`)
- Use `@pytest.mark.parametrize` for data-driven tests
- Use helper functions with `_` prefix for test data construction

### Environment Configuration

Settings are loaded from `.env` via `pydantic-settings`:
```env
PROFILE=api
ENVIRONMENT=local
API_HTTP_CLIENT.URL=https://api.example.com
API_HTTP_CLIENT.TIMEOUT=30
AUTH_CREDENTIALS_ADMIN.EMAIL=admin@example.com
AUTH_CREDENTIALS_ADMIN.PASSWORD=secret
```

## Testing Best Practices

1. **Always check prerequisites**: Use `pytest.skip()` if credentials are missing
2. **Validate schemas**: Use Pydantic `model_validate()` for response validation
3. **Use fakers**: Generate test data with `tools.fakers` module
4. **Clear assertions**: Include descriptive assertion messages
5. **Avoid magic strings**: Use constants for expected values
6. **Test isolation**: Each test should be independent
7. **Profile separation**: Use `PROFILE=api|e2e` for different test suites
