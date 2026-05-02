from fastapi import APIRouter, Depends, status, Response
import uuid
from application.contracts import ChatRequest, ChatResponse, TriggerRequest, TriggerResponse, CreateSessionResponse, SessionStateResponse
from application.services import IChatService, TriggerService, SessionService
from api.dependencies import get_chat_service, get_trigger_service, get_session_service, get_api_key
from domain.abstractions import ResultException

# --- Session Controller ---
session_router = APIRouter(prefix="/api/session", tags=["Session"])

@session_router.post("", response_model=CreateSessionResponse)
async def create_session(session_service: SessionService = Depends(get_session_service)):
    session_id = await session_service.create_session()
    return CreateSessionResponse(session_id=session_id)

@session_router.get("/{session_id}", response_model=SessionStateResponse)
async def get_session(session_id: uuid.UUID, session_service: SessionService = Depends(get_session_service)):
    result = await session_service.get_session_state(session_id)
    if result.is_failure:
        raise ResultException(result.error)
    return result.value

@session_router.delete("/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
async def close_session(session_id: uuid.UUID, session_service: SessionService = Depends(get_session_service)):
    result = await session_service.close_session(session_id)
    if result.is_failure:
        raise ResultException(result.error)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# --- Chat Controller ---
chat_router = APIRouter(prefix="/api/chat", tags=["Chat"], dependencies=[Depends(get_api_key)])

@chat_router.post("", response_model=ChatResponse)
async def ask(
    request: ChatRequest, 
    chat_service: IChatService = Depends(get_chat_service)
):
    result = await chat_service.ask_async(request)
    if result.is_failure:
        raise ResultException(result.error) 
    return result.value


# --- Trigger Controller ---
trigger_router = APIRouter(prefix="/api/trigger", tags=["Trigger"], dependencies=[Depends(get_api_key)])

@trigger_router.post("", response_model=TriggerResponse)
async def handle_trigger(
    request: TriggerRequest, 
    trigger_service: TriggerService = Depends(get_trigger_service)
):
    result = await trigger_service.handle_trigger_async(request)
    if result.is_failure:
        raise ResultException(result.error)
    return result.value