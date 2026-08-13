import { NavLink } from "react-router-dom";
import {
  FaHome,
  FaFileAlt,
  FaBalanceScale,
  FaFolderOpen,
  FaInfoCircle,
  FaChevronRight,
} from "react-icons/fa";

const menu = [
  {
    title: "Legal Assistant",
    icon: <FaHome />,
    path: "/",
  },
  {
    title: "Complaint Generator",
    icon: <FaFileAlt />,
    path: "/complaint",
  },
  {
    title: "My Legal Cases",
    icon: <FaFolderOpen />,
    path: "/my-cases",
  },
  {
    title: "Rights Guide",
    icon: <FaBalanceScale />,
    path: "/rights",
  },
  {
    title: "About",
    icon: <FaInfoCircle />,
    path: "/about",
  },
];

export default function Sidebar() {
  return (
    <aside className="bg-white rounded-3xl shadow-xl border border-slate-200 h-fit overflow-hidden">

      {/* Header */}

      <div className="bg-gradient-to-r from-blue-900 to-indigo-700 p-6 text-white">

        <h2 className="text-xl font-bold">
          Dashboard
        </h2>

        <p className="text-blue-100 text-sm mt-2">
          Navigate through the Legal Rights Explainer platform.
        </p>

      </div>

      {/* Navigation */}

      <nav className="p-4 space-y-2">

        {menu.map((item) => (

          <NavLink
            key={item.path}
            to={item.path}
            className={({ isActive }) =>
              `flex items-center justify-between rounded-xl px-4 py-3 transition-all duration-200
              ${
                isActive
                  ? "bg-blue-900 text-white shadow-lg"
                  : "text-slate-700 hover:bg-slate-100"
              }`
            }
          >

            <div className="flex items-center gap-3">

              <span className="text-lg">
                {item.icon}
              </span>

              <span className="font-medium">
                {item.title}
              </span>

            </div>

            <FaChevronRight className="text-sm opacity-70" />

          </NavLink>

        ))}

      </nav>

      {/* Footer */}

      <div className="border-t border-slate-200 px-5 py-4 bg-slate-50">

        <p className="text-xs text-slate-500">
          Version 1.0
        </p>

        <p className="text-sm font-semibold text-slate-700 mt-1">
          AI Legal Platform
        </p>

      </div>

    </aside>
  );
}