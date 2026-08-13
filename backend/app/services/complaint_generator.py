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

    def generate(self, request):

        # =====================================
        # STEP 1 : Retrieve Documents
        # =====================================

        retrieval_start = time.time()

        query = f"""
        Product: {request.product}

        Seller: {request.seller}

        Problem: {request.problem}

        Remedy: {request.remedy}
        """

        results = self.retriever.search(query)

        ranked_results = self.ranker.rank(query, results)

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
        # STEP 2 : Prepare Context
        # =====================================

        context = "\n\n".join(
            item["document"]
            for item in top_results
        )

        # =====================================
        # STEP 3 : Build Prompt
        # =====================================

        prompt = build_complaint_prompt(

            context=context,

            name=request.name,

            product=request.product,

            seller=request.seller,

            purchase_date=request.purchase_date,

            city=request.city,

            problem=request.problem,

            remedy=request.remedy,

        )

        # =====================================
        # STEP 4 : LLM
        # =====================================

        llm_start = time.time()

        complaint = self.llm.generate(prompt).strip()

        llm_time = round(
            time.time() - llm_start,
            2
        )

        # Remove Markdown headings if present
        complaint = re.sub(
            r"^#+",
            "",
            complaint,
            flags=re.MULTILINE
        ).strip()

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
# STEP 5.5 : Readiness Score
# =====================================

        readiness = readiness_service.calculate(request)

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

            "case_analysis": {

                "category": "Consumer Goods",

                "applicable_act": "Consumer Protection Act, 2019",

                "rights": [

                    "Right to Safety",

                    "Right to Information",

                    "Right to Redressal"

                ],

                "recommended_remedy": request.remedy,

                "legal_readiness": readiness["status"],

                "supporting_documents": [

                    "Purchase Invoice",

                    "Warranty Card (if applicable)",

                    "Photos of Product",

                    "Communication with Seller"

                ]

            },

            "complaint": complaint,

            "confidence": confidence,

            "readiness": readiness,

            "retrieval_time": retrieval_time,

            "llm_time": llm_time,

            "total_time": round(

                retrieval_time + llm_time,

                2

            ),

            "sources": sources

        }


complaint_generator = ComplaintGenerator()