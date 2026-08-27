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

            {caseData?.evidence_consistency && (
              <div className="bg-white rounded-3xl shadow-lg border border-slate-200 overflow-hidden">
                <div className="px-6 py-5 border-b border-slate-200">
                  <div className="flex items-center justify-between gap-4">
                    <div>
                      <h2 className="text-2xl font-bold text-slate-900">
                        Evidence Consistency Check
                      </h2>
                      <p className="mt-1 text-sm text-slate-600">
                        Compares the information you provided with the uploaded evidence.
                      </p>
                    </div>

                    <span
                      className={`px-4 py-2 rounded-full text-sm font-semibold ${
                        caseData.evidence_consistency.overall_status === "MISMATCH"
                          ? "bg-red-100 text-red-700"
                          : caseData.evidence_consistency.overall_status === "CONSISTENT"
                            ? "bg-green-100 text-green-700"
                            : "bg-amber-100 text-amber-700"
                      }`}
                    >
                      {caseData.evidence_consistency.overall_status}
                    </span>
                  </div>
                </div>

                <div className="p-6">
                  <div className="mb-5 rounded-2xl bg-slate-50 p-4">
                    <p className="font-medium text-slate-800">
                      {caseData.evidence_consistency.summary}
                    </p>

                    {caseData.evidence_consistency.overall_status === "MISMATCH" && (
                      <p className="mt-2 text-sm text-red-700">
                        Please verify these discrepancies before using the complaint draft.
                      </p>
                    )}
                  </div>

                  <div className="space-y-3">
                    {caseData.evidence_consistency.checks?.map((check) => (
                      <div
                        key={check.field}
                        className="rounded-2xl border border-slate-200 p-4"
                      >
                        <div className="flex items-start justify-between gap-4">
                          <div>
                            <h3 className="font-semibold text-slate-900">
                              {check.label}
                            </h3>

                            <div className="mt-2 grid gap-1 text-sm">
                              <p>
                                <span className="font-medium text-slate-600">
                                  Your information:
                                </span>{" "}
                                {check.user_value || "Not provided"}
                              </p>

                              <p>
                                <span className="font-medium text-slate-600">
                                  Evidence:
                                </span>{" "}
                                {check.evidence_value || "Not found"}
                              </p>
                            </div>
                          </div>

                          <span
                            className={`shrink-0 px-3 py-1 rounded-full text-xs font-semibold ${
                              check.status === "MISMATCH"
                                ? "bg-red-100 text-red-700"
                                : check.status === "MATCH"
                                  ? "bg-green-100 text-green-700"
                                  : "bg-amber-100 text-amber-700"
                            }`}
                          >
                            {check.status.replaceAll("_", " ")}
                          </span>
                        </div>

                        <p className="mt-3 text-xs text-slate-500">
                          {check.message}
                        </p>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            )}

            <ComplaintPreview
              caseData={caseData}
            />

          </div>

        </div>

      </main>

    </div>
  );
}