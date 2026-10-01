import { useState } from "react";
import {
  Eye,
  Trash2,
  Download,
  Calendar,
  User,
  Scale,
  MapPin,
  ShieldCheck
} from "lucide-react";
import toast from "react-hot-toast";
import { deleteCase, getCase, downloadComplaintPDF } from "../services/api";
import CaseDetailsModal from "./CaseDetailsModal";

export default function CaseCard({ caseItem, refreshCases }) {
  const [loading, setLoading] = useState(false);
  const [selectedCase, setSelectedCase] = useState(null);
  const [openModal, setOpenModal] = useState(false);

  const getBadgeColor = (confidence) => {
    switch (confidence) {
      case "High":
        return "bg-emerald-50 text-emerald-700 border-emerald-200";
      case "Medium":
        return "bg-amber-50 text-amber-700 border-amber-200";
      default:
        return "bg-red-50 text-red-700 border-red-200";
    }
  };

  const handleView = async () => {
    try {
      setLoading(true);
      const data = await getCase(caseItem.case_id);
      setSelectedCase(data);
      setOpenModal(true);
    } catch (err) {
      console.error(err);
      toast.error("Unable to load case details.");
    } finally {
      setLoading(false);
    }
  };

  const handleDownload = async () => {
    try {
      toast.loading(`Preparing PDF for ${caseItem.case_id}...`, { id: `pdf-${caseItem.case_id}` });
      const data = await getCase(caseItem.case_id);
      const pdfBlob = await downloadComplaintPDF(data.report);
      const url = window.URL.createObjectURL(pdfBlob);
      const link = document.createElement("a");
      link.href = url;
      link.download = `${caseItem.case_id}.pdf`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);
      toast.success("PDF downloaded successfully!", { id: `pdf-${caseItem.case_id}` });
    } catch (err) {
      console.error(err);
      toast.error("Unable to download PDF.", { id: `pdf-${caseItem.case_id}` });
    }
  };

  const handleDelete = async () => {
    const confirmDelete = window.confirm(`Are you sure you want to delete case ${caseItem.case_id}?`);
    if (!confirmDelete) return;

    try {
      await deleteCase(caseItem.case_id);
      toast.success(`Case ${caseItem.case_id} deleted.`);
      refreshCases();
    } catch (err) {
      console.error(err);
      toast.error("Unable to delete case.");
    }
  };

  return (
    <>
      <div className="bg-white rounded-2xl border border-slate-200 p-5 shadow-xs hover:shadow-md transition-all duration-200 flex flex-col justify-between space-y-4">
        <div>
          {/* Header ID & Confidence */}
          <div className="flex items-start justify-between gap-3">
            <div>
              <span className="text-[10px] font-bold text-indigo-600 bg-indigo-50 border border-indigo-100 px-2 py-0.5 rounded-md uppercase tracking-wider">
                Case Entry
              </span>
              <h3 className="text-lg font-black text-slate-900 tracking-tight mt-1">
                {caseItem.case_id}
              </h3>
            </div>

            <span className={`px-2.5 py-1 rounded-lg border text-xs font-extrabold ${getBadgeColor(caseItem.confidence)}`}>
              {caseItem.confidence || "Standard"} Confidence
            </span>
          </div>

          {/* Details list */}
          <div className="mt-4 space-y-2 text-xs text-slate-600">
            <div className="flex items-center gap-2">
              <User className="w-3.5 h-3.5 text-slate-400 flex-shrink-0" />
              <span className="font-semibold text-slate-800">{caseItem.citizen_name || "Anonymous Citizen"}</span>
            </div>

            <div className="flex items-center gap-2">
              <Scale className="w-3.5 h-3.5 text-slate-400 flex-shrink-0" />
              <span className="text-slate-700">{caseItem.category || "General Legal Issue"}</span>
            </div>

            <div className="flex items-center gap-2">
              <Calendar className="w-3.5 h-3.5 text-slate-400 flex-shrink-0" />
              <span className="text-slate-500">{caseItem.created_at || "Recent"}</span>
            </div>
          </div>
        </div>

        {/* Action Buttons */}
        <div className="pt-3 border-t border-slate-100 flex items-center justify-between gap-2">
          <div className="flex items-center gap-2">
            <button
              onClick={handleView}
              disabled={loading}
              className="px-3 py-1.5 rounded-lg bg-indigo-600 hover:bg-indigo-700 text-white text-xs font-semibold flex items-center gap-1.5 transition"
            >
              <Eye className="w-3.5 h-3.5" />
              <span>{loading ? "Loading..." : "View Details"}</span>
            </button>

            <button
              onClick={handleDownload}
              className="px-3 py-1.5 rounded-lg bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-semibold flex items-center gap-1.5 transition"
            >
              <Download className="w-3.5 h-3.5" />
              <span>PDF</span>
            </button>
          </div>

          <button
            onClick={handleDelete}
            className="p-1.5 rounded-lg text-slate-400 hover:text-red-600 hover:bg-red-50 transition"
            title="Delete Case"
          >
            <Trash2 className="w-4 h-4" />
          </button>
        </div>
      </div>

      <CaseDetailsModal
        open={openModal}
        onClose={() => setOpenModal(false)}
        caseData={selectedCase}
      />
    </>
  );
}