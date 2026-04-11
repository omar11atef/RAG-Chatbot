using Microsoft.AspNetCore.Mvc.Filters;
using Microsoft.AspNetCore.Http;
using UniversityRAGChatbot.Domain.Errors;

namespace RAG_Chatbot.Filters;

public class ValidationFilter : IActionFilter
{
    public void OnActionExecuting(ActionExecutingContext context)
    {
        if (!context.ModelState.IsValid)
        {
            throw new AppException(DomainErrorCodes.INVALID_QUESTION, "Invalid request payload.", StatusCodes.Status400BadRequest);
        }
    }

    public void OnActionExecuted(ActionExecutedContext context) { }
}