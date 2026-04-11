namespace UniversityRAGChatbot.Domain.Entities;

public class ChatSession
{
    public Guid SessionId { get; set; } = Guid.NewGuid();
    public DateTime Timestamp { get; set; } = DateTime.UtcNow;
    
    private readonly List<ChatTurn> _turns = new();
    public IReadOnlyCollection<ChatTurn> Turns => _turns.AsReadOnly();
    
    public void AddTurn(ChatTurn turn) => _turns.Add(turn);
}