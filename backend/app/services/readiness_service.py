import re


class ReadinessService:

    def __init__(self):

        self.evidence_keywords = [

            "invoice",
            "receipt",
            "bill",
            "photo",
            "photos",
            "image",
            "images",
            "email",
            "mail",
            "chat",
            "whatsapp",
            "call",
            "recording",
            "warranty",
            "guarantee"

        ]

    # =====================================
    # Calculate Readiness Score
    # =====================================

    def calculate(self, complaint):

        score = 0

        recommendations = []

        # -----------------------------
        # Name
        # -----------------------------

        if complaint.name.strip():

            score += 10

        else:

            recommendations.append(
                "Provide your full name."
            )

        # -----------------------------
        # City
        # -----------------------------

        if complaint.city.strip():

            score += 5

        else:

            recommendations.append(
                "Mention your city."
            )

        # -----------------------------
        # Product
        # -----------------------------

        if complaint.product.strip():

            score += 10

        else:

            recommendations.append(
                "Specify the product or service."
            )

        # -----------------------------
        # Seller
        # -----------------------------

        if complaint.seller.strip():

            score += 15

        else:

            recommendations.append(
                "Mention the seller's name."
            )

        # -----------------------------
        # Purchase Date
        # -----------------------------

        if complaint.purchase_date:

            score += 10

        else:

            recommendations.append(
                "Provide the purchase date."
            )

        # -----------------------------
        # Problem
        # -----------------------------

        if len(complaint.problem.strip()) >= 50:

            score += 20

        else:

            recommendations.append(
                "Describe the problem in more detail."
            )

        # -----------------------------
        # Remedy
        # -----------------------------

        if complaint.remedy:

            score += 10

        else:

            recommendations.append(
                "Choose a desired remedy."
            )

        # -----------------------------
        # Evidence Detection
        # -----------------------------

        problem = complaint.problem.lower()

        evidence_found = any(

            keyword in problem

            for keyword in self.evidence_keywords

        )

        if evidence_found:

            score += 20

        else:

            recommendations.append(

                "Mention evidence such as invoice, receipt, photographs, emails or chats."

            )

        # =====================================
        # Classification
        # =====================================

        if score >= 90:

            status = "Strong Case"

        elif score >= 70:

            status = "Good Case"

        elif score >= 50:

            status = "Moderate Case"

        else:

            status = "Weak Case"

        return {

            "score": score,

            "status": status,

            "recommendations": recommendations

        }


readiness_service = ReadinessService()