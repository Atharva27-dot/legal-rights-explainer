"""
Domain-aware semantic legal retriever.

Performs semantic retrieval from ChromaDB and supports
optional legal-domain filtering.
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

    # ============================================================
    # QUERY EXPANSION
    # ============================================================

    def expand_query(self, query: str):

        query_lower = query.lower()

        expanded = query

        if (
            "who is" in query_lower
            or "what is" in query_lower
        ):

            expanded += " definition meaning"

        if "consumer" in query_lower:

            expanded += " consumer definition"

        if "complaint" in query_lower:

            expanded += (
                " file complaint district commission"
            )

        if "appeal" in query_lower:

            expanded += " appeal procedure"

        if "insurance" in query_lower:

            expanded += (
                " insurance claim insurer policy grievance"
            )

        if any(
            word in query_lower
            for word in [
                "cyber",
                "upi",
                "online fraud",
                "phishing",
                "otp"
            ]
        ):

            expanded += (
                " cyber crime electronic transaction "
                "information technology"
            )

        if any(
            word in query_lower
            for word in [
                "accident",
                "vehicle",
                "motor",
                "driving"
            ]
        ):

            expanded += (
                " motor vehicle road accident compensation"
            )

        if any(
            word in query_lower
            for word in [
                "salary",
                "employee",
                "employer",
                "labour",
                "labor",
                "wages"
            ]
        ):

            expanded += (
                " employment labour wages workplace"
            )

        if any(
            word in query_lower
            for word in [
                "contract",
                "agreement",
                "breach"
            ]
        ):

            expanded += (
                " contract agreement breach obligations"
            )

        return expanded

    # ============================================================
    # SEARCH
    # ============================================================

    def search(
        self,
        query,
        top_k=10,
        domain=None
    ):

        expanded_query = self.expand_query(
            query
        )

        print("\nExpanded Query:")
        print(expanded_query)

        if domain:

            print(
                "Requested Legal Domain:",
                domain
            )

        query_embedding = (
            self.embedder.generate_embedding(
                expanded_query
            )
        )

        # --------------------------------------------------------
        # DOMAIN FILTER
        # --------------------------------------------------------

        where = None

        if domain:

            where = {
                "domain": domain
            }

        # --------------------------------------------------------
        # Chroma Search
        # --------------------------------------------------------

        try:

            results = self.collection.query(

                query_embeddings=[
                    query_embedding.tolist()
                ],

                n_results=top_k,

                where=where

            )

            # If domain filtering returns nothing,
            # fall back to normal semantic retrieval.
            if (
                domain
                and (
                    not results.get("documents")
                    or not results["documents"][0]
                )
            ):

                print(
                    "No documents found for domain.",
                    "Falling back to global retrieval."
                )

                results = self.collection.query(

                    query_embeddings=[
                        query_embedding.tolist()
                    ],

                    n_results=top_k

                )

        except Exception as exc:

            print(
                "Domain-filtered retrieval failed:",
                exc
            )

            print(
                "Falling back to global semantic retrieval."
            )

            results = self.collection.query(

                query_embeddings=[
                    query_embedding.tolist()
                ],

                n_results=top_k

            )

        return results