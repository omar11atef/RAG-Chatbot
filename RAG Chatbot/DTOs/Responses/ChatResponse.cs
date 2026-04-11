namespace UniversityRAGChatbot.Application.DTOs.Responses;

public class ChatResponse
{
    public string Answer { get; set; } = string.Empty;
    public List<SourceDto> Sources { get; set; } = new();
}