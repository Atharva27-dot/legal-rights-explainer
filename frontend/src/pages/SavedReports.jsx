import { useEffect, useState } from "react";
import AppShell from "../components/AppShell";
import { getCases, downloadComplaintPDF } from "../services/api";
import { BookmarkCheck, FileText, Download, Eye, Scale, ShieldCheck, Sparkles, Inbox } from "lucide-react";
import toast from "react-hot-toast";
import CaseDetailsModal from "../components/CaseDetailsModal";

export default function SavedReports() {
  const [cases, setCases] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedCase, setSelectedCase] = useState(null);
  const [openModal, setOpenModal] = useState(false);

  useEffect(() => {
    fetchReports();
  }, []);

  const fetchReports = async () => {
    try {
      setLoading(true);
      const res = await getCases();
      setCases(res.cases || []);
    } catch (err) {
      console.error(err);
      toast.error("Failed to load saved reports.");
    } finally {
      setLoading(false);
    }
  };

  const handleDownload = async (caseItem) => {
    try {
      toast.loading(`Preparing PDF for ${caseItem.case_id}...`, { id: `report-${caseItem.case_id}` });
      const pdfBlob = await downloadComplaintPDF(caseItem.report || {});
      const url = window.URL.createObjectURL(pdfBlob);
      const link = document.createElement("a");
      link.href = url;
      link.download = `${caseItem.case_id}_Report.pdf`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);
      toast.success("Report PDF downloaded!", { id: `report-${caseItem.case_id}` });
    } catch (err) {
      console.error(err);
      toast.error("Unable to download PDF.", { id: `report-${caseItem.case_id}` });
    }
  };

  return (
    <AppShell>
      <div className="space-y-6">
        {/* Banner */}
        <div className="bg-gradient-to-r from-slate-900 via-indigo-950 to-slate-900 rounded-3xl p-6 sm:p-8 text-white shadow-md border border-indigo-900/50">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
            <div className="flex items-start gap-4">
              <div className="w-12 h-12 rounded-2xl bg-indigo-600 flex items-center justify-center text-white shadow-md flex-shrink-0">
                <BookmarkCheck className="w-6 h-6" />
              </div>
              <div>
                <span className="text-xs font-bold uppercase tracking-wider text-indigo-300">
                  RAG Reports Summary
                </span>
                <h1 className="text-2xl sm:text-3xl font-black text-white tracking-tight mt-0.5">
                  Saved RAG Legal Reports
                </h1>
                <p className="text-xs sm:text-sm text-slate-300 mt-1 max-w-2xl leading-relaxed">
                  View and export all generated legal analysis reports, confidence scores, statutory grounding, and action plans.
                </p>
              </div>
            </div>

            <span className="text-xs font-bold px-3 py-1.5 rounded-full bg-indigo-500/20 text-indigo-300 border border-indigo-500/30 self-start sm:self-center">
              {cases.length} Saved Reports
            </span>
          </div>
        </div>

        {/* Reports List */}
        {loading ? (
          <div className="bg-white rounded-3xl border border-slate-200 p-12 text-center text-slate-500 text-sm font-semibold">
            Loading saved reports...
          </div>
        ) : cases.length === 0 ? (
          <div className="bg-white rounded-3xl border border-slate-200 p-12 text-center space-y-4">
            <div className="w-16 h-16 rounded-2xl bg-slate-100 text-slate-400 flex items-center justify-center mx-auto">
              <Inbox className="w-8 h-8" />
            </div>
            <h3 className="text-xl font-bold text-slate-800">No Saved Reports Found</h3>
            <p className="text-xs sm:text-sm text-slate-500 max-w-sm mx-auto">
              Generate a complaint or rights explanation and save the case to see it in your saved reports repository.
            </p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {cases.map((item) => (
              <div
                key={item.case_id}
                className="bg-white rounded-2xl border border-slate-200 p-5 space-y-4 shadow-xs hover:shadow-md transition-all"
              >
                <div className="flex items-start justify-between gap-3">
                  <div>
                    <span className="text-[10px] font-bold text-indigo-600 bg-indigo-50 border border-indigo-100 px-2 py-0.5 rounded-md uppercase">
                      {item.category || "Legal Report"}
                    </span>
                    <h3 className="font-extrabold text-slate-900 text-base mt-1">
                      {item.case_id}
                    </h3>
                    <p className="text-xs text-slate-500 mt-0.5">
                      Citizen: <span className="font-semibold text-slate-800">{item.citizen_name || "N/A"}</span> ({item.city || "India"})
                    </p>
                  </div>

                  <span className="px-2 py-1 rounded-md bg-emerald-50 text-emerald-700 border border-emerald-200 text-xs font-bold">
                    {item.confidence || "High"}
                  </span>
                </div>

                <div className="pt-3 border-t border-slate-100 flex items-center justify-between">
                  <span className="text-[11px] text-slate-400 font-medium">
                    {item.created_at || "Recent"}
                  </span>

                  <div className="flex items-center gap-2">
                    <button
                      onClick={() => {
                        setSelectedCase(item);
                        setOpenModal(true);
                      }}
                      className="px-3 py-1.5 rounded-lg bg-indigo-600 hover:bg-indigo-700 text-white text-xs font-semibold flex items-center gap-1 transition"
                    >
                      <Eye className="w-3.5 h-3.5" />
                      <span>View</span>
                    </button>

                    <button
                      onClick={() => handleDownload(item)}
                      className="px-3 py-1.5 rounded-lg bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-semibold flex items-center gap-1 transition"
                    >
                      <Download className="w-3.5 h-3.5" />
                      <span>PDF</span>
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}

        <CaseDetailsModal
          open={openModal}
          onClose={() => setOpenModal(false)}
          caseData={selectedCase}
        />
      </div>
    </AppShell>
  );
}