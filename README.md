## University Chatbot - .NET Backend Gateway
This service acts as the central orchestrator and API Gateway. It handles requests from the frontend, secures the connection, and communicates with the AI microservice.

### 🛠️ Tech Stack
Framework: .NET 8 (ASP.NET Core Web API)
Communication: HttpClient (Typed Client)
Security: API Key Authentication / CORS

### 🚀 Features
Proxy Logic: Forwards user queries to the Python AI service.

Automation Handler: Endpoints for n8n to trigger backend-specific tasks.

Error Handling: Standardized JSON error responses for the frontend.
