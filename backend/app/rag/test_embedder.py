from app.rag.embedder import EmbeddingGenerator

embedder = EmbeddingGenerator()

text = """
Consumer has the right to replacement
of defective goods.
"""

embedding = embedder.generate_embedding(text)

print("Embedding Length:", len(embedding))

print()

print(embedding[:20])