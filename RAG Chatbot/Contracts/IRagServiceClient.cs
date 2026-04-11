using UniversityRAGChatbot.Application.Models;

namespace UniversityRAGChatbot.Application.Contracts;

public interface IRagServiceClient
{
    Task<RagQueryResult> QueryAsync(string question);
    Task<bool> IngestAsync();
}