import time
import re

from app.rag.retriever import LegalRetriever
from app.retrieval.hybrid_ranker import HybridRanker
from app.llm.prompt_builder import PromptBuilder
from app.llm.ollama_service import OllamaService


class LegalAssistant:

    def __init__(self):
        self.retriever = LegalRetriever()
        self.ranker = HybridRanker()
        self.prompt_builder = PromptBuilder()
        self.llm = OllamaService()

    # ============================================================
    # TEXT CLEANING
    # ============================================================

    def _clean_text(self, text):

        if text is None:
            return ""

        text = str(text)

        # Common UTF-8 -> Windows-1252 mojibake
        replacements = {
            "â€”": "—",
            "â€“": "–",
            "â€˜": "‘",
            "â€™": "’",
            "â€œ": "“",
            "â€": "”",
            "â€¦": "…",
            "â€¢": "•",
            "Â ": " ",
            "Â": "",
        }

        for bad, good in replacements.items():

            text = text.replace(
                bad,
                good
            )

        return text.strip()

    # ============================================================
    # EXTRACT RESPONSE SECTION
    # ============================================================

    def _extract_section(
        self,
        answer,
        heading,
        next_headings
    ):

        if not answer:
            return ""

        next_pattern = "|".join(
            re.escape(item)
            for item in next_headings
        )

        pattern = re.compile(
            rf"(?ims)"
            rf"^\s*{re.escape(heading)}\s*:?\s*$"
            rf"(.*?)"
            rf"(?=^\s*(?:{next_pattern})\s*:?\s*$|\Z)"
        )

        match = pattern.search(answer)

        if not match:
            return ""

        return self._clean_text(
            match.group(1)
        )

    # ============================================================
    # NORMALIZE HEADINGS
    # ============================================================

    def _normalize_headings(
        self,
        answer
    ):

        if not answer:
            return ""

        replacements = {

            "Relevant Legal Provision:":
                "Relevant Legal Provision",

            "Relevant Legal Provision :":
                "Relevant Legal Provision",

            "Plain-Language Explanation:":
                "Plain Language Explanation",

            "Plain Language Explanation:":
                "Plain Language Explanation",

            "Possible Rights / Remedies:":
                "Possible Rights / Remedies",

            "Possible Rights and Remedies:":
                "Possible Rights / Remedies",

            "What the Citizen Can Do:":
                "What the Citizen Can Do",

            "What Citizen Can Do:":
                "What the Citizen Can Do",

            "Important Note:":
                "Important Note",

            "Important Notes:":
                "Important Note",
        }

        for old, new in replacements.items():

            answer = answer.replace(
                old,
                new
            )

        answer = re.sub(
            r"^\s*#{1,6}\s*",
            "",
            answer,
            flags=re.MULTILINE
        )

        return self._clean_text(
            answer
        )

    # ============================================================
    # REMOVE INTERNAL SECTION
    # ============================================================

    def _remove_internal_section(
        self,
        text,
        section_name
    ):

        if not text:
            return ""

        headings = [
            "Relevant Legal Provision",
            "Plain Language Explanation",
            "Possible Rights / Remedies",
            "What the Citizen Can Do",
            "Important Note",
        ]

        next_pattern = "|".join(
            re.escape(item)
            for item in headings
        )

        pattern = re.compile(
            rf"(?ims)"
            rf"^\s*{re.escape(section_name)}\s*:?"
            rf".*?"
            rf"(?=^\s*(?:{next_pattern})\s*:?\s*$|\Z)"
        )

        return pattern.sub(
            "",
            text
        ).strip()

    # ============================================================
    # FIND EXPLICIT REMEDIES / ACTIONS IN RETRIEVED EVIDENCE
    # ============================================================

    def _supported_remedies(
        self,
        evidence
    ):
        """
        Return only remedies/actions explicitly supported
        by the retrieved legal text.

        This is rule-based to prevent the LLM from inventing
        legal remedies.
        """

        if not evidence:
            return []

        evidence = self._clean_text(
            evidence
        ).lower()

        remedies = []

        checks = [

            (
                [
                    "remove the defect",
                    "removal of the defect",
                ],
                "Removal of the defect"
            ),

            (
                [
                    "replace the goods",
                    "replacement of the goods",
                ],
                "Replacement of the goods"
            ),

            (
                [
                    "return the price",
                    "return of the price",
                ],
                "Return of the price"
            ),

            (
                [
                    "refund",
                ],
                "Refund"
            ),

            (
                [
                    "compensation",
                    "pay compensation",
                    "payment of compensation",
                ],
                "Compensation"
            ),

            (
                [
                    "damages",
                    "pay damages",
                ],
                "Damages"
            ),

            (
                [
                    "protection order",
                ],
                "Protection order"
            ),

            (
                [
                    "residence order",
                ],
                "Residence order"
            ),

            (
                [
                    "monetary relief",
                ],
                "Monetary relief"
            ),

            (
                [
                    "custody order",
                ],
                "Custody order"
            ),

            (
                [
                    "legal aid",
                    "legal services",
                    "free legal services",
                ],
                "Legal aid / legal services"
            ),

            (
                [
                    "appeal",
                    "first appeal",
                    "second appeal",
                ],
                "Appeal"
            ),

            (
                [
                    "information commission",
                    "central information commission",
                    "state information commission",
                ],
                "Approach the Information Commission"
            ),

            (
                [
                    "penalty",
                    "penalties",
                ],
                "Penalty where the provision applies"
            ),
        ]

        for phrases, label in checks:

            if any(
                phrase in evidence
                for phrase in phrases
            ):

                if label not in remedies:

                    remedies.append(
                        label
                    )

        return remedies

    # ============================================================
    # FIND EXPLICIT CITIZEN ACTIONS
    # ============================================================

    def _supported_actions(
        self,
        evidence,
        domain=None,
        issue_type=None
    ):
        """
        Build citizen actions using the selected legal domain.

        Actions are generated only when the relevant concept is
        explicitly present in the retrieved evidence.

        Domain-specific filtering prevents unrelated rules such as
        Motor Vehicle actions from appearing in an RTI case.
        """

        if not evidence:
            return []

        evidence = self._clean_text(
            evidence
        ).lower()

        selected_domain = self._clean_text(
            domain or ""
        ).lower()

        selected_issue = self._clean_text(
            issue_type or ""
        ).lower()

        actions = []

        def add_action(action):

            if action not in actions:

                actions.append(
                    action
                )

        # ========================================================
        # RIGHT TO INFORMATION
        # ========================================================

        if selected_domain == "right to information":

            if any(
                phrase in evidence
                for phrase in [
                    "appeal",
                    "first appeal",
                    "second appeal",
                    "section 19",
                ]
            ):

                add_action(
                    "File a first appeal under Section 19(1) with the designated "
                    "Appellate Authority if information is denied or delayed, or "
                    "a second appeal with the Information Commission under Section 19(3)."
                )

            if any(
                phrase in evidence
                for phrase in [
                    "public information officer",
                    "information officer",
                    "pio",
                    "section 6",
                    "section 7",
                ]
            ):

                add_action(
                    "Submit a formal RTI application to the Public Information Officer (PIO) "
                    "under Section 6 or track disposal under Section 7."
                )

            if any(
                phrase in evidence
                for phrase in [
                    "exemption from disclosure",
                    "grounds for rejection",
                    "exemption",
                    "section 8",
                    "section 9",
                ]
            ):

                add_action(
                    "Review whether the refusal is based on non-disclosure exemptions "
                    "or grounds for rejection specified under Section 8 or Section 9."
                )

        # ========================================================
        # CONSUMER PROTECTION
        # ========================================================

        elif selected_domain == "consumer protection":

            if any(
                phrase in evidence
                for phrase in [
                    "district commission",
                    "state commission",
                    "national commission",
                    "consumer commission",
                    "complaint",
                    "section 35",
                    "section 39",
                ]
            ):

                add_action(
                    "File a consumer complaint before the appropriate District, State, "
                    "or National Consumer Disputes Redressal Commission seeking relief "
                    "such as replacement, refund, or compensation under Section 39."
                )

            if any(
                phrase in evidence
                for phrase in [
                    "mediation",
                    "section 37",
                    "section 79",
                ]
            ):

                add_action(
                    "Opt for dispute resolution through the Consumer Mediation Cell "
                    "attached to the Commission where provided for under Section 37 or 79."
                )

        # ========================================================
        # REAL ESTATE / RERA
        # ========================================================

        elif selected_domain == "real estate / rera":

            if any(
                phrase in evidence
                for phrase in [
                    "real estate regulatory authority",
                    "regulatory authority",
                    "adjudicating officer",
                    "complaint",
                    "section 31",
                ]
            ):

                add_action(
                    "File a complaint with the Real Estate Regulatory Authority (RERA) "
                    "or Adjudicating Officer under Section 31 for any violation by the promoter."
                )

            if any(
                phrase in evidence
                for phrase in [
                    "delayed possession",
                    "refund",
                    "interest",
                    "section 18",
                ]
            ):

                add_action(
                    "Claim refund of the amount paid along with interest and compensation "
                    "under Section 18 if the builder fails to complete or hand over possession on time."
                )

        # ========================================================
        # DOMESTIC VIOLENCE
        # ========================================================

        elif selected_domain == "domestic violence":

            if any(
                phrase in evidence
                for phrase in [
                    "protection officer",
                    "service provider",
                ]
            ):

                add_action(
                    "Approach a designated Protection Officer or Service Provider "
                    "for assistance in preparing and presenting an application."
                )

            if any(
                phrase in evidence
                for phrase in [
                    "magistrate",
                    "application",
                    "section 12",
                    "protection order",
                    "residence order",
                ]
            ):

                add_action(
                    "Present an application to the Magistrate under Section 12 for seeking "
                    "protection orders, residence orders, or monetary relief under Sections 18–22."
                )

        # ========================================================
        # LEGAL SERVICES / LEGAL AID
        # ========================================================

        elif selected_domain == "legal services / legal aid":

            if any(
                phrase in evidence
                for phrase in [
                    "legal services authority",
                    "free legal services",
                    "legal aid",
                    "section 12",
                    "section 13",
                ]
            ):

                add_action(
                    "Apply for free legal aid or legal representation through the Member "
                    "Secretary or Secretary of the Legal Services Authority under Section 12/13."
                )

            if any(
                phrase in evidence
                for phrase in [
                    "lok adalat",
                    "section 19",
                ]
            ):

                add_action(
                    "Opt to refer the legal dispute for settlement to a Lok Adalat "
                    "organized by the Legal Services Authority under Section 19."
                )

        # ========================================================
        # CRIMINAL LAW / BNS
        # ========================================================

        elif selected_domain == "criminal law / bns":

            if any(
                phrase in evidence
                for phrase in [
                    "threat",
                    "intimidation",
                    "criminal intimidation",
                    "section 351",
                ]
            ):

                add_action(
                    "Lodge a complaint or report at the local police station regarding criminal "
                    "intimidation under Section 351 of the Bharatiya Nyaya Sanhita, 2023."
                )

            if any(
                phrase in evidence
                for phrase in [
                    "police",
                    "complaint",
                    "first information report",
                    "fir",
                    "offence",
                ]
            ):

                add_action(
                    "Report the criminal offence to the police station or Magistrate having jurisdiction."
                )

        # ========================================================
        # MOTOR VEHICLE
        # ========================================================

        elif selected_domain == "motor vehicle":

            if any(
                phrase in evidence
                for phrase in [
                    "licence",
                    "license",
                    "driving licence",
                    "section 130",
                    "police officer",
                    "demand",
                ]
            ):

                add_action(
                    "Produce your driving licence upon demand by a police officer in uniform "
                    "or authorized authority as required under Section 130 of the Motor Vehicles Act."
                )

            if any(
                phrase in evidence
                for phrase in [
                    "claims tribunal",
                    "tribunal",
                    "section 166",
                    "compensation",
                    "accident",
                ]
            ):

                add_action(
                    "Submit an application for compensation before the Motor Accidents Claims "
                    "Tribunal under Section 166 in case of road accidents or bodily injury."
                )

        # ========================================================
        # CYBER / IT
        # ========================================================

        elif selected_domain == "cyber / it":

            if any(
                phrase in evidence
                for phrase in [
                    "adjudicating officer",
                    "compensation",
                    "section 43",
                ]
            ):

                add_action(
                    "File an application before the Adjudicating Officer for claiming "
                    "compensation for unauthorized computer access or damage under Section 43."
                )

            if any(
                phrase in evidence
                for phrase in [
                    "police",
                    "cyber crime",
                    "complaint",
                    "cyber",
                ]
            ):

                add_action(
                    "Lodge a complaint with the local Cyber Crime Police Station or police authorities."
                )

        # ========================================================
        # CONTRACT / SERVICE
        # ========================================================

        elif selected_domain == "contract / service":

            if any(
                phrase in evidence
                for phrase in [
                    "damages",
                    "compensation",
                    "breach",
                    "section 73",
                ]
            ):

                add_action(
                    "Seek compensation for loss or damage naturally arising from the breach "
                    "of contract under Section 73 of the Indian Contract Act, 1872."
                )

            if any(
                phrase in evidence
                for phrase in [
                    "penalty",
                    "stipulated",
                    "section 74",
                ]
            ):

                add_action(
                    "Claim reasonable compensation up to the penalty or named sum specified "
                    "in the agreement under Section 74."
                )

        return actions

    # ============================================================
    # GROUND CITIZEN ACTION
    # ============================================================

    def _ground_citizen_action(
        self,
        evidence,
        domain=None,
        issue_type=None
    ):
        """
        Generate a safe citizen-action section from retrieved
        evidence only.
        """

        actions = self._supported_actions(
            evidence,
            domain=domain,
            issue_type=issue_type
        )

        if actions:

            return "\n".join(
                f"- {action}"
                for action in actions
            )

        return (
            "The retrieved legal provisions do not specify "
            "a clear procedure for taking action in this situation."
        )

    # ============================================================
    # ASK
    # ============================================================

    def ask(
        self,
        question,
        domain=None,
        issue_type=None,
        evidence=None,
    ):

        total_start = time.time()

        selected_domain = str(
            domain or ""
        ).strip()

        selected_issue = str(
            issue_type or ""
        ).strip()

        evidence = evidence or []

        print()
        print("=" * 70)
        print("LEGAL ASSISTANT")
        print("=" * 70)

        print(
            "Question:",
            question
        )

        print(
            "Domain:",
            selected_domain
        )

        print(
            "Issue Type:",
            selected_issue
        )

        # ========================================================
        # CASE-SPECIFIC EVIDENCE
        # ========================================================

        evidence_parts = []

        for item in evidence:

            if not isinstance(
                item,
                dict
            ):
                continue

            extracted_text = str(

                item.get(
                    "extracted_text"
                )

                or

                item.get(
                    "extractedText"
                )

                or ""

            ).strip()

            if not extracted_text:
                continue

            name = str(

                item.get(
                    "name"
                )

                or "Uploaded document"

            ).strip()

            evidence_parts.append(

                f"Document: {name}\n"
                f"Extracted text:\n"
                f"{self._clean_text(extracted_text[:6000])}"
            )

        evidence_context = ""

        if evidence_parts:

            evidence_context = (

                "\n\nCASE-SPECIFIC EVIDENCE\n"
                "=======================\n"
                "The following information comes from "
                "documents uploaded by the citizen. "
                "Treat this only as factual case information, "
                "not as legal authority.\n\n"
                +
                "\n\n".join(
                    evidence_parts
                )
            )

        # ========================================================
        # DOMAIN-AWARE QUERY
        # ========================================================

        retrieval_question = question

        if (
            selected_domain
            or selected_issue
        ):

            retrieval_question = (

                "Legal Domain: "
                + selected_domain

                + "\n\nLegal Issue: "
                + selected_issue

                + "\n\nCitizen Question: "
                + question
            )

        # ========================================================
        # STEP 1 — RETRIEVAL
        # ========================================================

        retrieval_start = time.time()

        results = self.retriever.search(

            retrieval_question,

            top_k=25,

            domain=(
                selected_domain
                or None
            ),

            issue_type=(
                selected_issue
                or None
            ),
        )

        # ========================================================
        # STEP 2 — HYBRID RANKING
        # ========================================================

        ranked_results = self.ranker.rank(

            retrieval_question,

            results,

            requested_domain=(
                selected_domain
                or None
            ),

            issue_type=(
                selected_issue
                or None
            ),
        )
                # ========================================================
        # REMOVE DUPLICATE LEGAL PROVISIONS
        # ========================================================

        unique_results = []

        seen_provisions = set()

        for item in ranked_results:

            metadata = (
                item.get(
                    "metadata",
                    {}
                ) or {}
            )

            act = self._clean_text(
                metadata.get(
                    "act",
                    ""
                )
            ).lower().strip()

            section = self._clean_text(
                metadata.get(
                    "section",
                    ""
                )
            ).lower().strip()

            provision_key = (
                act,
                section
            )

            if provision_key in seen_provisions:
                continue

            seen_provisions.add(
                provision_key
            )

            unique_results.append(
                item
            )

        top_results = unique_results[:3]

        retrieval_time = round(
            time.time()
            -
            retrieval_start,
            2
        )

        # ========================================================
        # NO RESULTS
        # ========================================================

        if not top_results:

            return {

                "answer":
                    "I could not find sufficient "
                    "relevant legal information "
                    "in the available sources.",

                "confidence":
                    "Low",

                "retrieval_time":
                    retrieval_time,

                "llm_time":
                    0,

                "total_time":
                    round(
                        time.time()
                        -
                        total_start,
                        2
                    ),

                "sources":
                    [],
            }

        # ========================================================
        # DEBUG TOP RESULTS
        # ========================================================

        print()
        print("=" * 70)
        print("TOP RETRIEVED PROVISIONS")
        print("=" * 70)

        for i, item in enumerate(
            top_results,
            start=1
        ):

            metadata = (
                item.get(
                    "metadata",
                    {}
                ) or {}
            )

            print(
                f"{i}. "
                f"{metadata.get('act', '')} | "
                f"{metadata.get('section', '')} | "
                f"{metadata.get('title', '')} | "
                f"score={item.get('final_score', 0)}"
            )

        # ========================================================
        # PRIMARY PROVISION
        # ========================================================

        primary_result = top_results[0]

        primary_metadata = (
            primary_result.get(
                "metadata",
                {}
            ) or {}
        )

        primary_act = self._clean_text(

            primary_metadata.get(
                "act"
            )

            or "Unknown Act"
        )

        primary_section = self._clean_text(

            primary_metadata.get(
                "section"
            )

            or "Unknown Section"
        )

        primary_title = self._clean_text(

            primary_metadata.get(
                "title"
            )

            or ""
        )

        primary_document = self._clean_text(

            primary_result.get(
                "document"
            )

            or ""
        )

        # ========================================================
        # PRIMARY PROVISION DISPLAY
        # ========================================================

        primary_provision = (

            f"{primary_act}, "
            f"{primary_section}"
        )

        if primary_title:

            primary_provision += (

                " — "
                + primary_title
            )

        print()
        print(
            "PRIMARY PROVISION:",
            primary_provision
        )

        # ========================================================
        # SUPPORTING CONTEXT
        # ========================================================

        supporting_parts = []

        for index, item in enumerate(
            top_results[1:3],
            start=2
        ):

            metadata = (
                item.get(
                    "metadata",
                    {}
                ) or {}
            )

            document = self._clean_text(

                item.get(
                    "document"
                )

                or ""
            )

            supporting_parts.append(

                f"SUPPORTING PROVISION {index}\n"
                f"Act: "
                f"{self._clean_text(metadata.get('act', ''))}\n"
                f"Section: "
                f"{self._clean_text(metadata.get('section', ''))}\n"
                f"Title: "
                f"{self._clean_text(metadata.get('title', ''))}\n\n"
                f"Legal Text:\n"
                f"{document}"
            )

        supporting_text = (

            "\n\n".join(
                supporting_parts
            )
        )

        # ========================================================
        # RETRIEVED EVIDENCE FOR REMEDIES / ACTIONS
        # ========================================================

        retrieved_evidence = " ".join(

            self._clean_text(
                item.get(
                    "document"
                )
                or ""
            )

            + " "

            + self._clean_text(

                (
                    item.get(
                        "metadata",
                        {}
                    )
                    or {}
                ).get(
                    "title",
                    ""
                )

            )

            for item in top_results
        )

        # ========================================================
        # STEP 3 — PRIMARY-FOCUSED LLM PROMPT
        # ========================================================

        prompt = f"""
You are a legal information assistant for Indian citizens.

CITIZEN QUESTION:

{question}

SELECTED LEGAL DOMAIN:

{selected_domain}

SELECTED LEGAL ISSUE:

{selected_issue}

============================================================
PRIMARY LEGAL PROVISION
============================================================

The following is the PRIMARY legal provision.

Act:
{primary_act}

Section:
{primary_section}

Title:
{primary_title}

Legal Text:
{primary_document}

============================================================
SUPPORTING LEGAL PROVISIONS
============================================================

{supporting_text}

{evidence_context}

============================================================
STRICT LEGAL GROUNDING RULES
============================================================

1. The PRIMARY LEGAL PROVISION is the main provision
   answering the citizen's question.

2. Explain the PRIMARY provision.

3. Supporting provisions are secondary only.

4. Do NOT replace the primary provision with a supporting
   provision.

5. Do NOT answer using Section 18 simply because it mentions
   driving licences if the primary provision is Section 130.

6. Do NOT invent legal rights.

7. Do NOT invent remedies.

8. Do NOT invent procedures.

9. Do NOT invent authorities.

10. Do NOT invent deadlines.

11. Do NOT invent penalties.

12. Do NOT invent portals or helplines.

13. Use only information explicitly supported by the
    retrieved legal text.

14. If something is not stated in the retrieved text,
    say that the retrieved provision does not specify it.

15. Do not use general legal knowledge that is absent
    from the retrieved context.

16. The explanation must be understandable to an ordinary
    citizen.

Return exactly these sections:

Plain Language Explanation

Relevant Legal Provision

Possible Rights / Remedies

What the Citizen Can Do

Important Note

For Plain Language Explanation:

- Write 2 to 4 complete sentences.
- Directly explain how the PRIMARY provision relates
  to the citizen's question.
- State only what is supported by the PRIMARY legal text.
- Do not merely say that the provision is "relevant".
- If the retrieved legal text is incomplete or unclear,
  explicitly say so.

Do not add any additional sections.
"""

        # ========================================================
        # STEP 4 — LLM
        # ========================================================

        llm_start = time.time()

        try:

            answer = self.llm.generate(
                prompt
            ).strip()

        except Exception as exc:

            print(
                "LLM ERROR:",
                exc
            )

            answer = ""

        llm_time = round(
            time.time()
            -
            llm_start,
            2
        )

        # ========================================================
        # LLM FALLBACK
        # ========================================================

        if not answer:

            answer = (

                "Plain Language Explanation\n"

                "The system could not generate an "
                "automatic explanation of the retrieved "
                "legal provision.\n\n"

                "Relevant Legal Provision\n"

                f"{primary_provision}\n\n"

                "Possible Rights / Remedies\n"

                "The retrieved legal provision should "
                "be reviewed directly to determine "
                "whether it provides a remedy.\n\n"

                "What the Citizen Can Do\n"

                "The retrieved legal provisions do not "
                "specify the procedure for taking action "
                "in this situation.\n\n"

                "Important Note\n"

                "This explanation is based on the retrieved "
                "legal provisions and is not a substitute "
                "for professional legal advice."
            )

        # ========================================================
        # STEP 5 — CLEAN LLM OUTPUT
        # ========================================================

        answer = self._normalize_headings(
            answer
        )

        answer = self._remove_internal_section(

            answer,

            "Why It May Be Relevant"
        )

        # ========================================================
        # STEP 6 — PLAIN LANGUAGE
        # ========================================================

        plain_language = self._extract_section(

            answer,

            "Plain Language Explanation",

            [
                "Relevant Legal Provision",
                "Possible Rights / Remedies",
                "What the Citizen Can Do",
                "Important Note",
            ]
        )

        # --------------------------------------------------------
        # DETECT WEAK OR GENERIC LLM EXPLANATION
        # --------------------------------------------------------

        weak_explanation = (

            not plain_language

            or

            len(
                plain_language.strip()
            ) < 45

            or

            plain_language.strip().lower()

            in {

                "the retrieved primary legal provision "
                "is relevant to the citizen's question.",

                "the retrieved primary legal provision "
                "is relevant to the citizen's question",

            }
        )

        if weak_explanation:

            # Use only the retrieved primary legal text.

            provision_text = self._clean_text(

                primary_document
            )

            # Clean excessive whitespace.

            provision_text = re.sub(

                r"\s+",

                " ",

                provision_text

            ).strip()

            # Keep fallback reasonably short.

            if len(provision_text) > 500:

                provision_text = (

                    provision_text[:500]

                    .rsplit(
                        " ",
                        1
                    )[0]

                    + "..."
                )

            # ----------------------------------------------------
            # GROUNDED FALLBACK
            # ----------------------------------------------------

            if provision_text:

                plain_language = (

                    f"The primary provision is "
                    f"{primary_act}, "
                    f"{primary_section}"

                    +

                    (
                        f" ({primary_title})"
                        if primary_title
                        else ""
                    )

                    +

                    ". The retrieved legal text states: "

                    +

                    provision_text
                )

            else:

                plain_language = (

                    f"The retrieved primary provision is "
                    f"{primary_act}, "
                    f"{primary_section}. "

                    "The available legal text is insufficient "
                    "to provide a more specific plain-language "
                    "explanation."
                )
                        # ========================================================
        # VALIDATE PRIMARY SECTION IN LLM EXPLANATION
        # ========================================================
        #
        # The LLM must not mention a different section from the
        # actual highest-ranked primary provision.
        #
        # Example:
        # Primary = Section 8
        # LLM says = Section 18
        #
        # In that situation we discard the LLM explanation and
        # use a grounded fallback based on the actual provision.
        # ========================================================

        primary_section_match = re.search(
            r"\bsection\s+([0-9]+[A-Za-z]?)\b",
            primary_section,
            flags=re.IGNORECASE
        )

        explanation_sections = re.findall(
            r"\bsection\s+([0-9]+[A-Za-z]?)\b",
            plain_language,
            flags=re.IGNORECASE
        )

        invalid_section_reference = False

        if primary_section_match:

            expected_section = (
                primary_section_match.group(1).lower()
            )

            for mentioned_section in explanation_sections:

                if (
                    mentioned_section.lower()
                    != expected_section
                ):

                    invalid_section_reference = True
                    break

        if invalid_section_reference:

            provision_text = self._clean_text(
                primary_document
            )

            provision_text = re.sub(
                r"\s+",
                " ",
                provision_text
            ).strip()

            if len(provision_text) > 500:

                provision_text = (
                    provision_text[:500]
                    .rsplit(" ", 1)[0]
                    + "..."
                )

            if provision_text:

                plain_language = (
                    f"The primary provision is "
                    f"{primary_act}, "
                    f"{primary_section}"
                    +
                    (
                        f" ({primary_title})"
                        if primary_title
                        else ""
                    )
                    +
                    ". The retrieved legal text states: "
                    +
                    provision_text
                )

            else:

                plain_language = (
                    f"The primary provision is "
                    f"{primary_act}, "
                    f"{primary_section}. "
                    "The retrieved legal text is insufficient "
                    "to provide a more specific explanation."
                )

        # ========================================================
        # STEP 7 — REMEDIES
        # ========================================================

        # Use the top retrieved provisions as evidence.
        # This allows supporting provisions to contribute
        # evidence for remedies while keeping the primary
        # provision unchanged.

        supported_remedies = (
            self._supported_remedies(
                retrieved_evidence
            )
        )

        if supported_remedies:

            remedies = (

                "The retrieved legal provision "
                "expressly supports the following "
                "possible relief, subject to the "
                "conditions stated in that provision:\n\n"

                +

                "\n".join(

                    f"- {item}"

                    for item
                    in supported_remedies
                )
            )

        else:

            remedies = (

                "The retrieved legal provision does "
                "not clearly specify a separate remedy "
                "for the situation described."
            )

        # ========================================================
        # STEP 8 — CITIZEN ACTION
        # ========================================================

        # IMPORTANT:
        # Actions are generated from retrieved evidence and
        # filtered according to the selected legal domain.
        #
        # This prevents unrelated actions such as:
        # Motor Vehicle claim/compensation procedures
        # appearing inside an RTI case.

        citizen_action = (
            self._ground_citizen_action(
                retrieved_evidence,
                domain=selected_domain,
                issue_type=selected_issue,
            )
        )

        # ========================================================
        # STEP 9 — IMPORTANT NOTE
        # ========================================================

        important_note = (

            "This explanation is based only on the "
            "retrieved legal provisions available in "
            "the system. It is general legal information "
            "and is not a substitute for advice from a "
            "qualified legal professional."
        )

        # ========================================================
        # STEP 10 — FINAL RESPONSE
        # ========================================================

        # The primary provision is inserted directly from
        # the highest-ranked retrieval result.
        #
        # Therefore the LLM cannot change Section 130
        # into Section 18.

        final_answer = (

            "Plain Language Explanation\n"
            f"{plain_language}\n\n"

            "Relevant Legal Provision\n"
            f"{primary_provision}\n\n"

            "Possible Rights / Remedies\n"
            f"{remedies}\n\n"

            "What the Citizen Can Do\n"
            f"{citizen_action}\n\n"

            "Important Note\n"
            f"{important_note}"
        )

        # ========================================================
        # STEP 11 — CONFIDENCE
        # ========================================================

        try:

            top_score = float(

                top_results[0].get(
                    "final_score",
                    0
                )

            )

        except (
            ValueError,
            TypeError
        ):

            top_score = 0.0

        if top_score >= 0.75:

            confidence = "High"

        elif top_score >= 0.45:

            confidence = "Medium"

        else:

            confidence = "Low"

        # ========================================================
        # STEP 12 — SOURCES
        # ========================================================

        sources = []

        for item in top_results:

            metadata = (
                item.get(
                    "metadata",
                    {}
                ) or {}
            )

            sources.append({

                "act":
                    self._clean_text(
                        metadata.get(
                            "act"
                        )
                    ),

                "chapter":
                    self._clean_text(
                        metadata.get(
                            "chapter"
                        )
                    ),

                "section":
                    self._clean_text(
                        metadata.get(
                            "section"
                        )
                    ),

                "title":
                    self._clean_text(
                        metadata.get(
                            "title"
                        )
                    ),

                "domain":
                    self._clean_text(
                        metadata.get(
                            "domain"
                        )
                    ),

                "semantic_score":
                    item.get(
                        "semantic_score",
                        0
                    ),

                "keyword_score":
                    item.get(
                        "keyword_score",
                        0
                    ),

                "metadata_score":
                    item.get(
                        "metadata_score",
                        0
                    ),

                "domain_score":
                    item.get(
                        "domain_score",
                        0
                    ),

                "legal_issue_score":
                    item.get(
                        "legal_issue_score",
                        0
                    ),

                "final_score":
                    item.get(
                        "final_score",
                        0
                    ),
            })

        # ========================================================
        # TOTAL TIME
        # ========================================================

        total_time = round(

            time.time()
            -
            total_start,

            2
        )

        print()
        print("=" * 70)
        print("FINAL RESULT")
        print("=" * 70)

        print(
            "Primary Provision:",
            primary_provision
        )

        print(
            "Confidence:",
            confidence
        )

        print(
            "Retrieval Time:",
            retrieval_time,
            "seconds"
        )

        print(
            "LLM Time:",
            llm_time,
            "seconds"
        )

        print(
            "Total Time:",
            total_time,
            "seconds"
        )

        print("=" * 70)

        return {

            "answer":
                final_answer,

            "confidence":
                confidence,

            "retrieval_time":
                retrieval_time,

            "llm_time":
                llm_time,

            "total_time":
                total_time,

            "sources":
                sources,
        }


# ================================================================
# GLOBAL INSTANCE
# ================================================================

legal_assistant = LegalAssistant()