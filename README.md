University Chatbot - n8n Workflows
Automated pipelines to ensure the university data stays fresh and the team is notified of system performance.

🛠️ Tech Stack
Tool: n8n (Self-hosted or Cloud)

Integrations: Google Drive / Local File System, HTTP Request nodes, Slack/Email.

🚀 Workflows Included
Auto-Ingest: Watches a Google Drive folder. When a new PDF is uploaded, it calls the AI Service POST /ingest endpoint.

Low Confidence Alerts: If the LLM returns "I don't know," n8n sends a message to the admin to update the documentation.

Weekly Cleanup: A scheduled trigger to optimize the vector database.

⚙️ Setup & Installation
Import the .json workflow files located in this folder into your n8n instance.

Configure Credentials for:

HTTP Request (API Keys for Backend/AI service).

Google Drive (if using cloud storage).

Activate the workflows.
