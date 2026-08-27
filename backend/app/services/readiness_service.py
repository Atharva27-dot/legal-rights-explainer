import re


class ReadinessService:

    def __init__(self):
        # General evidence that can apply across domains.
        self.general_evidence = {
            "Communication Evidence": [
                "email", "mail", "chat", "whatsapp", "message",
                "messages", "call", "recording", "notice"
            ],
            "Complaint / Reference": [
                "complaint", "grievance", "ticket", "reference number",
                "case id", "support ticket"
            ],
        }

        self.consumer_evidence = {
            "Purchase / Payment Proof": [
                "invoice", "receipt", "bill", "purchase proof",
                "order confirmation", "order id", "order number",
                "payment proof", "payment receipt", "amount paid",
                "total amount", "price", "paid"
            ],
            "Product Evidence": [
                "photo", "photos", "photograph", "photographs",
                "image", "images", "screenshot", "screenshots",
                "video", "unboxing video", "product image"
            ],
            "Warranty / Policy Documents": [
                "warranty", "guarantee", "warranty card",
                "warranty period", "return policy", "replacement policy"
            ],
        }

        self.cyber_evidence = {
            "Transaction Evidence": [
                "transaction", "transaction id", "transaction number",
                "transaction reference", "upi id", "upi transaction",
                "bank transaction", "bank statement"
            ],
            "Digital Evidence": [
                "screenshot", "screenshots", "screen recording",
                "email", "sms", "message", "notification",
                "ip address", "device", "login"
            ],
            "Financial Loss Evidence": [
                "amount", "₹", "rs", "rupees", "money",
                "loss", "transferred", "debited"
            ],
            "Bank / Payment Provider Communication": [
                "bank complaint", "bank", "upi complaint",
                "payment provider", "payment app", "customer support"
            ],
            "Cyber Complaint / Reference": [
                "cyber complaint", "cybercrime", "cyber crime",
                "complaint number", "ticket", "reference number"
            ],
        }

        self.contract_evidence = {
            "Agreement / Contract": [
                "agreement", "contract", "terms",
                "terms and conditions", "signed agreement"
            ],
            "Payment Evidence": [
                "invoice", "receipt", "payment", "transaction",
                "payment proof"
            ],
        }

        self.employment_evidence = {
            "Employment Proof": [
                "appointment letter", "employment contract",
                "employee id", "salary slip", "salary slips",
                "payslip", "payslips", "offer letter"
            ],
            "Communication Evidence": [
                "email", "mail", "message", "whatsapp", "notice",
                "hr communication"
            ],
            "Workplace Evidence": [
                "attendance", "timesheet", "hr complaint",
                "termination letter", "workplace record"
            ],
        }

        self.motor_evidence = {
            "Vehicle / Licence Documents": [
                "driving licence", "driver licence", "vehicle registration",
                "registration certificate", "rc book", "insurance"
            ],
            "Accident Evidence": [
                "accident photograph", "accident photo", "damage photo",
                "police report", "accident report", "medical report"
            ],
            "Communication Evidence": [
                "email", "message", "notice", "claim communication"
            ],
        }

        self.insurance_evidence = {
            "Policy / Agreement": [
                "insurance policy", "policy document", "policy number",
                "insurance agreement"
            ],
            "Payment / Premium Evidence": [
                "premium", "premium receipt", "payment receipt",
                "payment record"
            ],
            "Claim Evidence": [
                "claim", "claim form", "claim document",
                "claim rejection", "rejection letter"
            ],
            "Communication Evidence": [
                "email", "mail", "message", "notice",
                "insurer communication"
            ],
        }

    # ============================================================
    # DOMAIN-SPECIFIC EVIDENCE
    # ============================================================

    def _get_domain_evidence(self, domain):
        domain_lower = str(domain or "").lower()

        if "consumer" in domain_lower:
            return self.consumer_evidence

        if (
            "cyber" in domain_lower
            or "information technology" in domain_lower
            or domain_lower == "it"
        ):
            return self.cyber_evidence

        if "contract" in domain_lower:
            return self.contract_evidence

        if (
            "employment" in domain_lower
            or "labour" in domain_lower
            or "labor" in domain_lower
        ):
            return self.employment_evidence

        if "motor" in domain_lower:
            return self.motor_evidence

        if "insurance" in domain_lower or "financial" in domain_lower:
            return self.insurance_evidence

        return {}

    # ============================================================
    # TEXT HELPERS
    # ============================================================

    @staticmethod
    def _read_evidence_value(evidence, field, default=""):
        if isinstance(evidence, dict):
            return evidence.get(field, default)
        return getattr(evidence, field, default)

    def _get_complaint_text(self, complaint):
        fields = [
            "name", "city", "product", "seller", "problem",
            "remedy", "purchase_date", "bank", "transaction_date",
            "amount"
        ]

        parts = []

        for field in fields:
            value = getattr(complaint, field, "")
            if value:
                parts.append(str(value))

        return " ".join(parts).lower()

    def _get_evidence_text(self, complaint):
        """
        Use the actual extracted evidence text and filenames.
        This is the key improvement over the old detector, which only
        inspected the problem/remedy fields.
        """
        parts = []

        for evidence in getattr(complaint, "evidence", []) or []:
            filename = self._read_evidence_value(
                evidence, "filename", ""
            )
            extracted_text = self._read_evidence_value(
                evidence, "extracted_text", ""
            )

            if filename:
                parts.append(str(filename))

            if extracted_text:
                parts.append(str(extracted_text))

        return " ".join(parts).lower()

    @staticmethod
    def _keyword_found(text, keyword):
        keyword = str(keyword or "").strip().lower()

        if not keyword:
            return False

        # Word/phrase matching avoids accidental matches such as
        # "mail" inside an unrelated word.
        pattern = r"(?<![a-z0-9])" + re.escape(keyword) + r"(?![a-z0-9])"
        return re.search(pattern, text, flags=re.IGNORECASE) is not None

    # ============================================================
    # DETECT EVIDENCE
    # ============================================================

    def _detect_evidence(self, complaint, evidence_groups):
        complaint_text = self._get_complaint_text(complaint)
        evidence_text = self._get_evidence_text(complaint)

        # Evidence uploaded by the citizen is the strongest signal for
        # an evidence group. Case fields are used only where they
        # genuinely describe evidence (e.g. transaction/order details).
        detected = []
        missing = []

        for group, keywords in evidence_groups.items():
            evidence_found = any(
                self._keyword_found(evidence_text, keyword)
                for keyword in keywords
            )

            # Allow the user's case fields to identify evidence only when
            # the field itself is an evidence-like fact.
            case_found = False

            if group in {
                "Communication Evidence",
                "Complaint / Reference",
                "Transaction Evidence",
            }:
                case_found = any(
                    self._keyword_found(complaint_text, keyword)
                    for keyword in keywords
                )

            if evidence_found or case_found:
                detected.append(group)
            else:
                missing.append(group)

        return detected, missing

    # ============================================================
    # BASIC INFORMATION SCORE
    # ============================================================

    def _calculate_basic_score(self, complaint, recommendations):
        score = 0

        checks = [
            ("name", 5, "Provide your full name."),
            ("city", 5, "Mention your city."),
            ("product", 5, "Specify the product or service involved."),
            (
                "seller",
                5,
                "Mention the seller, service provider, bank or other relevant party."
            ),
        ]

        for field, points, message in checks:
            if str(getattr(complaint, field, "")).strip():
                score += points
            else:
                recommendations.append(message)

        if getattr(complaint, "purchase_date", None):
            score += 5
        else:
            recommendations.append(
                "Provide the relevant purchase or incident date."
            )

        return score

    # ============================================================
    # PROBLEM SCORE
    # ============================================================

    def _calculate_problem_score(self, complaint, recommendations):
        problem_text = str(
            getattr(complaint, "problem", "")
        ).strip()

        if len(problem_text) >= 100:
            return 20

        if len(problem_text) >= 50:
            return 15

        if len(problem_text) >= 25:
            recommendations.append(
                "Describe what happened in more detail, including "
                "when and how the incident occurred."
            )
            return 10

        recommendations.append(
            "Provide a detailed description of the problem."
        )
        return 5

    # ============================================================
    # REMEDY SCORE
    # ============================================================

    def _calculate_remedy_score(self, complaint, recommendations):
        remedy = str(
            getattr(complaint, "remedy", "")
        ).strip()

        if remedy:
            return 10

        recommendations.append(
            "Specify the remedy you are seeking."
        )
        return 0

    # ============================================================
    # EVIDENCE SCORE
    # ============================================================

    def _calculate_evidence_score(
        self,
        detected_evidence,
        missing_evidence,
        domain
    ):
        total_groups = len(detected_evidence) + len(missing_evidence)

        if total_groups == 0:
            return 0

        # Evidence contributes a maximum of 40 points, preserving the
        # existing scoring model.
        return round(
            (len(detected_evidence) / total_groups) * 40
        )

    # ============================================================
    # RECOMMENDATIONS
    # ============================================================

    def _generate_evidence_recommendations(
        self,
        missing_evidence,
        domain
    ):
        domain_lower = str(domain or "").lower()

        if "consumer" in domain_lower:
            mapping = {
                "Purchase / Payment Proof":
                    "Keep the invoice, receipt, order confirmation or payment proof.",
                "Product Evidence":
                    "Keep photographs, videos or screenshots showing the product problem.",
                "Warranty / Policy Documents":
                    "Keep the warranty card or applicable warranty/policy documents.",
                "Communication Evidence":
                    "Preserve emails, messages, chats or call records with the seller.",
                "Complaint / Reference":
                    "Keep any complaint, grievance, ticket or reference number.",
            }

        elif "cyber" in domain_lower:
            mapping = {
                "Transaction Evidence":
                    "Preserve the bank statement, UPI transaction ID and transaction/reference number.",
                "Digital Evidence":
                    "Preserve screenshots, SMS alerts, emails, login notifications and other digital evidence.",
                "Financial Loss Evidence":
                    "Document the amount transferred or financial loss with supporting records.",
                "Bank / Payment Provider Communication":
                    "Keep records of complaints or communication with your bank or payment provider.",
                "Cyber Complaint / Reference":
                    "Keep any cybercrime complaint number, ticket ID or reference number.",
                "Communication Evidence":
                    "Preserve relevant emails, messages or chats.",
                "Complaint / Reference":
                    "Keep complaint, ticket or reference numbers.",
            }

        elif "contract" in domain_lower:
            mapping = {
                "Agreement / Contract":
                    "Keep the signed agreement, contract or applicable terms.",
                "Payment Evidence":
                    "Keep invoices, receipts and payment records.",
                "Communication Evidence":
                    "Preserve communication between the parties.",
                "Complaint / Reference":
                    "Keep any notice, complaint or reference number.",
            }

        elif (
            "employment" in domain_lower
            or "labour" in domain_lower
            or "labor" in domain_lower
        ):
            mapping = {
                "Employment Proof":
                    "Keep your appointment letter, employment contract, salary slips or other employment records.",
                "Communication Evidence":
                    "Preserve emails, messages, notices and communication with the employer or HR.",
                "Workplace Evidence":
                    "Keep attendance, timesheets, HR complaints and relevant workplace records.",
                "Complaint / Reference":
                    "Keep any HR complaint, grievance or reference number.",
            }

        elif "motor" in domain_lower:
            mapping = {
                "Vehicle / Licence Documents":
                    "Keep your driving licence, registration and relevant vehicle documents.",
                "Accident Evidence":
                    "Keep photographs, police/accident reports and relevant medical records.",
                "Communication Evidence":
                    "Preserve communication with the insurer or other relevant party.",
            }

        elif "insurance" in domain_lower or "financial" in domain_lower:
            mapping = {
                "Policy / Agreement":
                    "Keep the insurance policy, policy number and applicable agreement.",
                "Payment / Premium Evidence":
                    "Keep premium receipts and payment records.",
                "Claim Evidence":
                    "Keep claim documents and any claim rejection communication.",
                "Communication Evidence":
                    "Preserve communication with the insurer or provider.",
            }

        else:
            mapping = {}

        return [
            mapping[item]
            for item in missing_evidence
            if item in mapping
        ]

    # ============================================================
    # STATUS
    # ============================================================

    def _get_status(self, score):
        if score >= 85:
            return "Strong Case"

        if score >= 70:
            return "Good Case"

        if score >= 50:
            return "Moderate Case"

        return "Weak Case"

    # ============================================================
    # MAIN CALCULATION
    # ============================================================

    def calculate(self, complaint, domain=None):
        recommendations = []

        domain_evidence = self._get_domain_evidence(domain)

        evidence_groups = dict(self.general_evidence)
        evidence_groups.update(domain_evidence)

        detected_evidence, missing_evidence = self._detect_evidence(
            complaint,
            evidence_groups
        )

        score = self._calculate_basic_score(
            complaint,
            recommendations
        )

        score += self._calculate_problem_score(
            complaint,
            recommendations
        )

        score += self._calculate_remedy_score(
            complaint,
            recommendations
        )

        score += self._calculate_evidence_score(
            detected_evidence,
            missing_evidence,
            domain
        )

        recommendations.extend(
            self._generate_evidence_recommendations(
                missing_evidence,
                domain
            )
        )

        score = min(100, max(0, score))
        status = self._get_status(score)

        unique_recommendations = []
        for recommendation in recommendations:
            if recommendation not in unique_recommendations:
                unique_recommendations.append(recommendation)

        return {
            "score": score,
            "status": status,
            "recommendations": unique_recommendations,
            "evidence": {
                "detected": detected_evidence,
                "missing": missing_evidence,
            },
            "domain": domain,
        }


readiness_service = ReadinessService()
