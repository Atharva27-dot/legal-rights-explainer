from fastapi import APIRouter

from app.api.schemas import (
    QuestionRequest,
    AnswerResponse
)

from app.services.legal_assistant import LegalAssistant


router = APIRouter()

assistant = LegalAssistant()


@router.get("/health")
def health():

    return {

        "status": "running",

        "model": "Ollama",

        "retriever": "Domain + Issue Aware Hybrid Retrieval",

        "version": "2.0"

    }


@router.post(
    "/ask",
    response_model=AnswerResponse
)
def ask(
    request: QuestionRequest
):

    result = assistant.ask(
    question=request.question,
    domain=request.domain,
    issue_type=request.issue_type,
    evidence=[
        item.model_dump()
        for item in request.evidence
    ]
    )

    return AnswerResponse(
        **result
    )
