from src.rag.embeddings import create_embedding


text = "APAC revenue increased in Q2 2026."

vector = create_embedding(text)

print("Vector type:", type(vector))
print("Vector dimensions:", len(vector))
print("First 10 values:", vector[:10])