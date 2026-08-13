"""
Domain-aware Hybrid Legal Ranker.

Ranking:

0.50 * Semantic Score
0.25 * Keyword Score
0.15 * Metadata Score
0.10 * Domain Score
"""

from app.retrieval.keyword_extractor import KeywordExtractor
from app.retrieval.intent_detector import IntentDetector


class HybridRanker:

    def __init__(self):

        self.keyword_extractor = (
            KeywordExtractor()
        )

        self.intent_detector = (
            IntentDetector()
        )

    # ============================================================
    # METADATA SCORE
    # ============================================================

    def calculate_metadata_score(
        self,
        intent,
        metadata
    ):

        score = 0.0

        section = metadata.get(
            "section",
            ""
        )

        chapter = metadata.get(
            "chapter",
            ""
        )

        title = metadata.get(
            "title",
            ""
        ).lower()

        if intent == "definition":

            if chapter == "CHAPTER I":

                score += 0.20

            if section.startswith(
                "Section 2"
            ):

                score += 0.40

            if "definition" in title:

                score += 0.20

            if (
                "unless the context otherwise requires"
                in title
            ):

                score += 0.20

        elif intent == "complaint":

            if "complaint" in title:

                score += 0.40

            if "district commission" in title:

                score += 0.20

        elif intent == "appeal":

            if "appeal" in title:

                score += 0.50

        return min(
            score,
            1.0
        )

    # ============================================================
    # DOMAIN SCORE
    # ============================================================

    def calculate_domain_score(
        self,
        requested_domain,
        metadata
    ):

        if not requested_domain:

            return 0.0

        document_domain = str(
            metadata.get(
                "domain",
                ""
            )
        ).lower()

        requested_domain = str(
            requested_domain
        ).lower()

        # Exact match
        if document_domain == requested_domain:

            return 1.0

        # Flexible matching
        domain_groups = {

            "consumer goods": [
                "consumer",
                "consumer protection"
            ],

            "consumer service": [
                "consumer",
                "consumer protection"
            ],

            "cyber / online fraud": [
                "cyber",
                "cyber / it"
            ],

            "insurance / financial service": [
                "insurance",
                "financial",
                "banking"
            ],

            "motor vehicle / road accident": [
                "motor",
                "motor vehicle"
            ],

            "employment / labour": [
                "employment",
                "labour"
            ],

            "contract / service dispute": [
                "contract"
            ]
        }

        accepted_domains = domain_groups.get(
            requested_domain,
            []
        )

        for accepted in accepted_domains:

            if accepted in document_domain:

                return 1.0

        return 0.0

    # ============================================================
    # RANK
    # ============================================================

    def rank(
        self,
        query,
        results,
        requested_domain=None
    ):

        keywords = (
            self.keyword_extractor.extract(
                query
            )
        )

        intent = (
            self.intent_detector.detect(
                query
            )
        )

        ranked_results = []

        documents = (
            results["documents"][0]
        )

        metadatas = (
            results["metadatas"][0]
        )

        distances = (
            results["distances"][0]
        )

        for doc, metadata, distance in zip(
            documents,
            metadatas,
            distances
        ):

            # ----------------------------------------------------
            # Semantic Score
            # ----------------------------------------------------

            semantic_score = (
                1 / (1 + distance)
            )

            # ----------------------------------------------------
            # Keyword Score
            # ----------------------------------------------------

            doc_lower = doc.lower()

            keyword_matches = sum(

                1

                for word in keywords

                if word.lower() in doc_lower

            )

            keyword_score = (

                keyword_matches
                /
                max(
                    len(keywords),
                    1
                )

            )

            # ----------------------------------------------------
            # Metadata Score
            # ----------------------------------------------------

            metadata_score = (
                self.calculate_metadata_score(
                    intent,
                    metadata
                )
            )

            # ----------------------------------------------------
            # Domain Score
            # ----------------------------------------------------

            domain_score = (
                self.calculate_domain_score(
                    requested_domain,
                    metadata
                )
            )

            # ----------------------------------------------------
            # Final Score
            # ----------------------------------------------------

            final_score = (

                (0.50 * semantic_score)

                +

                (0.25 * keyword_score)

                +

                (0.15 * metadata_score)

                +

                (0.10 * domain_score)

            )

            ranked_results.append({

                "document": doc,

                "metadata": metadata,

                "semantic_score":
                    round(
                        semantic_score,
                        3
                    ),

                "keyword_score":
                    round(
                        keyword_score,
                        3
                    ),

                "metadata_score":
                    round(
                        metadata_score,
                        3
                    ),

                "domain_score":
                    round(
                        domain_score,
                        3
                    ),

                "final_score":
                    round(
                        final_score,
                        3
                    )

            })

        ranked_results.sort(

            key=lambda x:
                x["final_score"],

            reverse=True

        )

        return ranked_results