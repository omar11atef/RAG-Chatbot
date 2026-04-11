namespace UniversityRAGChatbot.Domain.Errors;

public static class DomainErrorCodes
{
    public const string RAG_SERVICE_UNAVAILABLE = nameof(RAG_SERVICE_UNAVAILABLE);
    public const string RAG_SERVICE_ERROR = nameof(RAG_SERVICE_ERROR);
    public const string INVALID_QUESTION = nameof(INVALID_QUESTION);
    public const string INVALID_API_KEY = nameof(INVALID_API_KEY);
    public const string INGEST_FAILED = nameof(INGEST_FAILED);
    public const string INTERNAL_ERROR = nameof(INTERNAL_ERROR);
}