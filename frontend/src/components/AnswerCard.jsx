import { useMemo } from "react";
import {
  FaBalanceScale,
  FaCheckCircle,
  FaClipboardList,
  FaCopy,
  FaExclamationTriangle,
  FaGavel,
} from "react-icons/fa";
import toast from "react-hot-toast";

const SECTION_CONFIG = {
  "Plain Language Explanation": {
    icon: FaBalanceScale,
    color: "emerald",
  },
  "Relevant Legal Provision": {
    icon: FaGavel,
    color: "indigo",
  },
  "Possible Rights / Remedies": {
    icon: FaCheckCircle,
    color: "blue",
  },
  "What the Citizen Can Do": {
    icon: FaClipboardList,
    color: "violet",
  },
  "Important Note": {
    icon: FaExclamationTriangle,
    color: "amber",
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
  const sections = useMemo(
    () => parseAnswer(answer),
    [answer]
  );

  if (!answer) return null;

  const copyAnswer = async () => {
    try {
      await navigator.clipboard.writeText(answer);
      toast.success("Answer copied.");
    } catch (error) {
      console.error(error);
      toast.error("Unable to copy answer.");
    }
  };

  return (
    <div className="bg-white rounded-3xl border border-slate-200 shadow-sm overflow-hidden">

      {/* Header */}
      <div className="bg-gradient-to-r from-indigo-700 to-blue-700 text-white px-6 py-5">
        <div className="flex items-center justify-between gap-4">

          <div className="flex items-center gap-3 min-w-0">
            <div className="w-10 h-10 rounded-xl bg-white/15 flex items-center justify-center flex-shrink-0">
              <FaBalanceScale />
            </div>

            <div>
              <h2 className="text-xl font-bold">
                AI Legal Explanation
              </h2>

              <p className="text-blue-100 text-sm mt-0.5">
                Based on retrieved legal documents
              </p>
            </div>
          </div>

          <button
            onClick={copyAnswer}
            className="flex items-center gap-2 bg-white text-indigo-700 hover:bg-blue-50 px-3.5 py-2 rounded-xl text-sm font-semibold transition flex-shrink-0"
          >
            <FaCopy />
            Copy
          </button>

        </div>
      </div>

      {/* Structured answer */}
      <div className="p-6 space-y-4">

        {sections.map((section, index) => {
          const config =
            SECTION_CONFIG[section.title] ||
            SECTION_CONFIG["Plain Language Explanation"];

          const Icon = config.icon;

          const colorClasses = {
            emerald: {
              border: "border-emerald-200",
              icon: "bg-emerald-100 text-emerald-700",
              title: "text-emerald-900",
            },
            indigo: {
              border: "border-indigo-200",
              icon: "bg-indigo-100 text-indigo-700",
              title: "text-indigo-900",
            },
            blue: {
              border: "border-blue-200",
              icon: "bg-blue-100 text-blue-700",
              title: "text-blue-900",
            },
            violet: {
              border: "border-violet-200",
              icon: "bg-violet-100 text-violet-700",
              title: "text-violet-900",
            },
            amber: {
              border: "border-amber-200",
              icon: "bg-amber-100 text-amber-700",
              title: "text-amber-900",
            },
          };

          const colors = colorClasses[config.color];

          return (
            <div
              key={`${section.title}-${index}`}
              className={`rounded-2xl border ${colors.border} bg-white p-5`}
            >
              <div className="flex items-center gap-3 mb-3">

                <div
                  className={`w-9 h-9 rounded-xl flex items-center justify-center ${colors.icon}`}
                >
                  <Icon />
                </div>

                <h3 className={`font-bold ${colors.title}`}>
                  {section.title}
                </h3>

              </div>

              <div className="text-slate-700 text-sm sm:text-base leading-7 whitespace-pre-wrap">
                {section.content}
              </div>
            </div>
          );
        })}

      </div>

      {/* Footer notice */}
      <div className="px-6 pb-6">
        <div className="bg-slate-50 border border-slate-200 rounded-xl px-4 py-3 text-xs text-slate-500">
          This explanation is based on the retrieved legal documents and
          should be reviewed before relying on it.
        </div>
      </div>

    </div>
  );
}
