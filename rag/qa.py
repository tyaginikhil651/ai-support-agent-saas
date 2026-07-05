from rag.retriever import retrieve

from llm import ask_llm


def answer_question(question):

    docs = retrieve(question)

    context = "\n\n".join(docs)

    prompt = f"""
You are a customer support agent.

Answer ONLY from the provided context.

If answer not found,
say:
"I couldn't find that information."

Context:
{context}

Question:
{question}
"""

    return ask_llm(prompt)