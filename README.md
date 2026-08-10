# 🏢 Enterprise Q&A System

An end-to-end **Enterprise Question Answering System** built using **Retrieval-Augmented Generation (RAG)**.

The system allows users to upload enterprise PDF documents, process and index them using embeddings, store the embeddings in **PostgreSQL with pgvector**, retrieve the most relevant document chunks for a user question, and generate an answer using **Google Gemini** with document and page-level citations.

---

## 📌 Overview

Searching through large enterprise policy documents manually can be time-consuming.

This project provides an AI-powered question-answering system where users can:

- Upload enterprise PDF documents
- Automatically process and index documents
- Ask questions in natural language
- Retrieve relevant document content using semantic search
- Generate answers using an LLM
- View the source document and page used for the answer
- Continue asking questions in a chat-style interface

The system is designed with a layered architecture separating the:

- Frontend
- API layer
- Business services
- RAG components
- Database
- LLM

---

# 🏗️ System Architecture

```text
                         ┌─────────────────────────┐
                         │       Streamlit         │
                         │        Frontend         │
                         └────────────┬────────────┘
                                      │
                                      │ HTTP
                                      ▼
                         ┌─────────────────────────┐
                         │        FastAPI          │
                         │        API Layer        │
                         └────────────┬────────────┘
                                      │
                    ┌─────────────────┴─────────────────┐
                    │                                   │
                    ▼                                   ▼
             Document Upload                       User Query
                    │                                   │
                    ▼                                   ▼
             IndexingService                         QueryService
                    │                                   │
                    ▼                                   ▼
             DocumentLoader                     Query Embedding
                    │                                   │
                    ▼                                   ▼
             DocumentSplitter                   Similarity Search
                    │                                   │
                    ▼                                   ▼
             EmbeddingModel                      Relevant Chunks
                    │                                   │
                    └─────────────────┬─────────────────┘
                                      │
                                      ▼
                           PostgreSQL + pgvector
                                      │
                                      ▼
                                Google Gemini
                                      │
                                      ▼
                             Answer + Citations
