import time
import re

from app.rag.retriever import LegalRetriever
from app.retrieval.hybrid_ranker import HybridRanker
from app.llm.complaint_prompt import build_complaint_prompt
from app.llm.ollama_service import OllamaService
from app.services.readiness_service import readiness_service


class ComplaintGenerator:

    def __init__(self):

        self.retriever = LegalRetriever()
        self.ranker = HybridRanker()
        self.llm = OllamaService()

    # ============================================================
    # GET ACT FROM RETRIEVED DOCUMENT
    # ============================================================

    def _get_retrieved_act(
        self,
        top_results,
        fallback
    ):

        for item in top_results:

            metadata = item.get(
                "metadata",
                {}
            )

            act = metadata.get("act")

            if act:
                return act

        return fallback

    # ============================================================
    # CLASSIFY LEGAL ISSUE
    # ============================================================

    def classify_legal_issue(
        self,
        request,
        top_results
    ):

        selected_domain = str(
            getattr(
                request,
                "domain",
                ""
            )
        ).strip()

        selected_issue = str(
            getattr(
                request,
                "issue_type",
                ""
            )
        ).strip()

        # ========================================================
        # USER SELECTED CYBER / IT
        # ========================================================

        if "cyber" in selected_domain.lower():

            return {

                "category":
                    "Cyber / IT",

                "issue":
                    selected_issue
                    or
                    "Cyber / IT related dispute",

                "applicable_act":
                    self._get_retrieved_act(
                        top_results,
                        "Information Technology Act, 2000"
                    ),

                "rights": [

                    "Right to seek appropriate redressal",

                    "Right to protection against unauthorized electronic transactions",

                    "Right to preserve and present digital evidence"

                ]
            }

        # ========================================================
        # USER SELECTED CONSUMER PROTECTION
        # ========================================================

        if "consumer" in selected_domain.lower():

            issue = (
                selected_issue
                or
                "Consumer dispute"
            )

            return {

                "category":
                    "Consumer Goods / Services",

                "issue":
                    issue,

                "applicable_act":
                    self._get_retrieved_act(
                        top_results,
                        "Consumer Protection Act, 2019"
                    ),

                "rights": [

                    "Right to Safety",

                    "Right to Information",

                    "Right to Redressal"

                ]
            }

        # ========================================================
        # USER SELECTED EMPLOYMENT / LABOUR
        # ========================================================

        if (
            "employment" in selected_domain.lower()
            or
            "labour" in selected_domain.lower()
            or
            "labor" in selected_domain.lower()
        ):

            return {

                "category":
                    "Employment / Labour",

                "issue":
                    selected_issue
                    or
                    "Employment related dispute",

                "applicable_act":
                    self._get_retrieved_act(
                        top_results,
                        "Applicable employment law"
                    ),

                "rights": [

                    "Right to seek appropriate grievance redressal"

                ]
            }

        # ========================================================
        # USER SELECTED CONTRACT
        # ========================================================

        if "contract" in selected_domain.lower():

            return {

                "category":
                    "Contract / Service",

                "issue":
                    selected_issue
                    or
                    "Contractual dispute",

                "applicable_act":
                    self._get_retrieved_act(
                        top_results,
                        "Applicable contract law"
                    ),

                "rights": [

                    "Right to seek appropriate contractual remedy"

                ]
            }

        # ========================================================
        # USER SELECTED MOTOR VEHICLE
        # ========================================================

        if "motor" in selected_domain.lower():

            return {

                "category":
                    "Motor Vehicle / Road Accident",

                "issue":
                    selected_issue
                    or
                    "Motor vehicle related dispute",

                "applicable_act":
                    self._get_retrieved_act(
                        top_results,
                        "Applicable motor vehicle law"
                    ),

                "rights": [

                    "Right to seek appropriate compensation or redressal"

                ]
            }

        # ========================================================
        # INSURANCE / FINANCIAL
        # ========================================================

        if (
            "insurance" in selected_domain.lower()
            or
            "financial" in selected_domain.lower()
        ):

            return {

                "category":
                    "Insurance / Financial",

                "issue":
                    selected_issue
                    or
                    "Insurance or financial dispute",

                "applicable_act":
                    self._get_retrieved_act(
                        top_results,
                        "Applicable financial or insurance law"
                    ),

                "rights": [

                    "Right to seek grievance redressal",

                    "Right to receive services as agreed"

                ]
            }

        # ========================================================
        # FALLBACK
        # ========================================================

        return {

            "category":
                selected_domain
                or
                "General Legal Issue",

            "issue":
                selected_issue
                or
                "Legal dispute",

            "applicable_act":
                self._get_retrieved_act(
                    top_results,
                    "Not established from the current knowledge base"
                ),

            "rights": []

        }

    # ============================================================
    # SUPPORTING DOCUMENTS
    # ============================================================

    def get_supporting_documents(
        self,
        domain
    ):

        domain_lower = str(
            domain
        ).lower()

        # --------------------------------------------------------
        # CYBER
        # --------------------------------------------------------

        if "cyber" in domain_lower:

            return [

                "Bank statement showing the unauthorized transaction",

                "UPI transaction ID / reference number",

                "Screenshots of the transaction or fraud",

                "SMS / email transaction alerts",

                "Communication with bank or payment provider",

                "Cybercrime complaint acknowledgement, if available"

            ]

        # --------------------------------------------------------
        # CONSUMER
        # --------------------------------------------------------

        if "consumer" in domain_lower:

            return [

                "Purchase Invoice",

                "Warranty Card (if applicable)",

                "Photos / Videos of the product",

                "Communication with Seller / Service Provider",

                "Payment / Order confirmation"

            ]

        # --------------------------------------------------------
        # EMPLOYMENT
        # --------------------------------------------------------

        if (
            "employment" in domain_lower
            or
            "labour" in domain_lower
            or
            "labor" in domain_lower
        ):

            return [

                "Employment / Appointment Letter",

                "Salary Slips",

                "Employment related communication",

                "HR Complaint / Notice",

                "Termination Letter, if applicable"

            ]

        # --------------------------------------------------------
        # CONTRACT
        # --------------------------------------------------------

        if "contract" in domain_lower:

            return [

                "Signed Contract / Agreement",

                "Invoices / Receipts",

                "Payment Records",

                "Communication between parties",

                "Notice / Breach communication"

            ]

        # --------------------------------------------------------
        # MOTOR VEHICLE
        # --------------------------------------------------------

        if "motor" in domain_lower:

            return [

                "Driving Licence",

                "Vehicle Registration",

                "Insurance Documents",

                "Accident Photographs",

                "Police / Accident Report",

                "Medical Documents, if applicable"

            ]

        # --------------------------------------------------------
        # INSURANCE
        # --------------------------------------------------------

        if (
            "insurance" in domain_lower
            or
            "financial" in domain_lower
        ):

            return [

                "Insurance Policy / Agreement",

                "Payment / Premium Records",

                "Claim Documents",

                "Communication with Insurer / Provider",

                "Claim Rejection Letter, if applicable"

            ]

        # --------------------------------------------------------
        # GENERAL
        # --------------------------------------------------------

        return [

            "Identity / Basic Information",

            "Relevant documents",

            "Communication records",

            "Payment or transaction records, if applicable"

        ]


    # ============================================================
    # GROUNDED COMPLAINT VALIDATION
    # ============================================================

    def _allowed_legal_sources(self, top_results):
        """Build the allow-list exclusively from retrieved metadata."""
        acts = set()
        sections = set()

        for item in top_results:
            metadata = item.get("metadata", {}) or {}

            act = str(metadata.get("act") or "").strip()
            section = str(metadata.get("section") or "").strip()

            if act:
                acts.add(act.lower())

            if section:
                sections.add(section.lower())

        return acts, sections

    def _primary_source(self, top_results):
        if not top_results:
            return {}

        return top_results[0].get("metadata", {}) or {}

    def _retrieved_text(self, top_results):
        parts = []

        for item in top_results:
            document = item.get("document")
            if document:
                parts.append(str(document))

            metadata = item.get("metadata", {}) or {}
            for key in ("act", "section", "title", "chapter"):
                value = metadata.get(key)
                if value:
                    parts.append(str(value))

        return "\n".join(parts)

    def _supported_remedies(self, top_results):
        """Return remedies explicitly supported by the highest-ranked provision."""
        if not top_results:
            return []

        primary = top_results[0]
        parts = []

        for key in (
            "document", "text", "content", "page_content",
            "chunk_text", "excerpt", "title"
        ):
            value = primary.get(key)
            if value:
                parts.append(str(value))

        metadata = primary.get("metadata", {}) or {}
        for key in ("title", "section", "act"):
            value = metadata.get(key)
            if value:
                parts.append(str(value))

        text = "\n".join(parts).lower()

        checks = [
            (["remove the defect", "removal of the defect"], "Removal of the defect"),
            (["replace the goods", "replacement of the goods"], "Replacement of the goods"),
            (["return the price", "return of the price", "return the amount"],
             "Return of the price"),
            (["pay compensation", "compensation"], "Compensation"),
            (["pay damages"], "Damages"),
        ]

        return [
            label for phrases, label in checks
            if any(phrase in text for phrase in phrases)
        ]

    def _validate_complaint_grounding(self, complaint, top_results):
        """
        Validate legal authorities in the generated complaint.

        The validator does not try to decide the merits of the case.
        It only checks whether legal authorities/sections introduced by
        the LLM were present in the retrieved evidence.
        """
        allowed_acts, allowed_sections = self._allowed_legal_sources(top_results)
        primary = self._primary_source(top_results)
        retrieved_text = self._retrieved_text(top_results).lower()

        issues = []

        # --------------------------------------------------------
        # Act-name validation
        # --------------------------------------------------------
        known_act_pattern = re.compile(
            r"\b(?:Consumer Protection Act|Information Technology Act|"
            r"Indian Contract Act|Motor Vehicles Act|Insurance Act|"
            r"Code of Civil Procedure|Indian Penal Code|"
            r"Bharatiya Nyaya Sanhita|Bharatiya Nagarik Suraksha Sanhita|"
            r"Bharatiya Sakshya Adhiniyam)\s*,?\s*\d{4}\b",
            flags=re.IGNORECASE,
        )

        cited_acts = {
            match.group(0).strip().lower()
            for match in known_act_pattern.finditer(complaint)
        }

        for cited_act in cited_acts:
            if cited_act not in allowed_acts:
                issues.append(
                    f"Unsupported legal authority: {cited_act}"
                )

        # --------------------------------------------------------
        # Section-number validation
        # --------------------------------------------------------
        cited_sections = {
            match.group(0).strip().lower()
            for match in re.finditer(
                r"\bSection\s+[0-9]+[A-Za-z]*(?:\([0-9A-Za-z]+\))?(?:\([0-9A-Za-z]+\))?",
                complaint,
                flags=re.IGNORECASE,
            )
        }

        for cited_section in cited_sections:
            if cited_section not in allowed_sections:
                issues.append(
                    f"Unsupported legal section: {cited_section}"
                )

        # --------------------------------------------------------
        # Explicit CPC contamination check
        # --------------------------------------------------------
        cpc_terms = [
            "code of civil procedure",
            "civil procedure code",
            "cpc",
        ]

        if any(term in complaint.lower() for term in cpc_terms):
            if not any(term in retrieved_text for term in cpc_terms):
                issues.append(
                    "Unsupported reference to the Code of Civil Procedure."
                )

        # --------------------------------------------------------
        # Old Consumer Protection Act contamination check
        # --------------------------------------------------------
        if (
            "consumer protection act, 1986" in complaint.lower()
            and "consumer protection act, 1986" not in allowed_acts
        ):
            issues.append(
                "Unsupported reference to the Consumer Protection Act, 1986."
            )

        # --------------------------------------------------------
        # Strong legal-conclusion language
        # --------------------------------------------------------
        risky_patterns = [
            r"\bis legally liable\b",
            r"\bis liable under\b",
            r"\bconstitutes a breach of\b",
            r"\bis entitled to\b",
            r"\bhas a guaranteed right\b",
            r"\bmust be ordered to\b",
            r"\bfailed to provide adequate instructions\b",
            r"\bquality standards required by law\b",
            r"\bviolat(?:es|ed)\s+(?:the\s+)?(?:Act|law|rights)\b",
        ]

        for pattern in risky_patterns:
            if re.search(pattern, complaint, flags=re.IGNORECASE):
                issues.append(
                    "The draft contains a potentially unsupported "
                    "categorical legal conclusion."
                )
                break

        # --------------------------------------------------------
        # Ensure relief/prayer is not truncated
        # --------------------------------------------------------
        upper = complaint.upper()

        if "RELIEF / PRAYER" not in upper and "RELIEF" not in upper:
            issues.append("Missing RELIEF / PRAYER section.")

        return {
            "status": "Verified" if not issues else "Needs Review",
            "issues": issues,
            "allowed_acts": sorted(allowed_acts),
            "allowed_sections": sorted(allowed_sections),
            "primary_act": primary.get("act"),
            "primary_section": primary.get("section"),
            "supported_remedies": self._supported_remedies(top_results),
        }

    def _repair_grounding(self, complaint, grounding, request, top_results):
        """
        Conservative repair: remove/neutralize clearly unsupported
        authority claims instead of inventing replacement law.
        """
        if grounding["status"] == "Verified":
            return complaint

        repaired = complaint

        # Remove clearly unsupported CPC wording from the legal-basis sentence.
        repaired = re.sub(
            r"\s*and the relevant provisions of the District Commission's "
            r"powers under Section 39 of the Code of Civil Procedure, 1908\.?",
            "",
            repaired,
            flags=re.IGNORECASE,
        )

        repaired = re.sub(
            r"\bConsumer Protection Act,\s*1986\b",
            lambda _: str(
                grounding.get("primary_act")
                or "the retrieved consumer protection law"
            ),
            repaired,
            flags=re.IGNORECASE,
        )

        # --------------------------------------------------------
        # Replace the GROUNDS section when unsupported legal
        # conclusions are detected. This is safer than trying to
        # surgically rewrite arbitrary LLM prose.
        # --------------------------------------------------------
        grounds_match = re.search(
            r"(?is)\bGROUNDS\b\s*(.*?)(?=\n(?:RELIEF\s*/\s*PRAYER|DOCUMENTS|DECLARATION|LEGAL SOURCES)\b|\Z)",
            repaired,
        )

        if grounds_match:
            grounds_text = grounds_match.group(1)

            unsupported_grounding_language = [
                r"\bconstitutes\s+a\s+breach\b",
                r"\bis\s+legally\s+liable\b",
                r"\bis\s+liable\s+under\b",
                r"\bis\s+entitled\s+to\b",
                r"\bmust\s+be\s+ordered\s+to\b",
                r"\bfailed\s+to\s+provide\s+adequate\s+instructions\b",
                r"\bquality\s+standards\s+required\s+by\s+law\b",
                r"\bviolat(?:es|ed)\s+(?:the\s+)?(?:Act|law|rights)\b",
            ]

            if any(
                re.search(pattern, grounds_text, flags=re.IGNORECASE)
                for pattern in unsupported_grounding_language
            ):
                primary_act = str(
                    grounding.get("primary_act")
                    or "the retrieved legal provision"
                )
                primary_section = str(
                    grounding.get("primary_section")
                    or ""
                )

                repaired_grounds = (
                    "GROUNDS\n\n"
                    "1. The Complainant states that the mobile phone stopped "
                    "working after five days.\n\n"
                    "2. The Complainant states that the seller refused to "
                    "replace the product or provide a refund.\n\n"
                    f"3. The retrieved legal basis is {primary_act}, "
                    f"{primary_section}. The applicable provision should "
                    "be considered in light of the facts stated above and "
                    "the conditions contained in that provision."
                )

                repaired = (
                    repaired[:grounds_match.start()]
                    + repaired_grounds
                    + "\n\n"
                    + repaired[grounds_match.end():]
                )

        # If the LLM stopped midway through the prayer, replace the incomplete
        # tail with a grounded request based on the citizen's selected remedy.
        prayer_match = re.search(
            r"(?is)(RELIEF\s*/\s*PRAYER.*?)(?=\n(?:DOCUMENTS|DECLARATION|LEGAL SOURCES)\b|\Z)",
            repaired,
        )

        if prayer_match:
            prayer = prayer_match.group(1).strip()

            if prayer.endswith("be directed") or len(prayer.split()) < 12:
                supported = grounding.get("supported_remedies") or []
                remedy = str(getattr(request, "remedy", "") or "appropriate relief")

                if supported:
                    remedy_text = ", ".join(
                        item.lower() for item in supported
                    )
                    replacement = (
                        "RELIEF / PRAYER\n"
                        "The Complainant respectfully requests appropriate "
                        f"relief based on the retrieved legal provision, "
                        f"including, where applicable, {remedy_text}. "
                        "The requested relief remains subject to the "
                        "conditions of the applicable provision."
                    )
                else:
                    replacement = (
                        "RELIEF / PRAYER\n"
                        "The Complainant respectfully requests appropriate "
                        f"relief, including {remedy}, subject to the "
                        "applicable law and the facts of the case."
                    )

                repaired = (
                    repaired[:prayer_match.start()]
                    + replacement
                    + repaired[prayer_match.end():]
                )

        # Ensure the legal basis identifies the actual retrieved authority.
        primary_act = str(grounding.get("primary_act") or "").strip()
        primary_section = str(grounding.get("primary_section") or "").strip()

        if primary_act and primary_section:
            legal_basis_text = (
                f"The retrieved legal basis is {primary_act}, "
                f"{primary_section}. The provision should be read "
                "together with the facts of the case and the conditions "
                "contained in the provision."
            )

            basis_pattern = re.compile(
                r"(?is)LEGAL BASIS\\s*.*?(?=\\n(?:GROUNDS|RELIEF\\s*/\\s*PRAYER|DOCUMENTS|DECLARATION)\\b|\\Z)"
            )
            match = basis_pattern.search(repaired)
            if match:
                repaired = (
                    repaired[:match.start()]
                    + "LEGAL BASIS\\n"
                    + legal_basis_text
                    + "\\n"
                    + repaired[match.end():]
                )

        # If the primary retrieved provision explicitly contains remedies,
        # make sure the prayer does not silently omit them.
        supported = grounding.get("supported_remedies") or []
        if supported:
            prayer_pattern = re.compile(
                r"(?is)(RELIEF\\s*/\\s*PRAYER\\s*)(.*?)(?=\\n(?:DOCUMENTS|DECLARATION|LEGAL SOURCES)\\b|\\Z)"
            )
            match = prayer_pattern.search(repaired)
            if match:
                remedy_lines = "\\n".join(f"- {item}" for item in supported)
                prayer_text = (
                    "The Complainant respectfully requests appropriate "
                    "relief based on the retrieved legal provision, "
                    "subject to its conditions. The provision supports "
                    "the following possible forms of relief:\\n\\n"
                    + remedy_lines
                )
                repaired = (
                    repaired[:match.start()]
                    + match.group(1)
                    + prayer_text
                    + "\\n"
                    + repaired[match.end():]
                )

        return repaired.strip()


    # ============================================================
    # GENERATE COMPLAINT
    # ============================================================

    def generate(
        self,
        request
    ):

        # ========================================================
        # STEP 1 : USER SELECTED LEGAL DOMAIN
        # ========================================================

        requested_domain = str(
            getattr(
                request,
                "domain",
                ""
            )
        ).strip()

        if not requested_domain:

            requested_domain = (
                "Consumer Protection"
            )

        issue_type = str(
            getattr(
                request,
                "issue_type",
                ""
            )
        ).strip()

        print()
        print("==============================")
        print("USER SELECTED LEGAL DOMAIN")
        print("==============================")

        print(
            "Domain:",
            requested_domain
        )

        print(
            "Specific Issue:",
            issue_type
        )

        # ========================================================
        # STEP 2 : BUILD DOMAIN-AWARE QUERY
        # ========================================================

        retrieval_start = time.time()

        query = f"""
Legal Domain:
{requested_domain}

Specific Legal Issue:
{issue_type}

Product / Service:
{getattr(request, "product", "")}

Seller / Bank / Platform:
{getattr(request, "seller", "")}

Purchase / Transaction Date:
{getattr(request, "purchase_date", "")}

Bank / Payment Platform:
{getattr(request, "bank", "")}

Transaction Date:
{getattr(request, "transaction_date", "")}

Amount Involved:
{getattr(request, "amount", "")}

Problem:
{request.problem}

Requested Remedy:
{request.remedy}
"""

        print()
        print("==============================")
        print("DOMAIN-AWARE QUERY")
        print("==============================")

        print(query)

        # ========================================================
        # STEP 3 : DOMAIN-AWARE RETRIEVAL
        # ========================================================

        results = self.retriever.search(

            query,

            top_k=10,

            domain=requested_domain

        )

        # ========================================================
        # STEP 4 : DOMAIN-AWARE RANKING
        # ========================================================

        ranked_results = self.ranker.rank(

            query,

            results,

            requested_domain=requested_domain,

            issue_type=issue_type

        )

        top_results = ranked_results[:3]

        # ========================================================
        # RETRIEVAL TIME
        # ========================================================

        retrieval_time = round(

            time.time()
            -
            retrieval_start,

            2

        )

        # ========================================================
        # SHOW RETRIEVED DOCUMENTS
        # ========================================================

        print()
        print("==============================")
        print("TOP RETRIEVED DOCUMENTS")
        print("==============================")

        for i, item in enumerate(
            top_results,
            start=1
        ):

            print()
            print(
                f"Rank {i}"
            )

            print(
                item.get(
                    "metadata",
                    {}
                )
            )

            print(
                "Final Score :",
                item.get(
                    "final_score",
                    0.0
                )
            )

        # ========================================================
        # STEP 5 : LEGAL ISSUE CLASSIFICATION
        # ========================================================

        case_analysis = (
            self.classify_legal_issue(
                request,
                top_results
            )
        )

        # ========================================================
        # STEP 6 : PREPARE LEGAL CONTEXT
        # ========================================================

        context = "\n\n".join(

            item.get(
                "document",
                ""
            )

            for item in top_results

        )

        # ========================================================
        # STEP 7 : BUILD COMPLAINT PROMPT
        # ========================================================

        prompt = build_complaint_prompt(
            context=context,
            name=request.name,
            domain=requested_domain,
            issue_type=issue_type,
            product=getattr(request, "product", ""),
            seller=getattr(request, "seller", ""),
            purchase_date=getattr(request, "purchase_date", ""),
            city=request.city,
            problem=request.problem,
            remedy=request.remedy,
        )

        prompt += f"""

ADDITIONAL CASE DETAILS
Bank / Payment Platform:
{getattr(request, "bank", "")}

Transaction Date:
{getattr(request, "transaction_date", "")}

Amount Involved:
{getattr(request, "amount", "")}

STRICT GROUNDING RULES
1. Use the retrieved legal context as the only legal authority.
2. Do not invent statutory sections, acts, rules, cases, deadlines,
   authorities, portals, procedures, or guaranteed outcomes.
3. The citizen's desired remedy is a requested relief, not proof of
   legal entitlement.
4. Preserve the citizen's factual details exactly where supplied.
5. If the retrieved context is insufficient for a legal point, say so.
6. Generate a reviewable draft complaint, not a final legal opinion.

COMPLAINT OUTPUT FORMAT
Generate these sections:

COMPLAINT / DRAFT COMPLAINT
PARTIES
FACTS OF THE CASE
LEGAL BASIS
GROUNDS
RELIEF / PRAYER
DOCUMENTS / EVIDENCE
DECLARATION

For LEGAL BASIS and GROUNDS, use only propositions supported by the
retrieved legal context.

For RELIEF / PRAYER, reflect the citizen's desired remedy as a request.
Do not state that the citizen is legally guaranteed that remedy unless
the retrieved provision expressly supports it.

Do not include procedural instructions unless the retrieved context
supports them.
"""

        # ========================================================
        # STEP 8 : LLM
        # ========================================================

        llm_start = time.time()

        complaint = self.llm.generate(
            prompt
        ).strip()

        llm_time = round(

            time.time()
            -
            llm_start,

            2

        )

        # ========================================================
        # STEP 8.1 : CLEAN LLM OUTPUT
        # ========================================================

        complaint = re.sub(

            r"^#+\s*",

            "",

            complaint,

            flags=re.MULTILINE

        ).strip()

        # --------------------------------------------------------
        # GROUNDED CITATION CHECK
        # --------------------------------------------------------

        retrieved_sections = {
            str((item.get("metadata", {}) or {}).get("section", "")).strip().lower()
            for item in top_results
            if (item.get("metadata", {}) or {}).get("section")
        }

        cited_sections = {
            match.lower()
            for match in re.findall(
                r"\bSection\s+[0-9A-Za-z()]+(?:[-–][0-9A-Za-z()]+)?",
                complaint,
                flags=re.IGNORECASE,
            )
        }

        unsupported_citations = [
            section
            for section in cited_sections
            if section not in retrieved_sections
        ]

        if unsupported_citations:
            complaint += (
                "\n\n[Grounding Notice]\n"
                "The draft contains a legal section reference that was "
                "not found in the top retrieved legal provisions: "
                + ", ".join(sorted(set(unsupported_citations)))
                + ". Please review this draft before using it."
            )

        # If the model generated a Case Analysis
        # before the actual complaint, keep the complaint.

        complaint_markers = [

            "To,",

            "To :",

            "To:",

            "To\n"

        ]

        complaint_start = -1

        for marker in complaint_markers:

            position = complaint.find(
                marker
            )

            if position != -1:

                complaint_start = position

                break

        if complaint_start != -1:

            complaint = complaint[
                complaint_start:
            ].strip()

        # ========================================================
        # STEP 8.5 : GROUNDING VALIDATION
        # ========================================================

        grounding = self._validate_complaint_grounding(
            complaint,
            top_results
        )

        if grounding["status"] == "Needs Review":
            complaint = self._repair_grounding(
                complaint,
                grounding,
                request,
                top_results
            )

            # Re-check after conservative repair.
            grounding = self._validate_complaint_grounding(
                complaint,
                top_results
            )

        final_grounding = self._validate_complaint_grounding(
            complaint,
            top_results
        )

        # Always expose the final post-repair grounding state.
        grounding = final_grounding

        # ========================================================
        # STEP 9 : CONFIDENCE
        # ========================================================

        if top_results:

            score = top_results[0].get(
                "final_score",
                0
            )

        else:

            score = 0

        if score >= 0.75:

            confidence = "High"

        elif score >= 0.55:

            confidence = "Medium"

        else:

            confidence = "Low"

        # ========================================================
        # STEP 10 : LEGAL READINESS
        # ========================================================

        readiness = readiness_service.calculate(

            request,

            domain=requested_domain

        )

        # ========================================================
        # STEP 11 : SUPPORTING DOCUMENTS
        # ========================================================

        supporting_documents = (
            self.get_supporting_documents(
                requested_domain
            )
        )

        # ========================================================
        # STEP 12 : SOURCES
        # ========================================================

        sources = []

        seen = set()

        for item in top_results:

            metadata = item.get(
                "metadata",
                {}
            )

            key = (

                metadata.get(
                    "act"
                ),

                metadata.get(
                    "section"
                )

            )

            if key in seen:

                continue

            seen.add(key)

            sources.append({

                "act":
                    metadata.get(
                        "act"
                    ),

                "chapter":
                    metadata.get(
                        "chapter"
                    ),

                "section":
                    metadata.get(
                        "section"
                    ),

                "title":
                    metadata.get(
                        "title"
                    ),

                "domain":
                    metadata.get(
                        "domain"
                    ),

                "semantic_score":
                    item.get(
                        "semantic_score",
                        0.0
                    ),

                "keyword_score":
                    item.get(
                        "keyword_score",
                        0.0
                    ),

                "metadata_score":
                    item.get(
                        "metadata_score",
                        0.0
                    ),

                "domain_score":
                    item.get(
                        "domain_score",
                        0.0
                    ),

                "final_score":
                    item.get(
                        "final_score",
                        0.0
                    )

            })

        # ========================================================
        # STEP 13 : FINAL RESPONSE
        # ========================================================

        return {

            "case_analysis": {

                "category":
                    case_analysis[
                        "category"
                    ],

                "applicable_act":
                    case_analysis[
                        "applicable_act"
                    ],

                "rights":
                    case_analysis[
                        "rights"
                    ],

                "recommended_remedy":
                    request.remedy,

                "legal_readiness":
                    readiness[
                        "status"
                    ],

                "supporting_documents":
                    supporting_documents,

                "grounding_status":
                    grounding["status"],

                "grounding_issues":
                    grounding["issues"]

            },

            "complaint":
                complaint,

            "confidence":
                confidence,

            "readiness":
                readiness,

            "grounding":
                grounding,

            "retrieval_time":
                retrieval_time,

            "llm_time":
                llm_time,

            "total_time":
                round(

                    retrieval_time
                    +
                    llm_time,

                    2

                ),

            "sources":
                sources

        }


# ================================================================
# GLOBAL INSTANCE
# ================================================================

complaint_generator = ComplaintGenerator()