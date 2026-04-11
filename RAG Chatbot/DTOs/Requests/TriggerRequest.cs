using System.ComponentModel.DataAnnotations;

namespace UniversityRAGChatbot.Application.DTOs.Requests;

public class TriggerRequest
{
    [Required] public string Trigger { get; set; } = string.Empty;
}