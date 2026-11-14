
from app.services.document_loader import (
    extract_text_from_pdf,
    split_text_into_chunks
)

from app.services.embedding_service import (
    load_embedding_model,
    generate_embeddings
)

pdf_path = "data/sample.pdf"

# Extract PDF text
extracted_text = extract_text_from_pdf(pdf_path)

# Split text into chunks
chunks = split_text_into_chunks(extracted_text)

# Display summary
print("\n--- PDF PROCESSING SUMMARY ---")
print("Total characters:", len(extracted_text))
print("Total chunks:", len(chunks))
print("Average characters per chunk:",
      round(len(extracted_text) / len(chunks), 2) if chunks else 0)

# Display only the first two chunks
for index, chunk in enumerate(chunks[:2], start=1):
    print(f"\n--- Chunk {index} ---")
    print(chunk[:300])


# Load the embedding model
embedding_model = load_embedding_model()

# Generate embeddings for document chunks
vectors = generate_embeddings(chunks, embedding_model)

print("\n--- EMBEDDING SUMMARY ---")
print("Total vectors:", len(vectors))
print("Dimensions of first vector:", len(vectors[0]))
print("First 5 values:", vectors[0][:5])