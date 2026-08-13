import { FaPaperPlane, FaRobot } from "react-icons/fa";

export default function ChatInput({
  question,
  setQuestion,
  loading,
  handleAsk,
}) {
  const onKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();

      if (!loading && question.trim()) {
        handleAsk();
      }
    }
  };

  return (
    <div className="bg-white rounded-3xl shadow-xl border border-slate-200 overflow-hidden">

      {/* Header */}

      <div className="bg-gradient-to-r from-blue-900 via-indigo-700 to-blue-600 px-8 py-5 flex items-center gap-4">

        <div className="w-12 h-12 rounded-2xl bg-white/20 flex items-center justify-center">

          <FaRobot className="text-white text-xl" />

        </div>

        <div>

          <h2 className="text-white text-2xl font-bold">

            Ask the AI Legal Assistant

          </h2>

          <p className="text-blue-100 text-sm mt-1">

            Ask questions in simple language and receive legally grounded explanations.

          </p>

        </div>

      </div>

      {/* Input Area */}

      <div className="p-8">

        <textarea
          rows="5"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          onKeyDown={onKeyDown}
          placeholder="Example: I purchased a mobile phone online and received a defective product. Can I get a refund?"
          className="w-full rounded-2xl border border-slate-300 bg-slate-50 p-5 resize-none outline-none focus:border-blue-700 focus:ring-4 focus:ring-blue-100 transition text-slate-700 leading-7"
        />

        {/* Footer */}

        <div className="flex items-center justify-between mt-6">

          <div>

            <p className="text-sm text-slate-500">

              💡 Press <strong>Enter</strong> to send · <strong>Shift + Enter</strong> for a new line

            </p>

          </div>

          <button
            onClick={handleAsk}
            disabled={loading || !question.trim()}
            className="flex items-center gap-3 bg-gradient-to-r from-blue-900 to-indigo-700 hover:from-blue-800 hover:to-indigo-600 disabled:opacity-50 disabled:cursor-not-allowed text-white px-8 py-3 rounded-xl font-semibold shadow-lg transition-all duration-300 hover:scale-105"
          >

            <FaPaperPlane />

            {loading ? "Thinking..." : "Ask AI"}

          </button>

        </div>

      </div>

    </div>
  );
}