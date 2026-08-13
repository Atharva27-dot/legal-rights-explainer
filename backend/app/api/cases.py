from fastapi import APIRouter, HTTPException

from app.schemas.case_schema import (
    SaveCaseRequest,
)

from app.services.case_service import (
    case_service,
)

router = APIRouter(
    prefix="/cases",
    tags=["My Legal Cases"],
)


# =====================================
# Save Case
# =====================================

@router.post("/save")
def save_case(request: SaveCaseRequest):

    try:

        return case_service.save_case(request)

    except Exception as e:

        raise HTTPException(

            status_code=500,

            detail=str(e)

        )


# =====================================
# Get All Cases
# =====================================

@router.get("")
def get_cases():

    try:

        return {

            "cases": case_service.get_cases()

        }

    except Exception as e:

        raise HTTPException(

            status_code=500,

            detail=str(e)

        )


# =====================================
# Get Single Case
# =====================================

@router.get("/{case_id}")
def get_case(case_id: str):

    case = case_service.get_case(case_id)

    if case is None:

        raise HTTPException(

            status_code=404,

            detail="Case not found."

        )

    return case


# =====================================
# Delete Case
# =====================================

@router.delete("/{case_id}")
def delete_case(case_id: str):

    try:

        return case_service.delete_case(case_id)

    except Exception as e:

        raise HTTPException(

            status_code=500,

            detail=str(e)

        )