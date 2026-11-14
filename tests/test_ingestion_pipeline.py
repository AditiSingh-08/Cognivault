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


from app.services.llm_service import load_llm, generate_answer

# Extract PDF text
pdf_path = "data/sample.pdf"
extracted_text = extract_text_from_pdf(pdf_path)

# Split text into chunks
chunks = split_text_into_chunks(extracted_text)

#  Load embedding model
embedding_model = load_embedding_model()

# Generate embeddings
vectors = generate_embeddings(chunks, embedding_model)

# Create ChromaDB collection
collection = create_vector_store()

# Store chunks and embeddings
total_stored = store_embeddings(collection, chunks, vectors)

print("\n--- INGESTION PIPELINE SUMMARY ---")
print("Total chunks:", len(chunks))
print("Total vectors:", len(vectors))
print("Total stored:", total_stored)
print("Collection name:", collection.name)

print("Records in ChromaDB:", collection.count())


# Generate a query embedding
question = "How should critical incidents be prioritized?"

query_vector = generate_query_embedding(
    question,
    embedding_model
)

print("\n--- QUERY EMBEDDING SUMMARY ---")
print("Question:", question)
print("Vector dimensions:", len(query_vector))
print("First 5 values:", query_vector[:5])


# Search for relevant document chunks
results = search_similar_chunks(
    collection,
    query_vector,
    n_results=3
)

print("\n--- RETRIEVAL SUMMARY ---")

for i, document in enumerate(results["documents"][0], start=1):
    print(f"\n--- Retrieved Chunk {i} ---")
    print(document[:500])






#  Generate answer using Gemini

llm = load_llm()

context = "\n\n".join(results["documents"][0])

answer = generate_answer(
    llm=llm,
    question=question,
    context=context
)

print("\n--- COGNIVAULT ANSWER ---")
print(answer)