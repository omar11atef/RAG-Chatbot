from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # App Settings
    app_name: str = "University RAG Chatbot API"
    environment: str = "Development"
    
    # RAG Service Settings
    rag_service_base_url: str = "http://localhost:8000"
    rag_service_api_key: str = "internal-secret-key"

    # API Security
    api_key: str = "my-secure-frontend-key"

    class Config:
        env_file = ".env"

# Singleton instance
settings = Settings()