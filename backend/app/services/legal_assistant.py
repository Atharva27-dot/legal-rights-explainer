
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

    def _retrieved_evidence_text(self, top_results):
        evidence_parts = []

        for item in top_results:
            metadata = item.get("metadata", {}) or {}

            document = item.get("document")
            if document:
                evidence_parts.append(str(document))

            for key in (
                "text",
                "content",
                "page_content",
                "chunk_text",
                "excerpt",
            ):
                value = item.get(key)
                if value is not None:
                    evidence_parts.append(str(value))

            for value in metadata.values():
                if value is not None:
                    evidence_parts.append(str(value))

        return "\n".join(evidence_parts).lower()

    def _extract_section(self, answer, heading, next_headings):
        pattern = (
            rf"(?ims)^\s*{re.escape(heading)}\s*:?\s*$"
            rf"(.*?)(?=^\s*(?:{'|'.join(map(re.escape, next_headings))})"
            rf"\s*:?\s*$|\Z)"
        )
        match = re.search(pattern, answer)
        return match.group(1).strip() if match else ""

    def _replace_section(self, answer, heading, replacement, next_headings):
        pattern = (
            rf"(?ims)(^\s*{re.escape(heading)}\s*:?\s*$)"
            rf"(.*?)(?=^\s*(?:{'|'.join(map(re.escape, next_headings))})"
            rf"\s*:?\s*$|\Z)"
        )
        match = re.search(pattern, answer)

        if not match:
            return answer

        return (
            answer[:match.start()]
            + match.group(1)
            + "\n"
            + replacement.strip()
            + "\n\n"
            + answer[match.end():].lstrip()
        )

    def _primary_evidence_text(self, top_results):
        """Use the highest-ranked provision for remedy extraction.

        This prevents remedies from unrelated secondary provisions
        (for example product-liability sections) from leaking into
        the remedy list for a directly relevant provision such as
        Section 39.
        """
        if not top_results:
            return ""

        item = top_results[0]
        parts = []

        document = item.get("document")
        if document:
            parts.append(str(document))

        for key in ("text", "content", "page_content", "chunk_text", "excerpt"):
            value = item.get(key)
            if value is not None:
                parts.append(str(value))

        # Metadata is intentionally limited to the primary result.
        metadata = item.get("metadata", {}) or {}
        for key in ("title", "section", "act"):
            value = metadata.get(key)
            if value is not None:
                parts.append(str(value))

        return "\\n".join(parts).lower()

    def _supported_remedies(self, evidence):
        remedies = []

        checks = [
            (
                ["remove the defect", "removal of the defect"],
                "Removal of the defect",
            ),
            (
                [
                    "replace the goods",
                    "replace goods",
                    "replacement of the goods",
                    "replacement",
                ],
                "Replacement of the goods",
            ),
            (
                [
                    "return the price",
                    "return of the price",
                    "return price",
                ],
                "Return of the price",
            ),
            (["refund"], "Refund"),
            (
                [
                    "pay compensation",
                    "payment of compensation",
                    "compensation",
                ],
                "Compensation",
            ),
            (["pay damages"], "Damages"),
        ]

        for phrases, label in checks:
            if any(phrase in evidence for phrase in phrases):
                remedies.append(label)

        return remedies

    def _validate_grounding(self, answer, top_results):
        evidence = self._retrieved_evidence_text(top_results)
        # Use only the highest-ranked provision when deciding which
        # remedies are explicitly supported. Other retrieved sections
        # may discuss different forms of liability or relief.
        remedy_evidence = self._primary_evidence_text(top_results)

        unsupported_authorities = [
            "google pay",
            "npci",
            "rbi",
            "reserve bank of india",
            "police",
            "cybercrime portal",
            "cyber crime portal",
            "national cyber crime reporting portal",
            "bank customer support",
            "customer support",
            "helpline",
        ]

        citizen_action = self._extract_section(
            answer,
            "What the Citizen Can Do",
            [
                "Important Note",
                "Possible Rights / Remedies",
                "Relevant Legal Provision",
                "Plain Language Explanation",
            ],
        )

        for authority in unsupported_authorities:
            if authority in citizen_action.lower() and authority not in evidence:
                answer = self._replace_section(
                    answer,
                    "What the Citizen Can Do",
                    "The retrieved legal provisions do not specify "
                    "the reporting procedure or authority for this situation.",
                    [
                        "Important Note",
                        "Possible Rights / Remedies",
                        "Relevant Legal Provision",
                        "Plain Language Explanation",
                    ],
                )
                break

        remedies = self._extract_section(
            answer,
            "Possible Rights / Remedies",
            [
                "What the Citizen Can Do",
                "Important Note",
                "Relevant Legal Provision",
                "Plain Language Explanation",
            ],
        )

        supported = self._supported_remedies(remedy_evidence)

        uncertainty_patterns = [
            "do not provide enough information to determine a specific remedy",
            "do not provide sufficient information to determine a specific remedy",
            "not enough information to determine a specific remedy",
            "cannot determine a specific remedy",
            "no specific remedy",
        ]

        if supported and any(
            phrase in remedies.lower()
            for phrase in uncertainty_patterns
        ):
            replacement = (
                "The retrieved legal provisions expressly support "
                "the following possible relief, subject to the "
                "conditions in the applicable provision:\n\n"
                + "\n".join(f"- {item}" for item in supported)
            )

            answer = self._replace_section(
                answer,
                "Possible Rights / Remedies",
                replacement,
                [
                    "What the Citizen Can Do",
                    "Important Note",
                    "Relevant Legal Provision",
                    "Plain Language Explanation",
                ],
            )

        remedies = self._extract_section(
            answer,
            "Possible Rights / Remedies",
            [
                "What the Citizen Can Do",
                "Important Note",
                "Relevant Legal Provision",
                "Plain Language Explanation",
            ],
        )

        remedy_aliases = {
            "refund": [
                "refund",
                "return the price",
                "return of the price",
                "return price",
            ],
            "replacement": [
                "replacement",
                "replace the goods",
                "replace goods",
                "replace the product",
            ],
            "compensation": [
                "compensation",
                "pay compensation",
            ],
            "damages": [
                "damages",
                "pay damages",
            ],
            "penalty": ["penalty"],
            "remove the defect": [
                "remove the defect",
                "removal of the defect",
            ],
        }

        unsupported_remedy = False

        for generated_term, supported_phrases in remedy_aliases.items():
            if generated_term not in remedies.lower():
                continue

            if not any(
                phrase in remedy_evidence
                for phrase in supported_phrases
            ):
                unsupported_remedy = True
                break

        if unsupported_remedy:
            if supported:
                replacement = (
                    "The retrieved legal provisions expressly support "
                    "the following possible relief, subject to the "
                    "conditions in the applicable provision:\n\n"
                    + "\n".join(f"- {item}" for item in supported)
                )
            else:
                replacement = (
                    "The retrieved legal provisions do not provide "
                    "enough information to determine a specific remedy "
                    "for this situation."
                )

            answer = self._replace_section(
                answer,
                "Possible Rights / Remedies",
                replacement,
                [
                    "What the Citizen Can Do",
                    "Important Note",
                    "Relevant Legal Provision",
                    "Plain Language Explanation",
                ],
            )

        citizen_action = self._extract_section(
            answer,
            "What the Citizen Can Do",
            [
                "Important Note",
                "Possible Rights / Remedies",
                "Relevant Legal Provision",
                "Plain Language Explanation",
            ],
        )

        mechanism_phrases = [
            "mediation",
            "product liability action",
            "file a complaint",
            "district commission",
            "state commission",
            "national commission",
        ]

        for phrase in mechanism_phrases:
            if phrase in citizen_action.lower() and phrase not in evidence:
                answer = self._replace_section(
                    answer,
                    "What the Citizen Can Do",
                    "The retrieved legal provisions do not specify "
                    "enough procedural information to determine the "
                    "appropriate action for this situation.",
                    [
                        "Important Note",
                        "Possible Rights / Remedies",
                        "Relevant Legal Provision",
                        "Plain Language Explanation",
                    ],
                )
                break

        plain = self._extract_section(
            answer,
            "Plain Language Explanation",
            [
                "Relevant Legal Provision",
                "Possible Rights / Remedies",
                "What the Citizen Can Do",
                "Important Note",
            ],
        )

        categorical_patterns = [
            r"\bis definitely\b",
            r"\bis certainly\b",
            r"\bis a cybercrime\b",
            r"\bis considered a cybercrime\b",
            r"\bis legally a\b",
            r"\bwill receive\b",
            r"\bwill be entitled\b",
        ]

        if any(
            re.search(pattern, plain, flags=re.IGNORECASE)
            for pattern in categorical_patterns
        ):
            answer = self._replace_section(
                answer,
                "Plain Language Explanation",
                "The retrieved legal provisions may be relevant to "
                "the situation described by the citizen. The available "
                "documents should be read together with the specific "
                "facts before reaching a legal conclusion.",
                [
                    "Relevant Legal Provision",
                    "Possible Rights / Remedies",
                    "What the Citizen Can Do",
                    "Important Note",
                ],
            )

        return answer.strip()

    def ask(self, question, domain=None, issue_type=None):

        selected_domain = str(domain or "").strip()
        selected_issue = str(issue_type or "").strip()

        retrieval_question = question

        if selected_domain or selected_issue:
            retrieval_question = (
                "Legal Domain:\n"
                + selected_domain
                + "\n\nSpecific Legal Issue:\n"
                + selected_issue
                + "\n\nCitizen Question:\n"
                + question
            )

        print()
        print("==============================")
        print("LEGAL ASSISTANT REQUEST")
        print("==============================")
        print("Selected Domain:", selected_domain or "Not specified")
        print("Selected Issue:", selected_issue or "Not specified")
        print("Question:", question)

        retrieval_start = time.time()

        results = self.retriever.search(
            retrieval_question,
            top_k=10,
            domain=selected_domain or None,
            issue_type=selected_issue or None,
        )

        # V4 hybrid ranking call is intentionally unchanged.
        ranked_results = self.ranker.rank(
            retrieval_question,
            results,
            requested_domain=selected_domain or None,
            issue_type=selected_issue or None,
        )

        top_results = ranked_results[:3]

        retrieval_time = round(
            time.time() - retrieval_start,
            2,
        )

        print()
        print("==============================")
        print("TOP RETRIEVED DOCUMENTS")
        print("==============================")

        for i, item in enumerate(top_results, start=1):
            print()
            print(f"Rank {i}")
            print(item.get("metadata", {}))
            print("Semantic Score:", item.get("semantic_score", 0))
            print("Keyword Score:", item.get("keyword_score", 0))
            print("Metadata Score:", item.get("metadata_score", 0))
            print("Domain Score:", item.get("domain_score", 0))
            print("Legal Issue Score:", item.get("legal_issue_score", 0))
            print("Final Score:", item.get("final_score", 0))

        if not top_results:
            return {
                "answer": (
                    "I couldn't find sufficient information "
                    "in the uploaded legal documents."
                ),
                "confidence": "Low",
                "retrieval_time": retrieval_time,
                "llm_time": 0,
                "total_time": retrieval_time,
                "sources": [],
            }

        prompt = self.prompt_builder.build(
            question=retrieval_question,
            retrieved_results=top_results,
            domain=selected_domain,
            issue_type=selected_issue,
        )

        explanation_instruction = '''
STRICT GROUNDED LEGAL EXPLANATION MODE:

Use ONLY the retrieved legal context as the legal source.

Return exactly these five sections:

Plain Language Explanation
Relevant Legal Provision
Possible Rights / Remedies
What the Citizen Can Do
Important Note

For Possible Rights / Remedies, preserve remedies explicitly
stated in the retrieved text. Do not replace a supported remedy
with an uncertainty statement.

For What the Citizen Can Do, do not invent authorities,
procedures, deadlines, portals, helplines, or banking/payment
instructions. If the retrieved text does not specify a procedure,
say that it does not specify the procedure.

Do not introduce legal sections absent from the retrieved context.
Do not guarantee a legal outcome.

Do not use Markdown heading markers such as ### or **.
'''

        prompt = prompt + "\n\n" + explanation_instruction

        llm_start = time.time()

        answer = self.llm.generate(prompt).strip()

        if not answer:
            answer = (
                "I could not generate a grounded explanation from "
                "the retrieved legal documents."
            )

        llm_time = round(
            time.time() - llm_start,
            2,
        )

        heading_names = [
            "Plain Language Explanation",
            "Relevant Legal Provision",
            "Why It May Be Relevant",
            "Possible Rights / Remedies",
            "What the Citizen Can Do",
            "What the citizen should do",
            "Important Note",
        ]

        for heading in heading_names:
            answer = re.sub(
                rf"^\s*#+\s*{re.escape(heading)}\s*:?\s*$",
                heading,
                answer,
                flags=re.IGNORECASE | re.MULTILINE,
            )

        answer = re.sub(
            r"^\s*#{1,6}\s*$",
            "",
            answer,
            flags=re.MULTILINE,
        )

        answer = re.sub(
            r"What the citizen should do",
            "What the Citizen Can Do",
            answer,
            flags=re.IGNORECASE,
        )

        answer = self._validate_grounding(
            answer,
            top_results,
        )

        # Exactly one deterministic disclaimer.
        answer = re.sub(
            r"(?ims)\n*^\s*Important Note\s*:?\s*$.*?(?=^\s*"
            r"(?:Plain Language Explanation|Relevant Legal Provision|"
            r"Possible Rights / Remedies|What the Citizen Can Do|"
            r"Important Note)\s*:?\s*$|\Z)",
            "",
            answer,
        ).strip()

        answer = (
            answer.rstrip()
            + "\n\nImportant Note\n"
            + "This is general legal information and is not a "
              "substitute for advice from a qualified legal "
              "professional."
        )

        score = top_results[0].get("final_score", 0)

        if score >= 0.75:
            confidence = "High"
        elif score >= 0.50:
            confidence = "Medium"
        else:
            confidence = "Low"

        sources = []
        seen = set()

        for item in top_results:
            metadata = item.get("metadata", {}) or {}

            key = (
                metadata.get("act"),
                metadata.get("section"),
            )

            if key in seen:
                continue

            seen.add(key)

            sources.append({
                "act": metadata.get("act"),
                "chapter": metadata.get("chapter"),
                "section": metadata.get("section"),
                "title": metadata.get("title"),
                "domain": metadata.get("domain"),
                "semantic_score": item.get("semantic_score", 0),
                "keyword_score": item.get("keyword_score", 0),
                "metadata_score": item.get("metadata_score", 0),
                "domain_score": item.get("domain_score", 0),
                "legal_issue_score": item.get("legal_issue_score", 0),
                "final_score": item.get("final_score", 0),
            })

        return {
            "answer": answer,
            "confidence": confidence,
            "retrieval_time": retrieval_time,
            "llm_time": llm_time,
            "total_time": round(
                retrieval_time + llm_time,
                2,
            ),
            "sources": sources,
        }


legal_assistant = LegalAssistant()
