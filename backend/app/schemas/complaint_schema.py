from typing import Literal
from pydantic import BaseModel, Field


class EvidenceItem(BaseModel):
    file_id: str
    filename: str
    extraction_status: str | None = None
    extracted_text: str = ""


class ComplaintRequest(BaseModel):
    name: str = Field(..., min_length=2, max_length=100, description="Complainant Name")
    city: str = Field(..., min_length=2, max_length=100, description="City")
    domain: str = Field(..., min_length=2, max_length=100, description="User-selected legal domain")
    issue_type: str = Field(..., min_length=2, max_length=150, description="Specific legal issue selected by the user")
    product: str = Field(..., min_length=2, max_length=150, description="Product, service, issue type or relevant item")
    seller: str = Field(..., min_length=2, max_length=150, description="Seller, company, bank or relevant party")
    purchase_date: str = Field(..., description="Purchase or transaction date")
    bank: str | None = Field(default=None, max_length=150, description="Bank or payment platform")
    transaction_date: str | None = Field(default=None, description="Cyber transaction date")
    amount: str | None = Field(default=None, max_length=50, description="Amount involved in the dispute")
    problem: str = Field(..., min_length=20, max_length=3000, description="Problem Description")
    remedy: Literal["Refund", "Replacement", "Compensation", "Repair", "Other"]
    evidence: list[EvidenceItem] = Field(default_factory=list, description="Supporting evidence uploaded by the citizen")


class CaseAnalysis(BaseModel):
    category: str
    applicable_act: str
    rights: list[str]
    recommended_remedy: str
    legal_readiness: str
    supporting_documents: list[str]


class Source(BaseModel):
    act: str | None = None
    chapter: str | None = None
    section: str | None = None
    title: str | None = None
    domain: str | None = None
    semantic_score: float | None = None
    keyword_score: float | None = None
    metadata_score: float | None = None
    domain_score: float | None = None
    final_score: float | None = None


class ReadinessEvidence(BaseModel):
    detected: list[str] = Field(default_factory=list)
    missing: list[str] = Field(default_factory=list)


class ReadinessResponse(BaseModel):
    score: int
    status: str
    recommendations: list[str]
    evidence: ReadinessEvidence = Field(default_factory=ReadinessEvidence)


class EvidenceConsistencyCheck(BaseModel):
    field: str
    label: str
    user_value: str | None = None
    evidence_value: str | None = None
    status: str
    message: str


class EvidenceConsistencyResponse(BaseModel):
    overall_status: str
    summary: str
    checks: list[EvidenceConsistencyCheck]
    discrepancies: list[EvidenceConsistencyCheck]


class ComplaintResponse(BaseModel):
    case_analysis: CaseAnalysis
    complaint: str
    confidence: str
    readiness: ReadinessResponse
    grounding: dict | None = None
    evidence_consistency: EvidenceConsistencyResponse | None = None

    # Deterministic evidence timeline generated from case details
    # and extracted evidence. Kept as a dict so the timeline service
    # can evolve without changing the complaint generator.
    timeline: dict | None = None

    # Deterministic next-step workflow generated from the completed report.
    action_plan: dict | None = None

    retrieval_time: float
    llm_time: float
    total_time: float
    sources: list[Source]
