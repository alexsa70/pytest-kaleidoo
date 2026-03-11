from __future__ import annotations

import allure

from schema.operations import CreateResourceSchema, ResourceSchema, UpdateResourceSchema
from tools.assertions.base import assert_equal
from tools.logger import get_logger

logger = get_logger("RESOURCE_ASSERTIONS")


@allure.step("Check resource fields")
def assert_resource_fields(
    actual: ResourceSchema,
    expected: CreateResourceSchema | UpdateResourceSchema,
) -> None:
    logger.info("Check resource fields")

    if expected.name is not None:
        assert_equal(actual.name, expected.name, "name")
    if expected.description is not None:
        assert_equal(actual.description, expected.description, "description")


@allure.step("Check resource identity")
def assert_resource(actual: ResourceSchema, expected: ResourceSchema) -> None:
    logger.info("Check resource identity")

    assert_equal(actual.id, expected.id, "id")
    assert_equal(actual.name, expected.name, "name")
    assert_equal(actual.description, expected.description, "description")
