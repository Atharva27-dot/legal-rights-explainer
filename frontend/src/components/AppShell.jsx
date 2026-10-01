import { useState } from "react";
import Navbar from "./Navbar";
import Sidebar from "./Sidebar";
import Footer from "./Footer";

export default function AppShell({ children }) {
  const [isMobileSidebarOpen, setIsMobileSidebarOpen] = useState(false);

  const toggleSidebar = () => {
    setIsMobileSidebarOpen((prev) => !prev);
  };

  const closeSidebar = () => {
    setIsMobileSidebarOpen(false);
  };

  return (
    <div className="min-h-screen bg-slate-50 text-slate-800 flex flex-col font-sans selection:bg-indigo-500 selection:text-white">
      {/* Top Navbar */}
      <Navbar
        onToggleSidebar={toggleSidebar}
        isMobileMenuOpen={isMobileSidebarOpen}
      />

      {/* Main Container */}
      <div className="flex-1 max-w-[1600px] w-full mx-auto px-4 sm:px-6 lg:px-8 py-6 sm:py-8">
        <div className="grid grid-cols-1 lg:grid-cols-[280px_minmax(0,1fr)] gap-6 lg:gap-8 items-start">
          {/* Desktop Sticky Sidebar */}
          <div className="hidden lg:block sticky top-20">
            <Sidebar />
          </div>

          {/* Mobile Overlay Drawer Sidebar */}
          {isMobileSidebarOpen && (
            <div className="fixed inset-0 z-50 lg:hidden flex">
              {/* Backdrop */}
              <div
                className="fixed inset-0 bg-slate-900/60 backdrop-blur-xs transition-opacity"
                onClick={closeSidebar}
              />

              {/* Sidebar Content Panel */}
              <div className="relative w-80 max-w-[80vw] bg-white h-full shadow-2xl z-10 overflow-y-auto">
                <Sidebar onItemClick={closeSidebar} />
              </div>
            </div>
          )}

          {/* Page Content */}
          <main className="min-w-0 flex-1">{children}</main>
        </div>
      </div>

      {/* Footer */}
      <Footer />
    </div>
  );
}
