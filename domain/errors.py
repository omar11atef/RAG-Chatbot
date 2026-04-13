from domain.abstractions import Error

class ChatErrors:
    RagServiceUnavailable = Error(
        code="Chat.RagServiceUnavailable", 
        description="The AI service is currently unreachable.", 
        status_code=503
    )
    InvalidQuestion = Error(
        code="Chat.InvalidQuestion", 
        description="The submitted question is empty or invalid.", 
        status_code=400
    )

class TriggerErrors:
    IngestFailed = Error(
        code="Trigger.IngestFailed", 
        description="The RAG service failed to re-ingest the documents.", 
        status_code=500
    )
    InvalidTriggerType = Error(
        code="Trigger.InvalidTriggerType", 
        description="The trigger type must be 'manual', 'scheduled', or 'document_added'.", 
        status_code=400
    )