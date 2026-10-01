import { useState } from "react";
import { Link, useLocation } from "react-router-dom";
import {
  Scale,
  ShieldCheck,
  Menu,
  X,
  Sparkles,
  Search,
  BookOpen,
  FileText,
  FolderKanban,
  Info
} from "lucide-react";

export default function Navbar({ onToggleSidebar, isMobileMenuOpen }) {
  const location = useLocation();

  return (
    <header className="sticky top-0 z-40 bg-slate-900/95 backdrop-blur-md border-b border-slate-800 text-white shadow-md">
      <div className="max-w-[1600px] mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Left: Mobile Toggle & Brand Logo */}
          <div className="flex items-center gap-3 sm:gap-4">
            {/* Mobile Hamburger Button */}
            <button
              type="button"
              onClick={onToggleSidebar}
              className="lg:hidden p-2 rounded-xl text-slate-300 hover:text-white hover:bg-slate-800 transition"
              aria-label="Toggle navigation menu"
            >
              {isMobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
            </button>

            {/* Brand Logo */}
            <Link to="/" className="flex items-center gap-3 group">
              <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-indigo-500 via-indigo-600 to-blue-700 flex items-center justify-center shadow-lg shadow-indigo-500/20 group-hover:scale-105 transition-transform duration-200">
                <Scale className="w-5 h-5 text-white" />
              </div>
              <div>
                <div className="flex items-center gap-2">
                  <span className="font-bold text-lg text-white tracking-tight">
                    Legal Rights Explainer
                  </span>
                  <span className="hidden sm:inline-flex items-center px-2 py-0.5 rounded-md text-[10px] font-semibold bg-indigo-500/20 text-indigo-300 border border-indigo-500/30">
                    INDIA RAG
                  </span>
                </div>
                <p className="text-xs text-slate-400 font-medium hidden sm:block">
                  AI-Powered Citizen Legal Assistant
                </p>
              </div>
            </Link>
          </div>

          {/* Center: Desktop Navigation Quick Pills */}
          <nav className="hidden md:flex items-center gap-1 bg-slate-800/60 p-1 rounded-xl border border-slate-700/60">
            <Link
              to="/"
              className={`flex items-center gap-2 px-3.5 py-1.5 rounded-lg text-xs font-semibold transition ${
                location.pathname === "/"
                  ? "bg-indigo-600 text-white shadow-sm"
                  : "text-slate-300 hover:text-white hover:bg-slate-700/50"
              }`}
            >
              <Sparkles className="w-3.5 h-3.5 text-indigo-300" />
              Legal Assistant
            </Link>
            <Link
              to="/rights"
              className={`flex items-center gap-2 px-3.5 py-1.5 rounded-lg text-xs font-semibold transition ${
                location.pathname === "/rights"
                  ? "bg-indigo-600 text-white shadow-sm"
                  : "text-slate-300 hover:text-white hover:bg-slate-700/50"
              }`}
            >
              <BookOpen className="w-3.5 h-3.5 text-indigo-300" />
              Rights Guide
            </Link>
            <Link
              to="/complaint"
              className={`flex items-center gap-2 px-3.5 py-1.5 rounded-lg text-xs font-semibold transition ${
                location.pathname === "/complaint"
                  ? "bg-indigo-600 text-white shadow-sm"
                  : "text-slate-300 hover:text-white hover:bg-slate-700/50"
              }`}
            >
              <FileText className="w-3.5 h-3.5 text-indigo-300" />
              Complaint Generator
            </Link>
            <Link
              to="/my-cases"
              className={`flex items-center gap-2 px-3.5 py-1.5 rounded-lg text-xs font-semibold transition ${
                location.pathname === "/my-cases"
                  ? "bg-indigo-600 text-white shadow-sm"
                  : "text-slate-300 hover:text-white hover:bg-slate-700/50"
              }`}
            >
              <FolderKanban className="w-3.5 h-3.5 text-indigo-300" />
              My Cases
            </Link>
          </nav>

          {/* Right: AI Engine Status Indicator */}
          <div className="flex items-center gap-3">
            <div className="flex items-center gap-2 bg-emerald-950/80 border border-emerald-500/30 rounded-full px-3 py-1.5">
              <span className="relative flex h-2 w-2">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
                <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
              </span>
              <ShieldCheck className="w-3.5 h-3.5 text-emerald-400" />
              <span className="text-xs font-semibold text-emerald-300">
                AI Active
              </span>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
}