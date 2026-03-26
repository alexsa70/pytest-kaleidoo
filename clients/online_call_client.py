from __future__ import annotations

# Online Call сервис использует WebSocket/Socket.IO — HTTP-эндпоинтов нет.
# Этот клиент является заглушкой для будущих HTTP-хелперов (если появятся).
# Для тестирования WebSocket используйте python-socketio или socketio.AsyncClient
# с session token из AuthClient.create_session_token(service="kal-sense").

from clients.base_client import BaseClient


class OnlineCallClient(BaseClient):
    """Заглушка клиента для Online Call сервиса (WebSocket/Socket.IO).

    Actual real-time testing requires a Socket.IO client.
    Session token is obtained via AuthClient.create_session_token(service='kal-sense').
    """
