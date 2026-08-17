from typing import Literal

from pydantic import BaseModel, Field


# =====================================
# Request Schema
# =====================================

class ComplaintRequest(BaseModel):
    """
    Request model for Complaint Generator
    """

    # =====================================
    # Basic Information
    # =====================================

    name: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Complainant Name"
    )

    city: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="City"
    )

    # =====================================
    # Legal Classification
    # =====================================

    domain: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="User-selected legal domain"
    )

    issue_type: str = Field(
        ...,
        min_length=2,
        max_length=150,
        description="Specific legal issue selected by the user"
    )

    # =====================================
    # Consumer / General Fields
    # =====================================

    product: str = Field(
        ...,
        min_length=2,
        max_length=150,
        description="Product, service, issue type or relevant item"
    )

    seller: str = Field(
        ...,
        min_length=2,
        max_length=150,
        description="Seller, company, bank or relevant party"
    )

    purchase_date: str = Field(
        ...,
        description="Purchase or transaction date"
    )

    # =====================================
    # Cyber / IT Fields
    # =====================================

    bank: str | None = Field(
        default=None,
        max_length=150,
        description="Bank or payment platform"
    )

    transaction_date: str | None = Field(
        default=None,
        description="Cyber transaction date"
    )

    amount: str | None = Field(
        default=None,
        max_length=50,
        description="Amount involved in the dispute"
    )

    # =====================================
    # Complaint
    # =====================================

    problem: str = Field(
        ...,
        min_length=20,
        max_length=3000,
        description="Problem Description"
    )

    remedy: Literal[
        "Refund",
        "Replacement",
        "Compensation",
        "Repair",
        "Other"
    ]


# =====================================
# Case Analysis
# =====================================

class CaseAnalysis(BaseModel):

    category: str

    applicable_act: str

    rights: list[str]

    recommended_remedy: str

    legal_readiness: str

    supporting_documents: list[str]


# =====================================
# Legal Source
# =====================================

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

# =====================================
# Readiness Response
# =====================================

class ReadinessResponse(BaseModel):

    score: int

    status: str

    recommendations: list[str]


# =====================================
# Response Schema
# =====================================

class ComplaintResponse(BaseModel):

    case_analysis: CaseAnalysis

    complaint: str

    confidence: str

    readiness: ReadinessResponse

    retrieval_time: float

    llm_time: float

    total_time: float

    sources: list[Source]