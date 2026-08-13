from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from app.utils.pdf_generator import pdf_generator

router = APIRouter(
    prefix="/pdf",
    tags=["PDF Export"]
)


@router.post("/download")
def download_pdf(report: dict):

    pdf_buffer = pdf_generator.generate(report)

    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={
            "Content-Disposition":
            "attachment; filename=Legal_Report.pdf"
        }
    )