from src.llm.ollama_client import ask_llama
from src.rag.vector_retriever import retrieve_documents


def generate_rag_answer(question: str):

    results = retrieve_documents(
        question,
        top_k=3
    )

    if not results:
        return "I could not find relevant information."

    context_parts = []

    for result in results:

        context_parts.append(
            f"Source: {result['source']}\n"
            f"Similarity: {result['score']:.3f}\n"
            f"Content:\n{result['content']}"
        )

    context = "\n\n---\n\n".join(context_parts)

    prompt = f"""
You are an enterprise finance assistant.

Answer the user's question using ONLY the retrieved
enterprise context below.

Do not invent facts.

If the context does not contain enough information
to answer the question, say that the available
information is insufficient.

USER QUESTION:
{question}

RETRIEVED ENTERPRISE CONTEXT:

{context}

ANSWER:
"""

    return ask_llama(prompt)


if __name__ == "__main__":

    question = "Why did APAC revenue increase in Q2 2026?"

    answer = generate_rag_answer(question)

    print("\nRAG ANSWER:")
    print(answer)