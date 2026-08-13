import {
  FaBookOpen,
  FaBalanceScale,
  FaGavel,
  FaFolderOpen,
} from "react-icons/fa";

export default function SourceCard({ sources }) {
  if (!sources || sources.length === 0) return null;

  return (
    <div className="bg-white rounded-3xl shadow-xl border border-slate-200 overflow-hidden">

      {/* Header */}

      <div className="bg-gradient-to-r from-emerald-700 to-teal-600 px-8 py-5">

        <div className="flex items-center gap-3">

          <FaBookOpen className="text-white text-2xl" />

          <div>

            <h2 className="text-white text-2xl font-bold">
              Legal Sources
            </h2>

            <p className="text-emerald-100 text-sm">
              Retrieved legal provisions used to generate this answer
            </p>

          </div>

        </div>

      </div>

      {/* Sources */}

      <div className="p-8 space-y-5">

        {sources.map((source, index) => (

          <div
            key={index}
            className="rounded-2xl border border-slate-200 bg-slate-50 hover:bg-blue-50 hover:border-blue-300 transition-all duration-300 p-6 shadow-sm"
          >

            {/* Act */}

            <div className="flex items-center gap-3 mb-4">

              <FaBalanceScale className="text-blue-800 text-xl" />

              <h3 className="text-lg font-bold text-slate-800">
                {source.act}
              </h3>

            </div>

            <div className="grid md:grid-cols-3 gap-4">

              {/* Chapter */}

              <div className="bg-white rounded-xl border border-slate-200 p-4">

                <div className="flex items-center gap-2 mb-2">

                  <FaFolderOpen className="text-indigo-700" />

                  <span className="font-semibold">
                    Chapter
                  </span>

                </div>

                <p className="text-slate-700">
                  {source.chapter || "Not Available"}
                </p>

              </div>

              {/* Section */}

              <div className="bg-white rounded-xl border border-slate-200 p-4">

                <div className="flex items-center gap-2 mb-2">

                  <FaGavel className="text-emerald-700" />

                  <span className="font-semibold">
                    Section
                  </span>

                </div>

                <p className="text-slate-700">
                  {source.section || "Not Available"}
                </p>

              </div>

              {/* Title */}

              <div className="bg-white rounded-xl border border-slate-200 p-4">

                <div className="flex items-center gap-2 mb-2">

                  <FaBookOpen className="text-orange-600" />

                  <span className="font-semibold">
                    Title
                  </span>

                </div>

                <p className="text-slate-700">
                  {source.title || "Not Available"}
                </p>

              </div>

            </div>

          </div>

        ))}

      </div>

    </div>
  );
}