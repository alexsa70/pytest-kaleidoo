from enum import Enum


class APIRoutes(str, Enum):
    """Базовые маршруты API для шаблонного проекта."""

    RESOURCES = "/resources"

    def __str__(self) -> str:
        return self.value
