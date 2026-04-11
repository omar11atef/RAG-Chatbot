namespace UniversityRAGChatbot.Application.DTOs.Responses;

public class TriggerResponse
{
    public bool Accepted { get; set; }
    public string Message { get; set; } = string.Empty;
}