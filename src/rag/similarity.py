import numpy as np

from src.rag.embeddings import create_embedding


def cosine_similarity(vector_a, vector_b):

    return np.dot(vector_a, vector_b) / (
        np.linalg.norm(vector_a) *
        np.linalg.norm(vector_b)
    )


question = "Why did APAC revenue increase?"

document = """
The primary drivers of the increase were higher institutional
client activity and increased adoption of core financial products.
"""

question_vector = create_embedding(question)
document_vector = create_embedding(document)

score = cosine_similarity(
    question_vector,
    document_vector
)

print("Question:")
print(question)

print("\nDocument:")
print(document)

print("\nCosine similarity:")
print(score)