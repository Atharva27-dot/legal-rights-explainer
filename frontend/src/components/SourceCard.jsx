import { useState } from "react";
import {
  FaBookOpen,
  FaChevronDown,
  FaChevronUp,
  FaInfoCircle,
} from "react-icons/fa";

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

  if (number === null) return "Unavailable";
  if (number >= 0.75) return "High";
  if (number >= 0.5) return "Moderate";
  if (number > 0) return "Low";

  return "Very Low";
}

function ScoreBox({ label, value }) {
  const number = scoreNumber(value);

  return (
    <div className="bg-white border border-slate-200 rounded-xl p-3">
      <p className="text-xs text-slate-500">{label}</p>

      <p className="font-bold text-slate-800 mt-1">
        {number === null ? "—" : number.toFixed(3)}
      </p>
    </div>
  );
}

export default function SourceCard({ sources }) {
  const [expanded, setExpanded] = useState({});

  if (!sources || sources.length === 0) return null;

  const toggle = (index) => {
    setExpanded((previous) => ({
      ...previous,
      [index]: !previous[index],
    }));
  };

  return (
    <div className="bg-white rounded-3xl border border-slate-200 shadow-sm overflow-hidden">

      {/* Header */}
      <div className="px-6 py-5 border-b border-slate-200">
        <div className="flex items-center gap-3">

          <div className="w-10 h-10 rounded-xl bg-indigo-100 text-indigo-700 flex items-center justify-center">
            <FaBookOpen />
          </div>

          <div>
            <h2 className="text-xl font-bold text-slate-900">
              Legal Sources
            </h2>

            <p className="text-sm text-slate-500 mt-0.5">
              Legal provisions retrieved for this question
            </p>
          </div>

        </div>
      </div>

      {/* Sources */}
      <div className="p-6 space-y-4">

        {sources.map((source, index) => {
          const finalScore = scoreNumber(source.final_score);
          const finalPercent = scorePercent(source.final_score);
          const finalLabel = relevanceLabel(source.final_score);
          const isExpanded = Boolean(expanded[index]);

          return (
            <div
              key={`${source.act}-${source.section}-${index}`}
              className="border border-slate-200 rounded-2xl overflow-hidden"
            >

              {/* Main source information */}
              <div className="p-5">

                <div className="flex items-start justify-between gap-4">

                  <div className="min-w-0">

                    <p className="text-xs font-semibold uppercase tracking-wide text-indigo-600">
                      Source {index + 1}
                    </p>

                    <h3 className="font-bold text-slate-900 text-lg mt-1">
                      {source.act || "Legal Act"}
                    </h3>

                    <div className="mt-3 space-y-1 text-sm">

                      {source.chapter && (
                        <p>
                          <span className="font-semibold text-slate-500">
                            Chapter:
                          </span>{" "}
                          <span className="text-slate-700">
                            {source.chapter}
                          </span>
                        </p>
                      )}

                      {source.section && (
                        <p>
                          <span className="font-semibold text-slate-500">
                            Section:
                          </span>{" "}
                          <span className="font-semibold text-slate-800">
                            {source.section}
                          </span>
                        </p>
                      )}

                      {source.title && (
                        <p>
                          <span className="font-semibold text-slate-500">
                            Title:
                          </span>{" "}
                          <span className="text-slate-700">
                            {source.title}
                          </span>
                        </p>
                      )}

                    </div>
                  </div>

                  {/* Simple relevance indicator */}
                  <div className="flex-shrink-0 text-right">

                    <p className="text-xs text-slate-500">
                      Relevance
                    </p>

                    <p className="text-sm font-bold text-indigo-700">
                      {finalLabel}
                    </p>

                    {finalPercent !== null && finalPercent > 0 && (
                      <div className="mt-2 w-24 h-1.5 bg-slate-200 rounded-full overflow-hidden">
                        <div
                          className="h-full bg-indigo-600 rounded-full"
                          style={{ width: `${finalPercent}%` }}
                        />
                      </div>
                    )}

                  </div>

                </div>

                {/* Technical details toggle */}
                <button
                  type="button"
                  onClick={() => toggle(index)}
                  className="mt-5 flex items-center gap-2 text-sm font-semibold text-indigo-700 hover:text-indigo-900"
                >
                  <FaInfoCircle />

                  {isExpanded
                    ? "Hide retrieval details"
                    : "View retrieval details"}

                  {isExpanded ? (
                    <FaChevronUp />
                  ) : (
                    <FaChevronDown />
                  )}
                </button>

              </div>

              {/* Technical retrieval information */}
              {isExpanded && (
                <div className="border-t border-slate-200 bg-slate-50 p-5">

                  <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3 mb-5">

                    <div>
                      <p className="text-xs font-semibold uppercase tracking-wide text-slate-500">
                        Retrieval relevance
                      </p>

                      <p className="text-2xl font-bold text-slate-900 mt-1">
                        {finalScore === null
                          ? "—"
                          : finalScore.toFixed(3)}
                      </p>
                    </div>

                    <div className="text-sm text-slate-600">
                      Final retrieval score
                    </div>

                  </div>

                  <p className="text-xs font-semibold uppercase tracking-wide text-slate-500 mb-3">
                    Technical score breakdown
                  </p>

                  <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-3">

                    <ScoreBox
                      label="Semantic"
                      value={source.semantic_score}
                    />

                    <ScoreBox
                      label="Keyword"
                      value={source.keyword_score}
                    />

                    <ScoreBox
                      label="Metadata"
                      value={source.metadata_score}
                    />

                    <ScoreBox
                      label="Domain"
                      value={source.domain_score}
                    />

                    <ScoreBox
                      label="Legal Issue"
                      value={source.legal_issue_score}
                    />

                  </div>

                  <p className="text-xs text-slate-500 mt-4">
                    These are technical retrieval signals. They do not
                    represent legal certainty, legal probability, or the
                    likelihood of a particular outcome.
                  </p>

                </div>
              )}

            </div>
          );
        })}

      </div>
    </div>
  );
}