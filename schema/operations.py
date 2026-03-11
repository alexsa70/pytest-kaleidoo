from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field, RootModel

from tools.fakers import fake


class CreateResourceSchema(BaseModel):
    """Модель для создания сущности в API."""

    model_config = ConfigDict(populate_by_name=True)

    name: str = Field(default_factory=fake.word)
    description: str = Field(default_factory=fake.sentence)


class UpdateResourceSchema(BaseModel):
    """Модель для частичного обновления сущности."""

    model_config = ConfigDict(populate_by_name=True)

    name: str | None = None
    description: str | None = None


class ResourceSchema(CreateResourceSchema):
    """Модель сущности, возвращаемой API."""

    id: str | int


class ResourcesSchema(RootModel):
    """Контейнер для списка сущностей."""

    root: list[ResourceSchema]
