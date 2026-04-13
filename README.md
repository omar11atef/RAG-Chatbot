##🎓 University RAG Chatbot — Project Implementation Plan

###📌 Project Overview
FieldDetailsProject NameUniversity Information RAG ChatbotGoalA chatbot that answers student/client questions about the university (faculties, study systems, regulations, etc.) using Retrieval-Augmented Generation (RAG)ArchitectureRAG Pipeline: Document Ingestion → Vector Store → Retrieval → LLM Answer GenerationScaleSmall university task project🧠 How RAG Works in This Project
User Question
↓
[Query Embedding] ←── AI/ML Person builds this
↓
[Vector Search → Retrieve Relevant Chunks from University Docs]
↓
[Inject Context + Question into LLM Prompt]
↓
[LLM Generates Grounded Answer]
↓
Response to User
