import axios from "axios";

const API = axios.create({
  baseURL: "http://127.0.0.1:8000",
  headers: {
    "Content-Type": "application/json",
  },
});

/* =====================================
   Legal Assistant
===================================== */

export const askQuestion = async (
  question,
  domain = null,
  issueType = null,
  evidence = []
) => {

  const formattedEvidence = (evidence || []).map((item) => ({
    name: item.name || "",
    file_id: item.fileId || "",
    extracted_text: item.extractedText || "",
    extraction_status: item.extractionStatus || null,
  }));

  const response = await API.post(
    "/ask",
    {
      question,
      domain,
      issue_type: issueType,
      evidence: formattedEvidence,
    }
  );

  return response.data;
};

/* =====================================
   Complaint Generator
===================================== */

export const generateComplaint = async (complaintData) => {
  const response = await API.post(
    "/complaint/generate",
    complaintData
  );

  return response.data;
};

/* =====================================
   PDF Export
===================================== */

export const downloadComplaintPDF = async (report) => {
  const response = await API.post(
    "/pdf/download",
    report,
    {
      responseType: "blob",
    }
  );

  return response.data;
};

export const downloadComplaintDOCX = async (report) => {
  const response = await API.post(
    "/complaint/docx/download",
    report,
    {
      responseType: "blob",
    }
  );

  return response.data;
};

/* =====================================
   My Legal Cases
===================================== */

export const saveCase = async (caseData) => {
  const response = await API.post(
    "/cases/save",
    caseData
  );

  return response.data;
};

export const getCases = async () => {
  const response = await API.get("/cases");

  return response.data;
};

export const getCase = async (caseId) => {
  const response = await API.get(
    `/cases/${caseId}`
  );

  return response.data;
};

export const deleteCase = async (caseId) => {
  const response = await API.delete(
    `/cases/${caseId}`
  );

  return response.data;
};

/* =====================================
   Evidence
===================================== */

export const uploadEvidence = async (file) => {
  const formData = new FormData();

  formData.append("file", file);

  const response = await API.post(
    "/complaint/evidence/upload",
    formData,
    {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    }
  );

  return response.data;
};

export const extractEvidenceText = async (fileId) => {
  const response = await API.post(
    `/complaint/evidence/extract?file_id=${encodeURIComponent(fileId)}`
  );

  return response.data;
};

export default API;