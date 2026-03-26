from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, ConfigDict


# ── Create Conversation ────────────────────────────────────────────────────────

class ConversationCreateRequestSchema(BaseModel):
    question: str
    file_id: Optional[str] = None


class ConversationCreateResponseSchema(BaseModel):
    id: str
    question: str
    file_id: Optional[str] = None
    file_ids: list[str] = []
    timestamp: str
    created_at: str

    model_config = ConfigDict(extra="ignore")


# ── Get Conversation ───────────────────────────────────────────────────────────

class ConversationGetRequestSchema(BaseModel):
    conversation_id: str
    count_message: Optional[int] = None


class MessageSchema(BaseModel):
    id: str
    conversation_id: str
    question: str
    answer: Optional[str] = None
    file_ids: list[str] = []
    model_name: Optional[str] = None
    timestamp: str
    is_external_source: bool = False
    is_first_message: Optional[bool] = None
    chart: Optional[Any] = None
    question_domain: Optional[str] = None
    streaming_tokens: Optional[Any] = None

    model_config = ConfigDict(extra="ignore")


class ConversationGetResponseSchema(BaseModel):
    messages: list[MessageSchema]

    model_config = ConfigDict(extra="ignore")


# ── Get All Conversations ──────────────────────────────────────────────────────

class ConversationGetAllRequestSchema(BaseModel):
    count_conversation: Optional[int] = None


# ── Delete Conversations ───────────────────────────────────────────────────────

class ConversationDeleteRequestSchema(BaseModel):
    conversation_ids: Optional[list[str]] = None
    file_ids: Optional[list[str]] = None


class ConversationDeleteResponseSchema(BaseModel):
    message: str
    deleted_count: int

    model_config = ConfigDict(extra="ignore")


# ── Search Conversations ───────────────────────────────────────────────────────

class ConversationSearchRequestSchema(BaseModel):
    search_text: str


class ConversationSearchItemSchema(BaseModel):
    id: str
    question: str
    file_id: Optional[str] = None
    file_ids: list[str] = []
    timestamp: str
    created_at: str
    message_count: Optional[int] = None
    relevance_score: Optional[float] = None

    model_config = ConfigDict(extra="ignore")


class ConversationSearchResponseSchema(BaseModel):
    conversations: list[ConversationSearchItemSchema]
    total_results: int

    model_config = ConfigDict(extra="ignore")
