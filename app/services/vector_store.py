import chromadb #Imports the ChromaDB library so Python can communicate with the vector database


def create_vector_store(): #function responsible for preparing our vector database
    client = chromadb.PersistentClient( #creates a database connection that saves information on my computer.
        path="chroma_db"
    )

    collection = client.get_or_create_collection(
        name="cognivault_documents"
    )

    return collection


def store_embeddings(collection, chunks, vectors):
    ids = [f"chunk_{i}" for i in range(len(chunks))]

    collection.upsert( #inserts new records or updates existing records with the same IDs
    ids=ids,
    documents=chunks,
    embeddings=vectors
)

    return len(ids)


def search_similar_chunks(collection, query_vector, n_results=3):

    results = collection.query(
        query_embeddings=[query_vector],
        n_results=n_results
    )

    return results