from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, ConfigDict


# ── Join Room ──────────────────────────────────────────────────────────────────

class JoinRoomPayloadSchema(BaseModel):
    user_id: str
    org_id: str
    username: str
    room_id: Optional[str] = None
    lang_code: str
    file_name: str
    folder_id: str
    translation_mode: bool


# ── Room Created ───────────────────────────────────────────────────────────────

class RoomCreatedSchema(BaseModel):
    room_id: str
    message: str

    model_config = ConfigDict(extra="ignore")


# ── Send Audio ─────────────────────────────────────────────────────────────────

class SendAudioPayloadSchema(BaseModel):
    audio_file: str  # base64-encoded
    user_name: str
    user_id: str
    room_id: str
    username: str
    time: str
    source_language: str
    target_language: str
    message: Optional[str] = None


# ── Transcription ──────────────────────────────────────────────────────────────

class TranscriptionWordSchema(BaseModel):
    start: str
    end: str
    word: str

    model_config = ConfigDict(extra="ignore")


class TranscriptionEventSchema(BaseModel):
    room_id: str
    status: int
    code: int
    message: str
    audio_duration: Optional[float] = None
    transcription: list[TranscriptionWordSchema] = []
    org_id: Optional[str] = None
    user_id: Optional[str] = None
    user_name: Optional[str] = None
    time: Optional[str] = None
    is_on: Optional[bool] = None
    source_language: Optional[str] = None
    target_language: Optional[str] = None
    workflow_type: Optional[Any] = None

    model_config = ConfigDict(extra="ignore")


# ── Leave Room ─────────────────────────────────────────────────────────────────

class LeaveRoomPayloadSchema(BaseModel):
    room_id: str
    user_id: str
    username: str
    org_id: str
