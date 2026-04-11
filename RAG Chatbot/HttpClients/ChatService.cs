using Mapster;
using UniversityRAGChatbot.Application.Contracts;
using UniversityRAGChatbot.Application.DTOs.Requests;
using UniversityRAGChatbot.Application.DTOs.Responses;

namespace UniversityRAGChatbot.Application.Services;

public class ChatService : IChatService
{
    private readonly IRagServiceClient _ragServiceClient;

    public ChatService(IRagServiceClient ragServiceClient)
    {
        _ragServiceClient = ragServiceClient;
    }

    public async Task<ChatResponse> AskAsync(ChatRequest request)
    {
        var ragResult = await _ragServiceClient.QueryAsync(request.Question);
        return ragResult.Adapt<ChatResponse>();
    }
}