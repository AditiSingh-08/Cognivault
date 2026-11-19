
import chromadb


def create_vector_store():
    client = chromadb.PersistentClient(path="chroma_db")

    collection = client.get_or_create_collection(
        name="cognivault_documents"
    )

    return collection


def store_embeddings(collection, chunks, vectors, document_id):
    ids = [
        f"{document_id}_page_{chunk['metadata']['page']}_chunk_{chunk['metadata']['chunk']}"
        for chunk in chunks
    ]

    documents = [chunk["text"] for chunk in chunks]

    metadatas = [
        {**chunk["metadata"], "document_id": document_id}
        for chunk in chunks
    ]

    collection.upsert(
        ids=ids,
        documents=documents,
        embeddings=vectors,
        metadatas=metadatas
    )

    return len(ids)


def search_similar_chunks(
    collection,
    query_vector,
    n_results=5,
    source_filename=None
):
    search_params = {
        "query_embeddings": [query_vector],
        "n_results": n_results
    }

    if source_filename:
        search_params["where"] = {
            "source": source_filename
        }

    return collection.query(**search_params)
