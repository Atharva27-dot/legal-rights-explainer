import { useState } from "react";
import {
  BookOpen,
  ChevronDown,
  ChevronUp,
  Info,
  ShieldCheck,
  Sparkles,
  CheckCircle2,
  FileText
} from "lucide-react";

function scoreNumber(value) {
  const number = Number(value);
  return Number.isFinite(number) ? number : null;
}

function scorePercent(value) {
  const number = scoreNumber(value);
  if (number === null) return null;
  return Math.max(0, Math.min(100, Math.round(number * 100)));
}

function relevanceLabel(value) {
  const number = scoreNumber(value);
  if (number === null) return "Retrieved";
  if (number >= 0.75) return "High Relevance";
  if (number >= 0.5) return "Moderate Relevance";
  if (number > 0) return "Relevant";
  return "Retrieved";
}

function ScoreBox({ label, value }) {
  const number = scoreNumber(value);
  return (
    <div className="bg-white border border-slate-200 rounded-xl p-2.5 text-center shadow-2xs">
      <p className="text-[10px] font-bold uppercase text-slate-400">{label}</p>
      <p className="font-mono font-bold text-slate-800 text-xs mt-0.5">
        {number === null ? "—" : number.toFixed(3)}
      </p>
    </div>
  );
}

export default function SourceCard({ sources }) {
  const [expanded, setExpanded] = useState({});

  if (!sources || sources.length === 0) return null;

  const toggle = (index) => {
    setExpanded((prev) => ({
      ...prev,
      [index]: !prev[index],
    }));
  };

  return (
    <div className="bg-white rounded-3xl border border-slate-200 shadow-sm overflow-hidden space-y-0">
      {/* Banner message communicating RAG Grounding */}
      <div className="bg-slate-900 text-white p-5 border-b border-slate-800 flex flex-col sm:flex-row sm:items-center justify-between gap-3">
        <div className="flex items-center gap-3">
          <div className="w-9 h-9 rounded-xl bg-indigo-600 text-white flex items-center justify-center shadow-xs flex-shrink-0">
            <BookOpen className="w-4.5 h-4.5" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="text-[10px] font-extrabold tracking-widest uppercase text-indigo-300">
                SOURCES USED ({sources.length})
              </span>
            </div>
            <h3 className="font-bold text-sm sm:text-base text-white tracking-tight">
              Retrieved Official Statutory Sources
            </h3>
          </div>
        </div>

        <div className="flex items-center gap-2 text-xs font-semibold text-emerald-300 bg-emerald-950/80 border border-emerald-500/30 px-3 py-1.5 rounded-full self-start sm:self-center">
          <ShieldCheck className="w-4 h-4 text-emerald-400" />
          <span>This answer is grounded in retrieved legal sources.</span>
        </div>
      </div>

      {/* Sources list */}
      <div className="p-5 sm:p-6 space-y-4">
        {sources.map((source, index) => {
          const finalScore = scoreNumber(source.final_score);
          const finalPercent = scorePercent(source.final_score);
          const finalLabel = relevanceLabel(source.final_score);
          const isExpanded = Boolean(expanded[index]);

          return (
            <div
              key={`${source.act}-${source.section}-${index}`}
              className="border border-slate-200 rounded-2xl overflow-hidden bg-white hover:border-slate-300 transition-all duration-200"
            >
              {/* Main Source Details */}
              <div className="p-4 sm:p-5">
                <div className="flex items-start justify-between gap-4">
                  <div className="min-w-0 flex-1">
                    <div className="flex items-center gap-2">
                      <span className="text-[10px] font-extrabold uppercase tracking-wider text-indigo-700 bg-indigo-50 border border-indigo-200/80 px-2.5 py-0.5 rounded-md">
                        SOURCE CARD #{index + 1}
                      </span>
                      {source.section && (
                        <span className="text-xs font-extrabold font-mono text-slate-900 bg-slate-100 border border-slate-200 px-2 py-0.5 rounded-md">
                          § {source.section}
                        </span>
                      )}
                    </div>

                    <h4 className="font-black text-slate-900 text-base mt-2 tracking-tight">
                      {source.act || "Indian Statutory Act"}
                    </h4>

                    <div className="mt-2 space-y-1 text-xs text-slate-600">
                      {source.chapter && (
                        <p>
                          <span className="font-bold text-slate-500">Chapter:</span>{" "}
                          <span className="text-slate-800">{source.chapter}</span>
                        </p>
                      )}
                      {source.title && (
                        <p className="line-clamp-2">
                          <span className="font-bold text-slate-500">Title / Subject:</span>{" "}
                          <span className="text-slate-800 font-medium">{source.title}</span>
                        </p>
                      )}
                    </div>
                  </div>

                  {/* Relevance indicator pill */}
                  <div className="text-right flex-shrink-0">
                    <span className="inline-block text-xs font-bold text-indigo-700 bg-indigo-50 border border-indigo-200 px-3 py-1 rounded-lg">
                      {finalLabel}
                    </span>
                    {finalPercent !== null && (
                      <div className="mt-2 w-24 h-1.5 bg-slate-100 rounded-full overflow-hidden ml-auto">
                        <div
                          className="h-full bg-indigo-600 rounded-full"
                          style={{ width: `${finalPercent}%` }}
                        />
                      </div>
                    )}
                  </div>
                </div>

                {/* Toggle vector details */}
                <button
                  type="button"
                  onClick={() => toggle(index)}
                  className="mt-4 flex items-center gap-1.5 text-xs font-bold text-indigo-600 hover:text-indigo-800 transition-colors"
                >
                  <Info className="w-3.5 h-3.5" />
                  <span>{isExpanded ? "Hide technical RAG scores" : "View technical RAG scores"}</span>
                  {isExpanded ? <ChevronUp className="w-3.5 h-3.5" /> : <ChevronDown className="w-3.5 h-3.5" />}
                </button>
              </div>

              {/* Technical retrieval details accordion */}
              {isExpanded && (
                <div className="border-t border-slate-200 bg-slate-50/80 p-4 sm:p-5 space-y-3">
                  <div className="flex items-center justify-between text-xs">
                    <span className="font-bold text-slate-600">Composite Hybrid Vector Score:</span>
                    <span className="font-mono font-black text-slate-900 text-sm">
                      {finalScore === null ? "—" : finalScore.toFixed(3)}
                    </span>
                  </div>

                  <div className="grid grid-cols-2 sm:grid-cols-5 gap-2">
                    <ScoreBox label="Semantic" value={source.semantic_score} />
                    <ScoreBox label="Keyword" value={source.keyword_score} />
                    <ScoreBox label="Metadata" value={source.metadata_score} />
                    <ScoreBox label="Domain" value={source.domain_score} />
                    <ScoreBox label="Legal Issue" value={source.legal_issue_score} />
                  </div>
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}