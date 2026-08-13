import { useState } from "react";
import {
  FaEye,
  FaTrash,
  FaDownload,
  FaCalendarAlt,
  FaUser,
  FaBalanceScale,
} from "react-icons/fa";
import toast from "react-hot-toast";

import {
  deleteCase,
  getCase,
  downloadComplaintPDF,
} from "../services/api";

import CaseDetailsModal from "./CaseDetailsModal";

export default function CaseCard({
  caseItem,
  refreshCases,
}) {

  const [loading, setLoading] = useState(false);

  const [selectedCase, setSelectedCase] = useState(null);

  const [openModal, setOpenModal] = useState(false);

  const getBadgeColor = (confidence) => {

    switch (confidence) {

      case "High":
        return "bg-green-100 text-green-700";

      case "Medium":
        return "bg-yellow-100 text-yellow-700";

      default:
        return "bg-red-100 text-red-700";

    }

  };

  // =====================
  // View Case
  // =====================

  const handleView = async () => {

    try {

      setLoading(true);

      const data = await getCase(caseItem.case_id);

      setSelectedCase(data);

      setOpenModal(true);

    } catch (err) {

      console.error(err);

      toast.error("Unable to load case.");

    } finally {

      setLoading(false);

    }

  };

  // =====================
  // Download PDF
  // =====================

  const handleDownload = async () => {

    try {

      const data = await getCase(caseItem.case_id);

      const pdfBlob = await downloadComplaintPDF(
        data.report
      );

      const url = window.URL.createObjectURL(pdfBlob);

      const link = document.createElement("a");

      link.href = url;

      link.download = `${caseItem.case_id}.pdf`;

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

  // =====================
  // Delete
  // =====================

  const handleDelete = async () => {

    const confirmDelete = window.confirm(
      "Delete this saved case?"
    );

    if (!confirmDelete) return;

    try {

      await deleteCase(caseItem.case_id);

      toast.success("Case deleted.");

      refreshCases();

    } catch (err) {

      console.error(err);

      toast.error("Unable to delete case.");

    }

  };

  return (
    <>
      <div className="bg-white rounded-3xl shadow-lg border border-slate-200 p-8">

        <div className="flex justify-between items-start">

          <div>

            <h2 className="text-2xl font-bold text-blue-900">
              {caseItem.case_id}
            </h2>

            <div className="mt-4 space-y-3 text-slate-600">

              <div className="flex items-center gap-3">

                <FaUser />

                {caseItem.citizen_name}

              </div>

              <div className="flex items-center gap-3">

                <FaBalanceScale />

                {caseItem.category}

              </div>

              <div className="flex items-center gap-3">

                <FaCalendarAlt />

                {caseItem.created_at}

              </div>

            </div>

          </div>

          <span
            className={`px-4 py-2 rounded-full font-semibold ${getBadgeColor(
              caseItem.confidence
            )}`}
          >
            {caseItem.confidence}
          </span>

        </div>

        <div className="mt-8 flex flex-wrap gap-4">

          <button
            onClick={handleView}
            disabled={loading}
            className="bg-blue-900 hover:bg-blue-800 text-white px-5 py-3 rounded-xl flex items-center gap-2"
          >

            <FaEye />

            View

          </button>

          <button
            onClick={handleDownload}
            className="bg-emerald-700 hover:bg-emerald-600 text-white px-5 py-3 rounded-xl flex items-center gap-2"
          >

            <FaDownload />

            PDF

          </button>

          <button
            onClick={handleDelete}
            className="bg-red-600 hover:bg-red-500 text-white px-5 py-3 rounded-xl flex items-center gap-2"
          >

            <FaTrash />

            Delete

          </button>

        </div>

      </div>

      <CaseDetailsModal
        open={openModal}
        onClose={() => setOpenModal(false)}
        caseData={selectedCase}
      />
    </>
  );
}