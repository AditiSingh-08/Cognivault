from app.services.vector_store import create_vector_store

collection = create_vector_store()

print("Total records in ChromaDB:", collection.count())