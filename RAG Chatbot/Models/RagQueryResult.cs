namespace UniversityRAGChatbot.Application.Models;

public class RagQueryResult
{
    public string Answer { get; set; } = string.Empty;
    public List<RagSourceItem> Sources { get; set; } = new();
}

public class RagSourceItem
{
    // Example: "university_guide.pdf - page 3"
    public string Source { get; set; } = string.Empty; 
    public string Snippet { get; set; } = string.Empty;
}