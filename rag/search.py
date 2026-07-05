import chromadb

from sentence_transformers import (
    SentenceTransformer
)

client = chromadb.PersistentClient(
    path="rag/vector_db"
)

collection = client.get_collection(
    "knowledge"
)

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


def search_knowledge(
    query,
    top_k=3
):

    embedding = model.encode(
        query
    ).tolist()

    result = collection.query(
        query_embeddings=[
            embedding
        ],
        n_results=top_k
    )

    docs = result["documents"][0]

    return "\n\n".join(docs)