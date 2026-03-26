from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, ConfigDict


# ── Agent Schema ───────────────────────────────────────────────────────────────

class AgentSchema(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    org_id: Optional[str] = None
    type: str
    rules: list[Any] = []
    rule_ids: Optional[list[str]] = None
    logic_expression_string: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    model_config = ConfigDict(extra="ignore")


# ── Create Agent ───────────────────────────────────────────────────────────────

class CreateAgentRequestSchema(BaseModel):
    name: str
    description: Optional[str] = None
    type: Optional[str] = None
    folders: Optional[list[str]] = None
    rules: list[Any]


class CreateAgentResponseSchema(BaseModel):
    id: str

    model_config = ConfigDict(extra="ignore")


# ── Get Agent ──────────────────────────────────────────────────────────────────

class GetAgentRequestSchema(BaseModel):
    agent_id: str


# ── Get All Agents ─────────────────────────────────────────────────────────────

class GetAllAgentsRequestSchema(BaseModel):
    type: Optional[str] = None
    agents_ids: Optional[list[str]] = None
    folder_ids: Optional[list[str]] = None
    limit: Optional[int] = None
    cursor: Optional[str] = None


class GetAllAgentsResponseSchema(BaseModel):
    message: str
    agents: list[AgentSchema]
    next_cursor: Optional[str] = None
    has_more: Optional[bool] = None

    model_config = ConfigDict(extra="ignore")


# ── Update Agent ───────────────────────────────────────────────────────────────

class AgentUpdateDataSchema(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    folders: Optional[list[str]] = None
    rules: Optional[list[Any]] = None


class UpdateAgentRequestSchema(BaseModel):
    agent_id: str
    update_data: AgentUpdateDataSchema


class UpdateAgentResponseSchema(BaseModel):
    message: str
    id: str

    model_config = ConfigDict(extra="ignore")


# ── Delete Agent ───────────────────────────────────────────────────────────────

class DeleteAgentRequestSchema(BaseModel):
    agent_id: str


class DeleteAgentResponseSchema(BaseModel):
    message: str
    id: str

    model_config = ConfigDict(extra="ignore")
