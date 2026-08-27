"""
Deterministic Legal Action Plan Service.

Builds a practical next-step workflow from information already produced by
the legal complaint pipeline. No LLM call is made.
"""

from __future__ import annotations

from typing import Any


class ActionPlanService:

    def _get(self, obj: Any, key: str, default: Any = None) -> Any:
        if isinstance(obj, dict):
            return obj.get(key, default)

        return getattr(obj, key, default)

    def _step(
        self,
        number: int,
        title: str,
        description: str,
        actions: list[str],
        status: str,
        reason: str,
    ) -> dict[str, Any]:

        return {
            "step": number,
            "title": title,
            "description": description,
            "actions": actions,
            "status": status,
            "reason": reason,
        }

    def build_plan(
        self,
        request: Any,
        report: dict[str, Any] | None = None,
    ) -> dict[str, Any]:

        report = report or {}

        readiness = report.get("readiness") or {}
        readiness_evidence = readiness.get("evidence") or {}

        detected = readiness_evidence.get("detected") or []
        missing = readiness_evidence.get("missing") or []

        consistency = report.get("evidence_consistency") or {}
        discrepancies = consistency.get("discrepancies") or []

        timeline = report.get("timeline") or {}
        timeline_conflicts = timeline.get("conflicts") or []

        complaint = str(
            report.get("complaint") or ""
        ).strip()

        steps = []

        # ============================================================
        # STEP 1 — PRESERVE EVIDENCE
        # ============================================================

        evidence_actions = [
            "Keep the purchase invoice, receipt or order confirmation.",
            "Keep payment proof and transaction records.",
            "Keep photographs, videos or screenshots showing the problem.",
            "Keep warranty documents and written communication with the seller or service provider.",
        ]

        if detected:

            evidence_reason = (
                f"The readiness service detected {len(detected)} "
                "evidence group(s). Preserve the originals and keep "
                "copies available."
            )

        else:

            evidence_reason = (
                "The system did not identify supporting evidence groups "
                "yet. Collect and preserve relevant documents before filing."
            )

        steps.append(
            self._step(
                1,
                "Preserve Your Evidence",
                "Keep the documents and records that support the facts of the case.",
                evidence_actions,
                "READY" if detected else "ATTENTION_REQUIRED",
                evidence_reason,
            )
        )

        # ============================================================
        # STEP 2 — RESOLVE EVIDENCE CONFLICTS
        # ============================================================

        all_conflicts = list(discrepancies)

        existing_fields = {
            str(item.get("field"))
            for item in all_conflicts
            if isinstance(item, dict)
        }

        for conflict in timeline_conflicts:

            if not isinstance(conflict, dict):
                continue

            field = str(
                conflict.get("field")
            )

            if field not in existing_fields:

                all_conflicts.append(conflict)

                existing_fields.add(field)

        if all_conflicts:

            conflict_actions = [
                "Compare the conflicting value with the original document.",
                "Correct the case details if the uploaded evidence is the authoritative record.",
                "Do not submit the complaint until the discrepancy has been reviewed.",
            ]

            steps.append(
                self._step(
                    2,
                    "Resolve Evidence Conflicts",
                    "Some case details differ from information found in uploaded evidence.",
                    conflict_actions,
                    "ATTENTION_REQUIRED",
                    f"{len(all_conflicts)} discrepancy/discrepancies require verification.",
                )
            )

        else:

            steps.append(
                self._step(
                    2,
                    "Verify Case Details",
                    "No evidence conflicts were detected by the current checks.",
                    [
                        "Review the dates, parties, product/service and amount once before filing.",
                        "Confirm that the information in the complaint matches your supporting documents.",
                    ],
                    "READY",
                    "The current evidence consistency and timeline checks found no conflicts.",
                )
            )

        # ============================================================
        # STEP 3 — COMPLETE MISSING EVIDENCE
        # ============================================================

        if missing:

            steps.append(
                self._step(
                    3,
                    "Complete Missing Evidence",
                    "The readiness assessment identified evidence groups that may still be needed.",
                    [
                        f"Collect: {item}"
                        for item in missing
                    ],
                    "ATTENTION_REQUIRED",
                    f"{len(missing)} evidence group(s) are currently marked as missing.",
                )
            )

        else:

            steps.append(
                self._step(
                    3,
                    "Confirm Evidence Completeness",
                    "No missing evidence groups were reported by the readiness assessment.",
                    [
                        "Check that all supporting files are readable and available.",
                        "Keep the original documents safely stored.",
                    ],
                    "READY",
                    "The readiness assessment did not identify missing evidence groups.",
                )
            )

        # ============================================================
        # STEP 4 — REVIEW COMPLAINT
        # ============================================================

        if complaint:

            steps.append(
                self._step(
                    4,
                    "Review the Complaint Draft",
                    "A complaint draft has been generated from the retrieved legal information and case details.",
                    [
                        "Check names, dates, parties, product/service details and amounts.",
                        "Check the requested remedy and factual statements.",
                        "Review the cited legal provisions before using the draft.",
                    ],
                    "READY_FOR_REVIEW",
                    "A complaint draft is available for citizen review and editing.",
                )
            )

        else:

            steps.append(
                self._step(
                    4,
                    "Prepare the Complaint",
                    "A complaint draft is not currently available.",
                    [
                        "Complete the required case information.",
                        "Generate and review the complaint draft.",
                    ],
                    "PENDING",
                    "No generated complaint text was found in the current report.",
                )
            )

        # ============================================================
        # STEP 5 — APPROPRIATE REDRESSAL STEP
        # ============================================================

        remedy = self._get(
            request,
            "remedy",
            "",
        )

        remedy_text = str(
            remedy or ""
        ).strip()

        final_actions = [
            "If the dispute remains unresolved, consider the appropriate consumer redressal mechanism applicable to the case.",
            "Keep records of notices, emails, messages, receipts and responses.",
            "Review the applicable forum, jurisdiction and filing requirements before submitting anything.",
        ]

        if remedy_text:

            final_actions.insert(
                0,
                f"Review whether the requested remedy ({remedy_text}) is supported by the facts and applicable law.",
            )

        steps.append(
            self._step(
                5,
                "Proceed With the Appropriate Redressal Step",
                "If the issue remains unresolved after reviewing the evidence and complaint, proceed through the appropriate legal redressal mechanism.",
                final_actions,
                "NEXT_STEP",
                "The system provides a procedural next-step suggestion; it does not determine the legal merits or guarantee an outcome.",
            )
        )

        # ============================================================
        # OVERALL STATUS
        # ============================================================

        attention_count = sum(
            1
            for step in steps
            if step["status"] == "ATTENTION_REQUIRED"
        )

        if attention_count:

            overall_status = "REVIEW_REQUIRED"

        else:

            overall_status = "READY_FOR_REVIEW"

        return {
            "overall_status": overall_status,
            "steps": steps,
            "attention_count": attention_count,
            "summary": (
                "Review the highlighted items before proceeding."
                if attention_count
                else "The action plan is ready for citizen review."
            ),
        }


action_plan_service = ActionPlanService()