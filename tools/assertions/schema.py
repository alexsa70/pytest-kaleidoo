from typing import Any

import allure
from jsonschema import validate
from jsonschema.validators import Draft202012Validator

from tools.logger import get_logger

# Логгер для записи информации о процессе валидации
logger = get_logger("SCHEMA_ASSERTIONS")


@allure.step("Validating JSON schema")
def validate_json_schema(instance: Any, schema: dict) -> None:
    """"
    Проверяет, соответствует ли JSON-объект (instance) заданной JSON-схеме (schema).

    :param: instance (Any): JSON-объект, который необходимо проверить.
    :param: schema (dict): JSON-схема, согласно которой производится валидация.
    :raises:
        jsonschema.exceptions.ValidationError: В случае несоответствия JSON-объекта схеме.
        jsonschema.exceptions.SchemaError: Если переданная схема некорректна.
    """
    logger.info("Validating JSON schema")

    # Выполняем валидацию JSON-объекта по заданной схеме
    validate(
        schema=schema,  # JSON-схема, задающая структуру данных
        instance=instance,  # Проверяемый JSON-объект
        # Проверка форматов (например, email, дата и т.д.)
        format_checker=Draft202012Validator.FORMAT_CHECKER,
    )
