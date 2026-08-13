from pydantic import BaseModel
from typing import List


# =====================================
# Save Case Request
# =====================================

class SaveCaseRequest(BaseModel):

    citizen_name: str

    city: str

    report: dict


# =====================================
# Case Summary
# =====================================

class CaseSummary(BaseModel):

    case_id: str

    citizen_name: str

    city: str

    category: str

    confidence: str

    created_at: str


# =====================================
# Full Case
# =====================================

class CaseDetails(BaseModel):

    case_id: str

    citizen_name: str

    city: str

    category: str

    applicable_act: str

    confidence: str

    complaint: str

    report: dict

    created_at: str


# =====================================
# List Response
# =====================================

class CaseListResponse(BaseModel):

    cases: List[CaseSummary]