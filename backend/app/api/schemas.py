from typing import List
from pydantic import BaseModel


class QuestionRequest(BaseModel):
    question: str


class Source(BaseModel):
    act: str
    chapter: str
    section: str
    title: str


class AnswerResponse(BaseModel):

    answer: str

    confidence: str

    retrieval_time: float

    llm_time: float

    total_time: float

    sources: List[Source]