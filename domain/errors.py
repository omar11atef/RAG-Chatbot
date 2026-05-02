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

class SessionErrors:
    NotFound = Error(
        code="Session.NotFound",
        description="The specified session does not exist.",
        status_code=404
    )
    LimitReached = Error(
        code="Session.LimitReached",
        description="This session has reached its 10-message limit. Please start a new session.",
        status_code=429
    )