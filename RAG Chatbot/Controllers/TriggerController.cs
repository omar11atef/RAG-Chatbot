using Microsoft.AspNetCore.Mvc;
using UniversityRAGChatbot.Application.Contracts;
using UniversityRAGChatbot.Application.DTOs.Requests;

namespace RAG_Chatbot.Controllers;

[ApiController]
[Route("api/[controller]")]
public class TriggerController : ControllerBase
{
    private readonly ITriggerService _triggerService;

    public TriggerController(ITriggerService triggerService)
    {
        _triggerService = triggerService;
    }

    [HttpPost]
    public async Task<IActionResult> Post([FromBody] TriggerRequest request) => 
        Ok(await _triggerService.HandleAsync(request));
}