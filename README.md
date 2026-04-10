🤖 3. AI / RAG Model README (/ai-service)
🧠 University Chatbot - AI & RAG Pipeline
The "Brain" of the project. This service handles document ingestion, vector storage, and Retrieval-Augmented Generation.

🛠️ Tech Stack
Language: Python 3.10+

Framework: FastAPI

Orchestration: LangChain / LlamaIndex

Vector Database: ChromaDB (Local)

LLM: OpenAI GPT-4o (or HuggingFace local model)

🚀 Features
Document Ingestion: Processes PDFs and Text files into searchable chunks.

Vector Search: Finds relevant university regulations based on semantic meaning.

Context Injection: Feeds retrieved data into the LLM to prevent hallucinations.
