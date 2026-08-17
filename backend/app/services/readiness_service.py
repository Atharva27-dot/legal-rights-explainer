class ReadinessService:

    def __init__(self):

        # ========================================================
        # GENERAL EVIDENCE
        # ========================================================

        self.general_evidence = {

            "Identity / Basic Information": [
                "name",
                "address",
                "city"
            ],

            "Problem Description": [
                "problem",
                "issue",
                "incident"
            ],

            "Remedy Requested": [
                "remedy",
                "refund",
                "replacement",
                "compensation",
                "repair"
            ],

            "Communication Evidence": [
                "email",
                "mail",
                "chat",
                "chats",
                "whatsapp",
                "message",
                "messages",
                "call",
                "recording"
            ],

            "Complaint / Reference": [
                "complaint",
                "grievance",
                "ticket",
                "reference number"
            ]
        }

        # ========================================================
        # CONSUMER PROTECTION EVIDENCE
        # ========================================================

        self.consumer_evidence = {

            "Purchase / Payment Proof": [
                "invoice",
                "receipt",
                "bill",
                "purchase proof",
                "order confirmation",
                "order id",
                "order number",
                "payment proof",
                "payment receipt"
            ],

            "Product Evidence": [
                "photo",
                "photos",
                "photograph",
                "photographs",
                "image",
                "images",
                "video",
                "unboxing video"
            ],

            "Warranty / Policy Documents": [
                "warranty",
                "guarantee",
                "warranty card"
            ]
        }

        # ========================================================
        # CYBER / IT EVIDENCE
        # ========================================================

        self.cyber_evidence = {

            "Transaction Evidence": [
                "transaction",
                "transaction id",
                "transaction number",
                "transaction reference",
                "upi id",
                "upi transaction",
                "bank transaction",
                "bank statement"
            ],

            "Digital Evidence": [
                "screenshot",
                "screenshots",
                "screen recording",
                "email",
                "sms",
                "message",
                "notification",
                "ip address",
                "device",
                "login"
            ],

            "Financial Loss Evidence": [
                "amount",
                "₹",
                "rs",
                "rupees",
                "money",
                "loss",
                "transferred"
            ],

            "Bank / Payment Provider Communication": [
                "bank complaint",
                "bank",
                "upi complaint",
                "payment provider",
                "payment app",
                "customer support"
            ],

            "Cyber Complaint / Reference": [
                "cyber complaint",
                "cybercrime",
                "cyber crime",
                "complaint number",
                "ticket",
                "reference number"
            ]
        }

        # ========================================================
        # CONTRACT EVIDENCE
        # ========================================================

        self.contract_evidence = {

            "Agreement / Contract": [
                "agreement",
                "contract",
                "terms",
                "terms and conditions"
            ],

            "Payment Evidence": [
                "invoice",
                "receipt",
                "payment",
                "transaction"
            ]
        }

        # ========================================================
        # EMPLOYMENT / LABOUR
        # ========================================================

        self.employment_evidence = {

            "Employment Proof": [
                "offer letter",
                "appointment letter",
                "employment contract",
                "employee id",
                "salary slip",
                "payslip"
            ],

            "Communication Evidence": [
                "email",
                "mail",
                "message",
                "whatsapp",
                "notice"
            ],

            "Workplace Evidence": [
                "attendance",
                "timesheet",
                "hr complaint",
                "termination letter"
            ]
        }

    # ============================================================
    # GET DOMAIN-SPECIFIC EVIDENCE
    # ============================================================

    def _get_domain_evidence(self, domain):

        if not domain:
            return {}

        domain_lower = str(
            domain
        ).lower()

        if (
            "consumer" in domain_lower
        ):

            return self.consumer_evidence

        if (
            "cyber" in domain_lower
            or "information technology"
            in domain_lower
            or "it" == domain_lower
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

        return {}

    # ============================================================
    # CREATE SEARCH TEXT
    # ============================================================

    def _get_complaint_text(self, complaint):

        fields = [

            "name",
            "city",
            "product",
            "seller",
            "problem",
            "remedy",
            "purchase_date"
        ]

        text_parts = []

        for field in fields:

            value = getattr(
                complaint,
                field,
                ""
            )

            if value:

                text_parts.append(
                    str(value)
                )

        return " ".join(
            text_parts
        ).lower()

    # ============================================================
    # DETECT EVIDENCE
    # ============================================================

    def _detect_evidence(
        self,
        complaint,
        evidence_groups
    ):

        text = self._get_complaint_text(
            complaint
        )

        detected = []
        missing = []

        for group, keywords in (
            evidence_groups.items()
        ):

            found = any(
                keyword.lower() in text
                for keyword in keywords
            )

            if found:

                detected.append(
                    group
                )

            else:

                missing.append(
                    group
                )

        return detected, missing

    # ============================================================
    # BASIC INFORMATION SCORE
    # ============================================================

    def _calculate_basic_score(
        self,
        complaint,
        recommendations
    ):

        score = 0

        # --------------------------------------------------------
        # NAME
        # --------------------------------------------------------

        if str(
            getattr(
                complaint,
                "name",
                ""
            )
        ).strip():

            score += 5

        else:

            recommendations.append(
                "Provide your full name."
            )

        # --------------------------------------------------------
        # CITY
        # --------------------------------------------------------

        if str(
            getattr(
                complaint,
                "city",
                ""
            )
        ).strip():

            score += 5

        else:

            recommendations.append(
                "Mention your city."
            )

        # --------------------------------------------------------
        # PRODUCT / SERVICE
        # --------------------------------------------------------

        if str(
            getattr(
                complaint,
                "product",
                ""
            )
        ).strip():

            score += 5

        else:

            recommendations.append(
                "Specify the product or service involved."
            )

        # --------------------------------------------------------
        # SELLER / OTHER PARTY
        # --------------------------------------------------------

        if str(
            getattr(
                complaint,
                "seller",
                ""
            )
        ).strip():

            score += 5

        else:

            recommendations.append(
                "Mention the seller, service provider, "
                "bank or other relevant party."
            )

        # --------------------------------------------------------
        # DATE
        # --------------------------------------------------------

        if getattr(
            complaint,
            "purchase_date",
            None
        ):

            score += 5

        else:

            recommendations.append(
                "Provide the relevant purchase or incident date."
            )

        return score

    # ============================================================
    # PROBLEM SCORE
    # ============================================================

    def _calculate_problem_score(
        self,
        complaint,
        recommendations
    ):

        problem_text = str(
            getattr(
                complaint,
                "problem",
                ""
            )
        ).strip()

        if len(problem_text) >= 100:

            return 20

        if len(problem_text) >= 50:

            return 15

        if len(problem_text) >= 25:

            recommendations.append(
                "Describe what happened in more detail, "
                "including when and how the incident occurred."
            )

            return 10

        recommendations.append(
            "Provide a detailed description of the problem."
        )

        return 5

    # ============================================================
    # REMEDY SCORE
    # ============================================================

    def _calculate_remedy_score(
        self,
        complaint,
        recommendations
    ):

        remedy = str(
            getattr(
                complaint,
                "remedy",
                ""
            )
        ).strip()

        if remedy:

            return 10

        recommendations.append(
            "Specify the remedy you are seeking."
        )

        return 0

    # ============================================================
    # DOMAIN EVIDENCE SCORE
    # ============================================================

    def _calculate_evidence_score(
        self,
        detected_evidence,
        missing_evidence,
        domain
    ):

        if not detected_evidence:

            return 0

        total_groups = (
            len(detected_evidence)
            +
            len(missing_evidence)
        )

        if total_groups == 0:

            return 0

        # Evidence can contribute maximum 40 points.
        score = round(
            (
                len(detected_evidence)
                /
                total_groups
            ) * 40
        )

        return score

    # ============================================================
    # DOMAIN-SPECIFIC RECOMMENDATIONS
    # ============================================================

    def _generate_evidence_recommendations(
        self,
        missing_evidence,
        domain
    ):

        recommendations = []

        # ========================================================
        # CONSUMER
        # ========================================================

        if "consumer" in str(
            domain
        ).lower():

            mapping = {

                "Purchase / Payment Proof":
                    "Keep the invoice, receipt, order confirmation or payment proof.",

                "Product Evidence":
                    "Keep photographs, videos or screenshots showing the product problem.",

                "Warranty / Policy Documents":
                    "Keep the warranty card or applicable warranty/policy documents."
            }

        # ========================================================
        # CYBER
        # ========================================================

        elif (
            "cyber" in str(
                domain
            ).lower()
        ):

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
                    "Keep any cybercrime complaint number, ticket ID or reference number."
            }

        # ========================================================
        # CONTRACT
        # ========================================================

        elif "contract" in str(
            domain
        ).lower():

            mapping = {

                "Agreement / Contract":
                    "Keep the signed agreement, contract or applicable terms.",

                "Payment Evidence":
                    "Keep invoices, receipts and payment records."
            }

        # ========================================================
        # EMPLOYMENT
        # ========================================================

        elif (
            "employment" in str(
                domain
            ).lower()
            or
            "labour" in str(
                domain
            ).lower()
        ):

            mapping = {

                "Employment Proof":
                    "Keep your appointment letter, employment contract, salary slips or other employment records.",

                "Communication Evidence":
                    "Preserve emails, messages, notices and communication with the employer or HR.",

                "Workplace Evidence":
                    "Keep attendance, timesheets, HR complaints and relevant workplace records."
            }

        else:

            mapping = {}

        for evidence in missing_evidence:

            if evidence in mapping:

                recommendations.append(
                    mapping[evidence]
                )

        return recommendations

    # ============================================================
    # READINESS STATUS
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

    def calculate(
        self,
        complaint,
        domain=None
    ):

        recommendations = []

        # --------------------------------------------------------
        # DOMAIN-SPECIFIC EVIDENCE
        # --------------------------------------------------------

        domain_evidence = (
            self._get_domain_evidence(
                domain
            )
        )

        # General communication/complaint
        evidence_groups = dict(
            self.general_evidence
        )

        # Add domain-specific groups
        evidence_groups.update(
            domain_evidence
        )

        # --------------------------------------------------------
        # DETECT EVIDENCE
        # --------------------------------------------------------

        detected_evidence, missing_evidence = (
            self._detect_evidence(
                complaint,
                evidence_groups
            )
        )

        # --------------------------------------------------------
        # BASIC INFORMATION
        # --------------------------------------------------------

        score = (
            self._calculate_basic_score(
                complaint,
                recommendations
            )
        )

        # --------------------------------------------------------
        # PROBLEM
        # --------------------------------------------------------

        score += (
            self._calculate_problem_score(
                complaint,
                recommendations
            )
        )

        # --------------------------------------------------------
        # REMEDY
        # --------------------------------------------------------

        score += (
            self._calculate_remedy_score(
                complaint,
                recommendations
            )
        )

        # --------------------------------------------------------
        # EVIDENCE
        # --------------------------------------------------------

        score += (
            self._calculate_evidence_score(
                detected_evidence,
                missing_evidence,
                domain
            )
        )

        # --------------------------------------------------------
        # DOMAIN-SPECIFIC RECOMMENDATIONS
        # --------------------------------------------------------

        recommendations.extend(
            self._generate_evidence_recommendations(
                missing_evidence,
                domain
            )
        )

        # --------------------------------------------------------
        # LIMIT
        # --------------------------------------------------------

        score = min(
            100,
            max(
                0,
                score
            )
        )

        # --------------------------------------------------------
        # STATUS
        # --------------------------------------------------------

        status = self._get_status(
            score
        )

        # --------------------------------------------------------
        # REMOVE DUPLICATES
        # --------------------------------------------------------

        unique_recommendations = []

        for recommendation in recommendations:

            if (
                recommendation
                not in unique_recommendations
            ):

                unique_recommendations.append(
                    recommendation
                )

        # ========================================================
        # RESULT
        # ========================================================

        return {

            "score": score,

            "status": status,

            "recommendations":
                unique_recommendations,

            "evidence": {

                "detected":
                    detected_evidence,

                "missing":
                    missing_evidence
            },

            "domain":
                domain

        }


# ================================================================
# GLOBAL SERVICE INSTANCE
# ================================================================

readiness_service = ReadinessService()