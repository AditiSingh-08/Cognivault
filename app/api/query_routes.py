
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.embedding_service import (
    load_embedding_model,
    generate_query_embedding
)
from app.services.vector_store import (
    create_vector_store,
    search_similar_chunks
)
from app.services.llm_service import (
    load_llm,
    generate_answer
)

router = APIRouter()


class QuestionRequest(BaseModel):
    question: str


@router.post("/ask")
async def ask_question(request: QuestionRequest):

    question = request.question.strip()

    if not question:
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty"
        )

    # Step 1: Load embedding model
    embeddings = load_embedding_model()

    # Step 2: Convert question into a vector
    query_vector = generate_query_embedding(
        question,
        embeddings
    )

    # Step 3: Connect to ChromaDB
    collection = create_vector_store()

    if collection.count() == 0:
        raise HTTPException(
            status_code=404,
            detail="No documents found. Upload a PDF first."
        )

    # Step 4: Retrieve relevant chunks
    results = search_similar_chunks(
        collection,
        query_vector,
        n_results=min(5, collection.count())
    )

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]

    # Step 5: Prepare context for Gemini
    context = "\n\n".join(documents)

    # Step 6: Generate answer
    llm = load_llm()

    answer = generate_answer(
        llm,
        question,
        context
    )

    # Step 7: Collect source references
    sources = []

    for metadata in metadatas:
        source = {
            "filename": metadata["source"],
            "page": metadata["page"]
        }

        if source not in sources:
            sources.append(source)

    return {
        "question": question,
        "answer": answer,
        "sources": sources
    }
