import { FaTimes, FaDownload, FaCheckCircle } from "react-icons/fa";
import { downloadComplaintPDF } from "../services/api";
import toast from "react-hot-toast";

export default function CaseDetailsModal({
  open,
  onClose,
  caseData,
}) {
  if (!open || !caseData) return null;

  const handleDownload = async () => {
    try {
      const pdfBlob = await downloadComplaintPDF(caseData.report);

      const url = window.URL.createObjectURL(pdfBlob);

      const link = document.createElement("a");

      link.href = url;

      link.download = `${caseData.case_id}.pdf`;

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

  return (
    <div className="fixed inset-0 bg-black/50 z-50 flex justify-center items-center p-6">

      <div className="bg-white rounded-3xl shadow-2xl w-full max-w-5xl max-h-[90vh] overflow-y-auto">

        {/* Header */}

        <div className="bg-gradient-to-r from-blue-900 to-indigo-700 text-white p-6 flex justify-between items-center rounded-t-3xl">

          <div>

            <h2 className="text-3xl font-bold">
              Legal Case Details
            </h2>

            <p className="text-blue-100 mt-2">
              {caseData.case_id}
            </p>

          </div>

          <button
            onClick={onClose}
            className="text-2xl"
          >
            <FaTimes />
          </button>

        </div>

        <div className="p-8 space-y-8">

          {/* Summary */}

          <div className="grid md:grid-cols-2 gap-5">

            <InfoCard
              title="Citizen"
              value={caseData.citizen_name}
            />

            <InfoCard
              title="City"
              value={caseData.city}
            />

            <InfoCard
              title="Category"
              value={caseData.category}
            />

            <InfoCard
              title="Confidence"
              value={caseData.confidence}
            />

          </div>

          {/* Rights */}

          <div>

            <h3 className="text-xl font-bold mb-4">
              Applicable Rights
            </h3>

            <ul className="space-y-2">

              {caseData.report.case_analysis.rights.map((item, index) => (

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

          {/* Complaint */}

          <div>

            <h3 className="text-xl font-bold mb-4">
              Complaint Draft
            </h3>

            <div className="bg-slate-50 rounded-2xl p-6 whitespace-pre-wrap leading-8">

              {caseData.report.complaint}

            </div>

          </div>

        </div>

        {/* Footer */}

        <div className="border-t p-6 flex justify-end gap-4">

          <button
            onClick={handleDownload}
            className="bg-blue-900 text-white rounded-xl px-6 py-3 hover:bg-blue-800 flex items-center gap-2"
          >

            <FaDownload />

            Download PDF

          </button>

          <button
            onClick={onClose}
            className="border rounded-xl px-6 py-3 hover:bg-slate-100"
          >

            Close

          </button>

        </div>

      </div>

    </div>
  );
}

function InfoCard({ title, value }) {
  return (
    <div className="bg-slate-50 border rounded-2xl p-5">

      <h3 className="text-slate-500 text-sm">
        {title}
      </h3>

      <p className="mt-2 text-lg font-bold">
        {value}
      </p>

    </div>
  );
}