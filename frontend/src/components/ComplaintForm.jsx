import { useState } from "react";
import {
  User,
  MapPin,
  Scale,
  ShoppingBag,
  Store,
  Calendar,
  Landmark,
  DollarSign,
  Edit3,
  CheckCircle2,
  FileText,
  Sparkles,
  Send,
  HelpCircle,
  AlertCircle
} from "lucide-react";
import { generateComplaint } from "../services/api";
import EvidenceUploader from "./EvidenceUploader";
import toast from "react-hot-toast";

export default function ComplaintForm({ setCaseData }) {
  const [loading, setLoading] = useState(false);
  const [evidence, setEvidence] = useState([]);
  const [complaintGenerated, setComplaintGenerated] = useState(false);

  const [formData, setFormData] = useState({
    name: "",
    city: "",
    domain: "",
    issue_type: "",
    product: "",
    seller: "",
    purchase_date: "",
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

  const isCyber = formData.domain === "Cyber / IT";
  const isConsumer = formData.domain === "Consumer Protection";
  const isEmployment = formData.domain === "Employment / Labour";
  const isContract = formData.domain === "Contract / Service";

  const handleSubmit = async (e) => {
    if (e && e.preventDefault) e.preventDefault();

    if (!formData.name.trim()) {
      toast.error("Please enter your name.");
      return;
    }

    if (!formData.city.trim()) {
      toast.error("Please enter your city.");
      return;
    }

    if (!formData.domain) {
      toast.error("Please select a legal domain.");
      return;
    }

    if (!formData.issue_type) {
      toast.error("Please select the specific issue.");
      return;
    }

    if (isConsumer) {
      if (!formData.product.trim()) {
        toast.error("Please enter the product or service.");
        return;
      }
      if (!formData.seller.trim()) {
        toast.error("Please enter the seller or company.");
        return;
      }
      if (!formData.purchase_date) {
        toast.error("Please enter the purchase date.");
        return;
      }
    }

    if (isCyber) {
      if (!formData.bank.trim()) {
        toast.error("Please enter the bank or payment platform.");
        return;
      }
      if (!formData.transaction_date) {
        toast.error("Please enter the transaction date.");
        return;
      }
      if (!formData.amount) {
        toast.error("Please enter the amount involved.");
        return;
      }
    }

    if (!formData.problem.trim()) {
      toast.error("Please describe your problem.");
      return;
    }

    if (formData.problem.trim().length < 20) {
      toast.error("Problem description must contain at least 20 characters.");
      return;
    }

    try {
      setLoading(true);

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
      toast.success("Complaint draft generated successfully!");
    } catch (error) {
      console.error(error);
      toast.error(
        error.response?.data?.detail || "Failed to generate complaint draft."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-white rounded-3xl shadow-sm border border-slate-200 overflow-hidden">
      {/* Form Header */}
      <div className="bg-gradient-to-r from-slate-900 via-indigo-950 to-slate-900 text-white px-6 sm:px-8 py-5 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-indigo-600 flex items-center justify-center text-white shadow-xs">
            <FileText className="w-5 h-5" />
          </div>
          <div>
            <h2 className="text-lg font-bold text-white tracking-tight">
              Enter Case & Dispute Details
            </h2>
            <p className="text-xs text-indigo-200">
              Structured input for automatic legal drafting
            </p>
          </div>
        </div>

        <div className="hidden sm:flex items-center gap-1.5 text-xs text-emerald-300 font-semibold bg-emerald-950/80 border border-emerald-500/30 px-3 py-1.5 rounded-full">
          <Sparkles className="w-3.5 h-3.5" />
          <span>Step 1 of 2</span>
        </div>
      </div>

      <div className="p-6 sm:p-8 space-y-6">
        {/* Citizen Info Grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div>
            <label className="font-semibold text-xs text-slate-700 flex items-center gap-1.5 mb-1.5">
              <User className="w-3.5 h-3.5 text-indigo-600" />
              <span>Full Name</span>
            </label>
            <input
              type="text"
              name="name"
              value={formData.name}
              onChange={handleChange}
              placeholder="e.g. Rahul Sharma"
              className="w-full bg-slate-50 border border-slate-200 rounded-xl p-3 text-sm text-slate-800 outline-none focus:bg-white focus:border-indigo-500 focus:ring-4 focus:ring-indigo-100 transition"
            />
          </div>

          <div>
            <label className="font-semibold text-xs text-slate-700 flex items-center gap-1.5 mb-1.5">
              <MapPin className="w-3.5 h-3.5 text-indigo-600" />
              <span>City / Jurisdiction</span>
            </label>
            <input
              type="text"
              name="city"
              value={formData.city}
              onChange={handleChange}
              placeholder="e.g. Pune, Maharashtra"
              className="w-full bg-slate-50 border border-slate-200 rounded-xl p-3 text-sm text-slate-800 outline-none focus:bg-white focus:border-indigo-500 focus:ring-4 focus:ring-indigo-100 transition"
            />
          </div>
        </div>

        {/* Legal Domain & Specific Issue */}
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div>
            <label className="font-semibold text-xs text-slate-700 flex items-center gap-1.5 mb-1.5">
              <Scale className="w-3.5 h-3.5 text-indigo-600" />
              <span>Legal Domain</span>
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
              className="w-full bg-slate-50 border border-slate-200 rounded-xl p-3 text-sm text-slate-800 outline-none focus:bg-white focus:border-indigo-500 focus:ring-4 focus:ring-indigo-100 transition"
            >
              <option value="">Select legal domain</option>
              <option value="Consumer Protection">Consumer Protection</option>
              <option value="Cyber / IT">Cyber / IT</option>
              <option value="Employment / Labour">Employment / Labour</option>
              <option value="Contract / Service">Contract / Service</option>
              <option value="Motor Vehicle / Road Accident">Motor Vehicle / Road Accident</option>
              <option value="Other">Other</option>
            </select>
          </div>

          <div>
            <label className="font-semibold text-xs text-slate-700 flex items-center gap-1.5 mb-1.5">
              <Scale className="w-3.5 h-3.5 text-indigo-600" />
              <span>Specific Issue</span>
            </label>
            <select
              name="issue_type"
              value={formData.issue_type}
              onChange={handleChange}
              disabled={!formData.domain}
              className="w-full bg-slate-50 border border-slate-200 rounded-xl p-3 text-sm text-slate-800 outline-none focus:bg-white focus:border-indigo-500 focus:ring-4 focus:ring-indigo-100 transition disabled:bg-slate-100 disabled:text-slate-400"
            >
              <option value="">
                {formData.domain ? "Select specific issue" : "Select domain first"}
              </option>
              {isConsumer && (
                <>
                  <option value="Defective Product">Defective Product</option>
                  <option value="Wrong Product Delivered">Wrong Product Delivered</option>
                  <option value="Refund Not Received">Refund Not Received</option>
                  <option value="Product Warranty Issue">Product Warranty Issue</option>
                  <option value="Online Shopping Dispute">Online Shopping Dispute</option>
                  <option value="Service Deficiency">Service Deficiency</option>
                </>
              )}
              {isCyber && (
                <>
                  <option value="UPI Fraud">UPI / Online Payment Fraud</option>
                  <option value="Online Banking Fraud">Online Banking Fraud</option>
                  <option value="Phishing">Phishing / Fake Link</option>
                  <option value="Account Hacking">Account Hacking</option>
                  <option value="Identity Theft">Identity Theft</option>
                  <option value="Unauthorized Transaction">Unauthorized Transaction</option>
                  <option value="Other Cyber Crime">Other Cyber Crime</option>
                </>
              )}
              {isEmployment && (
                <>
                  <option value="Unpaid Salary">Unpaid Salary</option>
                  <option value="Wrongful Termination">Wrongful Termination</option>
                  <option value="Workplace Harassment">Workplace Harassment</option>
                  <option value="Employment Dispute">Employment Dispute</option>
                </>
              )}
              {isContract && (
                <>
                  <option value="Breach of Contract">Breach of Contract</option>
                  <option value="Non Payment">Non-Payment</option>
                  <option value="Contractual Dispute">Contractual Dispute</option>
                  <option value="Service Agreement Dispute">Service Agreement Dispute</option>
                </>
              )}
              {formData.domain === "Motor Vehicle / Road Accident" && (
                <>
                  <option value="Road Accident">Road Accident</option>
                  <option value="Vehicle Damage">Vehicle Damage</option>
                  <option value="Insurance Claim">Insurance Claim</option>
                  <option value="Traffic Dispute">Traffic Dispute</option>
                </>
              )}
              {formData.domain === "Other" && (
                <option value="General Legal Issue">General Legal Issue</option>
              )}
            </select>
          </div>
        </div>

        {/* Consumer Dynamic Fields */}
        {isConsumer && (
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 bg-indigo-50/40 p-4 rounded-2xl border border-indigo-100">
            <div>
              <label className="font-semibold text-xs text-slate-700 flex items-center gap-1.5 mb-1.5">
                <ShoppingBag className="w-3.5 h-3.5 text-indigo-600" />
                <span>Product / Service Name</span>
              </label>
              <input
                type="text"
                name="product"
                value={formData.product}
                onChange={handleChange}
                placeholder="e.g. Mobile Phone"
                className="w-full bg-white border border-slate-200 rounded-xl p-3 text-sm text-slate-800 outline-none focus:border-indigo-500 transition"
              />
            </div>

            <div>
              <label className="font-semibold text-xs text-slate-700 flex items-center gap-1.5 mb-1.5">
                <Store className="w-3.5 h-3.5 text-indigo-600" />
                <span>Seller / Company</span>
              </label>
              <input
                type="text"
                name="seller"
                value={formData.seller}
                onChange={handleChange}
                placeholder="e.g. Amazon / E-store"
                className="w-full bg-white border border-slate-200 rounded-xl p-3 text-sm text-slate-800 outline-none focus:border-indigo-500 transition"
              />
            </div>

            <div>
              <label className="font-semibold text-xs text-slate-700 flex items-center gap-1.5 mb-1.5">
                <Calendar className="w-3.5 h-3.5 text-indigo-600" />
                <span>Purchase Date</span>
              </label>
              <input
                type="date"
                name="purchase_date"
                value={formData.purchase_date}
                onChange={handleChange}
                className="w-full bg-white border border-slate-200 rounded-xl p-3 text-sm text-slate-800 outline-none focus:border-indigo-500 transition"
              />
            </div>
          </div>
        )}

        {/* Cyber Dynamic Fields */}
        {isCyber && (
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 bg-purple-50/40 p-4 rounded-2xl border border-purple-100">
            <div>
              <label className="font-semibold text-xs text-slate-700 flex items-center gap-1.5 mb-1.5">
                <Landmark className="w-3.5 h-3.5 text-purple-600" />
                <span>Bank / Payment Platform</span>
              </label>
              <input
                type="text"
                name="bank"
                value={formData.bank}
                onChange={handleChange}
                placeholder="e.g. SBI, HDFC, Google Pay"
                className="w-full bg-white border border-slate-200 rounded-xl p-3 text-sm text-slate-800 outline-none focus:border-indigo-500 transition"
              />
            </div>

            <div>
              <label className="font-semibold text-xs text-slate-700 flex items-center gap-1.5 mb-1.5">
                <Calendar className="w-3.5 h-3.5 text-purple-600" />
                <span>Transaction Date</span>
              </label>
              <input
                type="date"
                name="transaction_date"
                value={formData.transaction_date}
                onChange={handleChange}
                className="w-full bg-white border border-slate-200 rounded-xl p-3 text-sm text-slate-800 outline-none focus:border-indigo-500 transition"
              />
            </div>

            <div>
              <label className="font-semibold text-xs text-slate-700 flex items-center gap-1.5 mb-1.5">
                <DollarSign className="w-3.5 h-3.5 text-purple-600" />
                <span>Amount Involved (₹)</span>
              </label>
              <input
                type="number"
                name="amount"
                value={formData.amount}
                onChange={handleChange}
                placeholder="e.g. 20000"
                min="0"
                className="w-full bg-white border border-slate-200 rounded-xl p-3 text-sm text-slate-800 outline-none focus:border-indigo-500 transition"
              />
            </div>
          </div>
        )}

        {/* Problem Description & Desired Remedy */}
        <div className="space-y-4">
          <div>
            <label className="font-semibold text-xs text-slate-700 flex items-center gap-1.5 mb-1.5">
              <Edit3 className="w-3.5 h-3.5 text-indigo-600" />
              <span>Describe Problem & Facts</span>
            </label>
            <textarea
              rows={5}
              name="problem"
              value={formData.problem}
              onChange={handleChange}
              placeholder={
                isCyber
                  ? "Describe how the fraud occurred, transaction IDs, whether bank was informed within 3 days..."
                  : "Describe your problem in detail, including dates, defective behavior, and communications..."
              }
              className="w-full bg-slate-50 border border-slate-200 rounded-xl p-4 text-sm text-slate-800 placeholder:text-slate-400 outline-none focus:bg-white focus:border-indigo-500 focus:ring-4 focus:ring-indigo-100 transition resize-y"
            />
            <p className="text-[11px] text-slate-400 mt-1">
              Minimum 20 characters required. Include clear timelines for evidence consistency scoring.
            </p>
          </div>

          <div>
            <label className="font-semibold text-xs text-slate-700 flex items-center gap-1.5 mb-1.5">
              <CheckCircle2 className="w-3.5 h-3.5 text-indigo-600" />
              <span>Desired Remedy</span>
            </label>
            <select
              name="remedy"
              value={formData.remedy}
              onChange={handleChange}
              className="w-full bg-slate-50 border border-slate-200 rounded-xl p-3 text-sm text-slate-800 outline-none focus:bg-white focus:border-indigo-500 transition"
            >
              <option value="Refund">Refund of Amount</option>
              <option value="Replacement">Product Replacement</option>
              <option value="Compensation">Compensation for Damages</option>
              <option value="Repair">Free Repair / Service</option>
              <option value="Other">Other Relief</option>
            </select>
          </div>
        </div>

        {/* Supporting Evidence Uploader */}
        {!complaintGenerated && (
          <div className="pt-4 border-t border-slate-100">
            <EvidenceUploader
              onEvidenceChange={setEvidence}
              onSkip={() => setEvidence([])}
            />
          </div>
        )}

        {/* Disclaimer Notice */}
        <div className="bg-slate-50 border border-slate-200/80 rounded-xl p-3 text-xs text-slate-600 flex items-center gap-2">
          <Sparkles className="w-4 h-4 text-indigo-600 flex-shrink-0" />
          <span>The system uses retrieved legal provisions and case details to generate a reviewable draft. Review before formal filing.</span>
        </div>

        {/* Submit Action Button */}
        <button
          type="button"
          onClick={handleSubmit}
          disabled={loading}
          className="w-full inline-flex items-center justify-center gap-2 bg-indigo-600 hover:bg-indigo-700 disabled:bg-slate-300 text-white font-bold text-sm py-4 rounded-xl shadow-xs transition-all duration-200"
        >
          <Send className="w-4 h-4" />
          {loading ? "Generating Formal Complaint Draft..." : "Generate Formal Complaint Draft"}
        </button>
      </div>
    </div>
  );
}