import { NavLink } from "react-router-dom";
import {
  Sparkles,
  BookOpen,
  FileText,
  FolderKanban,
  BookmarkCheck,
  Info,
  ChevronRight,
  ShieldCheck,
  Scale
} from "lucide-react";

const mainMenuItems = [
  {
    title: "Legal Assistant",
    subtitle: "Plain-language RAG query",
    icon: Sparkles,
    path: "/",
    badge: "AI Quick Ask",
  },
  {
    title: "Rights Guide",
    subtitle: "Step-by-step rights breakdown",
    icon: BookOpen,
    path: "/rights",
    badge: "9 Domains",
  },
  {
    title: "Complaint Generator",
    subtitle: "Draft formal legal complaints",
    icon: FileText,
    path: "/complaint",
    badge: "PDF / DOCX",
  },
  {
    title: "My Legal Cases",
    subtitle: "Saved complaints & history",
    icon: FolderKanban,
    path: "/my-cases",
  },
  {
    title: "Saved Reports",
    subtitle: "Generated RAG reports",
    icon: BookmarkCheck,
    path: "/reports",
  },
];

const infoMenuItems = [
  {
    title: "About & Coverage",
    subtitle: "Supported acts & methodology",
    icon: Info,
    path: "/about",
  },
];

const domainList = [
  "Consumer Protection 2019",
  "Cyber / IT Act 2000",
  "Motor Vehicles Act 1988",
  "Right to Information 2005",
  "RERA Real Estate 2016",
  "Domestic Violence PWDVA",
  "Legal Services Act 1987",
  "Contract Act 1872",
  "Bharatiya Nyaya Sanhita 2023",
];

export default function Sidebar({ onItemClick }) {
  const renderNavItem = (item) => {
    const Icon = item.icon;
    return (
      <NavLink
        key={item.path}
        to={item.path}
        onClick={onItemClick}
        className={({ isActive }) =>
          `group flex items-center justify-between p-2.5 sm:p-3 rounded-xl transition-all duration-200 ${
            isActive
              ? "bg-indigo-50 text-indigo-950 border border-indigo-200/80 shadow-xs font-semibold"
              : "text-slate-700 hover:bg-slate-50 hover:text-slate-900"
          }`
        }
      >
        {({ isActive }) => (
          <>
            <div className="flex items-center gap-3 min-w-0">
              <div
                className={`p-2 rounded-lg transition-colors flex-shrink-0 ${
                  isActive
                    ? "bg-indigo-700 text-white shadow-xs"
                    : "bg-slate-100 text-slate-500 group-hover:bg-slate-200 group-hover:text-slate-700"
                }`}
              >
                <Icon className="w-4 h-4" />
              </div>
              <div className="min-w-0 flex-1">
                <div className="flex items-center gap-2">
                  <span className="font-semibold text-xs sm:text-sm truncate leading-tight">
                    {item.title}
                  </span>
                  {item.badge && (
                    <span
                      className={`text-[10px] font-bold px-1.5 py-0.5 rounded-md ${
                        isActive
                          ? "bg-indigo-100 text-indigo-800"
                          : "bg-slate-100 text-slate-500"
                      }`}
                    >
                      {item.badge}
                    </span>
                  )}
                </div>
                <p className="text-[11px] text-slate-400 truncate mt-0.5">
                  {item.subtitle}
                </p>
              </div>
            </div>
            <ChevronRight
              className={`w-4 h-4 flex-shrink-0 transition-transform duration-200 ${
                isActive
                  ? "text-indigo-600 translate-x-0.5"
                  : "text-slate-300 group-hover:text-slate-400"
              }`}
            />
          </>
        )}
      </NavLink>
    );
  };

  return (
    <aside className="bg-white rounded-2xl border border-slate-200/80 shadow-xs overflow-hidden flex flex-col h-full">
      {/* Header Banner */}
      <div className="bg-slate-900 p-4 sm:p-5 text-white">
        <div className="flex items-center gap-3">
          <div className="p-2 rounded-xl bg-indigo-600/30 border border-indigo-500/30 text-indigo-300">
            <Scale className="w-5 h-5" />
          </div>
          <div>
            <h2 className="font-bold text-sm sm:text-base tracking-tight text-white">
              Navigation
            </h2>
            <p className="text-[11px] text-slate-400">
              Indian Citizen AI Legal Assistant
            </p>
          </div>
        </div>
      </div>

      {/* Navigation Sections */}
      <div className="p-3 space-y-4 flex-1 overflow-y-auto">
        {/* MAIN Section */}
        <div className="space-y-1">
          <p className="px-3 text-[10px] font-bold tracking-wider uppercase text-slate-400 mb-1.5">
            MAIN
          </p>
          {mainMenuItems.map(renderNavItem)}
        </div>

        {/* INFORMATION Section */}
        <div className="space-y-1 pt-2 border-t border-slate-100">
          <p className="px-3 text-[10px] font-bold tracking-wider uppercase text-slate-400 mb-1.5">
            INFORMATION
          </p>
          {infoMenuItems.map(renderNavItem)}
        </div>
      </div>

      {/* Visually Compact Covered Legal Acts Section */}
      <div className="p-3.5 border-t border-slate-100 bg-slate-50/70">
        <div className="flex items-center gap-1.5 text-[11px] font-bold text-slate-700 mb-2">
          <ShieldCheck className="w-3.5 h-3.5 text-indigo-600" />
          <span>Covered Indian Legal Acts</span>
        </div>
        <div className="flex flex-wrap gap-1">
          {domainList.map((act) => (
            <span
              key={act}
              className="text-[10px] bg-white border border-slate-200/90 text-slate-600 font-medium px-2 py-0.5 rounded-md shadow-2xs"
            >
              {act}
            </span>
          ))}
        </div>
      </div>

      {/* Footer System Info */}
      <div className="p-2.5 border-t border-slate-200/80 bg-slate-100/60 text-center">
        <p className="text-[10px] font-medium text-slate-500">
          Grounded ChromaDB RAG + Ollama Engine
        </p>
      </div>
    </aside>
  );
}