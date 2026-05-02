from pydantic import BaseModel, Field, field_validator
from typing import List
import uuid

class SourceResponse(BaseModel):
    file_name: str
    page: int
    snippet: str

class ChatResponse(BaseModel):
    answer: str
    sources: List[SourceResponse] = []
    turn_index: int
    remaining_messages: int

class ChatRequest(BaseModel):
    session_id: uuid.UUID
    question: str = Field(..., max_length=1000)

    @field_validator('question')
    def validate_question(cls, v: str):
        if not v.strip():
            raise ValueError("Question cannot be empty.")
        return v

class CreateSessionResponse(BaseModel):
    session_id: uuid.UUID

class TurnHistoryDto(BaseModel):
    turn_index: int
    question: str
    answer: str

class SessionStateResponse(BaseModel):
    session_id: uuid.UUID
    message_count: int
    message_limit: int
    remaining_messages: int
    is_active: bool
    history: List[TurnHistoryDto]

class TriggerRequest(BaseModel):
    trigger: str

class TriggerResponse(BaseModel):
    accepted: bool
    message: str