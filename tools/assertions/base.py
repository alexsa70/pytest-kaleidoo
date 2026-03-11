from typing import Any

import allure

from tools.logger import get_logger

logger = get_logger("BASE_ASSERTIONS")


@allure.step("Check that response status code equals to {expected}")
def assert_status_code(actual: int, expected: int):
    """
    Проверяет, что HTTP-статус ответа соответствует ожидаемому.

    :param: actual (int): Фактический статус-код.
    :param: expected (int): Ожидаемый статус-код.
    :raises: AssertionError: Если статус-коды не совпадают.
    """
    logger.info(f"Check that response status code equals to {expected}")

    assert actual == expected, (
        f'Incorrect response status code. '
        f'Expected status code: {expected}. '
        f'Actual status code: {actual}'
    )


@allure.step("Check that {name} equals to {expected}")
def assert_equal(actual: Any, expected: Any, name: str):
    """
    Проверяет, что два значения равны.

    :param: actual (Any): Фактическое значение.
    :param: expected (Any): Ожидаемое значение.
    :param: name (str): Имя проверяемого параметра (для логирования).
    :raises: AssertionError: Если значения не равны.
    """
    logger.info(f'Check that "{name}" equals to {expected}')

    assert actual == expected, (
        f'Incorrect value: "{name}". '
        f'Expected value: {expected}. '
        f'Actual value: {actual}'
    )
