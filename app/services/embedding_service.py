from langchain_huggingface import HuggingFaceEmbeddings


def load_embedding_model():
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    return embeddings

def generate_embeddings(chunks, embeddings):
    vectors = embeddings.embed_documents(chunks)

    return vectors


def generate_query_embedding(question, embeddings):
    query_vector = embeddings.embed_query(question)

    return query_vector
