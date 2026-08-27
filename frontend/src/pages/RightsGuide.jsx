import { useState } from "react";
import { askQuestion } from "../services/api";
import EvidenceUploader from "../components/EvidenceUploader";
import {
  FaBalanceScale,
  FaBookOpen,
  FaCheckCircle,
  FaChevronDown,
  FaClipboardList,
  FaExclamationTriangle,
  FaInfoCircle,
  FaPaperPlane,
} from "react-icons/fa";

const issuesByDomain = {
  "Consumer Protection": [
    "Consumer Definition",
    "Consumer Rights",
    "Filing Complaint",
    "Mediation",
    "Defective Product",
    "Refund / Replacement",
    "Deficiency in Service",
    "Unfair Trade Practice",
    "Product Liability",
  ],
  "Cyber / IT": [
    "UPI Fraud",
    "Unauthorized Access",
    "Identity Theft",
    "Online Payment Fraud",
    "Cyber Crime",
  ],
  "Employment / Labour": [
    "Wrongful Termination",
    "Unpaid Salary",
    "Workplace Rights",
    "Employment Dispute",
  ],
  Property: [
    "Property Dispute",
    "Landlord Tenant Dispute",
    "Ownership Dispute",
    "Property Transfer",
  ],
  "Family Law": [
    "Divorce",
    "Maintenance",
    "Child Custody",
    "Domestic Dispute",
  ],
  "Motor Vehicle": [
    "Road Accident",
    "Motor Insurance Claim",
    "Vehicle Compensation",
    "Traffic Dispute",
  ],
};

function scoreNumber(value) {
  const number = Number(value);
  return Number.isFinite(number) ? number : null;
}

function relevanceLabel(value) {
  const number = scoreNumber(value);

  if (number === null) return "Unavailable";
  if (number >= 0.75) return "High";
  if (number >= 0.5) return "Moderate";
  if (number > 0) return "Low";

  return "Very Low";
}

export default function RightsGuide() {
  const [domain, setDomain] = useState("");
  const [issueType, setIssueType] = useState("");
  const [question, setQuestion] = useState("");
  const [evidence, setEvidence] = useState([]);
  const [answer, setAnswer] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleDomainChange = (event) => {
    setDomain(event.target.value);
    setIssueType("");
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    setError("");
    setAnswer(null);

    if (!domain) {
      setError("Please select a legal domain.");
      return;
    }

    if (!issueType) {
      setError("Please select the specific legal issue.");
      return;
    }

    if (!question.trim()) {
      setError("Please describe your legal problem.");
      return;
    }

    try {
      setLoading(true);

      const result = await askQuestion(
        question,
        domain,
        issueType,
        evidence
      );

      setAnswer(result);
    } catch (err) {
      console.error(err);

      setError(
        "Unable to process your request. Please make sure the backend is running."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-100">
      <main className="max-w-[1500px] mx-auto px-4 sm:px-6 lg:px-8 py-8">

        <section className="bg-white border border-slate-200 rounded-3xl shadow-sm overflow-hidden">

          <div className="bg-gradient-to-r from-indigo-700 to-blue-700 px-6 sm:px-8 py-7 text-white">
            <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-5">

              <div className="flex items-start gap-4">
                <div className="w-12 h-12 rounded-2xl bg-white/15 flex items-center justify-center flex-shrink-0">
                  <FaBalanceScale className="text-xl" />
                </div>

                <div>
                  <p className="text-xs font-semibold uppercase tracking-wider text-blue-100">
                    Legal Rights Guide
                  </p>

                  <h1 className="text-2xl sm:text-3xl font-bold mt-1">
                    Understand your legal rights
                  </h1>

                  <p className="text-blue-100 text-sm sm:text-base mt-2 max-w-2xl leading-6">
                    Select your legal domain and issue, describe what happened
                    in your own words, and get a plain-language explanation
                    grounded in retrieved legal provisions.
                  </p>
                </div>
              </div>

              <div className="flex items-center gap-2 bg-white/10 border border-white/20 rounded-full px-3 py-2 self-start sm:self-center">
                <span className="w-2.5 h-2.5 rounded-full bg-emerald-300" />
                <span className="text-xs font-semibold text-white">
                  AI Online
                </span>
              </div>

            </div>
          </div>

          <form onSubmit={handleSubmit} className="p-6 sm:p-8">

            <div className="space-y-6">

              <div className="space-y-4">

                <div>
                  <div className="flex items-center gap-3 mb-1">
                    <div className="w-9 h-9 rounded-xl bg-indigo-100 text-indigo-700 flex items-center justify-center">
                      <FaClipboardList />
                    </div>

                    <div>
                      <h2 className="font-bold text-slate-900">
                        Case Information
                      </h2>

                      <p className="text-xs text-slate-500">
                        Help the system narrow the legal context.
                      </p>
                    </div>
                  </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">

                  <div className="bg-slate-50 border border-slate-200 rounded-2xl p-5">

                    <label
                      htmlFor="legal-domain"
                      className="block text-sm font-semibold text-slate-800"
                    >
                      Legal Domain
                    </label>

                    <p className="text-xs text-slate-500 mt-1 mb-3">
                      Choose the broad area of law related to your problem.
                    </p>

                    <div className="relative">
                      <select
                        id="legal-domain"
                        value={domain}
                        onChange={handleDomainChange}
                        className="appearance-none w-full bg-white border border-slate-300 rounded-xl px-4 py-3 pr-10 text-sm text-slate-800 outline-none transition focus:border-indigo-500 focus:ring-2 focus:ring-indigo-100"
                      >
                        <option value="">
                          Select legal domain
                        </option>

                        {Object.keys(issuesByDomain).map((item) => (
                          <option key={item} value={item}>
                            {item}
                          </option>
                        ))}
                      </select>

                      <FaChevronDown className="absolute right-4 top-1/2 -translate-y-1/2 text-slate-400 pointer-events-none text-xs" />
                    </div>
                  </div>

                  <div
                    className={`bg-slate-50 border rounded-2xl p-5 transition ${
                      domain
                        ? "border-slate-200"
                        : "border-dashed border-slate-300"
                    }`}
                  >

                    <label
                      htmlFor="legal-issue"
                      className="block text-sm font-semibold text-slate-800"
                    >
                      Specific Legal Issue
                    </label>

                    <p className="text-xs text-slate-500 mt-1 mb-3">
                      Select the issue that most closely matches your situation.
                    </p>

                    <div className="relative">
                      <select
                        id="legal-issue"
                        value={issueType}
                        disabled={!domain}
                        onChange={(event) => setIssueType(event.target.value)}
                        className="appearance-none w-full bg-white border border-slate-300 rounded-xl px-4 py-3 pr-10 text-sm text-slate-800 outline-none transition focus:border-indigo-500 focus:ring-2 focus:ring-indigo-100 disabled:bg-slate-100 disabled:text-slate-400 disabled:cursor-not-allowed"
                      >
                        <option value="">
                          {domain
                            ? "Select specific issue"
                            : "Select a legal domain first"}
                        </option>

                        {domain &&
                          issuesByDomain[domain]?.map((item) => (
                            <option key={item} value={item}>
                              {item}
                            </option>
                          ))}
                      </select>

                      <FaChevronDown className="absolute right-4 top-1/2 -translate-y-1/2 text-slate-400 pointer-events-none text-xs" />
                    </div>

                  </div>
                </div>
              </div>

              <div>
                <label
                  htmlFor="legal-problem"
                  className="block text-sm font-bold text-slate-900"
                >
                  Describe Your Problem
                </label>

                <p className="text-xs text-slate-500 mt-1 mb-3">
                  Explain what happened in simple language. Include
                  important dates, parties, amounts, and what you want.
                </p>

                <textarea
                  id="legal-problem"
                  value={question}
                  onChange={(event) => setQuestion(event.target.value)}
                  placeholder="Example: I purchased a mobile phone online. It stopped working after five days and the seller refused to provide a replacement or refund..."
                  rows={8}
                  className="w-full bg-white border border-slate-300 rounded-2xl px-4 py-4 text-sm text-slate-800 leading-6 outline-none resize-y min-h-[190px] transition placeholder:text-slate-400 focus:border-indigo-500 focus:ring-4 focus:ring-indigo-50"
                />

                <div className="flex justify-between mt-2 text-xs text-slate-400">
                  <span>Describe only the facts you know.</span>
                  <span>{question.length} characters</span>
                </div>
              </div>

              {/* Supporting evidence - single EvidenceUploader only */}
              <EvidenceUploader
                onEvidenceChange={setEvidence}
                onSkip={() => setEvidence([])}
              />

            </div>

            {error && (
              <div className="mt-6 flex items-start gap-3 rounded-2xl border border-red-200 bg-red-50 px-4 py-4 text-sm text-red-800">

                <FaExclamationTriangle className="mt-0.5 flex-shrink-0" />

                <div>
                  <p className="font-semibold">
                    Please check the form
                  </p>

                  <p className="mt-1">
                    {error}
                  </p>
                </div>

              </div>
            )}

            <div className="mt-8 pt-6 border-t border-slate-200 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">

              <div className="flex items-start gap-3 text-xs text-slate-500 max-w-xl">
                <FaInfoCircle className="text-indigo-600 mt-0.5 flex-shrink-0" />

                <span>
                  The explanation is based on retrieved legal documents.
                  Review the result and supporting evidence before relying
                  on it.
                </span>
              </div>

              <button
                type="submit"
                disabled={loading}
                className="inline-flex items-center justify-center gap-2 rounded-xl bg-indigo-600 hover:bg-indigo-700 disabled:bg-indigo-300 disabled:cursor-not-allowed text-white font-semibold px-6 py-3.5 shadow-sm transition min-w-[220px]"
              >
                <FaPaperPlane />

                {loading
                  ? "Analyzing your case..."
                  : "Explain My Legal Rights"}
              </button>

            </div>

          </form>
        </section>

        {loading && (
          <div className="mt-6 bg-white border border-slate-200 rounded-3xl shadow-sm p-6">

            <div className="flex items-center gap-4">

              <div className="w-10 h-10 rounded-full border-4 border-indigo-100 border-t-indigo-600 animate-spin" />

              <div>
                <p className="font-semibold text-slate-900">
                  Analyzing your case
                </p>

                <p className="text-sm text-slate-500 mt-1">
                  Retrieving relevant legal provisions and preparing a
                  plain-language explanation.
                </p>
              </div>

            </div>

          </div>
        )}

        {answer && !loading && (
          <section className="mt-6 space-y-5">

            <div className="bg-white rounded-3xl border border-slate-200 shadow-sm overflow-hidden">

              <div className="bg-gradient-to-r from-indigo-700 to-blue-700 px-6 py-5 text-white">

                <div className="flex items-center justify-between gap-4">

                  <div className="flex items-center gap-3">

                    <div className="w-10 h-10 rounded-xl bg-white/15 flex items-center justify-center">
                      <FaBalanceScale />
                    </div>

                    <div>
                      <h2 className="text-xl font-bold">
                        Legal Explanation
                      </h2>

                      <p className="text-sm text-blue-100">
                        Generated from retrieved legal documents
                      </p>
                    </div>

                  </div>

                  <div className="hidden sm:flex items-center gap-2 bg-white/10 border border-white/20 rounded-full px-3 py-2 text-xs font-semibold">
                    <FaCheckCircle />
                    {answer.confidence || "Review"}
                  </div>

                </div>

              </div>

              <div className="p-6">

                <div className="bg-slate-50 border border-slate-200 rounded-2xl p-5 text-slate-700 text-sm sm:text-base leading-7 whitespace-pre-wrap">
                  {answer.answer}
                </div>

                <div className="mt-4 flex items-center gap-2 text-sm">
                  <span className="font-semibold text-slate-600">
                    Retrieval confidence:
                  </span>

                  <span className="font-bold text-indigo-700">
                    {answer.confidence}
                  </span>
                </div>

              </div>

            </div>

            {answer.sources && answer.sources.length > 0 && (
              <div className="bg-white rounded-3xl border border-slate-200 shadow-sm overflow-hidden">

                <div className="px-6 py-5 border-b border-slate-200">

                  <div className="flex items-center gap-3">

                    <div className="w-10 h-10 rounded-xl bg-indigo-100 text-indigo-700 flex items-center justify-center">
                      <FaBookOpen />
                    </div>

                    <div>
                      <h2 className="text-xl font-bold text-slate-900">
                        Retrieved Legal Sources
                      </h2>

                      <p className="text-sm text-slate-500 mt-0.5">
                        Provisions retrieved for this explanation
                      </p>
                    </div>

                  </div>

                </div>

                <div className="p-6 space-y-4">

                  {answer.sources.map((source, index) => {

                    const finalScore = scoreNumber(source.final_score);

                    return (
                      <div
                        key={`${source.act}-${source.section}-${index}`}
                        className="border border-slate-200 rounded-2xl p-5"
                      >

                        <div className="flex items-start justify-between gap-4">

                          <div className="min-w-0">

                            <p className="text-xs font-semibold uppercase tracking-wide text-indigo-600">
                              Source {index + 1}
                            </p>

                            <h3 className="font-bold text-slate-900 mt-1">
                              {source.act || "Legal Act"}
                            </h3>

                            <div className="mt-2 text-sm text-slate-600 space-y-1">

                              {source.chapter && (
                                <p>
                                  <span className="font-semibold">
                                    Chapter:
                                  </span>{" "}
                                  {source.chapter}
                                </p>
                              )}

                              {source.section && (
                                <p>
                                  <span className="font-semibold">
                                    Section:
                                  </span>{" "}
                                  {source.section}
                                </p>
                              )}

                              {source.title && (
                                <p className="leading-6">
                                  <span className="font-semibold">
                                    Title:
                                  </span>{" "}
                                  {source.title}
                                </p>
                              )}

                            </div>

                          </div>

                          <div className="flex-shrink-0 text-right">

                            <p className="text-xs text-slate-500">
                              Relevance
                            </p>

                            <p className="text-sm font-bold text-indigo-700">
                              {relevanceLabel(source.final_score)}
                            </p>

                            {finalScore !== null && (
                              <p className="text-xs text-slate-500 mt-1">
                                {finalScore.toFixed(3)}
                              </p>
                            )}

                          </div>

                        </div>

                      </div>
                    );
                  })}

                </div>
              </div>
            )}

          </section>
        )}

      </main>
    </div>
  );
}
