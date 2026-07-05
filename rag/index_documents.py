from rag.ingest import ingest_pdf
import os

folder = "rag/documents"

for file in os.listdir(folder):

    if file.endswith(".pdf"):

        ingest_pdf(
            os.path.join(
                folder,
                file
            )
        )