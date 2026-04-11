using Microsoft.AspNetCore.Http;
using Microsoft.Extensions.Logging;
using System.Text.Json;
using UniversityRAGChatbot.Domain.Errors;

namespace RAG_Chatbot.Middleware;

public class GlobalExceptionMiddleware
{
    private readonly RequestDelegate _next;
    private readonly ILogger<GlobalExceptionMiddleware> _logger;

    public GlobalExceptionMiddleware(RequestDelegate next, ILogger<GlobalExceptionMiddleware> logger)
    {
        _next = next;
        _logger = logger;
    }

    public async Task InvokeAsync(HttpContext context)
    {
        try
        {
            await _next(context);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "An unhandled exception has occurred.");
            await HandleExceptionAsync(context, ex);
        }
    }

    private static Task HandleExceptionAsync(HttpContext context, Exception exception)
    {
        context.Response.ContentType = "application/json";

        var (statusCode, errorCode, message) = exception switch
        {
            AppException appEx => (appEx.StatusCode, appEx.ErrorCode, appEx.Message),
            _ => (StatusCodes.Status500InternalServerError, DomainErrorCodes.INTERNAL_ERROR, "An unexpected internal server error occurred.")
        };

        context.Response.StatusCode = statusCode;
        return context.Response.WriteAsJsonAsync(new { errorCode, message, statusCode });
    }
}