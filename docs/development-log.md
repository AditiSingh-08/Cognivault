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




## Day 2 — Embeddings and Vector Storage

**Objective:** Convert document chunks into numerical vectors and store them for semantic retrieval.

### Implementation
- Integrated Hugging Face embeddings using `all-MiniLM-L6-v2`.
- Generated embeddings for all extracted text chunks.
- Used ChromaDB as a persistent vector database.
- Stored chunk IDs, original text, and their corresponding embeddings.
- Implemented similarity search to retrieve the top 3 relevant chunks.

### Testing Results
- Generated 23 embeddings.
- Each embedding contained 384 dimensions.
- Successfully stored all 23 records in ChromaDB.
- Tested retrieval using a sample question.

### Key Learning
Understood how embeddings represent semantic meaning, how vector databases store them, and how similarity search retrieves relevant document chunks.



## Day 3 — Gemini Integration and Answer Generation

**Objective:** Connect document retrieval with an LLM to generate answers using retrieved context.

### Implementation
- Integrated Google Gemini using `ChatGoogleGenerativeAI`.
- Loaded API credentials and model configuration from the `.env` file.
- Created a `load_llm()` function to initialize the Gemini model.
- Implemented `generate_answer()` to pass the user question and retrieved context to Gemini.
- Connected ChromaDB retrieval with Gemini answer generation.

### Testing Results
- Successfully generated responses through LangChain.
- Retrieved the top 3 relevant chunks from ChromaDB.
- Tested the system with a question about critical incident prioritization.
- Gemini correctly indicated that the retrieved context did not contain enough information to answer.

### Key Learning
Understood how retrieved document context is passed to an LLM, how prompts guide answer generation, and why a RAG system should avoid generating unsupported answers.
