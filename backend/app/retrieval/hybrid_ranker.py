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
    # TEXT NORMALIZATION
    # ============================================================

    def _normalize(
        self,
        text
    ):

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

        document_domain = self._normalize(
            metadata.get(
                "domain",
                ""
            )
        )

        requested_domain = self._normalize(
            requested_domain
        )

        # ========================================================
        # EXACT MATCH
        # ========================================================

        if (
            document_domain
            ==
            requested_domain
        ):

            return 1.0

        # ========================================================
        # DOMAIN GROUPS
        # ========================================================

        domain_groups = {

            "consumer protection": [
                "consumer",
                "consumer protection",
            ],

            "cyber it": [
                "cyber",
                "cyber it",
            ],

            "contract service": [
                "contract",
            ],

            "motor vehicle road accident": [
                "motor",
                "motor vehicle",
            ],

            "right to information": [
                "right to information",
            ],

            "real estate rera": [
                "real estate",
                "rera",
            ],

            "domestic violence": [
                "domestic violence",
            ],

            "legal services legal aid": [
                "legal services",
                "legal aid",
            ],

            "criminal law bns": [
                "criminal law",
                "bns",
            ],

            "employment labour": [
                "employment",
                "labour",
                "labor",
            ],

            "insurance financial": [
                "insurance",
                "financial",
                "banking",
            ],
        }

        accepted_domains = []

        for key, values in domain_groups.items():

            if (
                key in requested_domain
                or
                requested_domain in key
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

        # --------------------------------------------------------
        # CONSUMER
        # --------------------------------------------------------

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

        # --------------------------------------------------------
        # CYBER
        # --------------------------------------------------------

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
            "section 66c": 0.60,
            "section 66d": 0.60

        },

        "cyber crime": {

            "section 43": 0.90,
            "section 66": 0.70,
            "section 66c": 0.60,
            "section 66d": 0.60

        },

        # --------------------------------------------------------
        # CONTRACT
        # --------------------------------------------------------

        "breach of contract": {

            # Section 73 is the strongest target for a general
            # breach-of-contract query.

            "section 73": 1.00,

            # Section 74 is useful supporting material where
            # a contract specifies a penalty or named sum.

            "section 74": 0.75

        },

        "non payment": {

            "section 73": 0.90,
            "section 74": 0.70

        },

        "contractual dispute": {

            "section 73": 0.90,
            "section 74": 0.70

        },

        "service agreement dispute": {

            "section 73": 0.90,
            "section 74": 0.70

        },

        # --------------------------------------------------------
        # MOTOR VEHICLE
        # --------------------------------------------------------

        "driving licence": {

            "section 130": 1.00,
            "section 158": 0.55,
            "section 18": 0.45

        },

        "road accident": {

            "section 166": 1.00,
            "section 165": 0.75

        },

        "traffic dispute": {

            "section 177": 0.80,
            "section 179": 0.70

        },

        "motor insurance claim": {

            "section 146": 0.80,
            "section 147": 1.00,
            "section 149": 0.80

        },

        "vehicle compensation": {

            "section 166": 1.00,
            "section 165": 0.80

        },

        "vehicle registration": {

            "section 39": 1.00,
            "section 41": 0.80

        },

        "permit dispute": {

            "section 66": 1.00,
            "section 86": 0.70

        },

        # --------------------------------------------------------
        # RIGHT TO INFORMATION
        # --------------------------------------------------------

        "request for information": {

            "section 6": 1.00,
            "section 7": 0.95

        },

        "information denied": {

            # Appeal is the primary response to denial/refusal.

            "section 19": 1.00,

            # Section 7 concerns disposal of the request.

            "section 7": 0.75,

            # Section 8 concerns exemptions from disclosure.

            "section 8": 0.60,

            # Section 9 concerns grounds for rejection.

            "section 9": 0.45

        },

        "delay in information": {

            "section 7": 1.00,
            "section 19": 0.95

        },

        "rti appeal": {

            "section 19": 1.00,
            "section 20": 0.90

        },

        "public information officer": {

            "section 5": 1.00,
            "section 7": 0.90

        },

        "exempt information": {

            "section 8": 1.00,
            "section 9": 0.90

        },

        # --------------------------------------------------------
        # RERA
        # --------------------------------------------------------

        "delayed possession": {

            "section 18": 1.00

        },

        "builder dispute": {

            "section 31": 1.00,
            "section 18": 0.90

        },

        "project registration": {

            "section 3": 1.00,
            "section 4": 0.90

        },

        "real estate agent": {

            "section 9": 1.00,
            "section 10": 0.90

        },

        "defective construction": {

            "section 14": 1.00

        },

        "refund from builder": {

            "section 18": 1.00

        },

        "rera complaint": {

            "section 31": 1.00

        },

        # --------------------------------------------------------
        # DOMESTIC VIOLENCE
        # --------------------------------------------------------

        "domestic violence": {

            "section 3": 1.00

        },

        "protection order": {

            "section 18": 1.00

        },

        "residence order": {

            "section 17": 0.90,
            "section 19": 1.00

        },

        "monetary relief": {

            "section 20": 1.00

        },

        "custody order": {

            "section 21": 1.00

        },

        "compensation": {

            "section 22": 1.00

        },

        "protection officer": {

            "section 8": 1.00,
            "section 9": 0.90

        },

        # --------------------------------------------------------
        # LEGAL SERVICES / LEGAL AID
        # --------------------------------------------------------

        "free legal aid": {

            "section 12": 1.00,
            "section 13": 0.80

        },

        "eligibility for legal aid": {

            "section 12": 1.00

        },

        "legal services authority": {

            "section 3": 1.00,
            "section 4": 0.90

        },

        "lok adalat": {

            "section 19": 1.00,
            "section 20": 0.90

        },

        "legal aid application": {

            "section 12": 1.00,
            "section 13": 0.80

        },

        "legal representation": {

            "section 12": 1.00

        },

        # --------------------------------------------------------
        # BNS / CRIMINAL LAW
        # --------------------------------------------------------

        "criminal offence": {

            "section 4": 0.60

        },

        "threat intimidation": {

            "section 351": 1.00,
            "section 352": 0.50,
            "section 353": 0.40

        },

        "theft": {

            "section 303": 1.00

        },

        "assault": {

            "section 115": 0.80

        },

        "cheating": {

            "section 318": 1.00

        },

        "hurt": {

            "section 115": 1.00

        },

        "sexual offence": {

            "section 63": 1.00

        },

        "defamation": {

            "section 356": 1.00

        },
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

        chapter = self._normalize(
            metadata.get(
                "chapter",
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
            + chapter
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

            self._normalize(
                key
            ):
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
        # ISSUE KEYWORDS
        # ========================================================

        try:

            issue_keywords = (
                self.keyword_extractor
                .get_issue_keywords(
                    issue_type
                )
            )

        except Exception:

            issue_keywords = []

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

        try:

            keywords = (
                self.keyword_extractor.extract(
                    query=query,
                    domain=requested_domain,
                    issue_type=issue_type
                )
            )

        except TypeError:

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
            results.get(
                "documents",
                [[]]
            )[0]
        )

        metadatas = (
            results.get(
                "metadatas",
                [[]]
            )[0]
        )

        distances = (
            results.get(
                "distances",
                [[]]
            )[0]
        )

        for doc, metadata, distance in zip(

            documents,
            metadatas,
            distances

        ):

            metadata = (
                metadata or {}
            )

            # ====================================================
            # SEMANTIC SCORE
            # ====================================================

            semantic_score = (

                1.0
                /
                (
                    1.0
                    +
                    float(distance)
                )

            )

            # ====================================================
            # KEYWORD SCORE
            # ====================================================

            doc_lower = str(
                doc
            ).lower()

            keyword_matches = sum(

                1

                for word in keywords

                if str(word).lower()
                in doc_lower

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
            # FINAL HYBRID SCORE
            # ====================================================

            final_score = (

                (0.45 * semantic_score)

                +

                (0.15 * keyword_score)

                +

                (0.10 * metadata_score)

                +

                (0.10 * domain_score)

                +

                (0.20 * legal_issue_score)

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
                item[
                    "final_score"
                ],

            reverse=True

        )

        return ranked_results