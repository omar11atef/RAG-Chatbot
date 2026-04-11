using System.ComponentModel.DataAnnotations;

namespace UniversityRAGChatbot.Application.DTOs.Requests;

public class ChatRequest
{
    [Required, MaxLength(1000)] public string Question { get; set; } = string.Empty;
}