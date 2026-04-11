using UniversityRAGChatbot.Application.DTOs.Requests;
using UniversityRAGChatbot.Application.DTOs.Responses;

namespace UniversityRAGChatbot.Application.Contracts;

public interface IChatService
{
    Task<ChatResponse> AskAsync(ChatRequest request);
}