import { Scale, Database, Bot, CheckCircle2, Loader2, Sparkles } from "lucide-react";

export default function Loader() {
  return (
    <div className="bg-white rounded-3xl shadow-sm border border-slate-200 overflow-hidden">
      {/* Header */}
      <div className="bg-slate-900 px-6 py-5 text-white flex items-center justify-between border-b border-slate-800">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-indigo-600 flex items-center justify-center text-white shadow-xs">
            <Scale className="w-5 h-5 animate-pulse" />
          </div>
          <div>
            <h3 className="text-base font-extrabold text-white tracking-tight">
              Analyzing your situation...
            </h3>
            <p className="text-xs text-indigo-200">
              Retrieving Indian Legal Acts & Generating RAG Explanation
            </p>
          </div>
        </div>
        <Loader2 className="w-5 h-5 text-indigo-400 animate-spin" />
      </div>

      {/* Professional Progress Indicators */}
      <div className="p-6 space-y-3">
        <div className="flex items-center gap-4 bg-slate-50 p-4 rounded-2xl border border-slate-100 transition-all">
          <div className="w-9 h-9 rounded-xl bg-indigo-100 text-indigo-700 flex items-center justify-center flex-shrink-0">
            <Database className="w-4.5 h-4.5 animate-pulse" />
          </div>
          <div>
            <p className="font-bold text-xs sm:text-sm text-slate-900">
              Finding relevant legal provisions...
            </p>
            <p className="text-xs text-slate-500">
              Searching official gazette documents in ChromaDB vector database...
            </p>
          </div>
        </div>

        <div className="flex items-center gap-4 bg-slate-50 p-4 rounded-2xl border border-slate-100 transition-all">
          <div className="w-9 h-9 rounded-xl bg-purple-100 text-purple-700 flex items-center justify-center flex-shrink-0">
            <Bot className="w-4.5 h-4.5 animate-pulse" />
          </div>
          <div>
            <p className="font-bold text-xs sm:text-sm text-slate-900">
              Preparing your explanation...
            </p>
            <p className="text-xs text-slate-500">
              Synthesizing plain-language rights, remedies, and actionable guidance...
            </p>
          </div>
        </div>

        <div className="flex items-center gap-4 bg-slate-50 p-4 rounded-2xl border border-slate-100 transition-all">
          <div className="w-9 h-9 rounded-xl bg-emerald-100 text-emerald-700 flex items-center justify-center flex-shrink-0">
            <CheckCircle2 className="w-4.5 h-4.5 animate-pulse" />
          </div>
          <div>
            <p className="font-bold text-xs sm:text-sm text-slate-900">
              Verifying statutory grounding & sources...
            </p>
            <p className="text-xs text-slate-500">
              Calculating vector relevance scores and attaching Act/Section references...
            </p>
          </div>
        </div>
      </div>

      {/* Footer info bar */}
      <div className="px-6 py-3 border-t border-slate-100 bg-slate-50 flex items-center justify-between text-xs text-slate-500 font-medium">
        <div className="flex items-center gap-2">
          <span className="w-2 h-2 rounded-full bg-indigo-600 animate-ping" />
          <span>Statutory RAG Pipeline Executing</span>
        </div>
        <span>Local Ollama + ChromaDB</span>
      </div>
    </div>
  );
}