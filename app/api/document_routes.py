
import os
from fastapi import APIRouter, UploadFile, File, HTTPException

from app.services.document_loader import (
    extract_text_from_pdf,
    split_text_into_chunks
)

from app.services.embedding_service import (
    load_embedding_model,
    generate_embeddings
)

from app.services.vector_store import (
    create_vector_store,
    store_embeddings
)
router = APIRouter()

# Folder where uploaded PDFs will be stored
UPLOAD_DIR = "data/uploads"

os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):

    # Step 1: Validate file extension
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed"
        )

    # Step 2: Create a safe filename
    filename = os.path.basename(file.filename)
    file_path = os.path.join(UPLOAD_DIR, filename)

    # Step 3: Read uploaded file
    content = await file.read()

    if not content:
        raise HTTPException(
            status_code=400,
            detail="Uploaded PDF is empty"
        )

    # Step 4: Save PDF
    with open(file_path, "wb") as pdf_file:
        pdf_file.write(content)

    # Step 5: Extract text from PDF
    try:
        pages = extract_text_from_pdf(file_path)
        chunks = split_text_into_chunks(pages)
        # Step 7: Load the embedding model
        embeddings = load_embedding_model()

# Step 8: Generate vectors for all text chunks
        chunk_texts = [chunk["text"] for chunk in chunks]
        vectors = generate_embeddings(chunk_texts, embeddings)

        total_vectors = len(vectors)
        # Step 9: Create the ChromaDB collection
        collection = create_vector_store()

        # Step 10: Store chunks, vectors, and metadata
        total_stored = store_embeddings(
            collection,
            chunks,
            vectors
        )
        total_chunks = len(chunks)

        total_pages = len(pages)
        total_characters = sum(
            len(page["text"]) for page in pages
        )

        if total_characters == 0:
            raise HTTPException(
                status_code=422,
                detail="No readable text found in PDF"
            )

    except HTTPException:
        raise

    except Exception as error:
        raise HTTPException(
            status_code=422,
            detail=f"PDF processing failed: {str(error)}"
        )

    # Step 6: Return processing summary
    return {
    "filename": filename,
    "message": "PDF uploaded and processed successfully",
    "total_pages": total_pages,
    "total_characters": total_characters,
    "total_chunks": total_chunks,
    "total_vectors": total_vectors,
    "total_stored": total_stored
}