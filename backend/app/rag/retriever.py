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
    # DOMAIN NORMALIZATION
    # ============================================================

    DOMAIN_MAP = {

        # --------------------------------------------------------
        # CONSUMER
        # --------------------------------------------------------

        "consumer protection":
            "Consumer Protection",

        # --------------------------------------------------------
        # CYBER / IT
        # --------------------------------------------------------

        "cyber / it":
            "Cyber / IT",

        "cyber/it":
            "Cyber / IT",

        "cyber it":
            "Cyber / IT",

        # --------------------------------------------------------
        # CONTRACT
        # --------------------------------------------------------

        "contract":
            "Contract",

        "contract / service":
            "Contract",

        "contract/service":
            "Contract",

        "contract service":
            "Contract",

        # --------------------------------------------------------
        # MOTOR VEHICLE
        # --------------------------------------------------------

        "motor vehicle":
            "Motor Vehicle",

        "motor vehicle / road accident":
            "Motor Vehicle",

        "motor vehicle/road accident":
            "Motor Vehicle",

        "motor vehicle road accident":
            "Motor Vehicle",

        # --------------------------------------------------------
        # RTI
        # --------------------------------------------------------

        "right to information":
            "Right to Information",

        "rti":
            "Right to Information",

        # --------------------------------------------------------
        # RERA
        # --------------------------------------------------------

        "real estate / rera":
            "Real Estate / RERA",

        "real estate/rera":
            "Real Estate / RERA",

        "real estate":
            "Real Estate / RERA",

        "rera":
            "Real Estate / RERA",

        # --------------------------------------------------------
        # DOMESTIC VIOLENCE
        # --------------------------------------------------------

        "domestic violence":
            "Domestic Violence",

        # --------------------------------------------------------
        # LEGAL SERVICES
        # --------------------------------------------------------

        "legal services / legal aid":
            "Legal Services / Legal Aid",

        "legal services/legal aid":
            "Legal Services / Legal Aid",

        "legal services":
            "Legal Services / Legal Aid",

        "legal aid":
            "Legal Services / Legal Aid",

        # --------------------------------------------------------
        # CRIMINAL LAW / BNS
        # --------------------------------------------------------

        "criminal law / bns":
            "Criminal Law / BNS",

        "criminal law/bns":
            "Criminal Law / BNS",

        "criminal law":
            "Criminal Law / BNS",

        "bns":
            "Criminal Law / BNS",

        # --------------------------------------------------------
        # INSURANCE
        # --------------------------------------------------------

        "insurance":
            "Insurance",

        "insurance / financial":
            "Insurance",

        # --------------------------------------------------------
        # EMPLOYMENT
        # --------------------------------------------------------

        "employment / labour":
            "Employment / Labour",

        "employment/labour":
            "Employment / Labour",

        "employment":
            "Employment / Labour",

        "labour":
            "Employment / Labour",
    }

    # ============================================================
    # NORMALIZE DOMAIN
    # ============================================================

    def normalize_domain(
        self,
        domain
    ):

        if not domain:

            return None

        domain_key = str(
            domain
        ).strip().lower()

        return self.DOMAIN_MAP.get(
            domain_key,
            str(domain).strip()
        )

    # ============================================================
    # QUERY EXPANSION
    # ============================================================

    def expand_query(
        self,
        query: str
    ):

        query_lower = (
            str(query)
            .lower()
        )

        expanded = str(
            query
        )

        # --------------------------------------------------------
        # GENERAL LEGAL QUERIES
        # --------------------------------------------------------

        if (
            "who is" in query_lower
            or
            "what is" in query_lower
        ):

            expanded += (
                " definition meaning"
            )

        # --------------------------------------------------------
        # CONSUMER
        # --------------------------------------------------------

        if "consumer" in query_lower:

            expanded += (
                " consumer protection "
                "consumer rights "
                "defective goods "
                "deficiency in service "
                "redressal"
            )

        if "defective" in query_lower:

            expanded += (
                " defective product "
                "defect in goods "
                "replacement "
                "refund "
                "compensation "
                "consumer commission"
            )

        if "refund" in query_lower:

            expanded += (
                " refund "
                "return price "
                "consumer complaint"
            )

        if "replacement" in query_lower:

            expanded += (
                " replacement of goods "
                "defective goods "
                "consumer complaint"
            )

        if "complaint" in query_lower:

            expanded += (
                " file complaint "
                "district commission "
                "redressal"
            )

        if "appeal" in query_lower:

            expanded += (
                " appeal procedure "
                "appeal commission"
            )

        # --------------------------------------------------------
        # CYBER / IT
        # --------------------------------------------------------

        if any(
            word in query_lower
            for word in [
                "cyber",
                "unauthorized access",
                "unauthorised access",
                "hacking",
                "computer access",
            ]
        ):

            expanded += """

unauthorized access
unauthorised access
computer resource
computer system
access without permission
damage to computer
Information Technology Act
Section 43
"""

        if any(
            word in query_lower
            for word in [
                "identity theft",
                "stolen identity",
                "stolen credentials",
                "account credentials",
            ]
        ):

            expanded += """

identity theft
fraudulent use of password
electronic signature
unique identification feature
Information Technology Act
Section 66C
"""

        if any(
            word in query_lower
            for word in [
                "cheating",
                "personation",
                "impersonation",
                "fake account",
            ]
        ):

            expanded += """

cheating by personation
personation using computer resource
fraud
electronic communication
Information Technology Act
Section 66D
"""

        if any(
            word in query_lower
            for word in [
                "upi",
                "online payment",
                "payment fraud",
                "online fraud",
            ]
        ):

            expanded += """

UPI fraud
online payment fraud
electronic transaction
computer resource
Information Technology Act
Section 43
"""

        # --------------------------------------------------------
        # MOTOR VEHICLE
        # --------------------------------------------------------

        if any(
            word in query_lower
            for word in [
                "accident",
                "vehicle",
                "motor",
                "driving",
                "licence",
                "license",
            ]
        ):

            expanded += (
                " motor vehicle "
                "road accident "
                "compensation "
                "driver "
                "vehicle liability"
            )

        # --------------------------------------------------------
        # CONTRACT
        # --------------------------------------------------------

        if any(
            word in query_lower
            for word in [
                "contract",
                "agreement",
                "breach",
                "contractual",
                "obligation",
            ]
        ):

            expanded += """

Indian Contract Act 1872
contract
agreement
breach of contract
failure to perform
contractual obligations
compensation
damages
Section 73
Section 74
"""

        # --------------------------------------------------------
        # RTI
        # --------------------------------------------------------

        if any(
            word in query_lower
            for word in [
                "rti",
                "right to information",
                "information denied",
                "information refused",
                "information refusal",
                "public information officer",
                "pio",
            ]
        ):

            expanded += """

Right to Information Act 2005
information denied
refusal of information
Public Information Officer
PIO
appeal
first appeal
second appeal
Information Commission
Section 7
Section 8
Section 9
Section 19
"""

        # --------------------------------------------------------
        # RERA
        # --------------------------------------------------------

        if any(
            word in query_lower
            for word in [
                "rera",
                "builder",
                "real estate",
                "delayed possession",
                "property builder",
            ]
        ):

            expanded += """

Real Estate Regulation and Development Act 2016
RERA
real estate regulatory authority
builder
promoter
delayed possession
complaint
refund
compensation
"""

        # --------------------------------------------------------
        # DOMESTIC VIOLENCE
        # --------------------------------------------------------

        if any(
            word in query_lower
            for word in [
                "domestic violence",
                "protection order",
                "residence order",
                "monetary relief",
                "protection officer",
            ]
        ):

            expanded += """

Protection of Women from Domestic Violence Act 2005
domestic violence
protection order
residence order
monetary relief
protection officer
magistrate
"""

        # --------------------------------------------------------
        # LEGAL AID
        # --------------------------------------------------------

        if any(
            word in query_lower
            for word in [
                "legal aid",
                "free legal aid",
                "legal services",
                "lok adalat",
            ]
        ):

            expanded += """

Legal Services Authorities Act 1987
free legal services
legal aid
Legal Services Authority
Lok Adalat
legal representation
"""

        # --------------------------------------------------------
        # CRIMINAL LAW / BNS
        # --------------------------------------------------------

        if any(
            word in query_lower
            for word in [
                "threat",
                "threatening",
                "intimidation",
                "criminal intimidation",
                "threatened",
                "harm",
                "fear",
                "alarm",
            ]
        ):

            expanded += """

Bharatiya Nyaya Sanhita 2023
criminal intimidation
threat
threatening
injury to person
harm
alarm
Section 351
Section 352
"""

        if any(
            word in query_lower
            for word in [
                "criminal offence",
                "theft",
                "assault",
                "hurt",
                "cheating",
                "sexual offence",
                "defamation",
            ]
        ):

            expanded += """

Bharatiya Nyaya Sanhita 2023
criminal offence
theft
assault
hurt
criminal intimidation
cheating
defamation
"""

        # --------------------------------------------------------
        # EMPLOYMENT
        # --------------------------------------------------------

        if any(
            word in query_lower
            for word in [
                "salary",
                "employee",
                "employer",
                "labour",
                "labor",
                "wages",
            ]
        ):

            expanded += (
                " employment "
                "labour "
                "wages "
                "workplace "
                "employment dispute"
            )

        return expanded

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
        Perform domain-aware semantic retrieval.

        The frontend may use labels such as:
            Contract / Service

        while ChromaDB stores:
            Contract

        Therefore the domain is normalized before applying
        the Chroma metadata filter.
        """

        normalized_domain = (
            self.normalize_domain(
                domain
            )
        )

        expanded_query = (
            self.expand_query(
                query
            )
        )

        print()
        print("=" * 70)
        print("DOMAIN-AWARE RETRIEVAL")
        print("=" * 70)

        print(
            "Original Query:",
            query
        )

        print(
            "Expanded Query:",
            expanded_query
        )

        print(
            "Requested Domain:",
            domain or "Not specified"
        )

        print(
            "Normalized Chroma Domain:",
            normalized_domain or "None"
        )

        print(
            "Issue Type:",
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

        if normalized_domain:

            where = {
                "domain":
                    normalized_domain
            }

        # ========================================================
        # CHROMA RETRIEVAL
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
            # CHECK EMPTY RESULT
            # ====================================================

            documents = results.get(
                "documents",
                [[]]
            )

            if (
                normalized_domain
                and
                (
                    not documents
                    or
                    not documents[0]
                )
            ):

                print(
                    "No documents found for domain:",
                    normalized_domain
                )

                print(
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