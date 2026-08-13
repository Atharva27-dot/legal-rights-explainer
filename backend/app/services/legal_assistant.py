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

    def ask(self, question):

        # =====================================
        # STEP 1 : Retrieve Documents
        # =====================================

        retrieval_start = time.time()

        results = self.retriever.search(question)

        ranked_results = self.ranker.rank(question, results)

        top_results = ranked_results[:3]

        retrieval_time = round(
            time.time() - retrieval_start,
            2
        )

        print("\n==============================")
        print("TOP RETRIEVED DOCUMENTS")
        print("==============================")

        for i, item in enumerate(top_results, start=1):

            print(f"\nRank {i}")

            print(item["metadata"])

            print("Final Score :", item["final_score"])

        # =====================================
        # STEP 2 : Prompt
        # =====================================

        prompt = self.prompt_builder.build(

            question,

            top_results

        )

        # =====================================
        # STEP 3 : LLM
        # =====================================

        llm_start = time.time()

        answer = self.llm.generate(prompt).strip()

        llm_time = round(
            time.time() - llm_start,
            2
        )

        # =====================================
        # STEP 4 : Clean Answer
        # =====================================

        answer = re.sub(
            r"##\s*Plain Language Explanation",
            "",
            answer,
            flags=re.IGNORECASE
        )

        answer = re.sub(
            r"##\s*What the citizen should do",
            "\n\nWhat the citizen should do:\n",
            answer,
            flags=re.IGNORECASE
        )

        answer = answer.strip()

        # =====================================
        # STEP 5 : Confidence
        # =====================================

        score = top_results[0]["final_score"]

        if score >= 0.75:

            confidence = "High"

        elif score >= 0.55:

            confidence = "Medium"

        else:

            confidence = "Low"

        # =====================================
        # STEP 6 : Sources
        # =====================================

        sources = []

        seen = set()

        for item in top_results:

            metadata = item["metadata"]

            key = (
                metadata.get("act"),
                metadata.get("section")
            )

            if key in seen:
                continue

            seen.add(key)

            sources.append({

                "act": metadata.get("act"),

                "chapter": metadata.get("chapter"),

                "section": metadata.get("section"),

                "title": metadata.get("title")

            })

        # =====================================
        # STEP 7 : Return JSON
        # =====================================

        return {

            "answer": answer,

            "confidence": confidence,

            "retrieval_time": retrieval_time,

            "llm_time": llm_time,

            "total_time": round(
                retrieval_time + llm_time,
                2
            ),

            "sources": sources

        }