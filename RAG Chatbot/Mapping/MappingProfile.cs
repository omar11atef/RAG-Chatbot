using Mapster;
using UniversityRAGChatbot.Application.DTOs.Responses;
using UniversityRAGChatbot.Application.Models;

namespace UniversityRAGChatbot.Application.Mapping;

public class MappingProfile : IRegister
{
    public void Register(TypeAdapterConfig config)
    {
        config.NewConfig<RagQueryResult, ChatResponse>()
            .Map(dest => dest.Answer, src => src.Answer)
            .Map(dest => dest.Sources, src => src.Sources);

        config.NewConfig<RagSourceItem, SourceDto>()
            .Map(dest => dest.Snippet, src => src.Snippet)
            .Map(dest => dest.FileName, src => ExtractFileName(src.Source))
            .Map(dest => dest.Page, src => ExtractPage(src.Source));
    }

    private static string ExtractFileName(string source) => source.Split(" - ").FirstOrDefault()?.Trim() ?? "Unknown";
    
    private static int ExtractPage(string source)
    {
        var parts = source.ToLowerInvariant().Split("page");
        if (parts.Length > 1 && int.TryParse(parts[1].Trim(), out int page)) return page;
        return 1;
    }
}