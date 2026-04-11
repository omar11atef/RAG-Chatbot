using Mapster;
using Microsoft.Extensions.DependencyInjection;
using UniversityRAGChatbot.Application.Contracts;
using UniversityRAGChatbot.Application.Mapping;
using UniversityRAGChatbot.Application.Services;

namespace RAG_Chatbot.Extensions;

public static class ServiceCollectionExtensions
{
    public static IServiceCollection AddApplication(this IServiceCollection services)
    {
        services.AddScoped<IChatService, ChatService>();
        services.AddScoped<ITriggerService, TriggerService>();
        
        // Register Mapster profiles globally once
        TypeAdapterConfig.GlobalSettings.Scan(typeof(MappingProfile).Assembly);
        
        return services;
    }
}