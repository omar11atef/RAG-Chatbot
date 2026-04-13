from pydantic import BaseModel, Field, field_validator
from typing import List

# --- Responses ---
class SourceResponse(BaseModel):
    file_name: str
    page: int
    snippet: str

class ChatResponse(BaseModel):
    answer: str
    sources: List[SourceResponse] = []

class TriggerResponse(BaseModel):
    accepted: bool
    message: str

# --- Requests & Validation (Equivalent to FluentValidation) ---
class ChatRequest(BaseModel):
    question: str = Field(..., max_length=1000)

    @field_validator('question')
    def question_must_not_be_empty(cls, v: str):
        if not v.strip():
            raise ValueError("Question cannot be empty.")
        return v

class TriggerRequest(BaseModel):
    trigger: str

    @field_validator('trigger')
    def validate_trigger_type(cls, v: str):
        valid_triggers = {"manual", "scheduled", "document_added"}
        if v.lower() not in valid_triggers:
            raise ValueError("Trigger must be 'manual', 'scheduled', or 'document_added'.")
        return v.lower()