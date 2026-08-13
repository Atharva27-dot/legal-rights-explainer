import {
  FaCopy,
  FaFileAlt,
  FaCheckCircle,
} from "react-icons/fa";

export default function AnswerCard({ answer }) {
  if (!answer) return null;

  const copyAnswer = () => {
    navigator.clipboard.writeText(answer);
    alert("Answer copied successfully!");
  };

  return (
    <div className="bg-white rounded-3xl shadow-xl border border-slate-200 overflow-hidden">

      {/* Header */}

      <div className="bg-gradient-to-r from-indigo-700 to-blue-900 px-8 py-5 flex items-center justify-between">

        <div className="flex items-center gap-3">

          <FaFileAlt className="text-white text-2xl" />

          <div>

            <h2 className="text-white text-2xl font-bold">
              AI Response
            </h2>

            <p className="text-blue-100 text-sm">
              Generated using retrieved legal documents
            </p>

          </div>

        </div>

        <button
          onClick={copyAnswer}
          className="flex items-center gap-2 bg-white text-blue-900 px-5 py-2 rounded-xl font-semibold hover:bg-blue-50 transition"
        >
          <FaCopy />

          Copy
        </button>

      </div>

      {/* Content */}

      <div className="p-8">

        <div className="flex items-center gap-3 mb-6">

          <FaCheckCircle className="text-green-600 text-xl" />

          <h3 className="text-xl font-bold text-slate-800">
            Plain Language Explanation
          </h3>

        </div>

        <div className="bg-slate-50 border border-slate-200 rounded-2xl p-6">

          <p className="text-slate-700 leading-8 whitespace-pre-wrap">

            {answer}

          </p>

        </div>

      </div>

    </div>
  );
}