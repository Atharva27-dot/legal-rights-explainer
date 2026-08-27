from typing import Optional, List

from pydantic import BaseModel


class EvidenceItem(BaseModel):

    name: str = ""

    file_id: str = ""

    extracted_text: str = ""

    extraction_status: Optional[str] = None


class QuestionRequest(BaseModel):

    question: str

    domain: Optional[str] = None

    issue_type: Optional[str] = None

    evidence: List[EvidenceItem] = []


class Source(BaseModel):

    act: str = ""

    chapter: str = ""

    section: str = ""

    title: str = ""

    domain: str = ""

    semantic_score: float = 0.0

    keyword_score: float = 0.0

    metadata_score: float = 0.0

    domain_score: float = 0.0

    legal_issue_score: float = 0.0

    final_score: float = 0.0


class AnswerResponse(BaseModel):

    answer: str

    confidence: str

    retrieval_time: float

    llm_time: float

    total_time: float

    sources: List[Source]