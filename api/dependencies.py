from fastapi import Depends, HTTPException, Security, status
from fastapi.security.api_key import APIKeyHeader
from typing import List, Dict
import uuid

from core.config import settings
from application.services import (
    IRagServiceClient, ChatService, TriggerService,
    SessionService, ConversationContextBuilder,
    ISessionRepository, ILogRepository
)
from domain.abstractions import Result
from domain.entities import Session, ConversationLog
from application.contracts import ChatResponse, TurnHistoryDto

# --- Security ---
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

async def get_api_key(api_key_header: str = Security(api_key_header)):
    if api_key_header != settings.api_key:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API Key")
    return api_key_header

# --- In-Memory DB ---
_db_sessions: Dict[uuid.UUID, Session] = {}
_db_logs: List[ConversationLog] = []

class InMemorySessionRepository(ISessionRepository):
    async def get_by_id(self, session_id: uuid.UUID) -> Session | None:
        return _db_sessions.get(session_id)
    
    async def save(self, session: Session) -> None:
        _db_sessions[session.id] = session

class InMemoryLogRepository(ILogRepository):
    async def get_by_session_id(self, session_id: uuid.UUID) -> List[ConversationLog]:
        return sorted(
            [log for log in _db_logs if log.session_id == session_id],
            key=lambda x: x.turn_index
        )
    
    async def add(self, log: ConversationLog) -> None:
        _db_logs.append(log)

# --- RAG Client ---
class RagServiceClient(IRagServiceClient):
    def __init__(self, base_url: str):
        self.base_url = base_url
        
    async def query_async(self, question: str, history: List[TurnHistoryDto]) -> Result[ChatResponse]:
        # 🔥 هنا التاريخ يُستخدم فعليًا
        return Result.success(ChatResponse(
            answer=f"Answer based on history of {len(history)} turns",
            sources=[],
            turn_index=0,
            remaining_messages=0
        ))

    async def ingest_async(self) -> Result[None]:
        return Result.success(None)

# --- Providers ---
def get_session_repo(): return InMemorySessionRepository()
def get_log_repo(): return InMemoryLogRepository()
def get_rag_client(): return RagServiceClient(settings.rag_service_base_url)

def get_session_service(
    session_repo=Depends(get_session_repo),
    log_repo=Depends(get_log_repo)
):
    return SessionService(session_repo, log_repo)

def get_context_builder(log_repo=Depends(get_log_repo)):
    return ConversationContextBuilder(log_repo)

def get_chat_service(
    rag_client=Depends(get_rag_client),
    session_service=Depends(get_session_service),
    context_builder=Depends(get_context_builder)
):
    return ChatService(rag_client, session_service, context_builder)

def get_trigger_service(rag_client=Depends(get_rag_client)):
    return TriggerService(rag_client)