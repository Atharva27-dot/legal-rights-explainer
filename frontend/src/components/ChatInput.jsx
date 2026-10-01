import { Send, Bot, Sparkles, HelpCircle, CornerDownLeft } from "lucide-react";

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
    <div className="bg-white rounded-2xl shadow-sm border border-slate-200 overflow-hidden transition-all focus-within:border-indigo-400 focus-within:ring-4 focus-within:ring-indigo-100">
      {/* Header Bar */}
      <div className="bg-slate-900 px-6 py-4 flex items-center justify-between text-white">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded-lg bg-indigo-600 flex items-center justify-center text-white shadow-xs">
            <Bot className="w-4 h-4" />
          </div>
          <div>
            <h3 className="font-bold text-sm text-white">
              Ask Legal Rights Question
            </h3>
            <p className="text-xs text-slate-400">
              Enter your issue in plain language (e.g. Hindi, English, or Hinglish)
            </p>
          </div>
        </div>
        <div className="hidden sm:flex items-center gap-1.5 text-xs text-indigo-300 font-medium bg-indigo-950/80 border border-indigo-800/60 px-2.5 py-1 rounded-lg">
          <Sparkles className="w-3.5 h-3.5 text-indigo-400" />
          <span>RAG Retrieval Active</span>
        </div>
      </div>

      {/* Input Textarea Area */}
      <div className="p-4 sm:p-5 space-y-4">
        <textarea
          rows={4}
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          onKeyDown={onKeyDown}
          placeholder="Describe your situation in simple words... (e.g., 'I purchased a defective laptop online. The seller refuses to accept return or refund after 5 days. What rights do I have under Consumer Protection Act?')"
          className="w-full bg-slate-50 border border-slate-200 rounded-xl p-4 text-sm text-slate-800 placeholder:text-slate-400 resize-y min-h-[110px] outline-none transition-colors focus:bg-white"
        />

        {/* Footer controls */}
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3 pt-2">
          <div className="flex items-center gap-2 text-xs text-slate-400">
            <CornerDownLeft className="w-3.5 h-3.5" />
            <span>Press <kbd className="font-semibold text-slate-600 bg-slate-100 px-1.5 py-0.5 rounded border border-slate-200">Enter</kbd> to submit or <kbd className="font-semibold text-slate-600 bg-slate-100 px-1.5 py-0.5 rounded border border-slate-200">Shift + Enter</kbd> for line break</span>
          </div>

          <button
            type="button"
            onClick={handleAsk}
            disabled={loading || !question.trim()}
            className="inline-flex items-center justify-center gap-2 bg-indigo-600 hover:bg-indigo-700 disabled:bg-slate-300 disabled:cursor-not-allowed text-white font-semibold text-sm px-6 py-2.5 rounded-xl shadow-xs transition-all duration-200 hover:scale-[1.02] active:scale-[0.98]"
          >
            <Send className="w-4 h-4" />
            {loading ? "Analyzing Legal Acts..." : "Ask Assistant"}
          </button>
        </div>
      </div>
    </div>
  );
}