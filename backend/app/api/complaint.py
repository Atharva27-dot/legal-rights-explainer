from fastapi import APIRouter, HTTPException, UploadFile, File
from fastapi.responses import Response
from app.services.complaint_docx_service import build_complaint_docx

from app.schemas.complaint_schema import (
    ComplaintRequest,
    ComplaintResponse,
)

from app.services.complaint_generator import (
    complaint_generator,
)

from app.services.evidence_consistency import (
    evidence_consistency_service,
)

from app.services.timeline_service import (
    evidence_timeline_service,
)

from app.services.action_plan_service import (
    action_plan_service,
)

from pathlib import Path
import uuid

from pypdf import PdfReader
from docx import Document


router = APIRouter(
    prefix="/complaint",
    tags=["Complaint Generator"],
)


# Store evidence inside the backend/uploads/evidence folder.
BACKEND_DIR = Path(__file__).resolve().parents[2]
EVIDENCE_DIR = BACKEND_DIR / "uploads" / "evidence"


@router.post(
    "/generate",
    response_model=ComplaintResponse,
)
def generate_complaint(request: ComplaintRequest):

    try:

        # ========================================================
        # EVIDENCE-FACT CONSISTENCY CHECK
        # ========================================================
        consistency_report = (
            evidence_consistency_service.check(request)
        )

        # Build the deterministic evidence timeline from the same
        # case details and extracted evidence already supplied to the
        # complaint pipeline. No LLM call is made here.
        timeline_report = (
            evidence_timeline_service.build_timeline(request)
        )

        # Generate the grounded complaint using the existing pipeline.
        response = complaint_generator.generate(request)

        # Expose the consistency and timeline results to the frontend.
        response["evidence_consistency"] = consistency_report
        response["timeline"] = timeline_report

        # Build a deterministic next-step action plan from the completed
        # report. This does not make another LLM call.
        response["action_plan"] = action_plan_service.build_plan(
            request,
            response,
        )

        return response

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@router.post("/docx/download")
def download_complaint_docx(payload: dict):

    try:

        report = payload.get("report") or payload
        form_data = payload.get("formData") or {}

        docx_bytes = build_complaint_docx(
            report=report,
            form_data=form_data,
        )

        return Response(
            content=docx_bytes,
            media_type=(
                "application/vnd.openxmlformats-officedocument."
                "wordprocessingml.document"
            ),
            headers={
                "Content-Disposition":
                    'attachment; filename="Legal_Complaint_Draft.docx"'
            },
        )

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e),
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"DOCX generation failed: {e}",
        )


@router.post("/evidence/upload")
async def upload_evidence(
    file: UploadFile = File(...)
):

    allowed_types = {
        "application/pdf",
        "image/jpeg",
        "image/png",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    }

    max_size = 10 * 1024 * 1024  # 10 MB

    if file.content_type not in allowed_types:

        raise HTTPException(
            status_code=400,
            detail=(
                "Unsupported file type. "
                "Upload PDF, JPG, PNG, or DOCX."
            ),
        )

    file_content = await file.read()

    if len(file_content) > max_size:

        raise HTTPException(
            status_code=400,
            detail="File is too large. Maximum size is 10 MB.",
        )

    EVIDENCE_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    file_id = str(uuid.uuid4())

    original_name = Path(
        file.filename or "evidence"
    ).name

    extension = Path(
        original_name
    ).suffix.lower()

    saved_filename = f"{file_id}{extension}"

    saved_path = EVIDENCE_DIR / saved_filename

    saved_path.write_bytes(file_content)

    return {
        "success": True,
        "file_id": file_id,
        "filename": original_name,
        "stored_filename": saved_filename,
        "content_type": file.content_type,
        "size": len(file_content),
        "message": "Evidence uploaded successfully.",
    }


@router.post("/evidence/extract")
async def extract_evidence_text(
    file_id: str,
):

    evidence_files = list(
        EVIDENCE_DIR.glob(f"{file_id}.*")
    )

    if not evidence_files:

        raise HTTPException(
            status_code=404,
            detail="Evidence file not found.",
        )

    file_path = evidence_files[0]
    extension = file_path.suffix.lower()

    try:

        # PDF text extraction
        if extension == ".pdf":

            reader = PdfReader(str(file_path))

            pages = []

            for page in reader.pages:

                page_text = page.extract_text() or ""

                if page_text.strip():
                    pages.append(page_text.strip())

            extracted_text = "\n\n".join(pages)

        # DOCX text extraction
        elif extension == ".docx":

            document = Document(str(file_path))

            paragraphs = [
                paragraph.text.strip()
                for paragraph in document.paragraphs
                if paragraph.text.strip()
            ]

            extracted_text = "\n".join(paragraphs)

        # Images will be handled by OCR in the next step.
        elif extension in {".jpg", ".jpeg", ".png"}:

            return {
                "success": True,
                "file_id": file_id,
                "filename": file_path.name,
                "extraction_status": "OCR_PENDING",
                "text": "",
                "message": (
                    "Image uploaded successfully. "
                    "OCR extraction will be added in the next step."
                ),
            }

        else:

            raise HTTPException(
                status_code=400,
                detail="Unsupported evidence format.",
            )

        return {
            "success": True,
            "file_id": file_id,
            "filename": file_path.name,
            "extraction_status": (
                "TEXT_EXTRACTED"
                if extracted_text.strip()
                else "NO_TEXT_FOUND"
            ),
            "text": extracted_text,
            "character_count": len(extracted_text),
            "message": (
                "Evidence text extracted successfully."
                if extracted_text.strip()
                else "No selectable text was found in the document."
            ),
        }

    except HTTPException:
        raise

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Evidence extraction failed: {e}",
        )
