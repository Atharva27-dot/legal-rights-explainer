import re
from datetime import datetime

from app.schemas.complaint_schema import ComplaintRequest


class EvidenceConsistencyService:
    """
    Deterministic comparison layer between citizen-provided case facts
    and facts extracted from uploaded evidence.

    This service does not make legal conclusions. It only reports
    whether factual fields are consistent, different, or unavailable.
    """

    FIELD_LABELS = {
        "seller": "Seller / Company",
        "product": "Product",
        "purchase_date": "Purchase Date",
        "amount": "Amount",
        "bank": "Bank / Payment Platform",
        "transaction_date": "Transaction Date",
        "invoice_number": "Invoice Number",
        "order_id": "Order ID",
    }

    def check(self, request: ComplaintRequest):
        evidence_text = self._combine_evidence(request)

        if not evidence_text:
            return {
                "overall_status": "NO_EVIDENCE",
                "summary": "No text-extractable supporting evidence was provided.",
                "checks": [],
                "discrepancies": [],
            }

        checks = []

        checks.append(
            self._compare_field(
                "seller",
                getattr(request, "seller", ""),
                self._extract_seller(evidence_text),
            )
        )

        checks.append(
            self._compare_field(
                "product",
                getattr(request, "product", ""),
                self._extract_product(evidence_text),
            )
        )

        checks.append(
            self._compare_field(
                "purchase_date",
                getattr(request, "purchase_date", ""),
                self._extract_purchase_date(evidence_text),
            )
        )

        checks.append(
            self._compare_field(
                "amount",
                getattr(request, "amount", ""),
                self._extract_amount(evidence_text),
            )
        )

        checks.append(
            self._compare_field(
                "bank",
                getattr(request, "bank", ""),
                self._extract_bank(evidence_text),
            )
        )

        checks.append(
            self._compare_field(
                "transaction_date",
                getattr(request, "transaction_date", ""),
                self._extract_transaction_date(evidence_text),
            )
        )

        invoice_number = self._extract_invoice_number(evidence_text)
        if invoice_number:
            checks.append({
                "field": "invoice_number",
                "label": self.FIELD_LABELS["invoice_number"],
                "user_value": None,
                "evidence_value": invoice_number,
                "status": "FOUND_IN_EVIDENCE",
                "message": "Invoice number found in uploaded evidence.",
            })

        order_id = self._extract_order_id(evidence_text)
        if order_id:
            checks.append({
                "field": "order_id",
                "label": self.FIELD_LABELS["order_id"],
                "user_value": None,
                "evidence_value": order_id,
                "status": "FOUND_IN_EVIDENCE",
                "message": "Order ID found in uploaded evidence.",
            })

        mismatches = [
            item for item in checks
            if item["status"] == "MISMATCH"
        ]

        if mismatches:
            overall_status = "MISMATCH"
            count = len(mismatches)
            summary = (
                f"{count} factual discrepancy found. "
                "Review the differences before filing."
                if count == 1
                else
                f"{count} factual discrepancies found. "
                "Review the differences before filing."
            )
        elif any(
            item["status"] == "MATCH"
            for item in checks
        ):
            overall_status = "CONSISTENT"
            summary = (
                "The supplied case details are consistent with "
                "the extracted evidence for the available fields."
            )
        else:
            overall_status = "PARTIAL"
            summary = (
                "Evidence was found, but the available text did not "
                "contain enough comparable fields."
            )

        return {
            "overall_status": overall_status,
            "summary": summary,
            "checks": checks,
            "discrepancies": mismatches,
        }

    # ============================================================
    # EVIDENCE TEXT
    # ============================================================

    def _combine_evidence(self, request):
        parts = []

        for evidence in getattr(request, "evidence", []) or []:
            text = str(
                getattr(evidence, "extracted_text", "")
                or ""
            ).strip()

            if text:
                parts.append(text)

        return "\n".join(parts)

    # ============================================================
    # FIELD COMPARISON
    # ============================================================

    def _compare_field(self, field, user_value, evidence_value):
        user_value = str(user_value or "").strip()
        evidence_value = str(evidence_value or "").strip()

        label = self.FIELD_LABELS[field]

        if not evidence_value:
            return {
                "field": field,
                "label": label,
                "user_value": user_value or None,
                "evidence_value": None,
                "status": "NOT_FOUND",
                "message": f"{label} was not found in the uploaded evidence.",
            }

        if not user_value:
            return {
                "field": field,
                "label": label,
                "user_value": None,
                "evidence_value": evidence_value,
                "status": "FOUND_IN_EVIDENCE",
                "message": f"{label} was found in the uploaded evidence.",
            }

        if field in {"purchase_date", "transaction_date"}:
            matched = self._dates_match(
                user_value,
                evidence_value
            )

        elif field == "amount":
            matched = self._amounts_match(
                user_value,
                evidence_value
            )

        else:
            matched = self._values_match(
                user_value,
                evidence_value
            )

        if matched:
            return {
                "field": field,
                "label": label,
                "user_value": user_value,
                "evidence_value": evidence_value,
                "status": "MATCH",
                "message": f"{label} matches the uploaded evidence.",
            }

        return {
            "field": field,
            "label": label,
            "user_value": user_value,
            "evidence_value": evidence_value,
            "status": "MISMATCH",
            "message": (
                f"{label} differs between the case details "
                "and uploaded evidence."
            ),
        }

    # ============================================================
    # NORMALIZATION
    # ============================================================

    @staticmethod
    def _normalize_text(value):
        value = str(value or "").lower()

        value = re.sub(
            r"[^a-z0-9]+",
            " ",
            value,
        )

        return re.sub(
            r"\s+",
            " ",
            value,
        ).strip()

    def _values_match(self, first, second):
        a = self._normalize_text(first)
        b = self._normalize_text(second)

        if not a or not b:
            return False

        return (
            a == b
            or a in b
            or b in a
        )

    # ============================================================
    # DATE HANDLING
    # ============================================================

    def _dates_match(self, first, second):
        first_dates = self._extract_dates(first)
        second_dates = self._extract_dates(second)

        if not first_dates or not second_dates:
            return self._values_match(first, second)

        return bool(
            set(first_dates) & set(second_dates)
        )

    @staticmethod
    def _extract_dates(text):
        text = str(text or "")
        dates = set()

        patterns = [
            r"\b(20\d{2})[-/](\d{1,2})[-/](\d{1,2})\b",
            r"\b(\d{1,2})[-/](\d{1,2})[-/](20\d{2})\b",
        ]

        for pattern in patterns:
            for match in re.finditer(pattern, text):
                groups = [int(value) for value in match.groups()]

                if groups[0] >= 2000:
                    year, month, day = groups
                else:
                    day, month, year = groups

                try:
                    dates.add(
                        datetime(
                            year,
                            month,
                            day
                        ).date()
                    )
                except ValueError:
                    continue

        month_pattern = re.compile(
            r"\b(\d{1,2})\s+"
            r"(January|February|March|April|May|June|July|August|"
            r"September|October|November|December)"
            r"\s+(20\d{2})\b",
            re.IGNORECASE,
        )

        month_numbers = {
            "january": 1,
            "february": 2,
            "march": 3,
            "april": 4,
            "may": 5,
            "june": 6,
            "july": 7,
            "august": 8,
            "september": 9,
            "october": 10,
            "november": 11,
            "december": 12,
        }

        for match in month_pattern.finditer(text):
            day = int(match.group(1))
            month = month_numbers[match.group(2).lower()]
            year = int(match.group(3))

            try:
                dates.add(
                    datetime(
                        year,
                        month,
                        day
                    ).date()
                )
            except ValueError:
                continue

        return dates

    # ============================================================
    # AMOUNT HANDLING
    # ============================================================

    @staticmethod
    def _extract_amount_numbers(text):
        text = str(text or "")

        matches = re.findall(
            r"(?:₹|rs\.?|inr)?\s*"
            r"(\d{1,3}(?:,\d{3})*(?:\.\d{1,2})?"
            r"|\d+(?:\.\d{1,2})?)",
            text,
            flags=re.IGNORECASE,
        )

        values = set()

        for match in matches:
            try:
                values.add(
                    round(
                        float(match.replace(",", "")),
                        2
                    )
                )
            except ValueError:
                continue

        return values

    def _amounts_match(self, first, second):
        first_values = self._extract_amount_numbers(first)
        second_values = self._extract_amount_numbers(second)

        if not first_values or not second_values:
            return self._values_match(first, second)

        return bool(
            first_values & second_values
        )

    # ============================================================
    # INVOICE FIELD EXTRACTION
    # ============================================================

    @staticmethod
    def _extract_seller(text):
        patterns = [
            r"(?im)^\s*(?:seller|sold\s+by|merchant|vendor)"
            r"\s*[:\-]?\s*([^\n]+)",
            r"(?im)^\s*(?:seller\s*/\s*company)"
            r"\s*[:\-]?\s*([^\n]+)",
        ]

        return EvidenceConsistencyService._first_match(
            text,
            patterns,
        )

    @staticmethod
    def _extract_product(text):
        patterns = [
            r"(?im)^\s*(?:product\s+name|item\s+description|item)"
            r"\s*[:\-]?\s*([^\n]+)",
            r"(?im)^\s*description\s*[:\-]?\s*([^\n]+)",
        ]

        value = EvidenceConsistencyService._first_match(
            text,
            patterns,
        )

        if value:
            return value

        # Handles invoice table layouts such as:
        # Product Quantity Unit Price Amount
        # Demo Smartphone 5G 128GB 1 ₹20,000 ₹20,000
        table_match = re.search(
            r"(?im)^\s*product\s+quantity\s+unit\s+price\s+amount\s*$"
            r"\s*\n\s*([^\n]+)",
            text,
        )

        if table_match:
            line = table_match.group(1).strip()

            # Remove the quantity and trailing monetary columns.
            cleaned = re.sub(
                r"\s+\d+\s+(?:[^\d\n]*\d[\d,]*(?:\.\d+)?)"
                r"\s+(?:[^\d\n]*\d[\d,]*(?:\.\d+)?)\s*$",
                "",
                line,
            ).strip()

            if cleaned:
                return cleaned

        return None

    @staticmethod
    def _extract_purchase_date(text):
        patterns = [
            r"(?im)^\s*(?:purchase\s+date|invoice\s+date|order\s+date)"
            r"\s*[:\-]?\s*([^\n]+)",
        ]

        return EvidenceConsistencyService._first_match(
            text,
            patterns,
        )

    @staticmethod
    def _extract_transaction_date(text):
        patterns = [
            r"(?im)^\s*(?:transaction\s+date|payment\s+date)"
            r"\s*[:\-]?\s*([^\n]+)",
        ]

        return EvidenceConsistencyService._first_match(
            text,
            patterns,
        )

    @staticmethod
    def _extract_amount(text):
        patterns = [
            r"(?im)^\s*(?:total\s+amount|amount\s+paid|grand\s+total|"
            r"total\s+paid|total)"
            r"\s*[:\-]?\s*[^\d\n]*([\d,]+(?:\.\d{1,2})?)",
        ]

        return EvidenceConsistencyService._first_match(
            text,
            patterns,
        )

    @staticmethod
    def _extract_bank(text):
        patterns = [
            r"(?im)^\s*(?:bank|payment\s+platform|paid\s+via|payment\s+method)"
            r"\s*[:\-]?\s*([^\n]+)",
        ]

        return EvidenceConsistencyService._first_match(
            text,
            patterns,
        )

    @staticmethod
    def _extract_invoice_number(text):
        patterns = [
            r"(?:invoice\s+(?:no|number|#))\s*[:\-]?\s*([A-Z0-9\-]+)",
            r"\b(TEST-INV-[A-Z0-9\-]+)\b",
        ]

        return EvidenceConsistencyService._first_match(
            text,
            patterns,
        )

    @staticmethod
    def _extract_order_id(text):
        patterns = [
            r"(?:order\s+(?:id|no|number|#))\s*[:\-]?\s*([A-Z0-9\-]+)",
            r"\b(TEST-ORDER-[A-Z0-9\-]+)\b",
        ]

        return EvidenceConsistencyService._first_match(
            text,
            patterns,
        )

    @staticmethod
    def _first_match(text, patterns):
        for pattern in patterns:
            match = re.search(
                pattern,
                text,
                flags=re.IGNORECASE,
            )

            if match:
                return match.group(1).strip()

        return None


evidence_consistency_service = EvidenceConsistencyService()
