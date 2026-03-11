from httpx import Request, Response

from tools.logger import get_logger

# Создаем логгер для HTTP-клиента
logger = get_logger("HTTP_CLIENT")


async def log_request_event_hook(request: Request):
    """
    Логирует информацию перед отправкой HTTP-запроса.

    :param request: Объект запроса HTTPX.
    """
    logger.info(f'Make {request.method} request to {request.url}')


async def log_response_event_hook(response: Response):
    """
    Логирует информацию после получения HTTP-ответа.

    :param response: Объект ответа HTTPX.
    """
    logger.info(
        f"Got response {response.status_code} {response.reason_phrase} from {response.url}"
    )