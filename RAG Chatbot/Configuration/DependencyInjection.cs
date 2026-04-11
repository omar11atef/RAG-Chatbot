using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Options;
using UniversityRAGChatbot.Application.Contracts;
using UniversityRAGChatbot.Infrastructure.HttpClients;

namespace UniversityRAGChatbot.Infrastructure.Configuration;

public static class DependencyInjection
{
    public static IServiceCollection AddInfrastructure(this IServiceCollection services, IConfiguration config)
    {
        services.Configure<RagServiceOptions>(config.GetSection("RagService"));

        services.AddHttpClient<IRagServiceClient, RagServiceClient>((serviceProvider, client) =>
        {
            var options = serviceProvider.GetRequiredService<IOptions<RagServiceOptions>>().Value;
            
            client.BaseAddress = new Uri(options.BaseUrl);
            client.Timeout = TimeSpan.FromSeconds(options.TimeoutSeconds);
            
            if (!string.IsNullOrEmpty(options.ApiKey))
                client.DefaultRequestHeaders.Add("X-API-Key", options.ApiKey);
        });

        return services;
    }
}