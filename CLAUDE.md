# CLAUDE.md

Этот файл описывает правила и ориентиры для работы с кодом в этом репозитории.

## Назначение проекта

Репозиторий является чистым шаблоном для async API тестов.

Базовый поток:

```text
Test -> Fixture -> ResourceClient -> BaseClient -> httpx.AsyncClient -> API
```

## Команды

```bash
# Все тесты
python -m pytest tests/

# Шаблонные тесты
python -m pytest tests/ -m template

# Интеграционные тесты
python -m pytest tests/ -m integration

# Allure-отчет
python -m pytest tests/ --alluredir=allure-results
allure serve allure-results
```

## Текущая архитектура

- `clients/base_client.py`
  - универсальная обертка над `httpx.AsyncClient`
  - содержит методы `get`, `post`, `patch`, `delete`

- `clients/operations_client.py`
  - шаблонный доменный клиент `ResourceClient`
  - содержит CRUD-методы для `APIRoutes.RESOURCES`

- `fixtures/settings.py`
  - сессионная фикстура `settings`

- `fixtures/operations.py`
  - async-фикстура `resource_client`
  - фикстура `sample_resource_payload`

- `schema/operations.py`
  - `CreateResourceSchema`, `UpdateResourceSchema`, `ResourceSchema`, `ResourcesSchema`

## Конфигурация

Настройки загружаются из `.env` через `pydantic-settings`.

Используемые переменные:

```env
API_HTTP_CLIENT.URL=https://api.example.com
API_HTTP_CLIENT.TIMEOUT=30
```

## pytest

- `asyncio_mode = auto` в `pytest.ini`
- Маркеры:
  - `template` — базовые шаблонные проверки
  - `integration` — тесты реального API

## Что важно при развитии проекта

- Держать `BaseClient` универсальным и без бизнес-логики.
- Бизнес-методы добавлять только в доменные клиенты.
- Фикстуры должны управлять жизненным циклом `AsyncClient`.
- Любые новые endpoint и контракты сначала отражать в `tools/routes.py` и `schema/`.

## Agents roles

**python-expert**: Для код-ревью, планирования фич и соблюдения стиля.
**python-debugger**: Только для исправления ошибок и анализа падений.
