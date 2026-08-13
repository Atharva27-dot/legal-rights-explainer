"""
retriever.py

Semantic Retriever with Query Expansion.
"""

import chromadb

from app.rag.embedder import EmbeddingGenerator


class LegalRetriever:

    def __init__(self):

        self.client = chromadb.PersistentClient(
            path="chroma_db"
        )

        self.collection = self.client.get_collection(
            "legal_documents"
        )

        self.embedder = EmbeddingGenerator()

    def expand_query(self, query: str):

        query_lower = query.lower()

        expanded = query

        if "who is" in query_lower or "what is" in query_lower:

            expanded += " definition meaning"

        if "consumer" in query_lower:

            expanded += " consumer definition"

        if "complaint" in query_lower:

            expanded += " file complaint district commission"

        if "appeal" in query_lower:

            expanded += " appeal procedure"

        return expanded

    def search(self, query, top_k=10):

        expanded_query = self.expand_query(query)

        print("\nExpanded Query:")
        print(expanded_query)

        query_embedding = self.embedder.generate_embedding(
            expanded_query
        )

        results = self.collection.query(

            query_embeddings=[query_embedding.tolist()],

            n_results=top_k

        )

        return results