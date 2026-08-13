class ReadinessService:

    def __init__(self):

        self.evidence_groups = {
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

            "Visual Evidence": [
                "photo",
                "photos",
                "photograph",
                "photographs",
                "image",
                "images",
                "screenshot",
                "screenshots",
                "video",
                "unboxing video"
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
                "recording",
                "call recording"
            ],

            "Warranty / Policy Documents": [
                "warranty",
                "guarantee",
                "warranty card",
                "policy",
                "policy document"
            ],

            "Agreement / Contract": [
                "agreement",
                "contract"
            ],

            "Transaction Evidence": [
                "bank statement",
                "transaction",
                "transaction id",
                "transaction number"
            ],

            "Complaint / Reference": [
                "complaint",
                "grievance",
                "ticket",
                "reference number"
            ]
        }

    # ============================================================
    # DETECT EVIDENCE
    # ============================================================

    def _detect_evidence(self, complaint):

        text = " ".join([
            str(getattr(complaint, "problem", "")),
            str(getattr(complaint, "remedy", ""))
        ]).lower()

        detected = []
        missing = []

        for group, keywords in self.evidence_groups.items():

            found = any(
                keyword.lower() in text
                for keyword in keywords
            )

            if found:
                detected.append(group)
            else:
                missing.append(group)

        return detected, missing

    # ============================================================
    # CALCULATE READINESS
    # ============================================================

    def calculate(self, complaint):

        score = 0
        recommendations = []

        # --------------------------------------------------------
        # BASIC INFORMATION
        # --------------------------------------------------------

        if str(getattr(complaint, "name", "")).strip():
            score += 10
        else:
            recommendations.append(
                "Provide your full name."
            )

        if str(getattr(complaint, "city", "")).strip():
            score += 5
        else:
            recommendations.append(
                "Mention your city."
            )

        if str(getattr(complaint, "product", "")).strip():
            score += 10
        else:
            recommendations.append(
                "Specify the product or service."
            )

        if str(getattr(complaint, "seller", "")).strip():
            score += 15
        else:
            recommendations.append(
                "Mention the seller or service provider."
            )

        if getattr(complaint, "purchase_date", None):
            score += 10
        else:
            recommendations.append(
                "Provide the purchase or transaction date."
            )

        # --------------------------------------------------------
        # PROBLEM DESCRIPTION
        # --------------------------------------------------------

        problem_text = str(
            getattr(complaint, "problem", "")
        ).strip()

        if len(problem_text) >= 50:

            score += 20

        elif len(problem_text) >= 25:

            score += 10

            recommendations.append(
                "Describe the problem in more detail, including what happened and when."
            )

        else:

            recommendations.append(
                "Describe the problem in more detail."
            )

        # --------------------------------------------------------
        # DESIRED REMEDY
        # --------------------------------------------------------

        if getattr(complaint, "remedy", None):

            score += 10

        else:

            recommendations.append(
                "Choose a desired remedy."
            )

        # --------------------------------------------------------
        # EVIDENCE
        # --------------------------------------------------------

        detected_evidence, missing_evidence = (
            self._detect_evidence(complaint)
        )

        if detected_evidence:

            evidence_score = min(
                20,
                len(detected_evidence) * 5
            )

            score += evidence_score

        else:

            recommendations.append(
                "Add supporting evidence such as an invoice, "
                "receipt, photographs, screenshots, emails or chats."
            )

        # --------------------------------------------------------
        # EVIDENCE GAP RECOMMENDATIONS
        # --------------------------------------------------------

        if "Purchase / Payment Proof" in missing_evidence:

            recommendations.append(
                "Keep your invoice, receipt, order confirmation or payment proof."
            )

        if "Visual Evidence" in missing_evidence:

            recommendations.append(
                "Keep photographs, screenshots or videos showing the problem."
            )

        if "Communication Evidence" in missing_evidence:

            recommendations.append(
                "Preserve emails, WhatsApp chats, messages or call records with the seller."
            )

        if "Warranty / Policy Documents" in missing_evidence:

            recommendations.append(
                "Keep the applicable warranty card or policy document."
            )

        if "Agreement / Contract" in missing_evidence:

            recommendations.append(
                "Keep the relevant agreement or contract if one exists."
            )

        if "Transaction Evidence" in missing_evidence:

            recommendations.append(
                "Keep bank statements or transaction records where relevant."
            )

        if "Complaint / Reference" in missing_evidence:

            recommendations.append(
                "Keep previous complaint, grievance or support ticket reference numbers."
            )

        # --------------------------------------------------------
        # LIMIT SCORE
        # --------------------------------------------------------

        score = min(100, score)

        # --------------------------------------------------------
        # READINESS STATUS
        # --------------------------------------------------------

        if score >= 90:

            status = "Strong Case"

        elif score >= 70:

            status = "Good Case"

        elif score >= 50:

            status = "Moderate Case"

        else:

            status = "Weak Case"

        # --------------------------------------------------------
        # REMOVE DUPLICATES
        # --------------------------------------------------------

        unique_recommendations = []

        for recommendation in recommendations:

            if recommendation not in unique_recommendations:

                unique_recommendations.append(
                    recommendation
                )

        # --------------------------------------------------------
        # RETURN RESULT
        # --------------------------------------------------------

        return {
            "score": score,

            "status": status,

            "recommendations": unique_recommendations,

            "evidence": {
                "detected": detected_evidence,
                "missing": missing_evidence
            }
        }


# ================================================================
# GLOBAL SERVICE INSTANCE
# ================================================================

readiness_service = ReadinessService()