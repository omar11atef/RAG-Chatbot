using UniversityRAGChatbot.Application.DTOs.Requests;
using UniversityRAGChatbot.Application.DTOs.Responses;

namespace UniversityRAGChatbot.Application.Contracts;

public interface ITriggerService
{
    Task<TriggerResponse> HandleAsync(TriggerRequest request);
}