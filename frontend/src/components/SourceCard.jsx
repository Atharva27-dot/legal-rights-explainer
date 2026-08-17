import { FaBookOpen, FaChartBar } from "react-icons/fa";

export default function SourceCard({ sources }) {

  if (!sources || sources.length === 0) {
    return null;
  }

  return (

    <div className="bg-white rounded-xl shadow-lg mt-8 p-8">

      <div className="flex items-center gap-3 mb-6">

        <FaBookOpen className="text-blue-800 text-2xl" />

        <h2 className="text-2xl font-bold">
          Legal Sources
        </h2>

      </div>

      <div className="grid gap-5">

        {sources.map((source, index) => (

          <div
            key={index}
            className="border-l-4 border-blue-800 bg-slate-50 rounded-lg p-5"
          >

            {/* ================================= */}
            {/* SOURCE INFORMATION */}
            {/* ================================= */}

            <h3 className="font-bold text-lg text-blue-900">
              {source.act || "Legal Act"}
            </h3>

            <p className="mt-2">

              <strong>Domain:</strong>{" "}

              {source.domain || "General Legal"}

            </p>

            <p>

              <strong>Chapter:</strong>{" "}

              {source.chapter || "Not available"}

            </p>

            <p>

              <strong>Section:</strong>{" "}

              {source.section || "Not available"}

            </p>

            <p>

              <strong>Title:</strong>{" "}

              {source.title || "Not available"}

            </p>

            {/* ================================= */}
            {/* RETRIEVAL EXPLANATION */}
            {/* ================================= */}

            <div className="mt-5 pt-5 border-t">

              <div className="flex items-center gap-2 mb-4">

                <FaChartBar className="text-indigo-700" />

                <h4 className="font-bold text-indigo-900">

                  Retrieval Relevance

                </h4>

              </div>

              <div className="grid grid-cols-2 md:grid-cols-5 gap-3">

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
                  label="Final"
                  value={source.final_score}
                  highlight
                />

              </div>

            </div>

          </div>

        ))}

      </div>

    </div>

  );
}


/* ============================================================
   SCORE BOX
============================================================ */

function ScoreBox({
  label,
  value,
  highlight = false
}) {

  const numericValue =
    typeof value === "number"
      ? value
      : 0;

  return (

    <div
      className={
        highlight
          ? "bg-blue-100 border border-blue-300 rounded-lg p-3"
          : "bg-white border rounded-lg p-3"
      }
    >

      <p className="text-xs text-gray-500 font-semibold">

        {label}

      </p>

      <p
        className={
          highlight
            ? "text-xl font-bold text-blue-900 mt-1"
            : "text-lg font-bold text-gray-800 mt-1"
        }
      >

        {numericValue.toFixed(3)}

      </p>

    </div>

  );
}