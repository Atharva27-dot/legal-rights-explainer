import { Link } from "react-router-dom";
import {
  Scale,
  Sparkles,
  ArrowRight,
  ShieldCheck,
  ShoppingBag,
  Smartphone,
  Briefcase,
  Car,
  FileCheck2,
  Building,
  HeartHandshake,
  Gavel,
  BookOpenCheck,
  HelpCircle,
  FileText
} from "lucide-react";

const domainQuickCards = [
  {
    domain: "Consumer Protection",
    act: "Consumer Protection Act, 2019",
    icon: ShoppingBag,
    bgColor: "bg-blue-50 text-blue-700 border-blue-200",
    sampleQuestion: "I purchased a defective product online and the seller refuses to refund. What are my rights?",
  },
  {
    domain: "Cyber / IT",
    act: "IT Act, 2000 & Cyber Rules",
    icon: Smartphone,
    bgColor: "bg-purple-50 text-purple-700 border-purple-200",
    sampleQuestion: "Someone committed unauthorized UPI transaction fraud from my account. What legal remedies exist?",
  },
  {
    domain: "Contract / Service",
    act: "Indian Contract Act, 1872",
    icon: Briefcase,
    bgColor: "bg-emerald-50 text-emerald-700 border-emerald-200",
    sampleQuestion: "A service provider breached our signed agreement and didn't complete work after receiving payment.",
  },
  {
    domain: "Motor Vehicle",
    act: "Motor Vehicles Act, 1988",
    icon: Car,
    bgColor: "bg-amber-50 text-amber-700 border-amber-200",
    bgColorDark: "bg-amber-600 text-white",
    sampleQuestion: "What is the procedure and right to claim third-party compensation for a road accident?",
  },
  {
    domain: "Right to Information",
    act: "RTI Act, 2005",
    icon: FileCheck2,
    bgColor: "bg-cyan-50 text-cyan-700 border-cyan-200",
    sampleQuestion: "Public Information Officer delayed my RTI response past 30 days. How do I file an appeal?",
  },
  {
    domain: "Real Estate / RERA",
    act: "RERA Act, 2016",
    icon: Building,
    bgColor: "bg-indigo-50 text-indigo-700 border-indigo-200",
    sampleQuestion: "Builder delayed possession of my flat by over two years. Can I claim interest or full refund?",
  },
  {
    domain: "Domestic Violence",
    act: "PWDVA Act, 2005",
    icon: HeartHandshake,
    bgColor: "bg-rose-50 text-rose-700 border-rose-200",
    sampleQuestion: "What protection orders and residence rights are granted under Protection of Women from Domestic Violence Act?",
  },
  {
    domain: "Legal Aid / Services",
    act: "Legal Services Act, 1987",
    icon: Scale,
    bgColor: "bg-teal-50 text-teal-700 border-teal-200",
    sampleQuestion: "Who is eligible for free legal aid and representation under the Legal Services Authorities Act?",
  },
  {
    domain: "Criminal Law / BNS",
    act: "Bharatiya Nyaya Sanhita, 2023",
    icon: Gavel,
    bgColor: "bg-slate-100 text-slate-800 border-slate-300",
    sampleQuestion: "What are the legal procedures and rights regarding cheating, theft, or criminal intimidation under BNS?",
  },
];

export default function WelcomeScreen({ setQuestion }) {
  return (
    <div className="space-y-8">
      {/* 1. HERO / ABOVE-THE-FOLD */}
      <div className="relative overflow-hidden bg-slate-900 rounded-3xl p-6 sm:p-10 text-white border border-slate-800 shadow-md">
        <div className="relative z-10 max-w-3xl space-y-5">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-indigo-500/20 border border-indigo-500/30 text-indigo-300 text-xs font-semibold">
            <Sparkles className="w-3.5 h-3.5 text-indigo-400" />
            <span>Official Indian Statutory RAG Assistance</span>
          </div>

          <h1 className="text-3xl sm:text-4xl lg:text-5xl font-extrabold tracking-tight leading-tight text-white">
            Understand your legal rights. <br />
            <span className="text-indigo-300 font-extrabold">
              Know what you can do next.
            </span>
          </h1>

          <p className="text-slate-300 text-sm sm:text-base leading-relaxed max-w-2xl">
            AI-powered legal information explained in plain language and grounded in Indian legal provisions.
          </p>

          {/* Prominent CTAs */}
          <div className="pt-2 flex flex-wrap items-center gap-3">
            <Link
              to="/rights"
              className="inline-flex items-center justify-center gap-2 bg-indigo-600 hover:bg-indigo-500 text-white font-bold text-sm px-6 py-3 rounded-xl shadow-xs transition-all duration-200 hover:scale-[1.02] active:scale-[0.98]"
            >
              <BookOpenCheck className="w-4 h-4" />
              <span>Explore Your Rights</span>
            </Link>

            <Link
              to="/about"
              className="inline-flex items-center justify-center gap-2 bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 font-semibold text-sm px-6 py-3 rounded-xl transition-all duration-200"
            >
              <HelpCircle className="w-4 h-4 text-slate-400" />
              <span>How It Works</span>
            </Link>
          </div>

          {/* Metrics bar */}
          <div className="pt-4 grid grid-cols-2 sm:grid-cols-4 gap-3 border-t border-slate-800/80">
            <div className="bg-slate-800/60 rounded-xl p-3 border border-slate-700/60">
              <p className="text-lg font-bold text-white">9 Supported</p>
              <p className="text-[11px] text-slate-400 font-medium">Legal Domains</p>
            </div>
            <div className="bg-slate-800/60 rounded-xl p-3 border border-slate-700/60">
              <p className="text-lg font-bold text-emerald-400">100% Grounded</p>
              <p className="text-[11px] text-slate-400 font-medium">Indian Legal Acts</p>
            </div>
            <div className="bg-slate-800/60 rounded-xl p-3 border border-slate-700/60">
              <p className="text-lg font-bold text-indigo-300">CPA, IT, RERA</p>
              <p className="text-[11px] text-slate-400 font-medium">Motor & RTI Acts</p>
            </div>
            <div className="bg-slate-800/60 rounded-xl p-3 border border-slate-700/60">
              <p className="text-lg font-bold text-indigo-300">PDF & DOCX</p>
              <p className="text-[11px] text-slate-400 font-medium">Formal Complaint</p>
            </div>
          </div>
        </div>
      </div>

      {/* 3. LEGAL DOMAIN CARDS (9 DOMAINS) */}
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-lg sm:text-xl font-bold text-slate-900 tracking-tight flex items-center gap-2">
              <BookOpenCheck className="w-5 h-5 text-indigo-600" />
              Supported Legal Domains (9 Covered Acts)
            </h2>
            <p className="text-xs text-slate-500">
              Select any domain to ask a question or explore your specific rights
            </p>
          </div>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {domainQuickCards.map((card) => {
            const Icon = card.icon;
            return (
              <div
                key={card.domain}
                onClick={() => setQuestion(card.sampleQuestion)}
                className="group relative bg-white rounded-2xl p-5 border border-slate-200 hover:border-indigo-300 shadow-2xs hover:shadow-md transition-all duration-200 cursor-pointer flex flex-col justify-between h-full"
              >
                <div>
                  <div className="flex items-center justify-between gap-3 mb-3">
                    <div className={`w-9 h-9 rounded-xl ${card.bgColor} flex items-center justify-center flex-shrink-0 transition-transform duration-200 group-hover:scale-105`}>
                      <Icon className="w-4 h-4" />
                    </div>
                    <span className="text-[10px] font-semibold px-2 py-0.5 rounded-md bg-slate-100 text-slate-600 border border-slate-200/80">
                      Indian Act
                    </span>
                  </div>

                  <h3 className="font-bold text-slate-900 text-base group-hover:text-indigo-600 transition-colors">
                    {card.domain}
                  </h3>
                  <p className="text-xs font-semibold text-slate-400 mt-0.5">
                    {card.act}
                  </p>

                  <p className="text-xs text-slate-600 mt-3 line-clamp-2 italic bg-slate-50 p-2.5 rounded-xl border border-slate-100">
                    "{card.sampleQuestion}"
                  </p>
                </div>

                <div className="mt-4 pt-3 border-t border-slate-100 flex items-center justify-between text-xs font-semibold text-indigo-600 group-hover:text-indigo-700">
                  <span>Ask about this domain</span>
                  <ArrowRight className="w-3.5 h-3.5 transform group-hover:translate-x-1 transition-transform duration-200" />
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}