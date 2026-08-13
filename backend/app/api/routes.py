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

        "retriever": "Hybrid Retrieval",

        "version": "1.0"

    }


@router.post(
    "/ask",
    response_model=AnswerResponse
)
def ask(request: QuestionRequest):

    result = assistant.ask(
        request.question
    )

    return AnswerResponse(**result)