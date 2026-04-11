using System.Net.Http.Json;
using System.Text.Json;
using UniversityRAGChatbot.Application.Contracts;
using UniversityRAGChatbot.Application.Models;
using UniversityRAGChatbot.Domain.Errors;

namespace UniversityRAGChatbot.Infrastructure.HttpClients;

public class RagServiceClient : IRagServiceClient
{
    private readonly HttpClient _httpClient;
    private static readonly JsonSerializerOptions JsonOptions = new() { PropertyNamingPolicy = JsonNamingPolicy.CamelCase };

    public RagServiceClient(HttpClient httpClient)
    {
        _httpClient = httpClient;
    }

    public async Task<RagQueryResult> QueryAsync(string question)
    {
        try
        {
            var response = await _httpClient.PostAsJsonAsync("/query", new { question });
            
            if (!response.IsSuccessStatusCode)
                throw new AppException(DomainErrorCodes.RAG_SERVICE_ERROR, "Python service returned a non-2xx response.", 502);
            
            return await response.Content.ReadFromJsonAsync<RagQueryResult>(JsonOptions) 
                   ?? throw new AppException(DomainErrorCodes.RAG_SERVICE_ERROR, "Empty response from AI service.", 502);
        }
        catch (Exception ex) when (ex is HttpRequestException or TaskCanceledException)
        {
            throw new AppException(DomainErrorCodes.RAG_SERVICE_UNAVAILABLE, "The AI service could not be reached. Please try again.", 503);
        }
    }

    public async Task<bool> IngestAsync()
    {
        try
        {
            var response = await _httpClient.PostAsync("/ingest", null);
            return response.IsSuccessStatusCode;
        }
        catch { return false; }
    }
}