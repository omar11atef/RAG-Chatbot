import uuid
import logging
from abc import ABC, abstractmethod
from typing import List

from application.contracts import (
    ChatRequest, ChatResponse, TriggerRequest,
    TriggerResponse, TurnHistoryDto, SessionStateResponse
)
from domain.abstractions import Result
from domain.errors import ChatErrors, TriggerErrors, SessionErrors
from domain.entities import Session, ConversationLog

logger = logging.getLogger(__name__)

# ---------------- Interfaces ----------------

class ISessionRepository(ABC):
    @abstractmethod
    async def get_by_id(self, session_id: uuid.UUID) -> Session | None: pass

    @abstractmethod
    async def save(self, session: Session) -> None: pass


class ILogRepository(ABC):
    @abstractmethod
    async def get_by_session_id(self, session_id: uuid.UUID) -> List[ConversationLog]: pass

    @abstractmethod
    async def add(self, log: ConversationLog) -> None: pass


class IChatService(ABC):
    @abstractmethod
    async def ask_async(self, request: ChatRequest) -> Result[ChatResponse]: pass


class IRagServiceClient(ABC):
    @abstractmethod
    async def query_async(self, question: str, history: List[TurnHistoryDto]) -> Result[ChatResponse]: pass

    @abstractmethod
    async def ingest_async(self) -> Result[None]: pass


# ---------------- Services ----------------

class SessionService:
    def __init__(self, session_repo: ISessionRepository, log_repo: ILogRepository):
        self._session_repo = session_repo
        self._log_repo = log_repo

    async def create_session(self) -> uuid.UUID:
        session = Session()
        await self._session_repo.save(session)
        return session.id

    async def get_session_state(self, session_id: uuid.UUID) -> Result[SessionStateResponse]:
        session = await self._session_repo.get_by_id(session_id)
        if not session:
            return Result.failure(SessionErrors.NotFound)

        logs = await self._log_repo.get_by_session_id(session_id)

        history = [
            TurnHistoryDto(
                turn_index=l.turn_index,
                question=l.question,
                answer=l.answer
            ) for l in logs
        ]

        return Result.success(SessionStateResponse(
            session_id=session.id,
            message_count=session.message_count,
            message_limit=session.message_limit,
            remaining_messages=session.message_limit - session.message_count,
            is_active=session.is_active,
            history=history
        ))

    async def validate_session(self, session_id: uuid.UUID) -> Result[Session]:
        session = await self._session_repo.get_by_id(session_id)

        if not session:
            return Result.failure(SessionErrors.NotFound)

        if not session.is_active or session.message_count >= session.message_limit:
            return Result.failure(SessionErrors.LimitReached)

        return Result.success(session)

    async def record_turn(self, session_id: uuid.UUID, question: str, answer: str) -> int:
        session = await self._session_repo.get_by_id(session_id)
        if not session:
            return 0

        session.message_count += 1

        if session.message_count >= session.message_limit:
            session.is_active = False

        await self._session_repo.save(session)

        log = ConversationLog(
            session_id=session.id,
            turn_index=session.message_count,
            question=question,
            answer=answer
        )

        await self._log_repo.add(log)

        return session.message_count

    async def close_session(self, session_id: uuid.UUID) -> Result[None]:
        session = await self._session_repo.get_by_id(session_id)

        if not session:
            return Result.failure(SessionErrors.NotFound)

        session.is_active = False
        await self._session_repo.save(session)

        return Result.success(None)


class ConversationContextBuilder:
    def __init__(self, log_repo: ILogRepository):
        self._log_repo = log_repo

    async def build_history(self, session_id: uuid.UUID) -> List[TurnHistoryDto]:
        logs = await self._log_repo.get_by_session_id(session_id)

        logs = logs[-6:]

        return [
            TurnHistoryDto(
                turn_index=l.turn_index,
                question=l.question,
                answer=l.answer
            )
            for l in logs
        ]


class ChatService(IChatService):
    def __init__(self, rag_client: IRagServiceClient, session_service: SessionService, context_builder: ConversationContextBuilder):
        self._rag_client = rag_client
        self._session_service = session_service
        self._context_builder = context_builder

    async def ask_async(self, request: ChatRequest) -> Result[ChatResponse]:

        session_result = await self._session_service.validate_session(request.session_id)
        if session_result.is_failure:
            return Result.failure(session_result.error)

        session = session_result.value

        history = await self._context_builder.build_history(request.session_id)

        rag_result = await self._rag_client.query_async(request.question, history)
        if rag_result.is_failure:
            return Result.failure(ChatErrors.RagServiceUnavailable)

        turn_index = await self._session_service.record_turn(
            session.id,
            request.question,
            rag_result.value.answer
        )

        remaining = max(session.message_limit - turn_index, 0)

        return Result.success(ChatResponse(
            answer=rag_result.value.answer,
            sources=rag_result.value.sources,
            turn_index=turn_index,
            remaining_messages=remaining
        ))


class TriggerService:
    def __init__(self, rag_client: IRagServiceClient):
        self._rag_client = rag_client

    async def handle_trigger_async(self, request: TriggerRequest) -> Result[TriggerResponse]:
        result = await self._rag_client.ingest_async()

        if result.is_failure:
            return Result.failure(TriggerErrors.IngestFailed)

        return Result.success(
            TriggerResponse(
                accepted=True,
                message="Ingestion triggered"
            )
        )