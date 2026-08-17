import { useState } from "react";
import {
  FaCopy,
  FaDownload,
  FaSave,
  FaCheckCircle,
} from "react-icons/fa";
import SourceCard from "./SourceCard";
import toast from "react-hot-toast";

import {
  downloadComplaintPDF,
  saveCase,
} from "../services/api";

export default function ComplaintPreview({ caseData }) {
  const [saving, setSaving] = useState(false);
  const [saved, setSaved] = useState(false);
  const [caseId, setCaseId] = useState("");

  if (!caseData) {
    return (
      <div className="bg-white rounded-3xl shadow-xl border border-slate-200 p-12 text-center">
        <h2 className="text-2xl font-bold text-slate-700">
          Complaint Preview
        </h2>

        <p className="text-slate-500 mt-4">
          Generate a complaint to preview it here.
        </p>
      </div>
    );
  }

  const { formData, report } = caseData;
  const readiness = report.readiness;

  // ==========================
  // Copy
  // ==========================

  const handleCopy = async () => {
    await navigator.clipboard.writeText(report.complaint);

    toast.success("Complaint copied.");
  };

  // ==========================
  // PDF
  // ==========================

  const handleDownload = async () => {
    try {
      const pdfBlob = await downloadComplaintPDF(report);

      const url = window.URL.createObjectURL(pdfBlob);

      const link = document.createElement("a");

      link.href = url;

      link.download = "Legal_Report.pdf";

      document.body.appendChild(link);

      link.click();

      document.body.removeChild(link);

      window.URL.revokeObjectURL(url);

      toast.success("PDF downloaded.");

    } catch (err) {

      console.error(err);

      toast.error("Unable to download PDF.");
    }
  };

  // ==========================
  // Save Case
  // ==========================

  const handleSave = async () => {

    if (saved) return;

    try {

      setSaving(true);

      const response = await saveCase({

        citizen_name: formData.name,

        city: formData.city,

        report: report,

      });

      setSaved(true);

      setCaseId(response.case_id);

      toast.success("Case saved successfully.");

    } catch (err) {

      console.error(err);

      toast.error("Unable to save case.");

    } finally {

      setSaving(false);

    }

  };

  return (
    <div className="bg-white rounded-3xl shadow-xl border border-slate-200 overflow-hidden">

      {/* Header */}

      <div className="bg-gradient-to-r from-emerald-700 to-teal-600 text-white px-8 py-6">

        <h2 className="text-3xl font-bold">
          AI Generated Legal Report
        </h2>

        <p className="text-emerald-100 mt-2">
          Review your complaint before downloading or saving.
        </p>

      </div>

      {/* Summary */}

      <div className="bg-blue-50 border border-blue-200 rounded-2xl p-5">

    <h3 className="text-blue-900 font-bold">

        Legal Readiness

    </h3>

    <div className="text-4xl font-bold mt-3">

        {readiness.score}%

    </div>

    <div className="mt-2 text-lg font-semibold">

        {readiness.status}

    </div>

</div>

      {/* Rights */}

      <div className="p-8 border-b">

        <h3 className="font-bold text-xl mb-4">
          Applicable Rights
        </h3>

        <ul className="space-y-3">

          {report.case_analysis.rights.map((item, index) => (

            <li
              key={index}
              className="flex items-center gap-3"
            >

              <FaCheckCircle className="text-green-600" />

              {item}

            </li>

          ))}

        </ul>

      </div>
      <div className="p-8 border-b">

    <h3 className="text-xl font-bold mb-4">

        Recommendations

    </h3>

    <ul className="space-y-2">

        {readiness.recommendations.map((item, index) => (

            <li
                key={index}
                className="flex gap-3"
            >

                ✅ {item}

            </li>

        ))}

    </ul>

</div>

      {/* Complaint */}

      <div className="p-8">

        <h3 className="font-bold text-xl mb-5">
          Complaint Draft
        </h3>

        <div className="whitespace-pre-wrap leading-9 text-slate-700">

          {report.complaint}

        </div>

      </div>
            {/* Legal Sources */}

      <SourceCard
        sources={report.sources}
      />

      {/* Case ID */}

      {saved && (

        <div className="px-8 pb-4">

          <div className="bg-green-50 border border-green-300 rounded-xl p-4">

            <p className="text-green-800 font-semibold">

              ✅ Case Saved Successfully

            </p>

            <p className="mt-2">

              Case ID:

              <strong className="ml-2">

                {caseId}

              </strong>

            </p>

          </div>

        </div>

      )}

      {/* Buttons */}

      <div className="border-t bg-slate-50 p-6 flex flex-wrap justify-end gap-4">

        <button
          onClick={handleCopy}
          className="border rounded-xl px-5 py-3 flex items-center gap-2 hover:bg-slate-100"
        >

          <FaCopy />

          Copy

        </button>

        <button
          onClick={handleSave}
          disabled={saving || saved}
          className="bg-emerald-700 text-white rounded-xl px-5 py-3 flex items-center gap-2 hover:bg-emerald-600 disabled:opacity-50"
        >

          <FaSave />

          {saved
            ? "Saved"
            : saving
            ? "Saving..."
            : "Save Case"}

        </button>

        <button
          onClick={handleDownload}
          className="bg-blue-900 text-white rounded-xl px-5 py-3 flex items-center gap-2 hover:bg-blue-800"
        >

          <FaDownload />

          Download PDF

        </button>

      </div>

    </div>
  );
}

function InfoCard({ title, value }) {

  return (

    <div className="bg-slate-50 border rounded-2xl p-5">

      <h4 className="text-slate-500 text-sm">

        {title}

      </h4>

      <p className="mt-2 text-lg font-bold">

        {value}

      </p>

    </div>

  );

}