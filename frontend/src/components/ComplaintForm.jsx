import { useState } from "react";
import {
  FaFileAlt,
  FaShoppingCart,
  FaStore,
  FaCalendarAlt,
  FaPen,
  FaUser,
  FaMapMarkerAlt,
} from "react-icons/fa";

import { generateComplaint } from "../services/api";

export default function ComplaintForm({ setCaseData }) {
  const [loading, setLoading] = useState(false);

  const [formData, setFormData] = useState({
    name: "",
    city: "",
    product: "",
    seller: "",
    purchase_date: "",
    problem: "",
    remedy: "Refund",
  });

  const handleChange = (e) => {
    const { name, value } = e.target;

    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSubmit = async () => {
    if (
      !formData.name ||
      !formData.city ||
      !formData.product ||
      !formData.seller ||
      !formData.purchase_date ||
      !formData.problem
    ) {
      alert("Please fill all required fields.");
      return;
    }

    if (formData.problem.trim().length < 20) {
      alert("Problem description must contain at least 20 characters.");
      return;
    }

    try {
      setLoading(true);

      const response = await generateComplaint(formData);

      // ⭐ Store BOTH form data and AI report
      setCaseData({
        formData,
        report: response,
      });

    } catch (error) {
      console.error(error);

      alert(
        error.response?.data?.detail ||
        "Failed to generate complaint."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-white rounded-3xl shadow-xl border border-slate-200 overflow-hidden">

      {/* Header */}

      <div className="bg-gradient-to-r from-blue-900 to-indigo-700 text-white px-8 py-5">

        <div className="flex items-center gap-3">

          <FaFileAlt className="text-2xl" />

          <div>

            <h2 className="text-2xl font-bold">
              Complaint Details
            </h2>

            <p className="text-blue-100 text-sm">
              Fill all details before generating your complaint.
            </p>

          </div>

        </div>

      </div>

      <div className="p-8 space-y-6">

        {/* Name */}

        <div>

          <label className="font-semibold flex items-center gap-2 mb-2">

            <FaUser />

            Your Name

          </label>

          <input
            type="text"
            name="name"
            value={formData.name}
            onChange={handleChange}
            placeholder="Enter your name"
            className="w-full border rounded-xl p-4"
          />

        </div>

        {/* City */}

        <div>

          <label className="font-semibold flex items-center gap-2 mb-2">

            <FaMapMarkerAlt />

            City

          </label>

          <input
            type="text"
            name="city"
            value={formData.city}
            onChange={handleChange}
            placeholder="Example: Pune"
            className="w-full border rounded-xl p-4"
          />

        </div>

        {/* Product */}

        <div>

          <label className="font-semibold flex items-center gap-2 mb-2">

            <FaShoppingCart />

            Product / Service

          </label>

          <input
            type="text"
            name="product"
            value={formData.product}
            onChange={handleChange}
            placeholder="Example: Mobile Phone"
            className="w-full border rounded-xl p-4"
          />

        </div>

        {/* Seller */}

        <div>

          <label className="font-semibold flex items-center gap-2 mb-2">

            <FaStore />

            Seller / Company

          </label>

          <input
            type="text"
            name="seller"
            value={formData.seller}
            onChange={handleChange}
            placeholder="Example: Amazon"
            className="w-full border rounded-xl p-4"
          />

        </div>

        {/* Purchase Date */}

        <div>

          <label className="font-semibold flex items-center gap-2 mb-2">

            <FaCalendarAlt />

            Purchase Date

          </label>

          <input
            type="date"
            name="purchase_date"
            value={formData.purchase_date}
            onChange={handleChange}
            className="w-full border rounded-xl p-4"
          />

        </div>

        {/* Problem */}

        <div>

          <label className="font-semibold flex items-center gap-2 mb-2">

            <FaPen />

            Describe Your Problem

          </label>

          <textarea
            rows="6"
            name="problem"
            value={formData.problem}
            onChange={handleChange}
            placeholder="Describe your issue in detail..."
            className="w-full border rounded-xl p-4 resize-none"
          />

          <p className="text-sm text-slate-500 mt-2">
            Minimum 20 characters required.
          </p>

        </div>

        {/* Remedy */}

        <div>

          <label className="font-semibold mb-4 block">

            Desired Remedy

          </label>

          <select
            name="remedy"
            value={formData.remedy}
            onChange={handleChange}
            className="w-full border rounded-xl p-4"
          >

            <option value="Refund">Refund</option>

            <option value="Replacement">Replacement</option>

            <option value="Compensation">Compensation</option>

          </select>

        </div>

        {/* Button */}

        <button
          onClick={handleSubmit}
          disabled={loading}
          className="w-full bg-gradient-to-r from-blue-900 to-indigo-700 hover:from-blue-800 hover:to-indigo-600 text-white py-4 rounded-xl font-semibold shadow-lg disabled:opacity-60"
        >

          {loading
            ? "Generating Complaint..."
            : "Generate Complaint"}

        </button>

      </div>

    </div>
  );
}