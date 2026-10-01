import { Scale, ShieldCheck } from "lucide-react";
import { Link } from "react-router-dom";

export default function Footer() {
  return (
    <footer className="mt-10 bg-slate-900 border-t border-slate-800 text-slate-400 text-xs">
      <div className="max-w-[1600px] mx-auto px-4 sm:px-6 lg:px-8 py-7">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-6">
          {/* Col 1: Platform Overview */}
          <div className="md:col-span-2 space-y-2.5">
            <div className="flex items-center gap-2.5">
              <div className="w-8 h-8 rounded-lg bg-indigo-600 flex items-center justify-center text-white shadow-xs">
                <Scale className="w-4 h-4" />
              </div>
              <span className="font-bold text-base text-white tracking-tight">
                Legal Rights Explainer
              </span>
            </div>
            <p className="text-slate-400 text-xs leading-relaxed max-w-xl">
              AI-powered legal assistant for Indian citizens. Powered by Retrieval-Augmented Generation (RAG) over ChromaDB vector database and Ollama LLM.
            </p>
            <div className="flex items-center gap-2 text-[11px] text-indigo-300 bg-indigo-950/60 border border-indigo-800/40 rounded-lg px-2.5 py-1 w-fit">
              <ShieldCheck className="w-3.5 h-3.5 text-indigo-400 flex-shrink-0" />
              <span>Grounded in Official Statutory Gazette Legal Texts</span>
            </div>
          </div>

          {/* Col 2: Navigation Links */}
          <div className="space-y-2">
            <h4 className="text-white font-bold text-xs uppercase tracking-wider">
              Quick Features
            </h4>
            <ul className="space-y-1 text-[11px]">
              <li>
                <Link to="/" className="hover:text-indigo-300 transition">
                  AI Legal Assistant
                </Link>
              </li>
              <li>
                <Link to="/rights" className="hover:text-indigo-300 transition">
                  Interactive Rights Guide
                </Link>
              </li>
              <li>
                <Link to="/complaint" className="hover:text-indigo-300 transition">
                  Complaint Generator & Exports
                </Link>
              </li>
              <li>
                <Link to="/my-cases" className="hover:text-indigo-300 transition">
                  My Saved Cases Repository
                </Link>
              </li>
            </ul>
          </div>

          {/* Col 3: Key Acts */}
          <div className="space-y-2">
            <h4 className="text-white font-bold text-xs uppercase tracking-wider">
              Key Legal Coverage
            </h4>
            <ul className="space-y-1 text-[11px] text-slate-400">
              <li>Consumer Protection Act, 2019</li>
              <li>Information Technology Act, 2000</li>
              <li>Motor Vehicles Act, 1988</li>
              <li>Right to Information Act, 2005</li>
              <li>Bharatiya Nyaya Sanhita, 2023</li>
            </ul>
          </div>
        </div>

        {/* Disclaimer Bar */}
        <div className="pt-4 border-t border-slate-800/80 flex flex-col sm:flex-row items-center justify-between gap-3 text-[11px] text-slate-500">
          <p>
            © {new Date().getFullYear()} Legal Rights Explainer. Built for Indian Citizens.
          </p>
          <p className="text-center sm:text-right text-[11px] text-slate-500 max-w-md">
            <strong>Disclaimer:</strong> Educational RAG system. Legal explanations are generated from retrieved legal documents and should be verified before formal filing.
          </p>
        </div>
      </div>
    </footer>
  );
}
