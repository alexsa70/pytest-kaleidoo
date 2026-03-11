from http import HTTPStatus

import allure
import pytest

from clients.operations_client import ResourceClient
from schema.operations import CreateResourceSchema
from tools.assertions.base import assert_status_code


@pytest.mark.template
class TestResourceTemplate:
    @allure.title("Template: local schema check")
    def test_create_resource_schema_defaults(self) -> None:
        payload = CreateResourceSchema()

        assert isinstance(payload.name, str)
        assert isinstance(payload.description, str)

    @pytest.mark.integration
    @pytest.mark.skip(reason="Шаблонный тест. Настройте .env и endpoint под ваш API.")
    @allure.title("Template: list resources")
    async def test_list_resources(self, resource_client: ResourceClient) -> None:
        response = await resource_client.list_resources_api()

        assert_status_code(response.status_code, HTTPStatus.OK)
