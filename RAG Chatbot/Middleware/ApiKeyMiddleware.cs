using Microsoft.AspNetCore.Http;
using Microsoft.Extensions.Configuration;
using UniversityRAGChatbot.Domain.Errors;

namespace RAG_Chatbot.Middleware;

public class ApiKeyMiddleware
{
    private readonly RequestDelegate _next;
    private const string ApiKeyHeaderName = "X-API-Key";

    public ApiKeyMiddleware(RequestDelegate next)
    {
        _next = next;
    }

    public async Task InvokeAsync(HttpContext context, IConfiguration config)
    {
        if (!context.Request.Headers.TryGetValue(ApiKeyHeaderName, out var extractedApiKey))
            throw new AppException(DomainErrorCodes.INVALID_API_KEY, "API Key was not provided.", 401);

        var allowedKeys = config.GetSection("ApiKeySecurity:AllowedKeys").Get<string[]>() ?? Array.Empty<string>();
        if (!allowedKeys.Contains(extractedApiKey.ToString()))
            throw new AppException(DomainErrorCodes.INVALID_API_KEY, "Unauthorized client.", 401);

        await _next(context);
    }
}