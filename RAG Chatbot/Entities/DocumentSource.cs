namespace UniversityRAGChatbot.Domain.Entities;

public class DocumentSource
{
    public string FileName { get; set; } = string.Empty;
    public int Page { get; set; }
    public string Snippet { get; set; } = string.Empty;
}