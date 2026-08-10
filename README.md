# 🏢 Enterprise Q&A System

An enterprise document question-answering system built using **Retrieval-Augmented Generation (RAG)**.

The system allows users to upload enterprise PDF documents, stores their embeddings in **PostgreSQL with pgvector**, retrieves the most relevant document chunks for a user query, and generates an answer using **Google Gemini** with source citations.

---

## 🚀 Overview

The Enterprise Q&A System is designed to answer questions from enterprise documents without requiring users to manually search through large PDF files.

The system follows a complete RAG pipeline:

```text
                  PDF Document
                       │
                       ▼
                Document Loader
                       │
                       ▼
                 SHA-256 Hash
                       │
                       ▼
               Duplicate Check
                       │
                       ▼
                Text Chunking
                       │
                       ▼
                  Embeddings
                       │
                       ▼
             PostgreSQL + pgvector
                       │
                       │
                  User Query
                       │
                       ▼
                Query Embedding
                       │
                       ▼
             Similarity Search
                       │
                       ▼
               Relevant Chunks
                       │
                       ▼
                 Google Gemini
                       │
                       ▼
                Generated Answer
                       │
                       ▼
              Source Citations
