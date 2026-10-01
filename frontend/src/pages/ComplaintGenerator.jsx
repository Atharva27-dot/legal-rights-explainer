import { useState } from "react";
import AppShell from "../components/AppShell";
import ComplaintForm from "../components/ComplaintForm";
import ComplaintPreview from "../components/ComplaintPreview";
import { FileText, Sparkles, ShieldCheck, AlertCircle } from "lucide-react";

export default function ComplaintGenerator() {
  const [caseData, setCaseData] = useState(null);

  return (
    <AppShell>
      <div className="space-y-8">
        {/* Banner */}
        <div className="bg-gradient-to-r from-slate-900 via-indigo-950 to-slate-900 rounded-3xl p-6 sm:p-8 text-white shadow-md border border-indigo-900/50">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
            <div className="flex items-start gap-4">
              <div className="w-12 h-12 rounded-2xl bg-indigo-600 flex items-center justify-center text-white shadow-md flex-shrink-0">
                <FileText className="w-6 h-6" />
              </div>
              <div>
                <span className="text-xs font-bold uppercase tracking-wider text-indigo-300">
                  Automated Formal Drafting
                </span>
                <h1 className="text-2xl sm:text-3xl font-black text-white tracking-tight mt-0.5">
                  AI Complaint Generator
                </h1>
                <p className="text-xs sm:text-sm text-slate-300 mt-1 max-w-2xl leading-relaxed">
                  Fill in your case facts, attach supporting evidence, and generate a legally grounded complaint draft with automatic evidence consistency checking and timeline extraction.
                </p>
              </div>
            </div>

            <div className="flex items-center gap-2 bg-emerald-950/80 border border-emerald-500/30 rounded-full px-3 py-1.5 self-start sm:self-center">
              <ShieldCheck className="w-4 h-4 text-emerald-400" />
              <span className="text-xs font-bold text-emerald-300">PDF & DOCX Export</span>
            </div>
          </div>
        </div>

        {/* Complaint Form Section */}
        <ComplaintForm setCaseData={setCaseData} />

        {/* Evidence Consistency Check Callout if present */}
        {caseData?.evidence_consistency && (
          <div className="bg-white rounded-3xl shadow-sm border border-slate-200 overflow-hidden">
            <div className="px-6 py-5 border-b border-slate-200 bg-slate-50/50 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
              <div>
                <h2 className="text-lg font-bold text-slate-900 flex items-center gap-2">
                  <ShieldCheck className="w-5 h-5 text-indigo-600" />
                  Evidence Consistency Analysis
                </h2>
                <p className="mt-0.5 text-xs text-slate-500">
                  Compares citizen-provided facts against OCR extracted evidence texts
                </p>
              </div>

              <span
                className={`px-3.5 py-1.5 rounded-full text-xs font-extrabold border ${
                  caseData.evidence_consistency.overall_status === "MISMATCH"
                    ? "bg-red-50 text-red-700 border-red-200"
                    : caseData.evidence_consistency.overall_status === "CONSISTENT"
                    ? "bg-emerald-50 text-emerald-700 border-emerald-200"
                    : "bg-amber-50 text-amber-700 border-amber-200"
                }`}
              >
                STATUS: {caseData.evidence_consistency.overall_status}
              </span>
            </div>

            <div className="p-6 space-y-4">
              <div className="rounded-xl bg-slate-50 p-4 border border-slate-200/80 text-xs sm:text-sm text-slate-700">
                <p className="font-semibold text-slate-900">
                  {caseData.evidence_consistency.summary}
                </p>
                {caseData.evidence_consistency.overall_status === "MISMATCH" && (
                  <p className="mt-1 text-xs text-red-600 font-medium flex items-center gap-1">
                    <AlertCircle className="w-3.5 h-3.5" />
                    Please review discrepancies below before submitting formal complaint.
                  </p>
                )}
              </div>

              <div className="grid gap-3">
                {caseData.evidence_consistency.checks?.map((check) => (
                  <div
                    key={check.field}
                    className="rounded-xl border border-slate-200 p-4 bg-white hover:border-slate-300 transition-colors"
                  >
                    <div className="flex items-start justify-between gap-4">
                      <div>
                        <h3 className="font-bold text-slate-900 text-sm">
                          {check.label}
                        </h3>

                        <div className="mt-2 grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs">
                          <p className="bg-slate-50 p-2 rounded-lg border border-slate-100">
                            <span className="font-medium text-slate-500">User Value:</span>{" "}
                            <span className="font-semibold text-slate-800">{check.user_value || "Not provided"}</span>
                          </p>

                          <p className="bg-slate-50 p-2 rounded-lg border border-slate-100">
                            <span className="font-medium text-slate-500">Evidence OCR:</span>{" "}
                            <span className="font-semibold text-slate-800">{check.evidence_value || "Not detected"}</span>
                          </p>
                        </div>
                      </div>

                      <span
                        className={`shrink-0 px-2.5 py-1 rounded-md text-[11px] font-bold ${
                          check.status === "MISMATCH"
                            ? "bg-red-100 text-red-700"
                            : check.status === "MATCH"
                            ? "bg-emerald-100 text-emerald-700"
                            : "bg-amber-100 text-amber-700"
                        }`}
                      >
                        {check.status.replaceAll("_", " ")}
                      </span>
                    </div>

                    <p className="mt-2 text-xs text-slate-500 italic">
                      {check.message}
                    </p>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* Complaint Preview & Actions */}
        <ComplaintPreview caseData={caseData} />
      </div>
    </AppShell>
  );
}