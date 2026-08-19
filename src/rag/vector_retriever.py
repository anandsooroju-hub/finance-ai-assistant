from pathlib import Path

from src.rag.embeddings import create_embedding
from src.rag.similarity import cosine_similarity


DOCUMENTS_PATH = Path("data/documents")


def retrieve_documents(query: str, top_k: int = 3):

    query_vector = create_embedding(query)

    results = []

    for file_path in DOCUMENTS_PATH.glob("*.txt"):

        text = file_path.read_text(encoding="utf-8")

        document_vector = create_embedding(text)

        score = cosine_similarity(
            query_vector,
            document_vector
        )

        results.append({
            "source": file_path.name,
            "content": text,
            "score": float(score)
        })

    results.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return results[:top_k]


if __name__ == "__main__":

    question = "Why did APAC revenue increase in Q2 2026?"

    results = retrieve_documents(question)

    print("\nVECTOR SEARCH RESULTS:")

    for result in results:

        print("\nSource:", result["source"])
        print("Similarity:", result["score"])
        print("Content:")
        print(result["content"])