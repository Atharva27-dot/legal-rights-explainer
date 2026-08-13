import { FaBalanceScale, FaCircle } from "react-icons/fa";

export default function Navbar() {
  return (
    <header className="sticky top-0 z-50 bg-white/90 backdrop-blur-md border-b border-slate-200 shadow-sm">
      <div className="max-w-7xl mx-auto px-8 py-4 flex items-center justify-between">

        {/* Logo + Title */}
        <div className="flex items-center gap-4">

          <div className="w-12 h-12 rounded-2xl bg-gradient-to-br from-blue-800 to-indigo-600 flex items-center justify-center shadow-lg">

            <FaBalanceScale className="text-white text-xl" />

          </div>

          <div>

            <h1 className="text-2xl font-bold text-slate-800">
              Legal Rights Explainer
            </h1>

            <p className="text-sm text-slate-500">
              AI powered legal assistance for Indian citizens
            </p>

          </div>

        </div>

        {/* Status */}
        <div className="flex items-center gap-3 bg-green-50 border border-green-200 rounded-full px-4 py-2">

          <FaCircle className="text-green-500 text-xs animate-pulse" />

          <span className="text-sm font-medium text-green-700">
            AI Online
          </span>

        </div>

      </div>
    </header>
  );
}