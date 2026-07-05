from pypdf import PdfReader
import chromadb
from sentence_transformers import SentenceTransformer

client = chromadb.PersistentClient(
    path="rag/vector_db"
)

collection = client.get_or_create_collection(
    "support_docs"
)

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


def read_pdf(path):

    reader = PdfReader(path)

    text = ""

    for page in reader.pages:
        extracted = page.extract_text()

        if extracted:
            text += extracted

    return text


def split_text(
    text,
    chunk_size=500
):

    chunks = []

    for i in range(
        0,
        len(text),
        chunk_size
    ):
        chunks.append(
            text[i:i + chunk_size]
        )

    return chunks


def ingest_pdf(path):

    text = read_pdf(path)

    chunks = split_text(text)

    embeddings = model.encode(
        chunks
    ).tolist()

    ids = [
        f"{path}_{i}"
        for i in range(len(chunks))
    ]

    collection.add(
        ids=ids,
        documents=chunks,
        embeddings=embeddings
    )

    print(f"Indexed {path}")


if __name__ == "__main__":

    files = [
        "rag/docs/policy.pdf",
        "rag/docs/pricing.pdf",
        "rag/docs/troubleshooting.pdf"
    ]

    for file in files:
        ingest_pdf(file)

    print("Documents indexed")