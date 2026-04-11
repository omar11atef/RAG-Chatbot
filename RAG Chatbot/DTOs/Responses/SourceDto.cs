namespace UniversityRAGChatbot.Application.DTOs.Responses;

public class SourceDto
{
    public string FileName { get; set; } = string.Empty;
    public int Page { get; set; }
    public string Snippet { get; set; } = string.Empty;
}