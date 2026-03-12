# Async API Test Template (pytest)

Чистый шаблон для асинхронного тестирования API на `pytest + pytest-asyncio + httpx.AsyncClient`.

Проект больше не привязан к конкретному сервису или текущим тест-кейсам. Внутри оставлен каркас, который нужно адаптировать под ваш API.

## Стек

- Python 3.9+
- pytest
- pytest-asyncio
- httpx
- pydantic
- pydantic-settings
- allure-pytest
- faker
- jsonschema

## Установка

```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate   # Windows

pip install -r requirements.txt
cp .env.example .env
```

## Конфигурация

`.env` использует вложенные переменные и единые ключи окружений:

```env
PROFILE=api
ENVIRONMENT=local
API_HTTP_CLIENT.URL=https://api.example.com
API_HTTP_CLIENT.TIMEOUT=30
AUTH_CREDENTIALS.EMAIL=user@example.com
AUTH_CREDENTIALS.PASSWORD=supersecret
ORG_ROLE_ID=507f1f77bcf86cd799439022
E2E_BASE_URL=https://app.example.com
```

## Запуск

```bash
# Все тесты
python -m pytest tests/

# Только шаблонные
python -m pytest tests/ -m template

# Только интеграционные
python -m pytest tests/ -m integration

# Allure
python -m pytest tests/ --alluredir=allure-results
allure serve allure-results
```

### Запуск по профилю

```bash
# API-профиль
PROFILE=api python -m pytest tests/api -m "api and integration"

# E2E-профиль
PROFILE=e2e python -m pytest tests/e2e -m e2e
```

## Что уже есть в каркасе

- `clients/base_client.py` — базовый async HTTP клиент (GET/POST/PATCH/DELETE)
- `clients/operations_client.py` — шаблонный `ResourceClient` для CRUD
- `fixtures/operations.py` — фикстура `resource_client`
- `schema/operations.py` — базовые Pydantic-схемы ресурса
- `tests/test_operations.py` — минимальный локальный тест + пример integration-теста (skip)

## Как адаптировать под свой API

1. Обновить маршруты в `tools/routes.py`.
2. Подстроить модели в `schema/operations.py` под контракт API.
3. Изменить/добавить методы в `clients/operations_client.py`.
4. Переписать `tests/test_operations.py` под ваши сценарии.
5. Убрать `@pytest.mark.skip` с integration-тестов после настройки endpoint.

## Структура

```text
├── tests/
├── fixtures/
├── clients/
├── schema/
├── tools/
└── config/
```
