import { useState } from "react";
import {
  FaFileAlt,
  FaShoppingCart,
  FaStore,
  FaCalendarAlt,
  FaPen,
  FaUser,
  FaMapMarkerAlt,
  FaBalanceScale,
  FaUniversity,
  FaMoneyBillWave,
} from "react-icons/fa";

import { generateComplaint } from "../services/api";
import EvidenceUploader from "./EvidenceUploader";

export default function ComplaintForm({ setCaseData }) {
  const [loading, setLoading] = useState(false);
  const [evidence, setEvidence] = useState([]);
  const [complaintGenerated, setComplaintGenerated] = useState(false);

  const [formData, setFormData] = useState({
    name: "",
    city: "",

    // Legal classification
    domain: "",
    issue_type: "",

    // Consumer fields
    product: "",
    seller: "",
    purchase_date: "",

    // Cyber fields
    bank: "",
    transaction_date: "",
    amount: "",

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

  const isCyber =
    formData.domain === "Cyber / IT";

  const isConsumer =
    formData.domain === "Consumer Protection";

  const isEmployment =
    formData.domain === "Employment / Labour";

  const isContract =
    formData.domain === "Contract / Service";

  const handleSubmit = async () => {
    if (!formData.name) {
      alert("Please enter your name.");
      return;
    }

    if (!formData.city) {
      alert("Please enter your city.");
      return;
    }

    if (!formData.domain) {
      alert("Please select a legal domain.");
      return;
    }

    if (!formData.issue_type) {
      alert("Please select the specific issue.");
      return;
    }

    // Consumer validation
    if (isConsumer) {
      if (!formData.product) {
        alert("Please enter the product or service.");
        return;
      }

      if (!formData.seller) {
        alert("Please enter the seller or company.");
        return;
      }

      if (!formData.purchase_date) {
        alert("Please enter the purchase date.");
        return;
      }
    }

    // Cyber validation
    if (isCyber) {
      if (!formData.bank) {
        alert("Please enter the bank or payment platform.");
        return;
      }

      if (!formData.transaction_date) {
        alert("Please enter the transaction date.");
        return;
      }

      if (!formData.amount) {
        alert("Please enter the amount involved.");
        return;
      }
    }

    // General problem validation
    if (!formData.problem) {
      alert("Please describe your problem.");
      return;
    }

    if (formData.problem.trim().length < 20) {
      alert("Problem description must contain at least 20 characters.");
      return;
    }

    try {
      setLoading(true);

      /*
       * Keep compatibility with the existing backend fields.
       *
       * For Cyber / IT:
       * product       = issue type
       * seller        = bank/payment platform
       * purchase_date = transaction date
       *
       * The original values are also preserved in the request.
       */

     const requestData = {
  ...formData,

  ...(isCyber && {
    product: formData.issue_type,
    seller: formData.bank,
    purchase_date: formData.transaction_date,
  }),

  evidence: evidence.map((item) => ({
    file_id: item.fileId,
    filename: item.name,
    extraction_status: item.extractionStatus,
    extracted_text: item.extractedText,
  })),
};

      const response = await generateComplaint(requestData);

      setCaseData({
        formData: requestData,
        report: response,
        evidence_consistency: response.evidence_consistency || null,
      });

      setComplaintGenerated(true);

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

      {/* =====================================================
          HEADER
      ====================================================== */}

      <div className="bg-gradient-to-r from-blue-900 to-indigo-700 text-white px-8 py-5">

        <div className="flex items-center gap-3">

          <FaFileAlt className="text-2xl" />

          <div>

            <h2 className="text-2xl font-bold">
              Complaint Details
            </h2>

            <p className="text-blue-100 text-sm">
              Select your legal issue and provide the relevant details.
            </p>

          </div>

        </div>

      </div>

      <div className="p-8 space-y-6">

        {/* =====================================================
            NAME
        ====================================================== */}

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

        {/* =====================================================
            CITY
        ====================================================== */}

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

        {/* =====================================================
            LEGAL DOMAIN
        ====================================================== */}

        <div>

          <label className="font-semibold flex items-center gap-2 mb-2">

            <FaBalanceScale />

            Legal Domain

          </label>

          <select
            name="domain"
            value={formData.domain}
            onChange={(e) => {

              const selectedDomain = e.target.value;

              setFormData((prev) => ({
                ...prev,

                domain: selectedDomain,

                issue_type: "",

                product: "",
                seller: "",
                purchase_date: "",

                bank: "",
                transaction_date: "",
                amount: "",
              }));

            }}
            className="w-full border rounded-xl p-4"
          >

            <option value="">
              Select your legal issue
            </option>

            <option value="Consumer Protection">
              Consumer Protection
            </option>

            <option value="Cyber / IT">
              Cyber / IT
            </option>

            <option value="Employment / Labour">
              Employment / Labour
            </option>

            <option value="Contract / Service">
              Contract / Service
            </option>

            <option value="Motor Vehicle / Road Accident">
              Motor Vehicle / Road Accident
            </option>

            <option value="Other">
              Other
            </option>

          </select>

        </div>

        {/* =====================================================
            ISSUE TYPE
        ====================================================== */}

        {formData.domain && (

          <div>

            <label className="font-semibold flex items-center gap-2 mb-2">

              <FaBalanceScale />

              Specific Issue

            </label>

            <select
              name="issue_type"
              value={formData.issue_type}
              onChange={handleChange}
              className="w-full border rounded-xl p-4"
            >

              <option value="">
                Select the specific issue
              </option>

              {/* CONSUMER */}

              {isConsumer && (
                <>
                  <option value="Defective Product">
                    Defective Product
                  </option>

                  <option value="Wrong Product Delivered">
                    Wrong Product Delivered
                  </option>

                  <option value="Refund Not Received">
                    Refund Not Received
                  </option>

                  <option value="Product Warranty Issue">
                    Product Warranty Issue
                  </option>

                  <option value="Online Shopping Dispute">
                    Online Shopping Dispute
                  </option>

                  <option value="Service Deficiency">
                    Service Deficiency
                  </option>
                </>
              )}

              {/* CYBER */}

              {isCyber && (
                <>
                  <option value="UPI Fraud">
                    UPI / Online Payment Fraud
                  </option>

                  <option value="Online Banking Fraud">
                    Online Banking Fraud
                  </option>

                  <option value="Phishing">
                    Phishing / Fake Link
                  </option>

                  <option value="Account Hacking">
                    Account Hacking
                  </option>

                  <option value="Identity Theft">
                    Identity Theft
                  </option>

                  <option value="Unauthorized Transaction">
                    Unauthorized Transaction
                  </option>

                  <option value="Other Cyber Crime">
                    Other Cyber Crime
                  </option>
                </>
              )}

              {/* EMPLOYMENT */}

              {isEmployment && (
                <>
                  <option value="Unpaid Salary">
                    Unpaid Salary
                  </option>

                  <option value="Wrongful Termination">
                    Wrongful Termination
                  </option>

                  <option value="Workplace Harassment">
                    Workplace Harassment
                  </option>

                  <option value="Employment Dispute">
                    Employment Dispute
                  </option>
                </>
              )}

              {/* CONTRACT */}

              {isContract && (
                <>
                  <option value="Breach of Contract">
                    Breach of Contract
                  </option>

                  <option value="Non Payment">
                    Non-Payment
                  </option>

                  <option value="Contractual Dispute">
                    Contractual Dispute
                  </option>

                  <option value="Service Agreement Dispute">
                    Service Agreement Dispute
                  </option>
                </>
              )}

              {/* MOTOR VEHICLE */}

              {formData.domain ===
                "Motor Vehicle / Road Accident" && (
                <>
                  <option value="Road Accident">
                    Road Accident
                  </option>

                  <option value="Vehicle Damage">
                    Vehicle Damage
                  </option>

                  <option value="Insurance Claim">
                    Insurance Claim
                  </option>

                  <option value="Traffic Dispute">
                    Traffic Dispute
                  </option>
                </>
              )}

              {/* OTHER */}

              {formData.domain === "Other" && (
                <>
                  <option value="General Legal Issue">
                    General Legal Issue
                  </option>
                </>
              )}

            </select>

          </div>

        )}

        {/* =====================================================
            CONSUMER FIELDS
        ====================================================== */}

        {isConsumer && (

          <>
            {/* PRODUCT */}

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

            {/* SELLER */}

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

            {/* PURCHASE DATE */}

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
          </>

        )}

        {/* =====================================================
            CYBER / IT FIELDS
        ====================================================== */}

        {isCyber && (

          <>

            {/* BANK / PLATFORM */}

            <div>

              <label className="font-semibold flex items-center gap-2 mb-2">

                <FaUniversity />

                Bank / Payment Platform

              </label>

              <input
                type="text"
                name="bank"
                value={formData.bank}
                onChange={handleChange}
                placeholder="Example: SBI, HDFC, Google Pay, PhonePe"
                className="w-full border rounded-xl p-4"
              />

            </div>

            {/* TRANSACTION DATE */}

            <div>

              <label className="font-semibold flex items-center gap-2 mb-2">

                <FaCalendarAlt />

                Transaction Date

              </label>

              <input
                type="date"
                name="transaction_date"
                value={formData.transaction_date}
                onChange={handleChange}
                className="w-full border rounded-xl p-4"
              />

            </div>

            {/* AMOUNT */}

            <div>

              <label className="font-semibold flex items-center gap-2 mb-2">

                <FaMoneyBillWave />

                Amount Involved

              </label>

              <input
                type="number"
                name="amount"
                value={formData.amount}
                onChange={handleChange}
                placeholder="Example: 20000"
                min="0"
                className="w-full border rounded-xl p-4"
              />

            </div>

          </>

        )}

        {/* =====================================================
            GENERAL DESCRIPTION
        ====================================================== */}

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
            placeholder={
              isCyber
                ? "Example: Someone accessed my bank account through UPI and transferred ₹20,000 without my permission..."
                : "Describe your issue in detail..."
            }
            className="w-full border rounded-xl p-4 resize-none"
          />

          <p className="text-sm text-slate-500 mt-2">
            Minimum 20 characters required.
          </p>

        </div>

        {/* =====================================================
            REMEDY
        ====================================================== */}

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

            <option value="Refund">
              Refund
            </option>

            <option value="Replacement">
              Replacement
            </option>

            <option value="Compensation">
              Compensation
            </option>

            <option value="Repair">
              Repair
            </option>

            <option value="Other">
              Other
            </option>

          </select>

        </div>
        {/* =====================================================
            SUPPORTING EVIDENCE
        ====================================================== */}

        {!complaintGenerated && (
          <EvidenceUploader
            onEvidenceChange={setEvidence}
            onSkip={() => setEvidence([])}
          />
        )}

        {/* =====================================================
            BUTTON
        ====================================================== */}

        <div className="bg-blue-50 border border-blue-200 rounded-xl p-4 text-sm text-slate-700">
          <strong>Complaint Draft:</strong> The system uses the retrieved
          legal provisions and the facts you provide to create a reviewable
          draft. It is not a final legal document or legal advice.
        </div>

        <button
          onClick={handleSubmit}
          disabled={loading}
          className="w-full bg-gradient-to-r from-blue-900 to-indigo-700 hover:from-blue-800 hover:to-indigo-600 text-white py-4 rounded-xl font-semibold shadow-lg disabled:opacity-60"
        >

          {loading
            ? "Generating Complaint Draft..."
            : "Generate Complaint Draft"}

        </button>

      </div>

    </div>
  );
}