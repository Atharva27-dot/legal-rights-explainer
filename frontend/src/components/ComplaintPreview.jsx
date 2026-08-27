import { useEffect, useState } from "react";
import {
  FaClipboardList,
  FaCopy,
  FaDownload,
  FaSave,
  FaCheckCircle,
  FaEdit,
  FaUndo,
} from "react-icons/fa";
import toast from "react-hot-toast";

import {
  downloadComplaintPDF,
  saveCase,
} from "../services/api";

/* ============================================================
   TIMELINE TYPE BADGE
   ============================================================ */

function TimelineTypeBadge({ type }) {
  const config = {
    USER_REPORTED: {
      label: "USER REPORTED",
      className: "bg-blue-100 text-blue-800 border-blue-200",
    },

    EVIDENCE_DERIVED: {
      label: "EVIDENCE DERIVED",
      className: "bg-emerald-100 text-emerald-800 border-emerald-200",
    },

    DERIVED: {
      label: "DERIVED",
      className: "bg-amber-100 text-amber-800 border-amber-200",
    },
  };

  const item = config[type] || {
    label: type || "UNKNOWN",
    className: "bg-slate-100 text-slate-700 border-slate-200",
  };

  return (
    <span
      className={`inline-flex items-center px-2.5 py-1 rounded-lg border text-xs font-semibold ${item.className}`}
    >
      {item.label}
    </span>
  );
}

/* ============================================================
   MAIN COMPONENT
   ============================================================ */

export default function ComplaintPreview({ caseData }) {
  const [saving, setSaving] = useState(false);
  const [saved, setSaved] = useState(false);
  const [caseId, setCaseId] = useState("");
  const [editing, setEditing] = useState(false);
  const [editedComplaint, setEditedComplaint] = useState("");

  useEffect(() => {
    if (caseData?.report?.complaint) {
      setEditedComplaint(caseData.report.complaint);
      setEditing(false);
      setSaved(false);
      setCaseId("");
    }
  }, [caseData]);

  if (!caseData) {
    return (
      <div className="bg-white rounded-3xl shadow-xl border border-slate-200 p-12 text-center">
        <div className="text-6xl mb-5">📝</div>

        <h2 className="text-2xl font-bold text-slate-700">
          Complaint Preview
        </h2>

        <p className="text-slate-500 mt-4">
          Generate a complaint to preview and edit it here.
        </p>
      </div>
    );
  }

  const { formData, report } = caseData;

  const readiness = report?.readiness || {};
  const caseAnalysis = report?.case_analysis || {};
  const grounding = report?.grounding || {};

  /* ============================================================
     TIMELINE DATA
     ============================================================ */

  const timeline = report?.timeline || {};

  const timelineEvents = Array.isArray(timeline.events)
    ? timeline.events
    : [];

  const timelineConflicts = Array.isArray(timeline.conflicts)
    ? timeline.conflicts
    : [];

  const complaintText =
    editedComplaint || report?.complaint || "";

  /* ============================================================
     CURRENT REPORT
     ============================================================ */

  const getCurrentReport = () => ({
    ...report,
    complaint: complaintText,
  });

  /* ============================================================
     EDIT HANDLERS
     ============================================================ */

  const handleEdit = () => {
    setEditing(true);
    setSaved(false);
  };

  const handleCancelEdit = () => {
    setEditedComplaint(report?.complaint || "");
    setEditing(false);
  };

  const handleSaveEdit = () => {
    if (!editedComplaint.trim()) {
      toast.error("Complaint cannot be empty.");
      return;
    }

    setEditing(false);
    setSaved(false);

    toast.success("Complaint changes saved in this draft.");
  };

  /* ============================================================
     COPY
     ============================================================ */

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(complaintText);

      toast.success("Complaint copied.");
    } catch (error) {
      console.error(error);

      toast.error("Unable to copy complaint.");
    }
  };

  /* ============================================================
     DOWNLOAD PDF
     ============================================================ */

  const handleDownload = async () => {
    if (!complaintText.trim()) {
      toast.error("There is no complaint to download.");
      return;
    }

    try {
      const pdfBlob = await downloadComplaintPDF(
        getCurrentReport()
      );

      const url = window.URL.createObjectURL(pdfBlob);

      const link = document.createElement("a");

      link.href = url;
      link.download = "Legal_Complaint_Draft.pdf";

      document.body.appendChild(link);

      link.click();

      document.body.removeChild(link);

      window.URL.revokeObjectURL(url);

      toast.success("Complaint PDF downloaded.");
    } catch (error) {
      console.error(error);

      toast.error("Unable to download PDF.");
    }
  };

  /* ============================================================
     SAVE CASE
     ============================================================ */

  const handleSave = async () => {
    if (saved) return;

    if (!complaintText.trim()) {
      toast.error("Complaint cannot be empty.");
      return;
    }

    try {
      setSaving(true);

      const response = await saveCase({
        citizen_name: formData?.name,
        city: formData?.city,
        report: getCurrentReport(),
      });

      setSaved(true);
      setCaseId(response.case_id);

      toast.success("Case saved successfully.");
    } catch (error) {
      console.error(error);

      toast.error("Unable to save case.");
    } finally {
      setSaving(false);
    }
  };

  /* ============================================================
     GROUNDING STATUS
     ============================================================ */

  const groundingVerified =
    grounding.status === "Verified" ||
    caseAnalysis.grounding_status === "Verified";

  const groundingNeedsReview =
    grounding.status === "Needs Review" ||
    caseAnalysis.grounding_status === "Needs Review";

  /* ============================================================
     EVIDENCE COMPLETENESS SCORE
     ============================================================ */

  const detectedEvidence =
    readiness.evidence?.detected || [];

  const missingEvidence =
    readiness.evidence?.missing || [];

  const evidenceTotal =
    detectedEvidence.length + missingEvidence.length;

  const evidenceCompleteness =
    Math.round(
      (detectedEvidence.length /
        Math.max(1, evidenceTotal)) *
        100
    );

  return (
    <div className="bg-white rounded-3xl shadow-xl border border-slate-200 overflow-hidden">

      {/* ======================================================
          HEADER
          ====================================================== */}

      <div className="bg-gradient-to-r from-emerald-700 to-teal-600 text-white px-8 py-6">

        <div className="flex items-center gap-3">

          <FaClipboardList className="text-2xl" />

          <div>

            <h2 className="text-3xl font-bold">
              AI-Assisted Legal Complaint Draft
            </h2>

            <p className="text-emerald-100 mt-1">
              Review and edit the generated draft before saving or downloading.
            </p>

          </div>

        </div>

      </div>

      {/* ======================================================
          WARNING
          ====================================================== */}

      <div className="mx-8 mt-6 bg-amber-50 border border-amber-200 rounded-2xl p-4 text-sm text-amber-900">

        <strong>Review before use:</strong>{" "}

        This is an AI-assisted draft generated from retrieved legal
        provisions. Review and edit it before submitting or relying on it.
        It is not a substitute for professional legal advice.

      </div>

      {/* ======================================================
          SUMMARY CARDS
          ====================================================== */}

      <div className="p-8 border-b">

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">

          {/* Legal Readiness */}

          <div className="bg-blue-50 border border-blue-200 rounded-2xl p-5">

            <p className="text-sm text-blue-700 font-semibold">
              Legal Readiness
            </p>

            <p className="text-4xl font-bold text-blue-900 mt-2">
              {readiness.score ?? 0}%
            </p>

            <p className="text-blue-900 font-semibold mt-1">
              {readiness.status || "Not evaluated"}
            </p>

          </div>

          {/* Retrieval Confidence */}

          <div className="bg-slate-50 border border-slate-200 rounded-2xl p-5">

            <p className="text-sm text-slate-500 font-semibold">
              Retrieval Confidence
            </p>

            <p className="text-2xl font-bold text-slate-800 mt-3">
              {report.confidence || "Unknown"}
            </p>

            <p className="text-sm text-slate-500 mt-1">
              Based on the highest-ranked legal provision.
            </p>

          </div>

          {/* Grounding */}

          <div
            className={
              groundingVerified
                ? "bg-green-50 border border-green-200 rounded-2xl p-5"
                : groundingNeedsReview
                ? "bg-yellow-50 border border-yellow-200 rounded-2xl p-5"
                : "bg-slate-50 border border-slate-200 rounded-2xl p-5"
            }
          >

            <p className="text-sm font-semibold">
              Grounding Status
            </p>

            <p className="text-2xl font-bold mt-3">

              {groundingVerified
                ? "✓ Verified"
                : groundingNeedsReview
                ? "⚠ Needs Review"
                : "Not available"}

            </p>

            <p className="text-sm mt-1">
              Legal authorities are checked against retrieved evidence.
            </p>

          </div>

        </div>

      </div>

      {/* ======================================================
          CASE ASSESSMENT
          ====================================================== */}

      <div className="p-8 border-b">

        <div className="flex items-center justify-between gap-4 mb-5">

          <div>

            <h3 className="font-bold text-xl text-slate-800">
              Case Assessment
            </h3>

            <p className="text-sm text-slate-500 mt-1">
              A summary of the retrieved legal analysis and available evidence.
            </p>

          </div>

          {report?.evidence_consistency?.overall_status ===
            "MISMATCH" && (

            <span className="px-3 py-2 rounded-xl bg-amber-100 text-amber-800 text-sm font-semibold">
              ⚠ Evidence mismatch
            </span>

          )}

        </div>

        {/* Case analysis cards */}

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">

          <div className="bg-slate-50 border border-slate-200 rounded-2xl p-5">

            <p className="text-sm text-slate-500 font-semibold">
              Category
            </p>

            <p className="text-lg font-bold text-slate-800 mt-2">
              {caseAnalysis.category || "Not provided"}
            </p>

          </div>

          <div className="bg-slate-50 border border-slate-200 rounded-2xl p-5">

            <p className="text-sm text-slate-500 font-semibold">
              Applicable Act
            </p>

            <p className="text-lg font-bold text-slate-800 mt-2">
              {caseAnalysis.applicable_act || "Not provided"}
            </p>

          </div>

          <div className="bg-slate-50 border border-slate-200 rounded-2xl p-5">

            <p className="text-sm text-slate-500 font-semibold">
              Recommended Remedy
            </p>

            <p className="text-lg font-bold text-slate-800 mt-2">
              {caseAnalysis.recommended_remedy || "Not provided"}
            </p>

          </div>

        </div>

        {/* ==================================================
            EVIDENCE COMPLETENESS
            ================================================== */}

        {readiness.evidence && (

          <div className="mt-5 bg-white border border-slate-200 rounded-2xl p-5">

            <div className="flex items-center justify-between mb-3">

              <div>

                <p className="font-semibold text-slate-800">
                  Evidence Completeness
                </p>

                <p className="text-sm text-slate-500">
                  Based on evidence groups detected by the readiness service.
                </p>

              </div>

              <span className="font-bold text-slate-800">
                {evidenceCompleteness}%
              </span>

            </div>

            <div className="h-3 bg-slate-200 rounded-full overflow-hidden">

              <div
                className="h-full bg-emerald-600 rounded-full"
                style={{
                  width: `${Math.min(
                    100,
                    evidenceCompleteness
                  )}%`,
                }}
              />

            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-5">

              {/* Detected */}

              <div>

                <p className="text-sm font-semibold text-green-700 mb-2">
                  Detected Evidence
                </p>

                {detectedEvidence.length > 0 ? (

                  <ul className="space-y-2">

                    {detectedEvidence.map(
                      (item, index) => (

                        <li
                          key={index}
                          className="flex gap-2 text-sm text-slate-700"
                        >

                          <FaCheckCircle className="text-green-600 mt-0.5 flex-shrink-0" />

                          {item}

                        </li>

                      )
                    )}

                  </ul>

                ) : (

                  <p className="text-sm text-slate-500">
                    No evidence groups detected.
                  </p>

                )}

              </div>

              {/* Missing */}

              <div>

                <p className="text-sm font-semibold text-amber-700 mb-2">
                  Missing Evidence
                </p>

                {missingEvidence.length > 0 ? (

                  <ul className="space-y-2">

                    {missingEvidence.map(
                      (item, index) => (

                        <li
                          key={index}
                          className="flex gap-2 text-sm text-slate-700"
                        >

                          <span className="text-amber-600">
                            ⚠
                          </span>

                          {item}

                        </li>

                      )
                    )}

                  </ul>

                ) : (

                  <p className="text-sm text-slate-500">
                    No missing evidence groups detected.
                  </p>

                )}

              </div>

            </div>

          </div>

        )}

        {/* ==================================================
            EVIDENCE DISCREPANCIES
            ================================================== */}

        {report?.evidence_consistency?.discrepancies?.length >
          0 && (

          <div className="mt-5 bg-amber-50 border border-amber-200 rounded-2xl p-5">

            <div className="mb-3">

              <p className="font-semibold text-amber-900">
                Evidence Conflicts
              </p>

              <p className="text-sm text-amber-800 mt-1">
                These differences should be verified before filing.
                The system does not decide which version is correct.
              </p>

            </div>

            <div className="space-y-3">

              {report.evidence_consistency.discrepancies.map(
                (item, index) => (

                  <div
                    key={index}
                    className="bg-white border border-amber-200 rounded-xl p-4"
                  >

                    <p className="font-semibold text-slate-800">
                      {item.label || item.field}
                    </p>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-3 mt-2 text-sm">

                      <div>

                        <p className="text-slate-500">
                          Case details
                        </p>

                        <p className="font-medium text-slate-800">
                          {item.user_value ??
                            "Not provided"}
                        </p>

                      </div>

                      <div>

                        <p className="text-slate-500">
                          Uploaded evidence
                        </p>

                        <p className="font-medium text-slate-800">
                          {item.evidence_value ??
                            "Not found"}
                        </p>

                      </div>

                    </div>

                  </div>

                )
              )}

            </div>

          </div>

        )}

      </div>

      {/* ======================================================
          EVIDENCE TIMELINE
          ====================================================== */}

      {timelineEvents.length > 0 && (

        <div className="p-8 border-b">

          <div className="flex flex-col md:flex-row md:items-start md:justify-between gap-4 mb-6">

            <div>

              <h3 className="font-bold text-xl text-slate-800">
                Evidence Timeline
              </h3>

              <p className="text-sm text-slate-500 mt-1">
                Chronological view of citizen-reported,
                evidence-derived, and derived events.
              </p>

            </div>

            {timeline.summary && (

              <div className="flex gap-2 flex-wrap">

                <span className="bg-slate-100 text-slate-700 rounded-xl px-3 py-2 text-sm font-semibold">
                  {timeline.summary.event_count ??
                    timelineEvents.length}{" "}
                  events
                </span>

                <span
                  className={
                    (timeline.summary.conflict_count || 0) > 0
                      ? "bg-amber-100 text-amber-800 rounded-xl px-3 py-2 text-sm font-semibold"
                      : "bg-emerald-100 text-emerald-800 rounded-xl px-3 py-2 text-sm font-semibold"
                  }
                >
                  {timeline.summary.conflict_count ??
                    timelineConflicts.length}{" "}
                  conflicts
                </span>

              </div>

            )}

          </div>

          {/* Timeline */}

          <div className="relative">

            {/* Vertical line */}

            <div className="absolute left-[11px] top-3 bottom-3 w-px bg-slate-200" />

            <div className="space-y-6">

              {timelineEvents.map(
                (event, index) => (

                  <div
                    key={`${event.date_iso || "undated"}-${event.title}-${index}`}
                    className="relative pl-9"
                  >

                    {/* Timeline dot */}

                    <div className="absolute left-0 top-1.5 h-6 w-6 rounded-full bg-white border-4 border-emerald-500 z-10" />

                    {/* Event card */}

                    <div className="bg-white border border-slate-200 rounded-2xl p-5 shadow-sm">

                      <div className="flex flex-col md:flex-row md:items-start md:justify-between gap-3">

                        <div>

                          <p className="text-sm font-semibold text-emerald-700">
                            {event.date ||
                              "Date not available"}
                          </p>

                          <h4 className="font-bold text-slate-800 mt-1">
                            {event.title ||
                              "Case event"}
                          </h4>

                        </div>

                        <TimelineTypeBadge
                          type={event.type}
                        />

                      </div>

                      {event.details && (

                        <p className="text-sm text-slate-600 mt-3 leading-6">
                          {event.details}
                        </p>

                      )}

                      <div className="flex flex-wrap gap-2 mt-3 text-xs">

                        {event.source && (

                          <span className="bg-slate-100 text-slate-600 rounded-lg px-2.5 py-1">
                            Source: {event.source}
                          </span>

                        )}

                        {event.confidence && (

                          <span className="bg-slate-100 text-slate-600 rounded-lg px-2.5 py-1">
                            Confidence: {event.confidence}
                          </span>

                        )}

                      </div>

                    </div>

                  </div>

                )
              )}

            </div>

          </div>

          {/* ==================================================
              TIMELINE CONFLICTS
              ================================================== */}

          {timelineConflicts.length > 0 && (

            <div className="mt-6 bg-amber-50 border border-amber-200 rounded-2xl p-5">

              <div className="flex items-start gap-3">

                <span className="text-xl">
                  ⚠
                </span>

                <div>

                  <p className="font-semibold text-amber-900">
                    Timeline Conflicts Require Verification
                  </p>

                  <p className="text-sm text-amber-800 mt-1">
                    The system does not decide which conflicting
                    version is correct.
                  </p>

                </div>

              </div>

              <div className="space-y-3 mt-4">

                {timelineConflicts.map(
                  (item, index) => (

                    <div
                      key={`${item.field || "conflict"}-${index}`}
                      className="bg-white border border-amber-200 rounded-xl p-4"
                    >

                      <p className="font-semibold text-slate-800">
                        {item.label ||
                          item.field ||
                          "Timeline conflict"}
                      </p>

                      <div className="grid grid-cols-1 md:grid-cols-2 gap-3 mt-3 text-sm">

                        <div>

                          <p className="text-slate-500">
                            Citizen-provided
                          </p>

                          <p className="font-medium text-slate-800">
                            {item.user_value ??
                              "Not provided"}
                          </p>

                        </div>

                        <div>

                          <p className="text-slate-500">
                            Uploaded evidence
                          </p>

                          <p className="font-medium text-slate-800">
                            {item.evidence_value ??
                              "Not found"}
                          </p>

                        </div>

                      </div>

                      {item.message && (

                        <p className="text-sm text-amber-800 mt-3">
                          {item.message}
                        </p>

                      )}

                    </div>

                  )
                )}

              </div>

            </div>

          )}

          {/* Timeline status */}

          {timeline.summary && (

            <div className="mt-5">

              {timeline.summary.status ===
              "CONFLICTS_FOUND" ? (

                <div className="bg-amber-50 border border-amber-200 rounded-xl p-4 text-sm text-amber-900">

                  <strong>Verification required:</strong>{" "}

                  One or more timeline facts conflict with the
                  uploaded evidence.

                </div>

              ) : (

                <div className="bg-emerald-50 border border-emerald-200 rounded-xl p-4 text-sm text-emerald-800">

                  ✓ No timeline conflicts were detected.

                </div>

              )}

            </div>

          )}

        </div>

      )}

            {/* ======================================================
          LEGAL ACTION PLAN
          ====================================================== */}

      {report?.action_plan?.steps?.length > 0 && (
        <div className="p-8 border-b">

          <div className="flex flex-col md:flex-row md:items-start md:justify-between gap-4 mb-6">

            <div>
              <h3 className="font-bold text-xl text-slate-800">
                Legal Action Plan
              </h3>

              <p className="text-sm text-slate-500 mt-1">
                Recommended next steps based on the case details,
                evidence assessment, conflicts, and generated complaint.
              </p>
            </div>

            <span
              className={
                report.action_plan.overall_status === "REVIEW_REQUIRED"
                  ? "bg-amber-100 text-amber-800 border border-amber-200 rounded-xl px-3 py-2 text-sm font-semibold"
                  : "bg-emerald-100 text-emerald-800 border border-emerald-200 rounded-xl px-3 py-2 text-sm font-semibold"
              }
            >
              {report.action_plan.overall_status === "REVIEW_REQUIRED"
                ? "⚠ Review Required"
                : "✓ Ready for Review"}
            </span>

          </div>

          {/* Action Plan Steps */}

          <div className="space-y-4">

            {report.action_plan.steps.map((step) => {

              const statusConfig = {
                READY: {
                  label: "READY",
                  icon: "✓",
                  classes:
                    "bg-emerald-100 text-emerald-800 border-emerald-200",
                  iconClasses:
                    "bg-emerald-600 text-white",
                },

                ATTENTION_REQUIRED: {
                  label: "ATTENTION REQUIRED",
                  icon: "⚠",
                  classes:
                    "bg-amber-100 text-amber-800 border-amber-200",
                  iconClasses:
                    "bg-amber-500 text-white",
                },

                READY_FOR_REVIEW: {
                  label: "READY FOR REVIEW",
                  icon: "📝",
                  classes:
                    "bg-blue-100 text-blue-800 border-blue-200",
                  iconClasses:
                    "bg-blue-600 text-white",
                },

                NEXT_STEP: {
                  label: "NEXT STEP",
                  icon: "→",
                  classes:
                    "bg-indigo-100 text-indigo-800 border-indigo-200",
                  iconClasses:
                    "bg-indigo-600 text-white",
                },

                PENDING: {
                  label: "PENDING",
                  icon: "○",
                  classes:
                    "bg-slate-100 text-slate-700 border-slate-200",
                  iconClasses:
                    "bg-slate-500 text-white",
                },
              };

              const config =
                statusConfig[step.status] ||
                statusConfig.PENDING;

              return (
                <div
                  key={step.step}
                  className={`border rounded-2xl p-5 ${
                    step.status === "ATTENTION_REQUIRED"
                      ? "border-amber-200 bg-amber-50/50"
                      : "border-slate-200 bg-white"
                  }`}
                >

                  <div className="flex items-start gap-4">

                    {/* Step Number */}

                    <div
                      className={`flex-shrink-0 w-10 h-10 rounded-full flex items-center justify-center font-bold ${config.iconClasses}`}
                    >
                      {step.step}
                    </div>

                    <div className="flex-1 min-w-0">

                      {/* Title + Status */}

                      <div className="flex flex-col md:flex-row md:items-start md:justify-between gap-3">

                        <div>

                          <h4 className="font-bold text-lg text-slate-800">
                            {step.title}
                          </h4>

                          <p className="text-sm text-slate-600 mt-1">
                            {step.description}
                          </p>

                        </div>

                        <span
                          className={`self-start inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg border text-xs font-bold whitespace-nowrap ${config.classes}`}
                        >
                          <span>
                            {config.icon}
                          </span>

                          {config.label}
                        </span>

                      </div>

                      {/* Actions */}

                      {Array.isArray(step.actions) &&
                        step.actions.length > 0 && (

                          <div className="mt-4">

                            <p className="text-sm font-semibold text-slate-700 mb-2">
                              Recommended actions
                            </p>

                            <ul className="space-y-2">

                              {step.actions.map(
                                (action, actionIndex) => (

                                  <li
                                    key={actionIndex}
                                    className="flex items-start gap-2 text-sm text-slate-700"
                                  >

                                    <span
                                      className={
                                        step.status ===
                                        "ATTENTION_REQUIRED"
                                          ? "text-amber-600 mt-0.5"
                                          : "text-emerald-600 mt-0.5"
                                      }
                                    >
                                      {step.status ===
                                      "ATTENTION_REQUIRED"
                                        ? "⚠"
                                        : "✓"}
                                    </span>

                                    <span>
                                      {action}
                                    </span>

                                  </li>

                                )
                              )}

                            </ul>

                          </div>

                        )}

                      {/* Reason */}

                      {step.reason && (

                        <div className="mt-4 bg-slate-50 border border-slate-200 rounded-xl p-3">

                          <p className="text-xs font-semibold text-slate-500 uppercase tracking-wide">
                            Why this step?
                          </p>

                          <p className="text-sm text-slate-600 mt-1">
                            {step.reason}
                          </p>

                        </div>

                      )}

                    </div>

                  </div>

                </div>
              );
            })}

          </div>

          {/* Overall Summary */}

          {report.action_plan.summary && (

            <div
              className={
                report.action_plan.overall_status ===
                "REVIEW_REQUIRED"
                  ? "mt-5 bg-amber-50 border border-amber-200 rounded-xl p-4 text-sm text-amber-900"
                  : "mt-5 bg-emerald-50 border border-emerald-200 rounded-xl p-4 text-sm text-emerald-800"
              }
            >

              <strong>
                Action Plan Summary:
              </strong>{" "}

              {report.action_plan.summary}

            </div>

          )}

        </div>
      )}

      {/* ======================================================
          APPLICABLE RIGHTS
          ====================================================== */}

      {Array.isArray(caseAnalysis.rights) &&
        caseAnalysis.rights.length > 0 && (

          <div className="p-8 border-b">

            <h3 className="font-bold text-xl mb-4">
              Applicable Rights
            </h3>

            <ul className="space-y-3">

              {caseAnalysis.rights.map(
                (item, index) => (

                  <li
                    key={index}
                    className="flex items-center gap-3 text-slate-700"
                  >

                    <FaCheckCircle className="text-green-600 flex-shrink-0" />

                    {item}

                  </li>

                )
              )}

            </ul>

          </div>

        )}

      {/* ======================================================
          READINESS RECOMMENDATIONS
          ====================================================== */}

      {Array.isArray(readiness.recommendations) &&
        readiness.recommendations.length > 0 && (

          <div className="p-8 border-b">

            <h3 className="font-bold text-xl mb-4">
              Evidence / Readiness Recommendations
            </h3>

            <ul className="space-y-2 text-slate-700">

              {readiness.recommendations.map(
                (item, index) => (

                  <li
                    key={index}
                    className="flex gap-3"
                  >

                    <span>•</span>

                    <span>
                      {item}
                    </span>

                  </li>

                )
              )}

            </ul>

          </div>

        )}

      {/* ======================================================
          COMPLAINT DRAFT
          ====================================================== */}

      <div className="p-8">

        <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4 mb-5">

          <div>

            <h3 className="font-bold text-xl text-slate-800">
              Complaint Draft
            </h3>

            <p className="text-sm text-slate-500 mt-1">

              {editing
                ? "Edit the draft below, then select Save Edits."
                : "Select Edit Draft if you want to modify the complaint."}

            </p>

          </div>

          {!editing ? (

            <button
              onClick={handleEdit}
              className="bg-indigo-700 hover:bg-indigo-600 text-white rounded-xl px-5 py-3 flex items-center justify-center gap-2"
            >

              <FaEdit />

              Edit Draft

            </button>

          ) : (

            <div className="flex gap-3">

              <button
                onClick={handleCancelEdit}
                className="border border-slate-300 rounded-xl px-5 py-3 flex items-center gap-2 hover:bg-slate-100"
              >

                <FaUndo />

                Cancel

              </button>

              <button
                onClick={handleSaveEdit}
                className="bg-emerald-700 hover:bg-emerald-600 text-white rounded-xl px-5 py-3 flex items-center gap-2"
              >

                <FaCheckCircle />

                Save Edits

              </button>

            </div>

          )}

        </div>

        {editing ? (

          <textarea
            value={editedComplaint}
            onChange={(event) =>
              setEditedComplaint(event.target.value)
            }
            rows={28}
            spellCheck={false}
            className="w-full border-2 border-indigo-200 rounded-2xl p-6 leading-8 text-slate-700 resize-y focus:outline-none focus:ring-2 focus:ring-indigo-500"
            aria-label="Editable complaint draft"
          />

        ) : (

          <div className="bg-slate-50 border border-slate-200 rounded-2xl p-6 whitespace-pre-wrap leading-8 text-slate-700">
            {complaintText}
          </div>

        )}

      </div>

      {/* ======================================================
          SAVED CASE
          ====================================================== */}

      {saved && (

        <div className="px-8 pb-4">

          <div className="bg-green-50 border border-green-300 rounded-xl p-4">

            <p className="text-green-800 font-semibold">
              ✓ Case Saved Successfully
            </p>

            <p className="mt-2 text-slate-700">

              Case ID:

              <strong className="ml-2">
                {caseId}
              </strong>

            </p>

          </div>

        </div>

      )}

      {/* ======================================================
          ACTION BUTTONS
          ====================================================== */}

      <div className="border-t bg-slate-50 p-6 flex flex-wrap justify-end gap-4">

        <button
          onClick={handleCopy}
          className="border border-slate-300 rounded-xl px-5 py-3 flex items-center gap-2 hover:bg-slate-100"
        >

          <FaCopy />

          Copy

        </button>

        <button
          onClick={handleSave}
          disabled={saving || saved}
          className="bg-emerald-700 text-white rounded-xl px-5 py-3 flex items-center gap-2 hover:bg-emerald-600 disabled:opacity-50"
        >

          <FaSave />

          {saved
            ? "Saved"
            : saving
            ? "Saving..."
            : "Save Case"}

        </button>

        <button
          onClick={handleDownload}
          className="bg-blue-900 text-white rounded-xl px-5 py-3 flex items-center gap-2 hover:bg-blue-800"
        >

          <FaDownload />

          Download PDF

        </button>

      </div>

    </div>
  );
}