import {
  FaBalanceScale,
  FaDatabase,
  FaRobot,
  FaCheckCircle,
} from "react-icons/fa";

export default function Loader() {
  return (
    <div className="bg-white rounded-3xl shadow-xl border border-slate-200 overflow-hidden animate-pulse">

      {/* Header */}

      <div className="bg-gradient-to-r from-blue-900 via-indigo-700 to-blue-600 px-8 py-6">

        <div className="flex items-center gap-4">

          <div className="w-16 h-16 rounded-2xl bg-white/20 flex items-center justify-center">

            <FaBalanceScale className="text-white text-3xl" />

          </div>

          <div>

            <h2 className="text-white text-2xl font-bold">

              AI Legal Assistant

            </h2>

            <p className="text-blue-100">

              Preparing your legal answer...

            </p>

          </div>

        </div>

      </div>

      {/* Steps */}

      <div className="p-8 space-y-6">

        <div className="flex items-center gap-4">

          <FaDatabase className="text-blue-700 text-2xl animate-bounce" />

          <div>

            <h3 className="font-semibold text-slate-800">

              Searching Legal Documents

            </h3>

            <p className="text-slate-500 text-sm">

              Finding the most relevant legal provisions.

            </p>

          </div>

        </div>

        <div className="flex items-center gap-4">

          <FaRobot className="text-purple-700 text-2xl animate-bounce" />

          <div>

            <h3 className="font-semibold text-slate-800">

              Generating AI Explanation

            </h3>

            <p className="text-slate-500 text-sm">

              Creating an easy-to-understand legal explanation.

            </p>

          </div>

        </div>

        <div className="flex items-center gap-4">

          <FaCheckCircle className="text-green-600 text-2xl animate-bounce" />

          <div>

            <h3 className="font-semibold text-slate-800">

              Preparing Legal Sources

            </h3>

            <p className="text-slate-500 text-sm">

              Collecting supporting legal references.

            </p>

          </div>

        </div>

      </div>

      {/* Footer */}

      <div className="border-t border-slate-200 bg-slate-50 px-8 py-5">

        <div className="flex items-center gap-2">

          <div className="w-3 h-3 rounded-full bg-blue-700 animate-ping"></div>
          <div className="w-3 h-3 rounded-full bg-indigo-700 animate-ping delay-150"></div>
          <div className="w-3 h-3 rounded-full bg-purple-700 animate-ping delay-300"></div>

          <span className="ml-3 text-slate-600 font-medium">

            This usually takes 5–15 seconds...

          </span>

        </div>

      </div>

    </div>
  );
}