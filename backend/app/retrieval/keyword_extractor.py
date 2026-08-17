"""
Issue-aware keyword extractor for legal queries.

Priority:

1. Original user terms
2. Specific legal issue terms
3. Limited domain terms

When an explicit issue is supplied, issue vocabulary is
preferred over broad domain vocabulary.
"""

import re


class KeywordExtractor:

    # ============================================================
    # STOP WORDS
    # ============================================================

    STOP_WORDS = {
        "the", "is", "a", "an", "to", "of", "and", "or",
        "in", "on", "at", "for", "with", "by", "from",
        "what", "who", "how", "when", "where", "which",
        "can", "could", "should", "would", "may", "might",
        "do", "does", "did", "are", "was", "were", "be",
        "been", "being", "i", "you", "he", "she", "it",
        "we", "they", "this", "that", "these", "those",
        "my", "your", "our", "their", "me", "him", "her",
        "under", "about", "tell", "please"
    }

    # ============================================================
    # DOMAIN VOCABULARY
    # ============================================================

    DOMAIN_KEYWORDS = {

        "Consumer Protection": [
            "consumer",
            "consumer rights",
            "consumer complaint",
            "consumer dispute",
            "defect",
            "deficiency",
            "seller",
            "service provider",
            "product",
            "goods",
            "refund",
            "replacement",
            "compensation",
            "redressal",
            "district commission",
            "state commission",
            "national commission"
        ],

        "Cyber / IT": [
            "cyber crime",
            "cyber offence",
            "computer resource",
            "computer system",
            "electronic transaction",
            "electronic record",
            "digital fraud",
            "online fraud",
            "unauthorized access",
            "unauthorised access",
            "identity theft",
            "electronic authentication",
            "cyber fraud",
            "information technology",
            "information technology act"
        ],

        "Employment / Labour": [
            "employee",
            "employer",
            "employment",
            "salary",
            "wages",
            "termination",
            "dismissal",
            "workplace",
            "labour",
            "labor"
        ],

        "Motor Vehicle": [
            "motor vehicle",
            "vehicle",
            "road accident",
            "traffic accident",
            "motor accident",
            "driver",
            "insurance",
            "compensation",
            "injury",
            "third party"
        ],

        "Property": [
            "property",
            "land",
            "ownership",
            "possession",
            "tenant",
            "landlord",
            "rent",
            "lease",
            "property dispute",
            "transfer",
            "sale deed"
        ],

        "Family Law": [
            "marriage",
            "divorce",
            "maintenance",
            "husband",
            "wife",
            "child",
            "custody",
            "domestic",
            "family",
            "inheritance"
        ]
    }

    # ============================================================
    # ISSUE VOCABULARY
    # ============================================================

    ISSUE_KEYWORDS = {

        "Defective Product": [
            "defect",
            "defective product",
            "defective goods",
            "manufacturing defect",
            "quality",
            "fault",
            "replacement",
            "refund",
            "repair",
            "compensation",
            "product liability"
        ],

        "Filing Complaint": [
            "complainant",
            "consumer complaint",
            "file complaint",
            "filing complaint",
            "district commission",
            "consumer commission",
            "complaint procedure",
            "jurisdiction",
            "redressal"
        ],

        "Mediation": [
            "mediation",
            "mediator",
            "consumer mediation",
            "mediation cell",
            "settlement",
            "dispute resolution",
            "mediation proceedings"
        ],

        "Consumer Definition": [
            "consumer",
            "definition of consumer",
            "consumer definition",
            "buys goods",
            "hires services",
            "consideration"
        ],

        "Consumer Rights": [
            "consumer rights",
            "right to safety",
            "right to information",
            "right to choose",
            "right to be heard",
            "right to redressal",
            "consumer education"
        ],

        "UPI Fraud": [
            "upi",
            "upi fraud",
            "unauthorized upi transaction",
            "unauthorised upi transaction",
            "unauthorized transaction",
            "unauthorised transaction",
            "unauthorized transfer",
            "unauthorised transfer",
            "electronic payment",
            "digital payment",
            "payment fraud",
            "bank account",
            "fraudulent transfer",
            "online financial fraud",
            "cyber fraud"
        ],

        "Unauthorized Access": [
            "unauthorized access",
            "unauthorised access",
            "access without permission",
            "computer resource",
            "computer system",
            "computer network",
            "damage to computer",
            "loss caused by unauthorized access",
            "loss caused by unauthorised access"
        ],

        "Identity Theft": [
            "identity theft",
            "password",
            "login credentials",
            "authentication",
            "electronic signature",
            "digital identity",
            "credential",
            "fraudulent use",
            "dishonest use"
        ],

        "Online Payment Fraud": [
            "online payment",
            "payment fraud",
            "electronic transaction",
            "unauthorized transaction",
            "unauthorised transaction",
            "fraudulent transfer",
            "digital payment",
            "bank account",
            "electronic banking",
            "cyber fraud"
        ]
    }

    # ============================================================
    # BASIC KEYWORDS
    # ============================================================

    def _extract_basic_keywords(
        self,
        query: str
    ):

        words = re.findall(
            r"\b[a-zA-Z0-9]+\b",
            query.lower()
        )

        keywords = []

        for word in words:

            if (
                word not in self.STOP_WORDS
                and len(word) > 2
                and word not in keywords
            ):

                keywords.append(word)

        return keywords

    # ============================================================
    # ISSUE LOOKUP
    # ============================================================

    def get_issue_keywords(
        self,
        issue_type
    ):

        if not issue_type:
            return []

        if issue_type in self.ISSUE_KEYWORDS:

            return self.ISSUE_KEYWORDS[
                issue_type
            ].copy()

        normalized = (
            issue_type.lower().strip()
        )

        for issue, keywords in (
            self.ISSUE_KEYWORDS.items()
        ):

            if issue.lower() == normalized:

                return keywords.copy()

        return []

    # ============================================================
    # DOMAIN LOOKUP
    # ============================================================

    def get_domain_keywords(
        self,
        domain
    ):

        if not domain:
            return []

        if domain in self.DOMAIN_KEYWORDS:

            return self.DOMAIN_KEYWORDS[
                domain
            ].copy()

        normalized = (
            domain.lower().strip()
        )

        for name, keywords in (
            self.DOMAIN_KEYWORDS.items()
        ):

            if name.lower() == normalized:

                return keywords.copy()

        return []

    # ============================================================
    # EXTRACT
    # ============================================================

    def extract(
        self,
        query,
        domain=None,
        issue_type=None
    ):

        basic_keywords = (
            self._extract_basic_keywords(
                query
            )
        )

        issue_keywords = (
            self.get_issue_keywords(
                issue_type
            )
        )

        domain_keywords = (
            self.get_domain_keywords(
                domain
            )
        )

        final_keywords = []

        # Original query
        for keyword in basic_keywords:

            if keyword not in final_keywords:

                final_keywords.append(
                    keyword
                )

        # Issue terms
        for keyword in issue_keywords:

            if keyword not in final_keywords:

                final_keywords.append(
                    keyword
                )

        # Only limited domain vocabulary
        for keyword in domain_keywords[:4]:

            if keyword not in final_keywords:

                final_keywords.append(
                    keyword
                )

        return final_keywords

    # ============================================================
    # QUERY EXPANSION
    # ============================================================

    def expand_query(
        self,
        query,
        domain=None,
        issue_type=None
    ):

        basic_keywords = (
            self._extract_basic_keywords(
                query
            )
        )

        issue_keywords = (
            self.get_issue_keywords(
                issue_type
            )
        )

        domain_keywords = (
            self.get_domain_keywords(
                domain
            )
        )

        expanded = []

        # Original query
        for word in basic_keywords:

            if word not in expanded:

                expanded.append(
                    word
                )

        # Explicit issue
        for word in issue_keywords:

            if word not in expanded:

                expanded.append(
                    word
                )

        # If issue is known, only add 3 domain terms.
        # If issue is unknown, allow 6 domain terms.
        domain_limit = (
            3
            if issue_type
            else 6
        )

        for word in domain_keywords[
            :domain_limit
        ]:

            if word not in expanded:

                expanded.append(
                    word
                )

        return " ".join(
            expanded
        )


keyword_extractor = KeywordExtractor()