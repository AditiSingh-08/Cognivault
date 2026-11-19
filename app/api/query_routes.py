
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
    document_name: str | None = None


@router.post("/ask")
async def ask_question(request: QuestionRequest):

    question = request.question.strip()

    if not question:
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty"
        )

    embeddings = load_embedding_model()

    query_vector = generate_query_embedding(
        question,
        embeddings
    )

    collection = create_vector_store()

    if collection.count() == 0:
        raise HTTPException(
            status_code=404,
            detail="No documents found. Upload a PDF first."
        )
    print("DOCUMENT FILTER RECEIVED:", request.document_name)
    
    results = search_similar_chunks(
        collection,
        query_vector,
        n_results=min(5, collection.count()),
        source_filename=request.document_name
    )

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]

    if not documents:
        raise HTTPException(
            status_code=404,
            detail="No relevant content found in the selected document."
        )

    context = "\n\n".join(documents)

    llm = load_llm()

    answer = generate_answer(
        llm,
        question,
        context
    )

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
