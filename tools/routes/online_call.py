from enum import Enum


class OnlineCallSocketEvents(str, Enum):
    """Online Call WebSocket event names (client → server)."""

    JOIN_ROOM = "join-room"
    SEND_AUDIO = "send_audio"
    LEAVE_ROOM = "leave_room"
    REFRESH_TOKEN = "refresh_token"

    def __str__(self) -> str:
        return self.value


class OnlineCallServerEvents(str, Enum):
    """Online Call WebSocket event names (server → client)."""

    ROOM_CREATED = "room_created"
    UPDATE_USER_LIST = "update_user_list"
    TRANSCRIPTION = "transcription"
    SENTIMENT = "sentiment"
    TRANSLATION = "translation"
    AGENTS = "agents"

    def __str__(self) -> str:
        return self.value
