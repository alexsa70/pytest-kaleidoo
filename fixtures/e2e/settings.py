import pytest

from config import E2ESettings


@pytest.fixture(scope="session")
def e2e_settings() -> E2ESettings:
    """Фикстура настроек для e2e тестов."""

    return E2ESettings()
