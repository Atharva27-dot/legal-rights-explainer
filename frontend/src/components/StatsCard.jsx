import { useState } from "react";
import {
  FaCheckCircle,
  FaChevronDown,
  FaChevronUp,
  FaClock,
  FaDatabase,
  FaRobot,
} from "react-icons/fa";

export default function StatsCard({
  confidence,
  retrieval_time,
  llm_time,
  total_time,
}) {
  const [expanded, setExpanded] = useState(false);

  if (!confidence) return null;

  return (
    <div className="bg-white rounded-3xl border border-slate-200 shadow-sm overflow-hidden">

      <div className="px-6 py-5">

        <div className="flex items-center justify-between gap-4">

          <div className="flex items-center gap-3">

            <div className="w-10 h-10 rounded-xl bg-slate-100 text-slate-700 flex items-center justify-center">
              <FaClock />
            </div>

            <div>
              <h2 className="font-bold text-slate-900">
                System Performance
              </h2>

              <p className="text-sm text-slate-500">
                Technical details about this response
              </p>
            </div>

          </div>

          <button
            type="button"
            onClick={() => setExpanded((value) => !value)}
            className="flex items-center gap-2 text-sm font-semibold text-indigo-700 hover:text-indigo-900"
          >
            {expanded ? "Hide details" : "Technical details"}

            {expanded ? <FaChevronUp /> : <FaChevronDown />}
          </button>

        </div>

        {/* Simple citizen-facing summary */}
        <div className="mt-5 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 bg-slate-50 border border-slate-200 rounded-2xl p-4">

          <div>
            <p className="text-xs font-semibold uppercase tracking-wide text-slate-500">
              Response completed
            </p>

            <p className="text-2xl font-bold text-slate-900 mt-1">
              {total_time} sec
            </p>
          </div>

          <div className="flex items-center gap-2">

            <FaCheckCircle className="text-emerald-600" />

            <div>
              <p className="text-xs text-slate-500">
                Retrieval confidence
              </p>

              <p className="font-semibold text-slate-800">
                {confidence}
              </p>
            </div>

          </div>

        </div>

      </div>

      {/* Technical details */}
      {expanded && (
        <div className="border-t border-slate-200 bg-slate-50 p-6">

          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">

            <div className="bg-white border border-slate-200 rounded-2xl p-4">
              <FaDatabase className="text-blue-700 text-xl mb-3" />

              <p className="text-xs text-slate-500">
                Retrieval
              </p>

              <p className="text-xl font-bold text-slate-900 mt-1">
                {retrieval_time} sec
              </p>
            </div>

            <div className="bg-white border border-slate-200 rounded-2xl p-4">
              <FaRobot className="text-violet-700 text-xl mb-3" />

              <p className="text-xs text-slate-500">
                AI Generation
              </p>

              <p className="text-xl font-bold text-slate-900 mt-1">
                {llm_time} sec
              </p>
            </div>

            <div className="bg-white border border-slate-200 rounded-2xl p-4">
              <FaClock className="text-orange-600 text-xl mb-3" />

              <p className="text-xs text-slate-500">
                Total
              </p>

              <p className="text-xl font-bold text-slate-900 mt-1">
                {total_time} sec
              </p>
            </div>

          </div>

          <div className="mt-4 text-xs text-slate-500">
            Performance metrics are provided for transparency and debugging.
            They do not represent legal confidence or the probability of a
            legal outcome.
          </div>

        </div>
      )}

    </div>
  );
}
