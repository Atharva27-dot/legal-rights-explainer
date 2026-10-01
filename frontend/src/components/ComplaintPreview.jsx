import { useEffect, useState } from "react";
import {
  FileText,
  Copy,
  Download,
  Save,
  CheckCircle2,
  Edit,
  Undo,
  Check,
  AlertTriangle,
  Clock,
  ShieldCheck,
  Award,
  Layers,
  Sparkles,
  ArrowRight,
  AlertCircle
} from "lucide-react";
import toast from "react-hot-toast";
import { downloadComplaintPDF, saveCase } from "../services/api";

function TimelineTypeBadge({ type }) {
  const config = {
    USER_REPORTED: {
      label: "USER REPORTED",
      className: "bg-blue-50 text-blue-700 border-blue-200",
    },
    EVIDENCE_DERIVED: {
      label: "EVIDENCE DERIVED",
      className: "bg-emerald-50 text-emerald-700 border-emerald-200",
    },
    DERIVED: {
      label: "DERIVED",
      className: "bg-amber-50 text-amber-700 border-amber-200",
    },
  };

  const item = config[type] || {
    label: type || "UNKNOWN",
    className: "bg-slate-100 text-slate-700 border-slate-200",
  };

  return (
    <span className={`inline-flex items-center px-2.5 py-1 rounded-md border text-[10px] font-bold ${item.className}`}>
      {item.label}
    </span>
  );
}

export default function ComplaintPreview({ caseData }) {
  const [saving, setSaving] = useState(false);
  const [saved, setSaved] = useState(false);
  const [caseId, setCaseId] = useState("");
  const [editing, setEditing] = useState(false);
  const [editedComplaint, setEditedComplaint] = useState("");
  const [copied, setCopied] = useState(false);

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
      <div className="bg-white rounded-3xl shadow-sm border border-slate-200 p-12 text-center space-y-4">
        <div className="w-16 h-16 rounded-2xl bg-indigo-50 text-indigo-600 flex items-center justify-center mx-auto shadow-xs">
          <FileText className="w-8 h-8" />
        </div>
        <h3 className="text-xl font-bold text-slate-800">
          Complaint Draft Preview
        </h3>
        <p className="text-xs sm:text-sm text-slate-500 max-w-md mx-auto">
          Fill out the case form above and click "Generate Complaint Draft" to preview the structured complaint, legal readiness score, timeline, and action plan here.
        </p>
      </div>
    );
  }

  const { formData, report } = caseData;
  const readiness = report?.readiness || {};
  const caseAnalysis = report?.case_analysis || {};
  const grounding = report?.grounding || {};
  const timeline = report?.timeline || {};
  const timelineEvents = Array.isArray(timeline.events) ? timeline.events : [];
  const timelineConflicts = Array.isArray(timeline.conflicts) ? timeline.conflicts : [];
  const complaintText = editedComplaint || report?.complaint || "";

  const getCurrentReport = () => ({
    ...report,
    complaint: complaintText,
  });

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
      toast.error("Complaint draft cannot be empty.");
      return;
    }
    setEditing(false);
    setSaved(false);
    toast.success("Complaint changes saved in current draft.");
  };

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(complaintText);
      setCopied(true);
      toast.success("Complaint text copied!");
      setTimeout(() => setCopied(false), 2000);
    } catch (error) {
      console.error(error);
      toast.error("Unable to copy complaint text.");
    }
  };

  const handleDownload = async () => {
    if (!complaintText.trim()) {
      toast.error("No complaint text available to download.");
      return;
    }
    try {
      toast.loading("Generating PDF...", { id: "download-pdf" });
      const pdfBlob = await downloadComplaintPDF(getCurrentReport());
      const url = window.URL.createObjectURL(pdfBlob);
      const link = document.createElement("a");
      link.href = url;
      link.download = `Legal_Complaint_${formData?.name ? formData.name.replace(/\s+/g, "_") : "Draft"}.pdf`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);
      toast.success("Complaint PDF downloaded!", { id: "download-pdf" });
    } catch (error) {
      console.error(error);
      toast.error("Unable to download PDF.", { id: "download-pdf" });
    }
  };

  const handleSave = async () => {
    if (saved) return;
    if (!complaintText.trim()) {
      toast.error("Complaint text cannot be empty.");
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
      toast.success("Case saved successfully in SQLite database!");
    } catch (error) {
      console.error(error);
      toast.error("Unable to save case.");
    } finally {
      setSaving(false);
    }
  };

  const groundingVerified = grounding.status === "Verified" || caseAnalysis.grounding_status === "Verified";
  const groundingNeedsReview = grounding.status === "Needs Review" || caseAnalysis.grounding_status === "Needs Review";

  const detectedEvidence = readiness.evidence?.detected || [];
  const missingEvidence = readiness.evidence?.missing || [];
  const evidenceTotal = detectedEvidence.length + missingEvidence.length;
  const evidenceCompleteness = Math.round((detectedEvidence.length / Math.max(1, evidenceTotal)) * 100);

  return (
    <div className="bg-white rounded-3xl shadow-sm border border-slate-200 overflow-hidden space-y-0">
      {/* Banner */}
      <div className="bg-gradient-to-r from-slate-900 via-indigo-950 to-slate-900 text-white px-6 sm:px-8 py-6 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-indigo-600 flex items-center justify-center text-white shadow-xs">
            <FileText className="w-5 h-5" />
          </div>
          <div>
            <h2 className="text-lg sm:text-xl font-bold text-white tracking-tight">
              AI-Assisted Legal Complaint Draft
            </h2>
            <p className="text-xs text-indigo-200">
              Review, edit, and export your legal complaint
            </p>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <button
            onClick={handleCopy}
            className="px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-white text-xs font-semibold flex items-center gap-1.5 border border-slate-700 transition"
          >
            {copied ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
            <span>{copied ? "Copied!" : "Copy"}</span>
          </button>
          <button
            onClick={handleSave}
            disabled={saving || saved}
            className="px-3.5 py-1.5 rounded-lg bg-emerald-600 hover:bg-emerald-500 disabled:bg-emerald-900/50 text-white text-xs font-semibold flex items-center gap-1.5 transition"
          >
            <Save className="w-3.5 h-3.5" />
            <span>{saved ? "Saved" : saving ? "Saving..." : "Save Case"}</span>
          </button>
          <button
            onClick={handleDownload}
            className="px-3.5 py-1.5 rounded-lg bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-semibold flex items-center gap-1.5 transition"
          >
            <Download className="w-3.5 h-3.5" />
            <span>PDF</span>
          </button>
        </div>
      </div>

      {/* Review Disclaimer Notice */}
      <div className="p-4 bg-amber-50 border-b border-amber-200/80 text-xs text-amber-900 flex items-center gap-2">
        <AlertTriangle className="w-4 h-4 text-amber-600 flex-shrink-0" />
        <span>Review before use: Educational AI draft generated from statutory provisions. Verify facts before formal filing.</span>
      </div>

      {/* Readiness Summary Metrics */}
      <div className="p-6 border-b border-slate-200/80 grid grid-cols-1 sm:grid-cols-3 gap-4 bg-slate-50/50">
        <div className="bg-white border border-slate-200 rounded-2xl p-4 shadow-xs">
          <p className="text-xs font-bold text-slate-400 uppercase">Legal Readiness</p>
          <p className="text-3xl font-black text-indigo-700 mt-1">{readiness.score ?? 0}%</p>
          <p className="text-xs font-semibold text-slate-700 mt-1">{readiness.status || "Not evaluated"}</p>
        </div>

        <div className="bg-white border border-slate-200 rounded-2xl p-4 shadow-xs">
          <p className="text-xs font-bold text-slate-400 uppercase">Retrieval Confidence</p>
          <p className="text-2xl font-bold text-slate-900 mt-1.5">{report.confidence || "Medium"}</p>
          <p className="text-[11px] text-slate-500 mt-0.5">Highest statutory match</p>
        </div>

        <div className={`border rounded-2xl p-4 shadow-xs ${groundingVerified ? "bg-emerald-50/50 border-emerald-200" : "bg-amber-50/50 border-amber-200"}`}>
          <p className="text-xs font-bold text-slate-400 uppercase">Grounding Status</p>
          <p className="text-xl font-bold mt-1.5 flex items-center gap-1.5">
            {groundingVerified ? (
              <span className="text-emerald-700 flex items-center gap-1">
                <CheckCircle2 className="w-4 h-4" /> Verified
              </span>
            ) : (
              <span className="text-amber-700 flex items-center gap-1">
                <AlertTriangle className="w-4 h-4" /> Needs Review
              </span>
            )}
          </p>
          <p className="text-[11px] text-slate-500 mt-0.5">Statutory authorities checked</p>
        </div>
      </div>

      {/* Case Assessment & Evidence Completeness */}
      <div className="p-6 border-b border-slate-200/80 space-y-5">
        <div>
          <h3 className="font-bold text-base text-slate-900">Case Assessment Summary</h3>
          <p className="text-xs text-slate-500">Classification and recommended legal remedies</p>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 text-xs">
          <div className="bg-slate-50 p-3.5 rounded-xl border border-slate-200">
            <span className="font-semibold text-slate-500">Category:</span>
            <p className="font-bold text-slate-900 text-sm mt-0.5">{caseAnalysis.category || "General Dispute"}</p>
          </div>

          <div className="bg-slate-50 p-3.5 rounded-xl border border-slate-200">
            <span className="font-semibold text-slate-500">Applicable Statutory Act:</span>
            <p className="font-bold text-slate-900 text-sm mt-0.5">{caseAnalysis.applicable_act || "Consumer Protection Act 2019"}</p>
          </div>

          <div className="bg-slate-50 p-3.5 rounded-xl border border-slate-200">
            <span className="font-semibold text-slate-500">Recommended Remedy:</span>
            <p className="font-bold text-indigo-700 text-sm mt-0.5">{caseAnalysis.recommended_remedy || "Refund / Replacement"}</p>
          </div>
        </div>

        {/* Evidence Completeness */}
        {readiness.evidence && (
          <div className="bg-slate-50 border border-slate-200 rounded-2xl p-4 space-y-3">
            <div className="flex items-center justify-between text-xs">
              <span className="font-bold text-slate-800">Evidence Completeness Score</span>
              <span className="font-black text-indigo-700 text-sm">{evidenceCompleteness}%</span>
            </div>

            <div className="h-2.5 bg-slate-200 rounded-full overflow-hidden">
              <div className="h-full bg-indigo-600 rounded-full transition-all duration-300" style={{ width: `${evidenceCompleteness}%` }} />
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-xs pt-2">
              <div>
                <span className="font-bold text-emerald-700 flex items-center gap-1 mb-1.5">
                  <CheckCircle2 className="w-3.5 h-3.5" /> Detected Evidence Groups
                </span>
                {detectedEvidence.length > 0 ? (
                  <ul className="space-y-1 text-slate-700">
                    {detectedEvidence.map((item, idx) => (
                      <li key={idx} className="bg-white p-2 rounded-lg border border-slate-200 font-medium">✓ {item}</li>
                    ))}
                  </ul>
                ) : (
                  <p className="text-slate-400 italic">No evidence detected.</p>
                )}
              </div>

              <div>
                <span className="font-bold text-amber-700 flex items-center gap-1 mb-1.5">
                  <AlertTriangle className="w-3.5 h-3.5" /> Recommended Additional Evidence
                </span>
                {missingEvidence.length > 0 ? (
                  <ul className="space-y-1 text-slate-700">
                    {missingEvidence.map((item, idx) => (
                      <li key={idx} className="bg-white p-2 rounded-lg border border-slate-200 font-medium">⚠ {item}</li>
                    ))}
                  </ul>
                ) : (
                  <p className="text-slate-400 italic">No missing evidence groups.</p>
                )}
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Timeline Section */}
      {timelineEvents.length > 0 && (
        <div className="p-6 border-b border-slate-200/80 space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <h3 className="font-bold text-base text-slate-900 flex items-center gap-2">
                <Clock className="w-4 h-4 text-indigo-600" />
                Case Evidence Timeline
              </h3>
              <p className="text-xs text-slate-500">Chronological view of reported & derived events</p>
            </div>
            <span className="text-xs font-semibold px-2.5 py-1 rounded-lg bg-indigo-50 text-indigo-700 border border-indigo-200">
              {timelineEvents.length} Events Logged
            </span>
          </div>

          <div className="relative pl-4 border-l-2 border-indigo-200 space-y-4 my-4">
            {timelineEvents.map((event, idx) => (
              <div key={idx} className="relative pl-4">
                <div className="absolute -left-[23px] top-1 w-3.5 h-3.5 rounded-full bg-indigo-600 ring-4 ring-indigo-100" />
                <div className="bg-slate-50 border border-slate-200 rounded-xl p-3.5 text-xs space-y-1">
                  <div className="flex items-center justify-between gap-2">
                    <span className="font-bold text-indigo-700">{event.date || "Undated"}</span>
                    <TimelineTypeBadge type={event.type} />
                  </div>
                  <h4 className="font-bold text-slate-900 text-sm">{event.title}</h4>
                  {event.details && <p className="text-slate-600 leading-relaxed">{event.details}</p>}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Legal Action Plan */}
      {report?.action_plan?.steps?.length > 0 && (
        <div className="p-6 border-b border-slate-200/80 space-y-4">
          <div>
            <h3 className="font-bold text-base text-slate-900">Recommended Next Action Steps</h3>
            <p className="text-xs text-slate-500">Sequential steps for formal resolution</p>
          </div>

          <div className="space-y-3">
            {report.action_plan.steps.map((step) => (
              <div key={step.step} className="bg-slate-50 border border-slate-200 rounded-xl p-4 space-y-2 text-xs">
                <div className="flex items-center justify-between">
                  <span className="font-bold text-slate-900 text-sm flex items-center gap-2">
                    <span className="w-5 h-5 rounded-full bg-indigo-600 text-white flex items-center justify-center text-[10px]">
                      {step.step}
                    </span>
                    {step.title}
                  </span>
                  <span className="font-bold px-2.5 py-0.5 rounded-md bg-indigo-100 text-indigo-800 text-[10px]">
                    {step.status}
                  </span>
                </div>
                <p className="text-slate-600">{step.description}</p>
                {step.reason && (
                  <p className="text-[11px] text-slate-400 italic bg-white p-2 rounded-lg border border-slate-100">
                    Why: {step.reason}
                  </p>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Editable Complaint Draft Text Area */}
      <div className="p-6 space-y-4">
        <div className="flex items-center justify-between">
          <div>
            <h3 className="font-bold text-base text-slate-900">Generated Complaint Draft</h3>
            <p className="text-xs text-slate-500">
              {editing ? "Editing enabled below. Click 'Save Edits' when done." : "Click 'Edit Draft' to customize text."}
            </p>
          </div>

          {!editing ? (
            <button
              onClick={handleEdit}
              className="px-3.5 py-1.5 rounded-xl bg-indigo-600 hover:bg-indigo-700 text-white text-xs font-semibold flex items-center gap-1.5 transition"
            >
              <Edit className="w-3.5 h-3.5" />
              <span>Edit Draft</span>
            </button>
          ) : (
            <div className="flex gap-2">
              <button
                onClick={handleCancelEdit}
                className="px-3.5 py-1.5 rounded-xl border border-slate-300 text-slate-700 hover:bg-slate-100 text-xs font-semibold flex items-center gap-1.5 transition"
              >
                <Undo className="w-3.5 h-3.5" />
                <span>Cancel</span>
              </button>
              <button
                onClick={handleSaveEdit}
                className="px-3.5 py-1.5 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-semibold flex items-center gap-1.5 transition"
              >
                <Check className="w-3.5 h-3.5" />
                <span>Save Edits</span>
              </button>
            </div>
          )}
        </div>

        {editing ? (
          <textarea
            value={editedComplaint}
            onChange={(e) => setEditedComplaint(e.target.value)}
            rows={22}
            className="w-full bg-slate-50 border-2 border-indigo-300 rounded-2xl p-5 text-sm text-slate-800 leading-relaxed font-mono resize-y outline-none focus:bg-white"
          />
        ) : (
          <div className="bg-slate-50 border border-slate-200 rounded-2xl p-6 text-sm text-slate-800 leading-relaxed font-mono whitespace-pre-wrap">
            {complaintText}
          </div>
        )}

        {/* Saved Case confirmation alert */}
        {saved && (
          <div className="p-4 bg-emerald-50 border border-emerald-200 rounded-xl text-xs font-semibold text-emerald-800 flex items-center justify-between">
            <span>✓ Saved to My Legal Cases (Case ID: {caseId})</span>
          </div>
        )}
      </div>

      {/* Footer Bottom Action Buttons Bar */}
      <div className="p-6 bg-slate-50 border-t border-slate-200 flex flex-wrap items-center justify-end gap-3">
        <button
          onClick={handleCopy}
          className="px-4 py-2.5 rounded-xl border border-slate-300 text-slate-700 hover:bg-white text-xs font-semibold flex items-center gap-2 transition"
        >
          {copied ? <Check className="w-4 h-4 text-emerald-600" /> : <Copy className="w-4 h-4" />}
          <span>{copied ? "Copied" : "Copy Draft"}</span>
        </button>

        <button
          onClick={handleSave}
          disabled={saving || saved}
          className="px-5 py-2.5 rounded-xl bg-emerald-600 hover:bg-emerald-700 disabled:bg-emerald-900/50 text-white text-xs font-bold flex items-center gap-2 transition shadow-xs"
        >
          <Save className="w-4 h-4" />
          <span>{saved ? "Saved in Cases" : saving ? "Saving..." : "Save Case"}</span>
        </button>

        <button
          onClick={handleDownload}
          className="px-5 py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-700 text-white text-xs font-bold flex items-center gap-2 transition shadow-xs"
        >
          <Download className="w-4 h-4" />
          <span>Download PDF Report</span>
        </button>
      </div>
    </div>
  );
}