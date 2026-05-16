from __future__ import annotations

from typing import Literal
from pydantic import BaseModel, Field, HttpUrl


AgentRole = Literal['expansive_optimist', 'defensive_skeptic', 'peer_reviewer', 'master_synthesizer']


class AgentResult(BaseModel):
    role: AgentRole
    title: str
    content: str
    model_used: str = 'mock'


class AuditCycle(BaseModel):
    cycle: int
    consensus_count: int = Field(ge=0)
    conflict_count: int = Field(ge=0)
    log_summary: str


class ReferenceLink(BaseModel):
    name: str
    url: str


class FinalReport(BaseModel):
    title: str
    content: str
    links: list[ReferenceLink] = Field(default_factory=list)


class PeerReviewJSON(BaseModel):
    consensus_count: int = Field(default=0, ge=0)
    conflict_count: int = Field(default=0, ge=0)
    critique_text: str = ''


class MetaVistaSession(BaseModel):
    session_id: str
    user_prompt: str
    history: list[AuditCycle]
    final_report: FinalReport
    agent_outputs: list[AgentResult] = Field(default_factory=list)
