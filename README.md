# Cognivault

### Intelligent Document Question Answering System using Retrieval-Augmented Generation (RAG)

Cognivault is an AI-powered document question-answering system that allows users to retrieve relevant information from PDF documents and generate context-aware answers using Large Language Models (LLMs).

The project combines semantic search, vector databases, and LLM-based generation to provide answers grounded in document content.



## Problem Statement

Searching through large PDF documents manually takes time. Cognivault uses RAG to find relevant information and generate answers from the uploaded documents.


## Tech Stack

- **Python** – Core programming language
- **PyPDF** – PDF text extraction
- **LangChain** – Text chunking and LLM integration
- **Hugging Face** – Text embeddings
- **ChromaDB** – Vector storage and similarity search
- **Google Gemini** – Answer generation

## Documentation

- [System Architecture](docs/architecture.md) – Overview of the RAG pipeline, components, and data flow.
  
## Features

- Extract text from PDF documents.
- Split text into smaller chunks.
- Generate embeddings using Hugging Face.
- Store and search document vectors using ChromaDB.
- Retrieve relevant chunks based on user questions.
- Generate context-based answers using Gemini.


## How It Works

1. Upload a PDF document.
2. Extract and split its text into chunks.
3. Convert chunks into embeddings.
4. Store embeddings in ChromaDB.
5. Retrieve relevant chunks for a question.
6. Send the retrieved context to Gemini to generate an answer.


## Project Structure

```text
Cognivault/
│
├── app/
│   ├── services/
│   │   ├── document_loader.py
│   │   ├── embedding_service.py
│   │   ├── vector_store.py
│   │   └── llm_service.py
│   └── main.py
│
├── frontend/
├── data/
├── tests/
│   ├── test_document_loader.py
│   ├── test_ingestion_pipeline.py
│   └── test_llm.py
│
├── .env.example
├── .gitignore
└── requirements.txt
```

## Installation

1. Clone the repository:

```bash
git clone https://github.com/AditiSingh-08/Cognivault.git
cd Cognivault
```

2. Create a virtual environment:

```bash
py -3.12 -m venv venv
```

3. Activate it (Windows PowerShell):

```powershell
.\venv\Scripts\Activate.ps1
```

4. Install dependencies:

```bash
pip install -r requirements.txt
```

5. Create a `.env` file and add your Gemini API key:

```env
GOOGLE_API_KEY=your_api_key
GEMINI_MODEL=your_model_name
```

6. Place a PDF inside the `data/` folder.

7. Run the pipeline:

```bash
python -m tests.test_ingestion_pipeline
```


## Development Status

Currently, the core RAG pipeline is implemented and tested.

- [x] PDF text extraction
- [x] Text chunking
- [x] Embedding generation
- [x] Vector storage and retrieval
- [x] Gemini integration
- [x] Context-based answer generation

### Upcoming Work
- [ ] Improve document processing
- [ ] Add source citations
- [ ] Build FastAPI backend
- [ ] Develop Streamlit interface
- [ ] Add evaluation and testing


