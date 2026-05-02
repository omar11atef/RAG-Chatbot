from pydantic import BaseModel
from typing import List, Optional


class CreateSessionResponse(BaseModel):
    session_id: str
    message_limit: int
    message_count: int
    is_active: bool


class ChatRequest(BaseModel):
    session_id: str
    question: str


class ChatResponse(BaseModel):
    answer: str
    sources: List[str] = []
    turn_index: int
    remaining_messages: int


class RagHistoryItem(BaseModel):
    turn_index: int
    question: str
    answer: str


class RagRequest(BaseModel):
    question: str
    history: List[RagHistoryItem] = []