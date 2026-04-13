from fastapi import APIRouter, Depends
from application.contracts import ChatRequest, ChatResponse, TriggerRequest, TriggerResponse
from application.services import IChatService, ITriggerService
from api.dependencies import get_chat_service, get_trigger_service
from domain.abstractions import ResultException

# Chat Controller
chat_router = APIRouter(prefix="/chat", tags=["Chat"])

@chat_router.post("", response_model=ChatResponse)
async def ask(
    request: ChatRequest, 
    chat_service: IChatService = Depends(get_chat_service)
):
    result = await chat_service.ask_async(request)
    
    # Check Call Result Pattern
    if result.is_failure:
        # Raising this triggers the global ProblemDetails handler in main.py
        raise ResultException(result.error) 
        
    return result.value

# Trigger Controller
trigger_router = APIRouter(prefix="/api/trigger", tags=["Trigger"])

@trigger_router.post("", response_model=TriggerResponse)
async def handle_trigger(
    request: TriggerRequest, 
    trigger_service: ITriggerService = Depends(get_trigger_service)
):
    result = await trigger_service.handle_trigger_async(request)
    
    if result.is_failure:
        raise ResultException(result.error)
        
    return result.value