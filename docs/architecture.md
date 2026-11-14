# Cognivault — System Architecture

## Overview

Cognivault follows a Retrieval-Augmented Generation (RAG) architecture. It retrieves relevant information from PDF documents and passes that information to Gemini to generate answers.

## 1. Document Ingestion

This stage processes the PDF and prepares it for retrieval.

1. **PDF Extraction:** PyPDF extracts text from each page.
2. **Text Chunking:** LangChain splits the extracted text into smaller chunks.
3. **Embedding Generation:** Hugging Face converts each chunk into a numerical vector.
4. **Vector Storage:** ChromaDB stores the text chunks and their embeddings.

## 2. Question Answering

This stage retrieves information and generates an answer.

1. **User Query:** The user submits a question.
2. **Query Embedding:** The same embedding model converts the question into a vector.
3. **Similarity Search:** ChromaDB finds the three most relevant chunks.
4. **Context Preparation:** The retrieved text is combined into context.
5. **Answer Generation:** Gemini receives the question and context and generates an answer.

## Architecture Flow

### Ingestion Pipeline

```text
PDF Document
     |
     v
Text Extraction (PyPDF)
     |
     v
Text Chunking (LangChain)
     |
     v
Embedding Generation (Hugging Face)
     |
     v
Vector Storage (ChromaDB)
```

### Retrieval and Generation Pipeline

```text
User Question
     |
     v
Query Embedding
     |
     v
Similarity Search (ChromaDB)
     |
     v
Top 3 Relevant Chunks
     |
     v
Context + User Question
     |
     v
Gemini (LLM)
     |
     v
Generated Answer
```

## Technologies and Responsibilities

| Technology | Responsibility |
|---|---|
| PyPDF | Extracts PDF text |
| LangChain | Splits text and integrates the LLM |
| Hugging Face | Generates embeddings |
| ChromaDB | Stores and retrieves vectors |
| Google Gemini | Generates context-based answers |

## Current Implementation

The ingestion, embedding, vector storage, retrieval, and Gemini answer-generation stages have been implemented and tested.

Source citations, API endpoints, and the user interface are planned improvements.
