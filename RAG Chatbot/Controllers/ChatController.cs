using Microsoft.AspNetCore.Mvc;
using UniversityRAGChatbot.Application.Contracts;
using UniversityRAGChatbot.Application.DTOs.Requests;

namespace RAG_Chatbot.Controllers;

[ApiController]
[Route("api/[controller]")]
public class ChatController : ControllerBase
{
    private readonly IChatService _chatService;

    public ChatController(IChatService chatService)
    {
        _chatService = chatService;
    }

    [HttpPost]
    public async Task<IActionResult> Post([FromBody] ChatRequest request) => 
        Ok(await _chatService.AskAsync(request));
}