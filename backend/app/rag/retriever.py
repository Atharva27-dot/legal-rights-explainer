"""
Domain-aware and issue-aware semantic legal retriever.

Pipeline:

    User Query
        ↓
    Legal Domain
        ↓
    Specific Legal Issue
        ↓
    Issue-aware Keyword Extraction
        ↓
    Controlled Query Expansion
        ↓
    Embedding
        ↓
    ChromaDB
        ↓
    Top-K Legal Documents
"""

import chromadb

from app.rag.embedder import EmbeddingGenerator
from app.retrieval.keyword_extractor import KeywordExtractor


class LegalRetriever:

    def __init__(self):

        # ========================================================
        # CHROMA DATABASE
        # ========================================================

        self.client = chromadb.PersistentClient(
            path="chroma_db"
        )

        self.collection = self.client.get_collection(
            "legal_documents"
        )

        # ========================================================
        # EMBEDDING MODEL
        # ========================================================

        self.embedder = EmbeddingGenerator()

        # ========================================================
        # ISSUE-AWARE KEYWORD EXTRACTOR
        # ========================================================

        self.keyword_extractor = KeywordExtractor()

    # ============================================================
    # QUERY EXPANSION
    # ============================================================

    def expand_query(
        self,
        query: str,
        domain: str | None = None,
        issue_type: str | None = None
    ):
        """
        Build a controlled legal query.

        Priority:

            Original user query
                ↓
            Issue-specific vocabulary
                ↓
            Limited domain vocabulary

        This prevents broad domain terms from overwhelming
        a specific legal issue.
        """

        # ========================================================
        # ISSUE-AWARE EXPANSION
        # ========================================================

        expanded_query = (
            self.keyword_extractor.expand_query(
                query=query,
                domain=domain,
                issue_type=issue_type
            )
        )

        # ========================================================
        # DISPLAY INFORMATION
        # ========================================================

        print()
        print(
            "=============================="
        )
        print(
            "DOMAIN-AWARE QUERY"
        )
        print(
            "=============================="
        )

        print(
            "Legal Domain:",
            domain or "Not specified"
        )

        print(
            "Specific Legal Issue:",
            issue_type or "Not specified"
        )

        print(
            "Original Query:"
        )

        print(
            query
        )

        print()
        print(
            "Expanded Query:"
        )

        print(
            expanded_query
        )

        return expanded_query

    # ============================================================
    # SEARCH
    # ============================================================

    def search(
        self,
        query,
        top_k=10,
        domain=None,
        issue_type=None
    ):
        """
        Perform domain-aware and issue-aware semantic retrieval.

        Parameters
        ----------
        query:
            User's original legal question.

        top_k:
            Number of documents to retrieve.

        domain:
            Selected legal domain.

        issue_type:
            Selected specific legal issue.

        Returns
        -------
        ChromaDB result dictionary.
        """

        # ========================================================
        # QUERY EXPANSION
        # ========================================================

        expanded_query = self.expand_query(

            query=query,

            domain=domain,

            issue_type=issue_type

        )

        # ========================================================
        # REQUEST INFORMATION
        # ========================================================

        print()
        print(
            "Requested Legal Domain:",
            domain or "Not specified"
        )

        print(
            "Requested Legal Issue:",
            issue_type or "Not specified"
        )

        # ========================================================
        # EMBEDDING
        # ========================================================

        query_embedding = (
            self.embedder.generate_embedding(
                expanded_query
            )
        )

        # ========================================================
        # DOMAIN FILTER
        # ========================================================

        where = None

        if domain:

            where = {
                "domain": domain
            }

        # ========================================================
        # CHROMA SEARCH
        # ========================================================

        try:

            results = self.collection.query(

                query_embeddings=[
                    query_embedding.tolist()
                ],

                n_results=top_k,

                where=where

            )

            # ====================================================
            # DOMAIN FALLBACK
            # ====================================================

            if (
                domain
                and
                (
                    not results.get(
                        "documents"
                    )
                    or
                    not results[
                        "documents"
                    ][0]
                )
            ):

                print()
                print(
                    "No documents found for selected domain."
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

        except Exception as exc:

            print()
            print(
                "Domain-filtered retrieval failed:"
            )

            print(
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

        # ========================================================
        # RETRIEVAL DEBUG INFORMATION
        # ========================================================

        print()
        print(
            "=============================="
        )

        print(
            "SEMANTIC RETRIEVAL"
        )

        print(
            "=============================="
        )

        documents = results.get(
            "documents",
            [[]]
        )

        metadatas = results.get(
            "metadatas",
            [[]]
        )

        distances = results.get(
            "distances",
            [[]]
        )

        if (
            documents
            and
            documents[0]
        ):

            for index, metadata in enumerate(
                metadatas[0]
            ):

                section = metadata.get(
                    "section",
                    "Unknown"
                )

                title = metadata.get(
                    "title",
                    ""
                )

                domain_name = metadata.get(
                    "domain",
                    ""
                )

                distance = None

                if (
                    distances
                    and
                    distances[0]
                    and
                    index < len(
                        distances[0]
                    )
                ):

                    distance = distances[
                        0
                    ][index]

                print()
                print(
                    f"Rank {index + 1}"
                )

                print(
                    "Section:",
                    section
                )

                print(
                    "Title:",
                    title
                )

                print(
                    "Domain:",
                    domain_name
                )

                if distance is not None:

                    print(
                        "Distance:",
                        round(
                            distance,
                            4
                        )
                    )

        else:

            print(
                "No documents retrieved."
            )

        return results