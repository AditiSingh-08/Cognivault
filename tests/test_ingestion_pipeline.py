
from app.services.document_loader import (
    extract_text_from_pdf,
    split_text_into_chunks
)

from app.services.embedding_service import (
    load_embedding_model,
    generate_embeddings,
    generate_query_embedding
)

from app.services.vector_store import (
    create_vector_store,
    store_embeddings,
    search_similar_chunks
)

from app.services.llm_service import (
    load_llm,
    generate_answer
)


# Step 1: Extract PDF pages
pdf_path = "data/fast_api_practice_questions.pdf"
pages = extract_text_from_pdf(pdf_path)

# Step 2: Split pages into chunks
chunks = split_text_into_chunks(pages)
if not chunks:
    raise ValueError(
        "No text could be extracted from this PDF. "
        "Please check whether the PDF is readable or scanned."
    )

# Step 3: Extract text from structured chunks
chunk_texts = [chunk["text"] for chunk in chunks]

# Step 4: Load embedding model
embedding_model = load_embedding_model()

# Step 5: Generate embeddings
vectors = generate_embeddings(chunk_texts, embedding_model)

# Step 6: Create ChromaDB collection
collection = create_vector_store()

# Step 7: Store chunks, embeddings and metadata
total_stored = store_embeddings(collection, chunks, vectors)

print("\n--- INGESTION PIPELINE SUMMARY ---")
print("Total pages:", len(pages))
print("Total chunks:", len(chunks))
print("Total vectors:", len(vectors))
print("Total stored:", total_stored)
print("Records in ChromaDB:", collection.count())


# Step 8: Generate query embedding
question = "What happens when a vehicle is updated in the FleetTrack API?"

query_vector = generate_query_embedding(
    question,
    embedding_model
)

# Step 9: Retrieve relevant chunks
results = search_similar_chunks(
    collection,
    query_vector,
    n_results=5
)

print("\n--- RETRIEVAL SUMMARY ---")

for i, document in enumerate(results["documents"][0], start=1):
    metadata = results["metadatas"][0][i - 1]

    print(f"\n--- Retrieved Chunk {i} ---")
    print(document[:300])
    print("Source metadata:", metadata)


# Step 10: Generate answer using Gemini
llm = load_llm()

context = "\n\n".join(results["documents"][0])

answer = generate_answer(
    llm=llm,
    question=question,
    retrieved_chunks=[
        {
            "text": document,
            "metadata": metadata
        }
        for document, metadata in zip(
            results["documents"][0],
            results["metadatas"][0]
        )
    ]
)
print("\n--- COGNIVAULT ANSWER ---")
print(answer["answer"])

print("\n--- SOURCES ---")

unique_sources = set()

for source in answer["sources"]:
    source_key = (source["source"], source["page"])

    if source_key not in unique_sources:
        unique_sources.add(source_key)
        print(f"{source['source']} | Page {source['page']}")