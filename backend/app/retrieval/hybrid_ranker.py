"""
hybrid_ranker.py

Metadata-Aware Hybrid Ranker

Ranking Score =
0.60 * Semantic Score +
0.25 * Keyword Score +
0.15 * Metadata Score
"""

from app.retrieval.keyword_extractor import KeywordExtractor
from app.retrieval.intent_detector import IntentDetector


class HybridRanker:

    def __init__(self):
        self.keyword_extractor = KeywordExtractor()
        self.intent_detector = IntentDetector()

    def calculate_metadata_score(self, intent, metadata):
        """
        Gives additional score based on legal metadata.
        """

        score = 0.0

        section = metadata.get("section", "")
        chapter = metadata.get("chapter", "")
        title = metadata.get("title", "").lower()

        if intent == "definition":

            # Definitions are generally found in Chapter I
            if chapter == "CHAPTER I":
                score += 0.20

            # Most Acts define terms in Section 2
            if section.startswith("Section 2"):
                score += 0.40

            if "definition" in title:
                score += 0.20

            if "unless the context otherwise requires" in title:
                score += 0.20

        elif intent == "complaint":

            if "complaint" in title:
                score += 0.40

            if "district commission" in title:
                score += 0.20

        elif intent == "appeal":

            if "appeal" in title:
                score += 0.50

        return min(score, 1.0)

    def rank(self, query, results):

        keywords = self.keyword_extractor.extract(query)
        intent = self.intent_detector.detect(query)

        ranked_results = []

        documents = results["documents"][0]
        metadatas = results["metadatas"][0]
        distances = results["distances"][0]

        for doc, metadata, distance in zip(documents, metadatas, distances):

            # -------------------------
            # Semantic Score
            # -------------------------
            semantic_score = 1 / (1 + distance)

            # -------------------------
            # Keyword Score
            # -------------------------
            doc_lower = doc.lower()

            keyword_matches = sum(
                1
                for word in keywords
                if word.lower() in doc_lower
            )

            keyword_score = (
                keyword_matches / max(len(keywords), 1)
            )

            # -------------------------
            # Metadata Score
            # -------------------------
            metadata_score = self.calculate_metadata_score(
                intent,
                metadata
            )

            # -------------------------
            # Final Weighted Score
            # -------------------------
            final_score = (
                (0.60 * semantic_score) +
                (0.25 * keyword_score) +
                (0.15 * metadata_score)
            )

            ranked_results.append({

                "document": doc,

                "metadata": metadata,

                "semantic_score": round(semantic_score, 3),

                "keyword_score": round(keyword_score, 3),

                "metadata_score": round(metadata_score, 3),

                "final_score": round(final_score, 3)

            })

        ranked_results.sort(
            key=lambda x: x["final_score"],
            reverse=True
        )

        return ranked_results