namespace UniversityRAGChatbot.Infrastructure.HttpClients;

public class RagServiceOptions
{
    public string BaseUrl { get; set; } = string.Empty;
    public string ApiKey { get; set; } = string.Empty;
    public int TimeoutSeconds { get; set; } = 30;
}