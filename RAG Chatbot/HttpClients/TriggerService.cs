using UniversityRAGChatbot.Application.Contracts;
using UniversityRAGChatbot.Application.DTOs.Requests;
using UniversityRAGChatbot.Application.DTOs.Responses;
using UniversityRAGChatbot.Domain.Errors;

namespace UniversityRAGChatbot.Application.Services;

public class TriggerService : ITriggerService
{
    private readonly IRagServiceClient _ragServiceClient;

    public TriggerService(IRagServiceClient ragServiceClient)
    {
        _ragServiceClient = ragServiceClient;
    }

    public async Task<TriggerResponse> HandleAsync(TriggerRequest request)
    {
        var success = await _ragServiceClient.IngestAsync();

        if (!success)
        {
            throw new AppException(DomainErrorCodes.INGEST_FAILED, "Failed to re-ingest documents on the RAG service.", 500);
        }

        return new TriggerResponse { Accepted = true, Message = "Re-ingestion triggered successfully." };
    }
}