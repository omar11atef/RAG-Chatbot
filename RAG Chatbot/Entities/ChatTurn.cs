namespace UniversityRAGChatbot.Domain.Entities;

public class ChatTurn
{
    public string Question { get; set; } = string.Empty;
    public string Answer { get; set; } = string.Empty;
    public List<DocumentSource> Sources { get; set; } = new();
}