import { useMemo, useState } from "react";
import {
  Scale,
  Gavel,
  CheckCircle2,
  ClipboardList,
  AlertTriangle,
  Copy,
  Check,
  Sparkles,
  BookOpen,
  ShieldCheck,
  ListOrdered
} from "lucide-react";
import toast from "react-hot-toast";

const SECTION_CONFIG = {
  "Plain Language Explanation": {
    label: "WHAT THIS MEANS",
    icon: Scale,
    iconBg: "bg-emerald-600 text-white",
    cardBorder: "border-emerald-200/80 bg-emerald-50/30",
  },
  "Relevant Legal Provision": {
    label: "RELEVANT LEGAL PROVISION",
    icon: Gavel,
    iconBg: "bg-indigo-600 text-white",
    cardBorder: "border-indigo-200/80 bg-indigo-50/30",
  },
  "Possible Rights / Remedies": {
    label: "POSSIBLE RIGHTS / REMEDIES",
    icon: CheckCircle2,
    iconBg: "bg-blue-600 text-white",
    cardBorder: "border-blue-200/80 bg-blue-50/30",
  },
  "What the Citizen Can Do": {
    label: "WHAT YOU CAN DO",
    icon: ListOrdered,
    iconBg: "bg-purple-600 text-white",
    cardBorder: "border-purple-200/80 bg-purple-50/30",
  },
  "What You Can Do": {
    label: "WHAT YOU CAN DO",
    icon: ListOrdered,
    iconBg: "bg-purple-600 text-white",
    cardBorder: "border-purple-200/80 bg-purple-50/30",
  },
  "Important Note": {
    label: "IMPORTANT NOTE",
    icon: AlertTriangle,
    iconBg: "bg-amber-500 text-white",
    cardBorder: "border-amber-200/80 bg-amber-50/40",
  },
};

const SECTION_NAMES = Object.keys(SECTION_CONFIG);

function cleanText(text) {
  return text
    .replace(/^#+\s*/, "")
    .replace(/\*\*/g, "")
    .trim();
}

function parseAnswer(answer) {
  const source = String(answer || "")
    .replace(/\r\n/g, "\n")
    .trim();

  if (!source) return [];

  const lines = source.split("\n");
  const sections = [];
  let current = null;

  for (const rawLine of lines) {
    const line = rawLine.trim();

    if (!line) {
      if (current) current.content.push("");
      continue;
    }

    const normalized = line
      .replace(/^#+\s*/, "")
      .replace(/:$/, "")
      .trim();

    const heading = SECTION_NAMES.find(
      (name) => normalized.toLowerCase() === name.toLowerCase()
    );

    if (heading) {
      current = {
        title: heading,
        content: [],
      };
      sections.push(current);
      continue;
    }

    if (!current) {
      current = {
        title: "Plain Language Explanation",
        content: [],
      };
      sections.push(current);
    }

    current.content.push(cleanText(line));
  }

  return sections.map((section) => ({
    ...section,
    content: section.content
      .join("\n")
      .replace(/\n{3,}/g, "\n\n")
      .trim(),
  }));
}

export default function AnswerCard({ answer }) {
  const [copied, setCopied] = useState(false);

  const sections = useMemo(
    () => parseAnswer(answer),
    [answer]
  );

  if (!answer) return null;

  const copyAnswer = async () => {
    try {
      await navigator.clipboard.writeText(answer);
      setCopied(true);
      toast.success("Legal explanation copied to clipboard!");
      setTimeout(() => setCopied(false), 2000);
    } catch (error) {
      console.error(error);
      toast.error("Unable to copy answer.");
    }
  };

  return (
    <div className="bg-white rounded-3xl border border-slate-200 shadow-md overflow-hidden">
      {/* Header Banner: AI LEGAL INSIGHT */}
      <div className="bg-slate-900 text-white p-5 sm:p-6 border-b border-slate-800">
        <div className="flex items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-indigo-600 flex items-center justify-center text-white shadow-xs">
              <Sparkles className="w-5 h-5 text-indigo-200" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <span className="text-[11px] font-bold tracking-widest uppercase text-indigo-300">
                  AI LEGAL INSIGHT
                </span>
                <span className="text-[10px] font-semibold bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 px-2 py-0.5 rounded-full">
                  Grounded
                </span>
              </div>
              <h2 className="text-lg font-black text-white tracking-tight mt-0.5">
                Plain-Language Legal Rights Analysis
              </h2>
            </div>
          </div>

          <button
            type="button"
            onClick={copyAnswer}
            className="flex items-center gap-1.5 bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-bold px-3.5 py-2 rounded-xl transition shadow-xs"
          >
            {copied ? (
              <>
                <Check className="w-3.5 h-3.5 text-emerald-300" />
                <span>Copied!</span>
              </>
            ) : (
              <>
                <Copy className="w-3.5 h-3.5" />
                <span>Copy Explanation</span>
              </>
            )}
          </button>
        </div>
      </div>

      {/* Structured Answer Cards */}
      <div className="p-5 sm:p-6 space-y-4">
        {sections.map((section, index) => {
          const config =
            SECTION_CONFIG[section.title] ||
            SECTION_CONFIG["Plain Language Explanation"];

          const Icon = config.icon;
          const displayLabel = config.label || section.title.toUpperCase();

          const lines = section.content.split("\n").filter((l) => l.trim().length > 0);
          const isRemedies = section.title.includes("Rights") || section.title.includes("Remedies");
          const isActionStep = section.title.includes("Can Do") || section.title.includes("Citizen");

          return (
            <div
              key={`${section.title}-${index}`}
              className={`rounded-2xl border ${config.cardBorder} p-4 sm:p-5 transition-all duration-200`}
            >
              <div className="flex items-center gap-3 mb-3">
                <div className={`w-8 h-8 rounded-lg flex items-center justify-center ${config.iconBg}`}>
                  <Icon className="w-4 h-4" />
                </div>
                <h3 className="font-extrabold text-slate-900 text-xs sm:text-sm tracking-wider uppercase">
                  {displayLabel}
                </h3>
              </div>

              {/* Formatted Content */}
              {isRemedies && lines.length > 1 ? (
                <ul className="space-y-2 text-xs sm:text-sm text-slate-800 font-medium">
                  {lines.map((line, lIdx) => (
                    <li key={lIdx} className="flex items-start gap-2 bg-white/80 p-2.5 rounded-xl border border-slate-200/70">
                      <span className="text-indigo-600 font-bold mt-0.5">•</span>
                      <span className="leading-relaxed">{line.replace(/^[•\-\*]\s*/, "")}</span>
                    </li>
                  ))}
                </ul>
              ) : isActionStep && lines.length > 1 ? (
                <div className="space-y-2 text-xs sm:text-sm text-slate-800 font-medium">
                  {lines.map((line, lIdx) => (
                    <div key={lIdx} className="flex items-start gap-3 bg-white/90 p-3 rounded-xl border border-slate-200/80 shadow-2xs">
                      <span className="font-mono font-extrabold text-indigo-700 text-xs bg-indigo-50 px-2 py-0.5 rounded-md border border-indigo-100">
                        {String(lIdx + 1).padStart(2, "0")}
                      </span>
                      <span className="leading-relaxed">{line.replace(/^\d+[\.\)]\s*/, "")}</span>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="text-slate-800 text-xs sm:text-sm leading-relaxed whitespace-pre-wrap font-medium">
                  {section.content}
                </div>
              )}
            </div>
          );
        })}
      </div>

      {/* Footer Disclaimer Bar */}
      <div className="px-5 pb-5">
        <div className="bg-slate-50 border border-slate-200/80 rounded-xl p-3 text-xs text-slate-500 flex items-center justify-between">
          <span>This legal analysis is grounded in retrieved Indian legal documents. Review sources below for verification.</span>
          <span className="font-bold text-indigo-600 hidden sm:inline">RAG Grounded</span>
        </div>
      </div>
    </div>
  );
}
