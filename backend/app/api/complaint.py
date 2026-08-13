from fastapi import APIRouter, HTTPException

from app.schemas.complaint_schema import (
    ComplaintRequest,
    ComplaintResponse,
)

from app.services.complaint_generator import (
    complaint_generator,
)

router = APIRouter(
    prefix="/complaint",
    tags=["Complaint Generator"],
)


@router.post(
    "/generate",
    response_model=ComplaintResponse,
)
def generate_complaint(request: ComplaintRequest):

    try:

        response = complaint_generator.generate(request)

        return response

    except Exception as e:

        raise HTTPException(

            status_code=500,

            detail=str(e)

        )