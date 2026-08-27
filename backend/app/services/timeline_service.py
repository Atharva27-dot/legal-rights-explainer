"""
Evidence Timeline Service

Builds a deterministic case timeline from:
1. Citizen-provided case details.
2. Text extracted from uploaded evidence.

No LLM call is used.

Each event is labelled as:
- USER_REPORTED: supplied by the citizen.
- EVIDENCE_DERIVED: directly supported by uploaded evidence text.
- DERIVED: calculated from an explicit user statement.

The service does not silently reconcile conflicting dates.
"""

from __future__ import annotations

import re
from datetime import date, datetime, timedelta
from typing import Any


class EvidenceTimelineService:
    DATE_PATTERNS = [
        # 15 August 2026 / 15 Aug 2026
        re.compile(
            r"\b(\d{1,2})\s+"
            r"(January|February|March|April|May|June|July|August|September|October|November|December|"
            r"Jan|Feb|Mar|Apr|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)"
            r"\s+(\d{4})\b",
            re.IGNORECASE,
        ),
        # 2026-08-09
        re.compile(r"\b(\d{4})-(\d{2})-(\d{2})\b"),
        # 15/08/2026 or 15-08-2026
        re.compile(r"\b(\d{1,2})[/-](\d{1,2})[/-](\d{4})\b"),
    ]

    MONTHS = {
        "jan": 1, "january": 1,
        "feb": 2, "february": 2,
        "mar": 3, "march": 3,
        "apr": 4, "april": 4,
        "may": 5,
        "jun": 6, "june": 6,
        "jul": 7, "july": 7,
        "aug": 8, "august": 8,
        "sep": 9, "sept": 9, "september": 9,
        "oct": 10, "october": 10,
        "nov": 11, "november": 11,
        "dec": 12, "december": 12,
    }

    def _parse_date(self, value: str) -> date | None:
        value = value.strip()

        for pattern in self.DATE_PATTERNS:
            match = pattern.search(value)
            if not match:
                continue

            try:
                groups = match.groups()

                if len(groups) == 3 and groups[0].isdigit() and len(groups[0]) == 4:
                    return date(
                        int(groups[0]),
                        int(groups[1]),
                        int(groups[2]),
                    )

                if len(groups) == 3 and groups[1].lower() in self.MONTHS:
                    return date(
                        int(groups[2]),
                        self.MONTHS[groups[1].lower()],
                        int(groups[0]),
                    )

                if len(groups) == 3:
                    return date(
                        int(groups[2]),
                        int(groups[1]),
                        int(groups[0]),
                    )

            except ValueError:
                continue

        return None

    def _format_date(self, value: date | None) -> str | None:
        if value is None:
            return None
        return value.strftime("%d %b %Y")

    def _add_event(
        self,
        events: list[dict[str, Any]],
        event_date: date | None,
        title: str,
        details: str,
        source: str,
        event_type: str,
        confidence: str = "high",
    ) -> None:
        events.append(
            {
                "date": self._format_date(event_date),
                "date_iso": event_date.isoformat() if event_date else None,
                "title": title,
                "details": details,
                "source": source,
                "type": event_type,
                "confidence": confidence,
            }
        )

    def _evidence_text(self, evidence: list[Any]) -> str:
        chunks: list[str] = []

        for item in evidence or []:
            filename = getattr(item, "filename", "") or ""
            extracted = getattr(item, "extracted_text", "") or ""

            if isinstance(item, dict):
                filename = item.get("filename", "") or ""
                extracted = item.get("extracted_text", "") or ""

            if filename:
                chunks.append(filename)

            if extracted:
                chunks.append(extracted)

        return "\n".join(chunks)

    def _find_evidence_date(
        self,
        text: str,
        labels: tuple[str, ...],
    ) -> date | None:
        """
        Find a date appearing near a labelled field such as:
        Invoice Date: 15 August 2026
        """
        label_pattern = "|".join(re.escape(label) for label in labels)

        match = re.search(
            rf"(?is)(?:{label_pattern})\s*[:\-]?\s*"
            rf"(.{{0,80}}?)"
            rf"(?=\n|$)",
            text,
        )

        if match:
            candidate = match.group(1)
            parsed = self._parse_date(candidate)
            if parsed:
                return parsed

        return None

    def _find_amount(self, text: str) -> str | None:
        match = re.search(
            r"(?i)(?:total\s+paid|total|amount)\s*[:\-]?\s*"
            r"(?:₹|rs\.?|inr)?\s*([0-9][0-9,]*(?:\.[0-9]+)?)",
            text,
        )

        if not match:
            return None

        return f"₹{match.group(1)}"

    def _find_product(self, text: str) -> str | None:
        match = re.search(
            r"(?im)^product(?:\s+quantity\s+unit\s+price\s+amount)?\s*$"
            r".*?\n([^\n]+)",
            text,
        )

        if match:
            candidate = match.group(1).strip()
            # Avoid returning a table header.
            if candidate and "quantity" not in candidate.lower():
                return candidate

        match = re.search(
            r"(?im)^([^\n]+?)\s+\d+\s+(?:₹|rs\.?|inr)?\s*"
            r"[0-9][0-9,]*(?:\.[0-9]+)?\s+"
            r"(?:₹|rs\.?|inr)?\s*[0-9][0-9,]*(?:\.[0-9]+)?\s*$",
            text,
        )

        return match.group(1).strip() if match else None

    def _find_field(self, text: str, labels: tuple[str, ...]) -> str | None:
        label_pattern = "|".join(re.escape(label) for label in labels)

        match = re.search(
            rf"(?im)^(?:{label_pattern})\s*[:\-]\s*(.+)$",
            text,
        )

        return match.group(1).strip() if match else None

    def build_timeline(self, request: Any) -> dict[str, Any]:
        events: list[dict[str, Any]] = []
        conflicts: list[dict[str, Any]] = []

        # ------------------------------------------------------------
        # USER-REPORTED EVENTS
        # ------------------------------------------------------------
        purchase_date = self._parse_date(
            str(getattr(request, "purchase_date", "") or "")
        )

        if purchase_date:
            self._add_event(
                events,
                purchase_date,
                "Purchase / transaction reported",
                f"The citizen provided the purchase/transaction date as {self._format_date(purchase_date)}.",
                "Citizen-provided case details",
                "USER_REPORTED",
            )

        problem = str(getattr(request, "problem", "") or "").strip()

        if problem:
            self._add_event(
                events,
                purchase_date,
                "Problem reported",
                problem,
                "Citizen-provided case details",
                "USER_REPORTED",
                confidence="medium",
            )

        # ------------------------------------------------------------
        # DERIVED EVENT: "stopped working after five days"
        # ------------------------------------------------------------
        if purchase_date and re.search(
            r"\b(?:after|within)\s+five\s+days?\b",
            problem,
            re.IGNORECASE,
        ):
            derived_problem_date = purchase_date + timedelta(days=5)

            self._add_event(
                events,
                derived_problem_date,
                "Product reportedly stopped working",
                "Date derived from the citizen's statement that the phone stopped working after five days.",
                "Citizen-provided case details",
                "DERIVED",
                confidence="medium",
            )

        # ------------------------------------------------------------
        # EVIDENCE-DERIVED EVENTS
        # ------------------------------------------------------------
        evidence = getattr(request, "evidence", []) or []
        evidence_text = self._evidence_text(evidence)

        invoice_date = self._find_evidence_date(
            evidence_text,
            ("invoice date",),
        )

        # Some documents use a standalone "Invoice" label followed by the
        # date on the same line. Only use that fallback when an explicit
        # "Invoice Date" field was not found.
        if invoice_date is None:
            invoice_date = self._find_evidence_date(
                evidence_text,
                ("invoice",),
            )

        transaction_date = self._find_evidence_date(
            evidence_text,
            ("transaction date", "payment date"),
        )

        evidence_seller = self._find_field(
            evidence_text,
            ("seller", "merchant", "vendor"),
        )

        evidence_product = self._find_product(evidence_text)
        amount = self._find_amount(evidence_text)

        payment_method = self._find_field(
            evidence_text,
            ("payment method", "payment mode"),
        )

        delivery_status = self._find_field(
            evidence_text,
            ("delivery status", "delivery"),
        )

        warranty = self._find_field(
            evidence_text,
            ("warranty",),
        )

        if invoice_date:
            self._add_event(
                events,
                invoice_date,
                "Invoice issued",
                (
                    f"Invoice date recorded in uploaded evidence. "
                    f"Seller: {evidence_seller or 'not identified'}."
                ),
                "Uploaded evidence",
                "EVIDENCE_DERIVED",
            )

        if transaction_date:
            self._add_event(
                events,
                transaction_date,
                "Transaction recorded",
                (
                    f"Transaction date found in uploaded evidence"
                    + (f"; payment method: {payment_method}." if payment_method else ".")
                ),
                "Uploaded evidence",
                "EVIDENCE_DERIVED",
            )

        if amount or payment_method:
            payment_details = []
            if amount:
                payment_details.append(f"Amount: {amount}")
            if payment_method:
                payment_details.append(f"Method: {payment_method}")

            # If the document has no separate payment/transaction date,
            # associate the payment with the invoice date rather than
            # leaving the timeline event undated.
            payment_event_date = transaction_date or invoice_date

            self._add_event(
                events,
                payment_event_date,
                "Payment recorded",
                "; ".join(payment_details),
                "Uploaded evidence",
                "EVIDENCE_DERIVED",
            )

        if evidence_product:
            self._add_event(
                events,
                invoice_date or transaction_date,
                "Product identified",
                f"Product recorded in uploaded evidence: {evidence_product}.",
                "Uploaded evidence",
                "EVIDENCE_DERIVED",
            )

        if delivery_status and "deliver" in delivery_status.lower():
            self._add_event(
                events,
                invoice_date or transaction_date,
                "Delivery recorded",
                f"Uploaded evidence records delivery status as: {delivery_status}.",
                "Uploaded evidence",
                "EVIDENCE_DERIVED",
            )

        if warranty:
            self._add_event(
                events,
                invoice_date or transaction_date,
                "Warranty recorded",
                f"Uploaded evidence states: {warranty}.",
                "Uploaded evidence",
                "EVIDENCE_DERIVED",
            )

        # ------------------------------------------------------------
        # DATE CONFLICT DETECTION
        # ------------------------------------------------------------
        if purchase_date and invoice_date and purchase_date != invoice_date:
            conflicts.append(
                {
                    "field": "purchase_date",
                    "label": "Purchase / Invoice Date",
                    "user_value": self._format_date(purchase_date),
                    "evidence_value": self._format_date(invoice_date),
                    "status": "MISMATCH",
                    "message": (
                        "The citizen-provided purchase date differs from "
                        "the invoice date recorded in uploaded evidence."
                    ),
                }
            )

        supplied_transaction = self._parse_date(
            str(getattr(request, "transaction_date", "") or "")
        )

        if supplied_transaction and transaction_date and supplied_transaction != transaction_date:
            conflicts.append(
                {
                    "field": "transaction_date",
                    "label": "Transaction Date",
                    "user_value": self._format_date(supplied_transaction),
                    "evidence_value": self._format_date(transaction_date),
                    "status": "MISMATCH",
                    "message": (
                        "The citizen-provided transaction date differs from "
                        "the date recorded in uploaded evidence."
                    ),
                }
            )

        # ------------------------------------------------------------
        # Sort only dated events; keep undated events at the end.
        # ------------------------------------------------------------
        events.sort(
            key=lambda item: (
                item["date_iso"] is None,
                item["date_iso"] or "",
            )
        )

        return {
            "events": events,
            "conflicts": conflicts,
            "summary": {
                "event_count": len(events),
                "conflict_count": len(conflicts),
                "status": "CONFLICTS_FOUND" if conflicts else "CONSISTENT",
            },
        }


evidence_timeline_service = EvidenceTimelineService()
