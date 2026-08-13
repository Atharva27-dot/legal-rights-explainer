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
    # LEGAL ISSUE CLASSIFICATION
    # ============================================================

    def classify_legal_issue(self, request, top_results):

        text = " ".join([
            str(getattr(request, "product", "")),
            str(getattr(request, "seller", "")),
            str(getattr(request, "problem", "")),
            str(getattr(request, "remedy", ""))
        ]).lower()

        # --------------------------------------------------------
        # Cyber / Online Fraud
        # --------------------------------------------------------

        cyber_keywords = [
            "cyber fraud",
            "online fraud",
            "upi fraud",
            "upi",
            "online scam",
            "cyber crime",
            "cybercrime",
            "phishing",
            "otp fraud",
            "otp scam",
            "bank fraud",
            "credit card fraud",
            "debit card fraud",
            "unauthorized transaction",
            "unauthorised transaction",
            "online transaction",
            "hacked account",
            "account hacked",
            "digital fraud",
            "internet fraud"
        ]

        if any(keyword in text for keyword in cyber_keywords):

            return {
                "category": "Cyber / Online Fraud",
                "issue": "Online or electronic transaction related dispute",
                "applicable_act": self._get_retrieved_act(
                    top_results,
                    fallback="No matching cyber law identified in the current knowledge base"
                ),
                "rights": [
                    "Right to seek appropriate redressal",
                    "Right to protection against fraudulent transactions"
                ]
            }

        # --------------------------------------------------------
        # Insurance
        # --------------------------------------------------------

        insurance_keywords = [
            "insurance",
            "insurance company",
            "insurance claim",
            "claim rejected",
            "claim rejection",
            "policy claim",
            "health insurance",
            "life insurance",
            "vehicle insurance",
            "motor insurance",
            "premium",
            "policyholder",
            "insurer"
        ]

        if any(keyword in text for keyword in insurance_keywords):

            return {
                "category": "Insurance / Financial Service",
                "issue": "Insurance claim or policy related dispute",
                "applicable_act": self._get_retrieved_act(
                    top_results,
                    fallback="No matching insurance law identified in the current knowledge base"
                ),
                "rights": [
                    "Right to seek grievance redressal",
                    "Right to receive services as agreed under the policy"
                ]
            }

        # --------------------------------------------------------
        # Employment / Labour
        # --------------------------------------------------------

        employment_keywords = [
            "salary",
            "wages",
            "employer",
            "employee",
            "employment",
            "job",
            "termination",
            "wrongful termination",
            "workplace",
            "labour",
            "labor",
            "overtime",
            "bonus",
            "unpaid salary"
        ]

        if any(keyword in text for keyword in employment_keywords):

            return {
                "category": "Employment / Labour",
                "issue": "Employment or workplace related dispute",
                "applicable_act": self._get_retrieved_act(
                    top_results,
                    fallback="No matching labour law identified in the current knowledge base"
                ),
                "rights": [
                    "Right to seek appropriate grievance redressal",
                    "Right to receive legally applicable employment benefits"
                ]
            }

        # --------------------------------------------------------
        # Motor Vehicle / Road Accident
        # --------------------------------------------------------

        motor_keywords = [
            "road accident",
            "road accident",
            "car accident",
            "bike accident",
            "vehicle accident",
            "motor accident",
            "motor vehicle",
            "driving",
            "driver",
            "traffic accident",
            "hit and run",
            "hit-and-run",
            "vehicle damage"
        ]

        if any(keyword in text for keyword in motor_keywords):

            return {
                "category": "Motor Vehicle / Road Accident",
                "issue": "Motor vehicle or road accident related dispute",
                "applicable_act": self._get_retrieved_act(
                    top_results,
                    fallback="No matching motor vehicle law identified in the current knowledge base"
                ),
                "rights": [
                    "Right to seek compensation where legally applicable",
                    "Right to seek appropriate redressal"
                ]
            }

        # --------------------------------------------------------
        # Contract / Service
        # --------------------------------------------------------

        contract_keywords = [
            "contract",
            "agreement",
            "breach of contract",
            "breach",
            "service agreement",
            "terms and conditions",
            "advance payment",
            "refund",
            "service provider",
            "professional service",
            "not delivered",
            "service not provided"
        ]

        if any(keyword in text for keyword in contract_keywords):

            return {
                "category": "Contract / Service Dispute",
                "issue": "Contractual or service-related dispute",
                "applicable_act": self._get_retrieved_act(
                    top_results,
                    fallback="No matching contract law identified in the current knowledge base"
                ),
                "rights": [
                    "Right to seek appropriate redressal",
                    "Right to receive the service agreed upon"
                ]
            }

        # --------------------------------------------------------
        # Consumer Goods
        # --------------------------------------------------------

        consumer_goods_keywords = [
            "product",
            "phone",
            "mobile",
            "laptop",
            "computer",
            "television",
            "tv",
            "refrigerator",
            "washing machine",
            "camera",
            "headphone",
            "earphone",
            "electronic",
            "defective",
            "damaged",
            "wrong product",
            "wrong item",
            "fake product",
            "counterfeit",
            "replacement",
            "warranty",
            "amazon",
            "flipkart",
            "online shopping",
            "ecommerce",
            "e-commerce"
        ]

        if any(keyword in text for keyword in consumer_goods_keywords):

            return {
                "category": "Consumer Goods",
                "issue": "Defective, damaged, incorrect or misrepresented consumer product",
                "applicable_act": self._get_retrieved_act(
                    top_results,
                    fallback="Consumer Protection Act, 2019"
                ),
                "rights": [
                    "Right to Safety",
                    "Right to Information",
                    "Right to Redressal"
                ]
            }

        # --------------------------------------------------------
        # Consumer Service
        # --------------------------------------------------------

        service_keywords = [
            "service",
            "service provider",
            "poor service",
            "bad service",
            "deficiency in service",
            "service deficiency",
            "not providing service",
            "service not delivered"
        ]

        if any(keyword in text for keyword in service_keywords):

            return {
                "category": "Consumer Service",
                "issue": "Deficiency or failure in consumer service",
                "applicable_act": self._get_retrieved_act(
                    top_results,
                    fallback="Consumer Protection Act, 2019"
                ),
                "rights": [
                    "Right to Information",
                    "Right to be Heard",
                    "Right to Redressal"
                ]
            }

        # --------------------------------------------------------
        # Fallback
        # --------------------------------------------------------

        return {
            "category": "General Legal Issue",
            "issue": "The legal domain could not be confidently classified",
            "applicable_act": self._get_retrieved_act(
                top_results,
                fallback="Not established from the current knowledge base"
            ),
            "rights": []
        }

    # ============================================================
    # GET ACT FROM RETRIEVED DOCUMENT
    # ============================================================

    def _get_retrieved_act(self, top_results, fallback):

        for item in top_results:

            metadata = item.get("metadata", {})

            act = metadata.get("act")

            if act:
                return act

        return fallback

    # ============================================================
    # GENERATE COMPLAINT
    # ============================================================

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
        # STEP 2 : Legal Issue Classification
        # =====================================

        case_analysis = self.classify_legal_issue(
            request,
            top_results
        )

        # =====================================
        # STEP 3 : Prepare Context
        # =====================================

        context = "\n\n".join(
            item["document"]
            for item in top_results
        )

        # =====================================
        # STEP 4 : Build Complaint Prompt
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
        # STEP 5 : LLM
        # =====================================

        llm_start = time.time()

        complaint = self.llm.generate(prompt).strip()

        llm_time = round(
            time.time() - llm_start,
            2
        )

        # =====================================
        # STEP 5.1 : Clean LLM Output
        # =====================================

        # Remove markdown headings
        complaint = re.sub(
            r"^#+\s*",
            "",
            complaint,
            flags=re.MULTILINE
        ).strip()

        # If the model accidentally adds Case Analysis,
        # keep only the actual complaint.
        complaint_markers = [
            "To,",
            "To :",
            "To:",
            "To\n"
        ]

        complaint_start = -1

        for marker in complaint_markers:

            position = complaint.find(marker)

            if position != -1:

                complaint_start = position
                break

        if complaint_start != -1:

            complaint = complaint[
                complaint_start:
            ].strip()

        # =====================================
        # STEP 6 : Confidence
        # =====================================

        if top_results:

            score = top_results[0]["final_score"]

        else:

            score = 0

        if score >= 0.75:

            confidence = "High"

        elif score >= 0.55:

            confidence = "Medium"

        else:

            confidence = "Low"

        # =====================================
        # STEP 7 : Readiness Score
        # =====================================

        readiness = readiness_service.calculate(
            request
        )

        # =====================================
        # STEP 8 : Supporting Documents
        # =====================================

        supporting_documents = [
            "Purchase Invoice",
            "Warranty Card (if applicable)",
            "Photos / Screenshots",
            "Communication with Seller / Service Provider"
        ]

        # =====================================
        # STEP 9 : Sources
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
        # STEP 10 : Return JSON
        # =====================================

        return {

            "case_analysis": {

                "category": case_analysis["category"],

                "applicable_act": case_analysis[
                    "applicable_act"
                ],

                "rights": case_analysis["rights"],

                "recommended_remedy": request.remedy,

                "legal_readiness": readiness["status"],

                "supporting_documents":
                    supporting_documents

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