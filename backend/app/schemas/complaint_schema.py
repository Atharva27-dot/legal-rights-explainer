from typing import Literal

from pydantic import BaseModel, Field


# =====================================
# Request Schema
# =====================================

class ComplaintRequest(BaseModel):
    """
    Request model for Complaint Generator
    """

    name: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Complainant Name"
    )

    product: str = Field(
        ...,
        min_length=2,
        max_length=150,
        description="Product or Service"
    )

    seller: str = Field(
        ...,
        min_length=2,
        max_length=150,
        description="Seller or Company Name"
    )

    purchase_date: str = Field(
        ...,
        description="Purchase Date"
    )

    city: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="City"
    )

    problem: str = Field(
        ...,
        min_length=20,
        max_length=3000,
        description="Problem Description"
    )

    remedy: Literal[
        "Refund",
        "Replacement",
        "Compensation"
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