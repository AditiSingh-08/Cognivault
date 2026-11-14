# Cognivault Development Log

## Day 1 — PDF Extraction and Text Chunking

**Objective:** Build the first stage of the document ingestion pipeline.

### Implementation
- Used PyPDF to extract text from PDF documents.
- Processed the PDF page by page.
- Used LangChain's `RecursiveCharacterTextSplitter` to divide extracted text into smaller chunks.
- Configured a chunk size of 500 characters and an overlap of 50 characters.

### Testing Results
- Extracted approximately 9,972 characters from the sample PDF.
- Generated 23 text chunks.
- Verified the extraction and chunking process using a test script.

### Key Learning
Understood how PDF text extraction and chunking prepare documents for the embedding and retrieval stages of a RAG pipeline.
