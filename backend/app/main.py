from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router as ask_router
from app.api.complaint import router as complaint_router
from app.api.pdf import router as pdf_router
from app.api.cases import router as cases_router


app = FastAPI(
    title="Legal Rights Explainer",
    version="2.0.0"
)


# =====================================
# Routers
# =====================================

app.include_router(ask_router)

app.include_router(complaint_router)

app.include_router(pdf_router)

app.include_router(cases_router)


# =====================================
# CORS
# =====================================

app.add_middleware(
    CORSMiddleware,

    allow_origins=[
        "http://localhost:5173"
    ],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],

)