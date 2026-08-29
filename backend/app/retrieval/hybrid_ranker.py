"""
Issue-Aware Hybrid Legal Ranker

Ranking combines:

1. Semantic similarity
2. Keyword matching
3. Metadata relevance
4. Legal-domain relevance
5. Explicit legal-issue relevance
"""

from app.retrieval.keyword_extractor import KeywordExtractor
from app.retrieval.intent_detector import IntentDetector


class HybridRanker:

    def __init__(self):
        self.keyword_extractor = KeywordExtractor()
        self.intent_detector = IntentDetector()

    # ============================================================
    # NORMALIZE
    # ============================================================

    def _normalize(self, text):

        if not text:
            return ""

        return (
            str(text)
            .lower()
            .replace("-", " ")
            .replace("/", " ")
            .replace(",", " ")
            .replace(".", " ")
            .replace("–", " ")
            .replace("—", " ")
            .strip()
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

        section = str(
            metadata.get(
                "section",
                ""
            )
        )

        chapter = str(
            metadata.get(
                "chapter",
                ""
            )
        )

        title = self._normalize(
            metadata.get(
                "title",
                ""
            )
        )

        if intent == "definition":

            if chapter == "CHAPTER I":
                score += 0.20

            if section.startswith("Section 2"):
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

        return min(score, 1.0)

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

        document_domain = self._normalize(
            metadata.get(
                "domain",
                ""
            )
        )

        requested_domain = self._normalize(
            requested_domain
        )

        if document_domain == requested_domain:
            return 1.0

        domain_groups = {

            "consumer protection": [
                "consumer",
                "consumer protection"
            ],

            "cyber it": [
                "cyber",
                "cyber it"
            ],

            "employment labour": [
                "employment",
                "labour",
                "labor"
            ],

            "contract service": [
                "contract"
            ],

            "motor vehicle road accident": [
                "motor",
                "motor vehicle"
            ],

            "insurance financial": [
                "insurance",
                "financial",
                "banking"
            ]
        }

        accepted_domains = []

        for key, values in domain_groups.items():

            if (
                key in requested_domain
                or requested_domain in key
            ):
                accepted_domains = values
                break

        for accepted in accepted_domains:

            if accepted in document_domain:
                return 1.0

        return 0.0

    # ============================================================
    # ISSUE → SECTION HINTS
    # ============================================================

    ISSUE_SECTION_HINTS = {

        "consumer definition": {
            "section 2(7)": 1.0
        },

        "filing complaint": {
            "section 35": 1.0,
            "section 36": 0.30,
            "section 38": 0.30
        },

        "mediation": {
            "section 2(25)": 1.0,
            "section 79": 1.0,
            "section 80": 0.80,
            "section 74": 0.60,
            "section 75": 0.50
        },

        "consumer rights": {
            "section 2": 0.60,
            "section 17": 1.0
        },

        "defective product": {
            "section 39": 1.0,
            "section 2(10)": 0.90,
            "section 84": 0.70,
            "section 85": 0.70,
            "section 86": 0.70,
            "section 83": 0.60,
            "section 82": 0.50
        },

        "upi fraud": {
            "section 43": 1.0,
            "section 66c": 0.50,
            "section 66d": 0.50
        },

        "unauthorized access": {
            "section 43": 1.0,
            "section 65": 0.40
        },

        "identity theft": {
            "section 66c": 1.0
        },

        "online payment fraud": {
            "section 43": 1.0,
            "section 66c": 0.80,
            "section 66d": 0.80
        },

        # --------------------------------------------------------
        # CONTRACT
        # --------------------------------------------------------

        "breach of contract": {
            "section 73": 1.00,
            "section 74": 0.90,
            "section 75": 0.80
        }
    }

    # ============================================================
    # LEGAL ISSUE SCORE
    # ============================================================

    def calculate_legal_issue_score(
        self,
        issue_type,
        metadata,
        document
    ):

        if not issue_type:
            return 0.0

        issue_key = self._normalize(
            issue_type
        )

        section = self._normalize(
            metadata.get(
                "section",
                ""
            )
        )

        title = self._normalize(
            metadata.get(
                "title",
                ""
            )
        )

        document_text = self._normalize(
            document
        )

        searchable_text = (
            title
            + " "
            + section
            + " "
            + document_text
        )

        score = 0.0

        # ========================================================
        # SECTION HINT
        # ========================================================

        section_hints = (
            self.ISSUE_SECTION_HINTS.get(
                issue_key,
                {}
            )
        )

        normalized_section_hints = {

            self._normalize(key):
                value

            for key, value
            in section_hints.items()
        }

        section_hint = (
            normalized_section_hints.get(
                section,
                0.0
            )
        )

        if section_hint > 0:

            score += (
                0.70
                *
                section_hint
            )

        # ========================================================
        # ISSUE KEYWORD MATCH
        # ========================================================

        issue_keywords = (
            self.keyword_extractor
            .get_issue_keywords(
                issue_type
            )
        )

        if issue_keywords:

            matched = 0

            for keyword in issue_keywords:

                normalized_keyword = (
                    self._normalize(
                        keyword
                    )
                )

                if (
                    normalized_keyword
                    in searchable_text
                ):
                    matched += 1

            keyword_ratio = (
                matched
                /
                len(issue_keywords)
            )

            score += (
                0.30
                *
                keyword_ratio
            )

        # ========================================================
        # TITLE MATCH
        # ========================================================

        title_matches = 0

        for keyword in issue_keywords:

            normalized_keyword = (
                self._normalize(
                    keyword
                )
            )

            if (
                normalized_keyword
                in title
            ):
                title_matches += 1

        if title_matches > 0:

            score += min(
                0.20,
                title_matches * 0.05
            )

        return max(
            0.0,
            min(
                score,
                1.0
            )
        )

    # ============================================================
    # RANK
    # ============================================================

    def rank(
        self,
        query,
        results,
        requested_domain=None,
        issue_type=None
    ):

        keywords = (
            self.keyword_extractor.extract(
                query=query,
                domain=requested_domain,
                issue_type=issue_type
            )
        )

        intent = (
            self.intent_detector.detect(
                query
            )
        )

        ranked_results = []

        documents = results.get(
            "documents",
            [[]]
        )[0]

        metadatas = results.get(
            "metadatas",
            [[]]
        )[0]

        distances = results.get(
            "distances",
            [[]]
        )[0]

        for doc, metadata, distance in zip(
            documents,
            metadatas,
            distances
        ):

            # ====================================================
            # SEMANTIC SCORE
            # ====================================================

            semantic_score = (
                1
                /
                (
                    1
                    +
                    distance
                )
            )

            # ====================================================
            # KEYWORD SCORE
            # ====================================================

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

            # ====================================================
            # METADATA SCORE
            # ====================================================

            metadata_score = (
                self.calculate_metadata_score(
                    intent,
                    metadata
                )
            )

            # ====================================================
            # DOMAIN SCORE
            # ====================================================

            domain_score = (
                self.calculate_domain_score(
                    requested_domain,
                    metadata
                )
            )

            # ====================================================
            # LEGAL ISSUE SCORE
            # ====================================================

            legal_issue_score = (
                self.calculate_legal_issue_score(
                    issue_type,
                    metadata,
                    doc
                )
            )

            # ====================================================
            # FINAL SCORE
            # ====================================================

            final_score = (

                0.45
                *
                semantic_score

                +

                0.15
                *
                keyword_score

                +

                0.10
                *
                metadata_score

                +

                0.10
                *
                domain_score

                +

                0.20
                *
                legal_issue_score

            )

            ranked_results.append({

                "document":
                    doc,

                "metadata":
                    metadata,

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

                "legal_issue_score":
                    round(
                        legal_issue_score,
                        3
                    ),

                "final_score":
                    round(
                        final_score,
                        3
                    )
            })

        # ========================================================
        # SORT
        # ========================================================

        ranked_results.sort(
            key=lambda item:
                item["final_score"],
            reverse=True
        )

        return ranked_results