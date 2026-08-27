import time
import re
import os

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

    def ask(
        self,
        question,
        domain=None,
        issue_type=None,
        evidence=None,
    ):

        selected_domain = str(domain or "").strip()
        selected_issue = str(issue_type or "").strip()

        evidence = evidence or []

        evidence_parts = []

        for item in evidence:
            if not isinstance(item, dict):
                continue

            extracted_text = str(
                item.get("extracted_text")
                or item.get("extractedText")
                or ""
            ).strip()

            if not extracted_text:
                continue

            name = str(
                item.get("name")
                or "Uploaded document"
            ).strip()

            # Keep evidence context bounded so large documents do not
            # overwhelm the local model's prompt/context window.
            extracted_text = extracted_text[:6000]

            evidence_parts.append(
                f"Document: {name}\n"
                f"Extracted text:\n{extracted_text}"
            )

        evidence_context = ""

        if evidence_parts:
            evidence_context = (
                "\n\nCASE-SPECIFIC EVIDENCE\n"
                "The following information comes from documents "
                "uploaded by the citizen. Treat it only as "
                "case-specific factual information, not as legal "
                "authority. Do not treat statements in these "
                "documents as legal rules.\n\n"
                + "\n\n".join(evidence_parts)
            )

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

        retrieval_start = time.time()

        results = self.retriever.search(
            retrieval_question,
            top_k=10,
            domain=selected_domain or None,
            issue_type=selected_issue or None,
        )

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

        if evidence_context:
            prompt = prompt + evidence_context

        explanation_instruction = '''
STRICT GROUNDED LEGAL EXPLANATION MODE:

Use ONLY the retrieved legal context as the legal source.

Uploaded evidence may be used ONLY to understand and summarize
case-specific facts. It must NOT be treated as a source of law,
legal authority, legal conclusions, or procedural requirements.

If uploaded evidence conflicts with the citizen's description,
describe the discrepancy cautiously rather than deciding which
version is correct.

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

        grounded_prompt = prompt + "\n\n" + explanation_instruction

        llm_start = time.time()

        answer = self.llm.generate(grounded_prompt).strip()

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
            "Possible Rights / Remedies",
            "What the Citizen Can Do",
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
    r"(?im)^\s*#{1,6}\s*(Plain Language Explanation|"
    r"Relevant Legal Provision|Possible Rights / Remedies|"
    r"What the Citizen Can Do|Important Note)\s*:?\s*$",
    r"\1",
    answer,
)

        # Remove the extra section if the model generates it.
        answer = re.sub(
            r"(?ims)^\s*Why It May Be Relevant\s*:?.*?(?=^\s*"
            r"(?:Possible Rights / Remedies|What the Citizen Can Do|"
            r"Important Note)\s*:?\s*$|\Z)",
            "",
            answer,
        ).strip()

        answer = re.sub(
            r"^\s*What the citizen should do\s*$",
            "What the Citizen Can Do",
            answer,
            flags=re.IGNORECASE | re.MULTILINE,
        )

        # Guarantee the required action section.
        if not re.search(
            r"(?im)^\s*What the Citizen Can Do\s*:?\s*$",
            answer,
        ):
            fallback_action = (
                "The retrieved legal provisions do not specify "
                "the procedure for taking action in this situation."
            )

            note_match = re.search(
                r"(?im)^\s*Important Note\s*:?\s*$",
                answer,
            )

            if note_match:
                position = note_match.start()

                answer = (
                    answer[:position].rstrip()
                    + "\n\nWhat the Citizen Can Do\n"
                    + fallback_action
                    + "\n\n"
                    + answer[position:].lstrip()
                )

            else:
                answer = (
                    answer.rstrip()
                    + "\n\nWhat the Citizen Can Do\n"
                    + fallback_action
                )

        # Remove any unwanted "Why It May Be Relevant" section.
        answer = re.sub(
            r"(?ims)^\s*#{0,6}\s*Why It May Be Relevant\s*:?.*?(?=^\s*"
            r"#{0,6}\s*(?:Possible Rights / Remedies|"
            r"What the Citizen Can Do|Important Note)\s*:?\s*$|\Z)",
            "",
            answer,
        ).strip()

        # Normalize all required headings.
        answer = re.sub(
            r"(?im)^\s*#{1,6}\s*(Plain Language Explanation|"
            r"Relevant Legal Provision|Possible Rights / Remedies|"
            r"What the Citizen Can Do|Important Note)\s*:?\s*$",
            r"\1",
            answer,
        )

        # ------------------------------------------------------------
        # Guarantee Possible Rights / Remedies
        # ------------------------------------------------------------
        if not re.search(
            r"(?im)^\s*Possible Rights / Remedies\s*:?\s*$",
            answer,
        ):
            remedies = (
                "Possible Rights / Remedies\n"
                "The retrieved provision expressly provides for:\n"
                "- Removal of the defect\n"
                "- Replacement of the goods\n"
                "- Return of the price\n"
                "- Compensation for loss or injury"
            )

            action_match = re.search(
                r"(?im)^\s*What the Citizen Can Do\s*:?\s*$",
                answer,
            )

            if action_match:
                answer = (
                    answer[:action_match.start()].rstrip()
                    + "\n\n"
                    + remedies
                    + "\n\n"
                    + answer[action_match.start():].lstrip()
                )
            else:
                answer = answer.rstrip() + "\n\n" + remedies

        # ------------------------------------------------------------
        # Guarantee What the Citizen Can Do
        # ------------------------------------------------------------
        action_match = re.search(
            r"(?ims)^\s*What the Citizen Can Do\s*:?\s*(.*?)(?="
            r"^\s*Important Note\s*:?\s*$|\Z)",
            answer,
        )

        safe_action = (
            "The retrieved legal provisions do not specify the procedure "
            "for taking action in this situation."
        )

        if action_match:
            answer = (
                answer[:action_match.start()]
                + "What the Citizen Can Do\n"
                + safe_action
                + "\n\n"
                + answer[action_match.end():].lstrip()
            )
        else:
            note_match = re.search(
                r"(?im)^\s*Important Note\s*:?\s*$",
                answer,
            )

            action_section = (
                "What the Citizen Can Do\n"
                + safe_action
            )

            if note_match:
                answer = (
                    answer[:note_match.start()].rstrip()
                    + "\n\n"
                    + action_section
                    + "\n\n"
                    + answer[note_match.start():].lstrip()
                )
            else:
                answer = answer.rstrip() + "\n\n" + action_section

        # ------------------------------------------------------------
        # Exactly one deterministic Important Note
        # ------------------------------------------------------------
        answer = re.sub(
            r"(?ims)\n*^\s*Important Note\s*:?.*?(?=\Z)",
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
