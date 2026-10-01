import { X, Download, CheckCircle2, User, MapPin, Scale, FileText, Sparkles } from "lucide-react";
import { downloadComplaintPDF } from "../services/api";
import toast from "react-hot-toast";

export default function CaseDetailsModal({ open, onClose, caseData }) {
  if (!open || !caseData) return null;

  const handleDownload = async () => {
    try {
      toast.loading("Downloading PDF...", { id: "modal-pdf" });
      const pdfBlob = await downloadComplaintPDF(caseData.report);
      const url = window.URL.createObjectURL(pdfBlob);
      const link = document.createElement("a");
      link.href = url;
      link.download = `${caseData.case_id}.pdf`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);
      toast.success("PDF downloaded!", { id: "modal-pdf" });
    } catch (err) {
      console.error(err);
      toast.error("Unable to download PDF.", { id: "modal-pdf" });
    }
  };

  const rightsList = caseData.report?.case_analysis?.rights || [];

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 sm:p-6 overflow-y-auto">
      {/* Backdrop */}
      <div className="fixed inset-0 bg-slate-900/60 backdrop-blur-xs transition-opacity" onClick={onClose} />

      {/* Modal Dialog */}
      <div className="relative bg-white rounded-3xl shadow-2xl w-full max-w-4xl max-h-[90vh] flex flex-col overflow-hidden z-10 border border-slate-200">
        {/* Header */}
        <div className="bg-gradient-to-r from-slate-900 via-indigo-950 to-slate-900 text-white p-6 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-indigo-600 flex items-center justify-center text-white shadow-xs">
              <FileText className="w-5 h-5" />
            </div>
            <div>
              <h2 className="text-lg font-bold text-white tracking-tight">
                Case Details Overview
              </h2>
              <p className="text-xs text-indigo-200 font-mono">
                ID: {caseData.case_id}
              </p>
            </div>
          </div>

          <button
            onClick={onClose}
            className="p-2 rounded-xl text-slate-300 hover:text-white hover:bg-slate-800 transition"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Modal Scrollable Body */}
        <div className="p-6 sm:p-8 overflow-y-auto space-y-6 flex-1">
          {/* Metadata Cards */}
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
            <InfoCard title="Citizen" value={caseData.citizen_name} icon={User} />
            <InfoCard title="Jurisdiction / City" value={caseData.city} icon={MapPin} />
            <InfoCard title="Category" value={caseData.category} icon={Scale} />
            <InfoCard title="Confidence" value={caseData.confidence} icon={Sparkles} />
          </div>

          {/* Applicable Rights */}
          {rightsList.length > 0 && (
            <div className="space-y-3 bg-slate-50 p-5 rounded-2xl border border-slate-200">
              <h3 className="font-bold text-sm text-slate-900 flex items-center gap-2">
                <CheckCircle2 className="w-4 h-4 text-emerald-600" />
                Applicable Statutory Rights
              </h3>
              <ul className="grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs text-slate-700">
                {rightsList.map((item, index) => (
                  <li key={index} className="flex items-center gap-2 bg-white p-2.5 rounded-xl border border-slate-200/80 font-medium">
                    <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 flex-shrink-0" />
                    <span>{item}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Complaint Text */}
          <div className="space-y-2">
            <h3 className="font-bold text-sm text-slate-900">Complaint Text</h3>
            <div className="bg-slate-50 rounded-2xl p-5 text-xs text-slate-800 font-mono leading-relaxed whitespace-pre-wrap border border-slate-200">
              {caseData.report?.complaint}
            </div>
          </div>
        </div>

        {/* Modal Footer */}
        <div className="p-4 sm:p-5 bg-slate-50 border-t border-slate-200 flex items-center justify-end gap-3">
          <button
            onClick={handleDownload}
            className="px-4 py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-700 text-white text-xs font-bold flex items-center gap-2 transition"
          >
            <Download className="w-4 h-4" />
            <span>Download PDF</span>
          </button>
          <button
            onClick={onClose}
            className="px-4 py-2.5 rounded-xl border border-slate-300 text-slate-700 hover:bg-white text-xs font-semibold transition"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
}

function InfoCard({ title, value, icon: Icon }) {
  return (
    <div className="bg-slate-50 border border-slate-200 rounded-2xl p-3.5 space-y-1">
      <div className="flex items-center gap-1.5 text-slate-400">
        {Icon && <Icon className="w-3.5 h-3.5 text-indigo-600" />}
        <span className="text-[11px] font-semibold uppercase">{title}</span>
      </div>
      <p className="font-bold text-slate-900 text-sm truncate">{value || "N/A"}</p>
    </div>
  );
}