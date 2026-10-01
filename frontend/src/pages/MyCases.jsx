import { useEffect, useMemo, useState } from "react";
import AppShell from "../components/AppShell";
import CaseCard from "../components/CaseCard";
import { getCases } from "../services/api";
import { FolderKanban, Search, Sparkles, Inbox, RefreshCw } from "lucide-react";
import toast from "react-hot-toast";

export default function MyCases() {
  const [cases, setCases] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState("");

  useEffect(() => {
    loadCases();
  }, []);

  const loadCases = async () => {
    try {
      setLoading(true);
      const response = await getCases();
      setCases(response.cases || []);
    } catch (error) {
      console.error(error);
      toast.error("Failed to fetch saved cases.");
    } finally {
      setLoading(false);
    }
  };

  const filteredCases = useMemo(() => {
    const keyword = search.toLowerCase().trim();
    if (!keyword) return cases;

    return cases.filter((item) => {
      return (
        item.case_id?.toLowerCase().includes(keyword) ||
        item.citizen_name?.toLowerCase().includes(keyword) ||
        item.category?.toLowerCase().includes(keyword)
      );
    });
  }, [cases, search]);

  return (
    <AppShell>
      <div className="space-y-6">
        {/* Banner */}
        <div className="bg-gradient-to-r from-slate-900 via-indigo-950 to-slate-900 rounded-3xl p-6 sm:p-8 text-white shadow-md border border-indigo-900/50">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
            <div className="flex items-start gap-4">
              <div className="w-12 h-12 rounded-2xl bg-indigo-600 flex items-center justify-center text-white shadow-md flex-shrink-0">
                <FolderKanban className="w-6 h-6" />
              </div>
              <div>
                <span className="text-xs font-bold uppercase tracking-wider text-indigo-300">
                  SQLite Case Storage
                </span>
                <h1 className="text-2xl sm:text-3xl font-black text-white tracking-tight mt-0.5">
                  My Legal Cases Repository
                </h1>
                <p className="text-xs sm:text-sm text-slate-300 mt-1 max-w-2xl leading-relaxed">
                  Manage, review, export, and search all your saved complaints and case reports.
                </p>
              </div>
            </div>

            <div className="flex items-center gap-2">
              <button
                onClick={loadCases}
                className="px-3.5 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-white text-xs font-semibold flex items-center gap-1.5 border border-slate-700 transition"
              >
                <RefreshCw className={`w-3.5 h-3.5 ${loading ? "animate-spin" : ""}`} />
                <span>Refresh</span>
              </button>
              <span className="text-xs font-bold px-3 py-1.5 rounded-full bg-indigo-500/20 text-indigo-300 border border-indigo-500/30">
                {cases.length} Total Saved
              </span>
            </div>
          </div>
        </div>

        {/* Search Bar */}
        <div className="relative bg-white rounded-2xl border border-slate-200 shadow-xs">
          <Search className="w-4 h-4 text-slate-400 absolute left-4 top-1/2 -translate-y-1/2" />
          <input
            type="text"
            placeholder="Search cases by Case ID, Citizen Name, or Legal Category..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="w-full bg-transparent pl-11 pr-4 py-3.5 text-sm text-slate-800 placeholder:text-slate-400 outline-none"
          />
        </div>

        {/* Content List */}
        {loading ? (
          <div className="bg-white rounded-3xl border border-slate-200 p-12 text-center space-y-3">
            <RefreshCw className="w-8 h-8 text-indigo-600 animate-spin mx-auto" />
            <p className="text-sm font-semibold text-slate-700">Loading saved legal cases...</p>
          </div>
        ) : filteredCases.length === 0 ? (
          <div className="bg-white rounded-3xl border border-slate-200 p-12 text-center space-y-4">
            <div className="w-16 h-16 rounded-2xl bg-slate-100 text-slate-400 flex items-center justify-center mx-auto">
              <Inbox className="w-8 h-8" />
            </div>
            <h3 className="text-xl font-bold text-slate-800">
              {search ? "No Matching Cases Found" : "No Saved Cases Yet"}
            </h3>
            <p className="text-xs sm:text-sm text-slate-500 max-w-sm mx-auto">
              {search
                ? `No cases match "${search}". Try searching with a different keyword.`
                : "Generate a formal complaint in the Complaint Generator or Rights Guide and click 'Save Case' to view it here."}
            </p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {filteredCases.map((caseItem) => (
              <CaseCard
                key={caseItem.case_id}
                caseItem={caseItem}
                refreshCases={loadCases}
              />
            ))}
          </div>
        )}
      </div>
    </AppShell>
  );
}