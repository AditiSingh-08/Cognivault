
from app.services.document_loader import (
    extract_text_from_pdf,
    split_text_into_chunks
)

from app.services.embedding_service import (
    load_embedding_model,
    generate_embeddings
)

pdf_path = "data/sample.pdf"

# Step 1: Extract PDF pages
pages = extract_text_from_pdf(pdf_path)

# Step 2: Split pages into chunks
chunks = split_text_into_chunks(pages)

# Step 3: Display processing summary
total_characters = sum(len(page["text"]) for page in pages)

print("\n--- PDF PROCESSING SUMMARY ---")
print("Total pages:", len(pages))
print("Total characters:", total_characters)
print("Total chunks:", len(chunks))

# Step 4: Display first two chunks with metadata
for index, chunk in enumerate(chunks[:2], start=1):
    print(f"\n--- Chunk {index} ---")
    print("Text:", chunk["text"][:300])
    print("Metadata:", chunk["metadata"])

# Step 5: Load embedding model
embedding_model = load_embedding_model()

# Step 6: Generate embeddings from chunk text
chunk_texts = [chunk["text"] for chunk in chunks]

vectors = generate_embeddings(chunk_texts, embedding_model)

print("\n--- EMBEDDING SUMMARY ---")
print("Total vectors:", len(vectors))
print("Dimensions of first vector:", len(vectors[0]))
print("First 5 values:", vectors[0][:5])
