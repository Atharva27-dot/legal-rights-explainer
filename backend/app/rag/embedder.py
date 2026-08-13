"""
embedder.py

Generates embeddings for legal text chunks.
Optimized Version
"""

from sentence_transformers import SentenceTransformer


class EmbeddingGenerator:

    _model = None

    def __init__(self):

        if EmbeddingGenerator._model is None:

            print("Loading embedding model...")

            EmbeddingGenerator._model = SentenceTransformer(
                "all-MiniLM-L6-v2"
            )

            print("Embedding model loaded.")

        self.model = EmbeddingGenerator._model

    def generate_embedding(self, text):

        return self.model.encode(
            text,
            normalize_embeddings=True
        )

    def generate_embeddings(self, texts):

        return self.model.encode(
            texts,
            normalize_embeddings=True
        )