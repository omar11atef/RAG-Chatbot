from fastapi import Depends
from core.config import settings
from application.services import IRagServiceClient, ChatService, TriggerService
from domain.abstractions import Result
from domain.errors import ChatErrors
from application.contracts import ChatResponse

# Simulated HTTP Client (Infrastructure Layer equivalent)
class RagServiceClient(IRagServiceClient):
    def __init__(self, base_url: str):
        self.base_url = base_url
        
    async def query_async(self, question: str) -> Result[ChatResponse]:
        # In reality, this would use httpx.AsyncClient to call the Python AI model
        return Result.success(ChatResponse(answer="Simulated Answer", sources=[]))

    async def ingest_async(self) -> Result[None]:
        return Result.success(None)

# --- Dependency Providers ---
def get_rag_client() -> IRagServiceClient:
    return RagServiceClient(base_url=settings.rag_service_base_url)

def get_chat_service(rag_client: IRagServiceClient = Depends(get_rag_client)) -> ChatService:
    return ChatService(rag_client)

def get_trigger_service(rag_client: IRagServiceClient = Depends(get_rag_client)) -> TriggerService:
    return TriggerService(rag_client)