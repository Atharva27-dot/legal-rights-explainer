import { useState } from "react";
import AppShell from "../components/AppShell";
import EvidenceUploader from "../components/EvidenceUploader";
import AnswerCard from "../components/AnswerCard";
import SourceCard from "../components/SourceCard";
import StatsCard from "../components/StatsCard";
import { askQuestion } from "../services/api";
import {
  Scale,
  ShoppingBag,
  Smartphone,
  Briefcase,
  Car,
  FileCheck2,
  Building,
  HeartHandshake,
  Gavel,
  CheckCircle2,
  AlertCircle,
  Send,
  BookOpen,
  Info,
  Check
} from "lucide-react";
import toast from "react-hot-toast";

const domainCards = [
  {
    id: "Consumer Protection",
    title: "Consumer Protection",
    act: "Consumer Protection Act, 2019",
    icon: ShoppingBag,
    color: "from-blue-600 to-indigo-600",
    description: "Defective products, wrong deliveries, service deficiency, refunds & warranty issues.",
  },
  {
    id: "Cyber / IT",
    title: "Cyber / IT Crime",
    act: "IT Act, 2000 & CERT-In Rules",
    icon: Smartphone,
    color: "from-purple-600 to-indigo-700",
    description: "UPI fraud, phishing, unauthorized access, identity theft & online payment disputes.",
  },
  {
    id: "Contract / Service",
    title: "Contract & Services",
    act: "Indian Contract Act, 1872",
    icon: Briefcase,
    color: "from-emerald-600 to-teal-700",
    description: "Breach of contract, non-payment of dues, service agreement disputes.",
  },
  {
    id: "Motor Vehicle",
    title: "Motor Vehicle & Accident",
    act: "Motor Vehicles Act, 1988",
    icon: Car,
    color: "from-amber-600 to-orange-700",
    description: "Road accident claims, insurance disputes, DL/RC & compensation claims.",
  },
  {
    id: "Right to Information",
    title: "Right to Information",
    act: "RTI Act, 2005",
    icon: FileCheck2,
    color: "from-cyan-600 to-blue-700",
    description: "Information request delays, PIO non-compliance, first & second appeals.",
  },
  {
    id: "Real Estate / RERA",
    title: "Real Estate & RERA",
    act: "RERA Act, 2016",
    icon: Building,
    color: "from-indigo-600 to-slate-800",
    description: "Delayed possession, builder fraud, defective construction & refund claims.",
  },
  {
    id: "Domestic Violence",
    title: "Domestic Violence",
    act: "PWDVA Act, 2005",
    icon: HeartHandshake,
    color: "from-rose-600 to-pink-700",
    description: "Protection orders, monetary relief, residence orders & custody claims.",
  },
  {
    id: "Legal Services / Legal Aid",
    title: "Free Legal Services",
    act: "Legal Services Authorities Act, 1987",
    icon: Scale,
    color: "from-teal-600 to-emerald-700",
    description: "Eligibility for free legal counsel, Lok Adalats & legal service authorities.",
  },
  {
    id: "Criminal Law / BNS",
    title: "Criminal Offenses (BNS)",
    act: "Bharatiya Nyaya Sanhita, 2023",
    icon: Gavel,
    color: "from-slate-700 to-slate-900",
    description: "Theft, cheating, criminal intimidation, assault & statutory offenses.",
  },
];

const issuesByDomain = {
  "Consumer Protection": [
    "Consumer Definition",
    "Consumer Rights",
    "Filing Complaint",
    "Mediation",
    "Defective Product",
    "Refund / Replacement",
    "Deficiency in Service",
    "Unfair Trade Practice",
    "Product Liability",
  ],
  "Cyber / IT": [
    "UPI Fraud",
    "Unauthorized Access",
    "Identity Theft",
    "Online Payment Fraud",
    "Cyber Crime",
  ],
  "Contract / Service": [
    "Breach of Contract",
    "Non-Payment",
    "Contractual Dispute",
    "Service Agreement Dispute",
  ],
  "Motor Vehicle": [
    "Driving Licence",
    "Road Accident",
    "Traffic Dispute",
    "Motor Insurance Claim",
    "Vehicle Compensation",
    "Vehicle Registration",
    "Permit Dispute",
  ],
  "Right to Information": [
    "Request for Information",
    "Information Denied",
    "Delay in Information",
    "RTI Appeal",
    "Public Information Officer",
    "Exempt Information",
  ],
  "Real Estate / RERA": [
    "Delayed Possession",
    "Builder Dispute",
    "Project Registration",
    "Real Estate Agent",
    "Defective Construction",
    "Refund from Builder",
    "RERA Complaint",
  ],
  "Domestic Violence": [
    "Domestic Violence",
    "Protection Order",
    "Residence Order",
    "Monetary Relief",
    "Custody Order",
    "Compensation",
    "Protection Officer",
  ],
  "Legal Services / Legal Aid": [
    "Free Legal Aid",
    "Eligibility for Legal Aid",
    "Legal Services Authority",
    "Lok Adalat",
    "Legal Aid Application",
    "Legal Representation",
  ],
  "Criminal Law / BNS": [
    "Criminal Offence",
    "Threat / Intimidation",
    "Theft",
    "Assault",
    "Cheating",
    "Hurt",
    "Sexual Offence",
    "Defamation",
  ],
};

export default function RightsGuide() {
  const [domain, setDomain] = useState("");
  const [issueType, setIssueType] = useState("");
  const [question, setQuestion] = useState("");
  const [evidence, setEvidence] = useState([]);
  const [answer, setAnswer] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSelectDomain = (selectedDomainId) => {
    setDomain(selectedDomainId);
    setIssueType("");
    setError("");
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError("");
    setAnswer(null);

    if (!domain) {
      setError("Please select a legal area (STEP 1).");
      toast.error("Please select a legal area.");
      return;
    }

    if (!issueType) {
      setError("Please choose a specific issue (STEP 2).");
      toast.error("Please choose an issue.");
      return;
    }

    if (!question.trim()) {
      setError("Please describe what happened (STEP 3).");
      toast.error("Please describe what happened.");
      return;
    }

    try {
      setLoading(true);
      const result = await askQuestion(question, domain, issueType, evidence);
      setAnswer(result);
      toast.success("Legal explanation generated successfully!");
    } catch (err) {
      console.error(err);
      setError("Unable to process your request. Please ensure FastAPI backend is running.");
      toast.error("Failed to fetch legal explanation.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <AppShell>
      <div className="space-y-8">
        {/* Page Top Heading */}
        <div className="bg-slate-900 rounded-3xl p-6 sm:p-8 text-white shadow-md border border-slate-800">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
            <div className="flex items-start gap-4">
              <div className="w-12 h-12 rounded-2xl bg-indigo-600 flex items-center justify-center text-white shadow-md flex-shrink-0">
                <BookOpen className="w-6 h-6" />
              </div>
              <div>
                <span className="text-xs font-bold uppercase tracking-wider text-indigo-300">
                  Interactive Guided Legal Assistant
                </span>
                <h1 className="text-2xl sm:text-3xl font-black text-white tracking-tight mt-0.5">
                  Rights Guide
                </h1>
                <p className="text-xs sm:text-sm text-slate-300 mt-1 max-w-2xl leading-relaxed">
                  Follow the step-by-step process to choose your legal area, select your issue, describe what happened, and receive an evidence-grounded legal explanation.
                </p>
              </div>
            </div>

            <div className="flex items-center gap-2 bg-emerald-950/80 border border-emerald-500/30 rounded-full px-3.5 py-1.5 self-start sm:self-center">
              <span className="w-2 h-2 rounded-full bg-emerald-400 animate-ping" />
              <span className="text-xs font-bold text-emerald-300">9 Legal Areas Ready</span>
            </div>
          </div>
        </div>

        {/* Workflow Progress Steps Bar */}
        <div className="grid grid-cols-3 gap-2 bg-white p-2 rounded-2xl border border-slate-200 shadow-xs text-xs font-semibold">
          <div className={`flex items-center gap-2 p-2.5 rounded-xl transition ${domain ? "bg-indigo-50 text-indigo-950 border border-indigo-200" : "bg-slate-50 text-slate-500"}`}>
            <span className={`w-6 h-6 rounded-full flex items-center justify-center text-xs font-bold ${domain ? "bg-indigo-600 text-white" : "bg-slate-200 text-slate-600"}`}>
              {domain ? <Check className="w-3.5 h-3.5" /> : "1"}
            </span>
            <span className="truncate">STEP 1: Choose legal area</span>
          </div>

          <div className={`flex items-center gap-2 p-2.5 rounded-xl transition ${issueType ? "bg-indigo-50 text-indigo-950 border border-indigo-200" : "bg-slate-50 text-slate-500"}`}>
            <span className={`w-6 h-6 rounded-full flex items-center justify-center text-xs font-bold ${issueType ? "bg-indigo-600 text-white" : "bg-slate-200 text-slate-600"}`}>
              {issueType ? <Check className="w-3.5 h-3.5" /> : "2"}
            </span>
            <span className="truncate">STEP 2: Choose issue</span>
          </div>

          <div className={`flex items-center gap-2 p-2.5 rounded-xl transition ${question.trim() ? "bg-indigo-50 text-indigo-950 border border-indigo-200" : "bg-slate-50 text-slate-500"}`}>
            <span className={`w-6 h-6 rounded-full flex items-center justify-center text-xs font-bold ${question.trim() ? "bg-indigo-600 text-white" : "bg-slate-200 text-slate-600"}`}>
              3
            </span>
            <span className="truncate">STEP 3: Describe what happened</span>
          </div>
        </div>

        {/* Form Container */}
        <form onSubmit={handleSubmit} className="bg-white rounded-3xl border border-slate-200 shadow-xs p-6 sm:p-8 space-y-8">
          {/* STEP 1: Choose legal area */}
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <div>
                <h2 className="text-base sm:text-lg font-extrabold text-slate-900 flex items-center gap-2">
                  <span className="w-6 h-6 rounded-lg bg-indigo-600 text-white flex items-center justify-center text-xs font-extrabold">1</span>
                  STEP 1: Choose legal area
                </h2>
                <p className="text-xs text-slate-500">
                  Select the primary legal area relevant to your problem from the 9 supported Indian legal domains
                </p>
              </div>
              {domain && (
                <span className="text-xs font-bold text-indigo-700 bg-indigo-50 px-3 py-1 rounded-lg border border-indigo-200 shadow-2xs">
                  Selected: {domain}
                </span>
              )}
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
              {domainCards.map((card) => {
                const Icon = card.icon;
                const isSelected = domain === card.id;

                return (
                  <div
                    key={card.id}
                    onClick={() => handleSelectDomain(card.id)}
                    className={`group relative p-4 rounded-2xl border transition-all duration-200 cursor-pointer flex items-start gap-3.5 ${
                      isSelected
                        ? "border-indigo-600 bg-indigo-50/70 ring-2 ring-indigo-500/20 shadow-xs"
                        : "border-slate-200 hover:border-slate-300 bg-white hover:bg-slate-50/50"
                    }`}
                  >
                    <div className={`w-10 h-10 rounded-xl bg-slate-900 text-white flex items-center justify-center shadow-xs flex-shrink-0 group-hover:scale-105 transition-transform`}>
                      <Icon className="w-5 h-5 text-indigo-300" />
                    </div>

                    <div className="min-w-0 flex-1">
                      <div className="flex items-center justify-between gap-1">
                        <h3 className="font-bold text-slate-900 text-sm truncate group-hover:text-indigo-600 transition-colors">
                          {card.title}
                        </h3>
                        {isSelected && (
                          <CheckCircle2 className="w-4.5 h-4.5 text-indigo-600 flex-shrink-0" />
                        )}
                      </div>
                      <p className="text-[11px] font-semibold text-slate-400">
                        {card.act}
                      </p>
                      <p className="text-[11px] text-slate-500 mt-1 line-clamp-2 leading-tight">
                        {card.description}
                      </p>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>

          {/* STEP 2: Choose issue */}
          <div className={`space-y-4 pt-6 border-t border-slate-100 transition-opacity ${domain ? "opacity-100" : "opacity-50 pointer-events-none"}`}>
            <div>
              <h2 className="text-base sm:text-lg font-extrabold text-slate-900 flex items-center gap-2">
                <span className="w-6 h-6 rounded-lg bg-indigo-600 text-white flex items-center justify-center text-xs font-extrabold">2</span>
                STEP 2: Choose issue
              </h2>
              <p className="text-xs text-slate-500">
                {domain ? `Select the specific issue under ${domain}` : "Select a legal area in STEP 1 first"}
              </p>
            </div>

            {domain && (
              <div className="flex flex-wrap gap-2 bg-slate-50/80 p-4 rounded-2xl border border-slate-200/80">
                {issuesByDomain[domain]?.map((issue) => {
                  const isSelected = issueType === issue;
                  return (
                    <button
                      key={issue}
                      type="button"
                      onClick={() => setIssueType(issue)}
                      className={`px-3.5 py-2 rounded-xl text-xs font-semibold transition-all duration-200 ${
                        isSelected
                          ? "bg-indigo-600 text-white shadow-xs scale-105 font-bold"
                          : "bg-white text-slate-700 hover:bg-slate-200/80 border border-slate-200"
                      }`}
                    >
                      {issue}
                    </button>
                  );
                })}
              </div>
            )}
          </div>

          {/* STEP 3: Describe what happened */}
          <div className="space-y-4 pt-6 border-t border-slate-100">
            <div>
              <h2 className="text-base sm:text-lg font-extrabold text-slate-900 flex items-center gap-2">
                <span className="w-6 h-6 rounded-lg bg-indigo-600 text-white flex items-center justify-center text-xs font-extrabold">3</span>
                STEP 3: Describe what happened
              </h2>
              <p className="text-xs text-slate-500">
                Explain your problem in detail, including dates, amounts, communication, and relevant facts
              </p>
            </div>

            <textarea
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              placeholder="Describe what happened... (e.g., 'I bought a laptop from an online portal on 15 Feb. The device failed to boot after 3 days. The seller and manufacturer refused replacement or refund despite the 10-day return policy.')"
              rows={6}
              className="w-full bg-slate-50 border border-slate-200 rounded-2xl p-4 text-sm text-slate-800 placeholder:text-slate-400 outline-none focus:bg-white focus:border-indigo-500 focus:ring-4 focus:ring-indigo-100 transition"
            />

            <div className="flex justify-between items-center text-xs text-slate-400 px-1">
              <span>Include facts, dates, and amounts for maximum RAG precision</span>
              <span>{question.length} characters</span>
            </div>

            {/* Evidence Uploader Component */}
            <EvidenceUploader
              onEvidenceChange={setEvidence}
              onSkip={() => setEvidence([])}
            />
          </div>

          {/* Error Message */}
          {error && (
            <div className="flex items-center gap-3 p-4 rounded-xl bg-red-50 border border-red-200 text-red-800 text-xs font-medium">
              <AlertCircle className="w-4 h-4 text-red-600 flex-shrink-0" />
              <span>{error}</span>
            </div>
          )}

          {/* Submit Action */}
          <div className="pt-4 border-t border-slate-100 flex flex-col sm:flex-row items-center justify-between gap-4">
            <div className="flex items-center gap-2 text-xs text-slate-500">
              <Info className="w-4 h-4 text-indigo-600 flex-shrink-0" />
              <span>Grounded in ChromaDB vector database of Indian Legal Acts.</span>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full sm:w-auto inline-flex items-center justify-center gap-2 bg-indigo-600 hover:bg-indigo-700 disabled:bg-slate-300 text-white font-bold text-sm px-8 py-3.5 rounded-xl shadow-xs transition-all duration-200 min-w-[220px]"
            >
              <Send className="w-4 h-4" />
              {loading ? "Analyzing Your Situation..." : "Analyze My Rights"}
            </button>
          </div>
        </form>

        {/* Results Area */}
        {answer && !loading && (
          <div className="space-y-6 pt-4">
            <AnswerCard answer={answer.answer} />
            <SourceCard sources={answer.sources} />
            <StatsCard
              confidence={answer.confidence}
              retrieval_time={answer.retrieval_time}
              llm_time={answer.llm_time}
              total_time={answer.total_time}
            />
          </div>
        )}
      </div>
    </AppShell>
  );
}
