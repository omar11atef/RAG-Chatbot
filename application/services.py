from abc import ABC, abstractmethod
import logging
from application.contracts import ChatRequest, ChatResponse, TriggerRequest, TriggerResponse
from domain.abstractions import Result
from domain.errors import ChatErrors, TriggerErrors

logger = logging.getLogger(__name__)

# --- Interfaces ---
class IRagServiceClient(ABC):
    @abstractmethod
    async def query_async(self, question: str) -> Result[ChatResponse]: pass
    
    @abstractmethod
    async def ingest_async(self) -> Result[None]: pass

class IChatService(ABC):
    @abstractmethod
    async def ask_async(self, request: ChatRequest) -> Result[ChatResponse]: pass

class ITriggerService(ABC):
    @abstractmethod
    async def handle_trigger_async(self, request: TriggerRequest) -> Result[TriggerResponse]: pass

# --- Implementations ---
class ChatService(IChatService):
    def __init__(self, rag_client: IRagServiceClient):
        self._rag_client = rag_client

    async def ask_async(self, request: ChatRequest) -> Result[ChatResponse]:
        logger.info(f"Processing chat request. Question length: {len(request.question)}")

        # 1. Delegate to Infrastructure (Python AI Service)
        rag_result = await self._rag_client.query_async(request.question)

        # 2. Check Call Result Pattern
        if rag_result.is_failure:
            logger.warning(f"RAG service failed. Error: {rag_result.error.code}")
            return Result.failure(ChatErrors.RagServiceUnavailable)

        logger.info(f"Chat response generated successfully.")
        return Result.success(rag_result.value)

class TriggerService(ITriggerService):
    def __init__(self, rag_client: IRagServiceClient):
        self._rag_client = rag_client

    async def handle_trigger_async(self, request: TriggerRequest) -> Result[TriggerResponse]:
        logger.info(f"Received ingestion trigger: {request.trigger}")

        ingest_result = await self._rag_client.ingest_async()

        if ingest_result.is_failure:
            logger.error("Ingestion failed at AI Service.")
            return Result.failure(TriggerErrors.IngestFailed)

        return Result.success(TriggerResponse(
            accepted=True, 
            message=f"Ingestion triggered successfully via '{request.trigger}'."
        ))