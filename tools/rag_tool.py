from rag.search import (
    search_knowledge
)


def answer_from_docs(question):

    context = search_knowledge(
        question
    )

    return context