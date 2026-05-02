from dataclasses import dataclass, field
from datetime import datetime, timezone
import uuid

@dataclass
class Session:
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    expires_at: datetime | None = None
    message_count: int = 0
    message_limit: int = 10
    is_active: bool = True

@dataclass
class ConversationLog:
    session_id: uuid.UUID
    turn_index: int
    question: str
    answer: str