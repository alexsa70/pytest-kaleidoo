import pytest

from config import APISettings


@pytest.fixture(scope="session")
def settings() -> APISettings:
    """
    Фикстура создаёт объект с настройками один раз на всю тестовую сессию.    
   :return: Экземпляр класса Settings с загруженными конфигурациями.
   """
    return APISettings()
