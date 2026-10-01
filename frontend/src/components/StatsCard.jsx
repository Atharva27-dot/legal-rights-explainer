import { useState } from "react";
import { Clock, Database, Cpu, CheckCircle2, ChevronDown, ChevronUp, Activity } from "lucide-react";

export default function StatsCard({
  confidence,
  retrieval_time,
  llm_time,
  total_time,
}) {
  const [expanded, setExpanded] = useState(false);

  if (!confidence) return null;

  return (
    <div className="bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden">
      <div className="p-4 sm:p-5">
        <div className="flex items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 rounded-lg bg-slate-100 text-slate-700 flex items-center justify-center">
              <Activity className="w-4 h-4 text-indigo-600" />
            </div>
            <div>
              <h3 className="font-bold text-slate-900 text-sm">
                RAG Pipeline Performance
              </h3>
              <p className="text-xs text-slate-500">
                Response generation timing & confidence
              </p>
            </div>
          </div>

          <button
            type="button"
            onClick={() => setExpanded((prev) => !prev)}
            className="flex items-center gap-1.5 text-xs font-semibold text-indigo-600 hover:text-indigo-800 transition"
          >
            <span>{expanded ? "Hide timing breakdown" : "View timing breakdown"}</span>
            {expanded ? <ChevronUp className="w-3.5 h-3.5" /> : <ChevronDown className="w-3.5 h-3.5" />}
          </button>
        </div>

        {/* Citizen summary pill */}
        <div className="mt-4 grid grid-cols-2 gap-3 bg-slate-50 border border-slate-200/80 rounded-xl p-3">
          <div>
            <p className="text-[11px] font-semibold uppercase text-slate-400">Total Latency</p>
            <p className="text-lg font-black text-slate-900 mt-0.5">{total_time} sec</p>
          </div>
          <div>
            <p className="text-[11px] font-semibold uppercase text-slate-400">Retrieval Confidence</p>
            <div className="flex items-center gap-1.5 mt-0.5">
              <CheckCircle2 className="w-4 h-4 text-emerald-600" />
              <span className="font-bold text-slate-800 text-sm">{confidence}</span>
            </div>
          </div>
        </div>

        {/* Expanded stats */}
        {expanded && (
          <div className="mt-3 pt-3 border-t border-slate-200/80 grid grid-cols-3 gap-3 text-center">
            <div className="bg-slate-50 p-2.5 rounded-xl border border-slate-100">
              <div className="flex items-center justify-center gap-1 text-xs text-slate-500 font-medium">
                <Database className="w-3.5 h-3.5 text-indigo-600" />
                <span>Vector Search</span>
              </div>
              <p className="font-bold text-slate-800 text-sm mt-1">{retrieval_time} s</p>
            </div>

            <div className="bg-slate-50 p-2.5 rounded-xl border border-slate-100">
              <div className="flex items-center justify-center gap-1 text-xs text-slate-500 font-medium">
                <Cpu className="w-3.5 h-3.5 text-purple-600" />
                <span>LLM Generation</span>
              </div>
              <p className="font-bold text-slate-800 text-sm mt-1">{llm_time} s</p>
            </div>

            <div className="bg-slate-50 p-2.5 rounded-xl border border-slate-100">
              <div className="flex items-center justify-center gap-1 text-xs text-slate-500 font-medium">
                <Clock className="w-3.5 h-3.5 text-emerald-600" />
                <span>Total Execution</span>
              </div>
              <p className="font-bold text-slate-800 text-sm mt-1">{total_time} s</p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
