import chromadb
from sentence_transformers import SentenceTransformer

client = chromadb.PersistentClient(
    path="rag/vector_db"
)

collection = client.get_collection(
    "support_docs"
)

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


def retrieve(
    query,
    top_k=3
):

    embedding = model.encode(
        query
    ).tolist()

    results = collection.query(
        query_embeddings=[embedding],
        n_results=top_k
    )

    return results["documents"][0]