from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict


# ── Word Edit ──────────────────────────────────────────────────────────────────

class WordEditSchema(BaseModel):
    start: str
    end: str
    word: str
    newWord: str
    speaker: str


# ── Speaker Edit ───────────────────────────────────────────────────────────────

class SpeakerEditSchema(BaseModel):
    speaker: str
    newSpeaker: str


# ── Conversation Editing ───────────────────────────────────────────────────────

class ConversationEditingRequestSchema(BaseModel):
    file_id: str
    words: Optional[list[WordEditSchema]] = None
    speakers: Optional[list[SpeakerEditSchema]] = None


class ConversationEditingResponseSchema(BaseModel):
    message: str

    model_config = ConfigDict(extra="ignore")
