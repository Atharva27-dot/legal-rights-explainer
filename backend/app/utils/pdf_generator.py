from io import BytesIO
from datetime import datetime

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
)
from reportlab.lib.enums import TA_CENTER


class PDFGenerator:

    def __init__(self):
        self.styles = getSampleStyleSheet()

    def _title(self, text):
        style = self.styles["Heading1"]
        style.alignment = TA_CENTER
        return Paragraph(text, style)

    def _heading(self, text):
        return Paragraph(f"<b>{text}</b>", self.styles["Heading2"])

    def _normal(self, text):
        return Paragraph(text, self.styles["BodyText"])

    def generate(self, report):

        buffer = BytesIO()

        doc = SimpleDocTemplate(buffer)

        story = []

        # =====================================
        # Cover
        # =====================================

        story.append(
            self._title("LEGAL RIGHTS EXPLAINER")
        )

        story.append(
            self._heading("AI Generated Consumer Complaint")
        )

        story.append(Spacer(1, 20))

        story.append(
            self._normal(
                f"<b>Generated On:</b> {datetime.now().strftime('%d-%m-%Y %H:%M')}"
            )
        )

        story.append(Spacer(1, 25))

        # =====================================
        # Case Analysis
        # =====================================

        analysis = report["case_analysis"]

        story.append(
            self._heading("Case Analysis")
        )

        story.append(
            self._normal(
                f"<b>Category:</b> {analysis['category']}"
            )
        )

        story.append(
            self._normal(
                f"<b>Applicable Act:</b> {analysis['applicable_act']}"
            )
        )

        story.append(
            self._normal(
                f"<b>Recommended Remedy:</b> {analysis['recommended_remedy']}"
            )
        )

        story.append(
            self._normal(
                f"<b>Legal Readiness:</b> {analysis['legal_readiness']}"
            )
        )

        story.append(Spacer(1, 15))

        story.append(
            self._heading("Applicable Rights")
        )

        for right in analysis["rights"]:
            story.append(
                self._normal(f"• {right}")
            )

        story.append(Spacer(1, 15))

        story.append(
            self._heading("Supporting Documents")
        )

        for doc_name in analysis["supporting_documents"]:
            story.append(
                self._normal(f"• {doc_name}")
            )

        story.append(Spacer(1, 20))

        # =====================================
        # Complaint
        # =====================================

        story.append(
            self._heading("Complaint Draft")
        )

        complaint_text = report["complaint"].replace(
            "\n",
            "<br/>"
        )

        story.append(
            Paragraph(
                complaint_text,
                self.styles["BodyText"]
            )
        )

        story.append(Spacer(1, 20))

        # =====================================
        # Sources
        # =====================================

        story.append(
            self._heading("Legal Sources")
        )

        for source in report["sources"]:

            story.append(
                self._normal(
                    f"{source.get('act','')} | "
                    f"{source.get('section','')} | "
                    f"{source.get('title','')}"
                )
            )

        story.append(Spacer(1, 20))

        # =====================================
        # Footer
        # =====================================

        story.append(
            self._normal(
                "<b>Generated using Legal Rights Explainer</b>"
            )
        )

        doc.build(story)

        buffer.seek(0)

        return buffer


pdf_generator = PDFGenerator()