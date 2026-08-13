import { useState } from "react";

import Navbar from "../components/Navbar";
import Sidebar from "../components/Sidebar";
import ComplaintForm from "../components/ComplaintForm";
import ComplaintPreview from "../components/ComplaintPreview";

export default function ComplaintGenerator() {

  const [caseData, setCaseData] = useState(null);

  return (
    <div className="min-h-screen bg-slate-100">

      <Navbar />

      <main className="max-w-7xl mx-auto py-10 px-6">

        <div className="grid grid-cols-12 gap-8">

          {/* Sidebar */}

          <div className="col-span-3">

            <Sidebar />

          </div>

          {/* Main */}

          <div className="col-span-9 space-y-8">

            <div className="bg-gradient-to-r from-blue-900 via-indigo-700 to-blue-600 rounded-3xl shadow-xl p-10 text-white">

              <h1 className="text-4xl font-bold">
                Complaint Generator
              </h1>

              <p className="mt-3 text-blue-100 text-lg">
                Generate professionally formatted consumer complaints using AI.
              </p>

            </div>

            <ComplaintForm
              setCaseData={setCaseData}
            />

            <ComplaintPreview
              caseData={caseData}
            />

          </div>

        </div>

      </main>

    </div>
  );
}