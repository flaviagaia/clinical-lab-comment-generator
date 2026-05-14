from __future__ import annotations

from fastapi import FastAPI
from pydantic import BaseModel, Field

from src.pipeline import ClinicalLabCommentGeneratorPipeline


app = FastAPI(title="Clinical Lab Comment Generator")
pipeline = ClinicalLabCommentGeneratorPipeline()


class CommentRequest(BaseModel):
    hemoglobin_g_dl: float = Field(..., ge=0.0, le=25.0)
    wbc_k_ul: float = Field(..., ge=0.0, le=100.0)
    platelets_k_ul: float = Field(..., ge=0.0, le=2000.0)
    creatinine_mg_dl: float = Field(..., ge=0.0, le=20.0)
    egfr_ml_min: float = Field(..., ge=0.0, le=200.0)
    alt_u_l: float = Field(..., ge=0.0, le=5000.0)
    ast_u_l: float = Field(..., ge=0.0, le=5000.0)
    a1c_percent: float = Field(..., ge=0.0, le=20.0)
    glucose_mg_dl: float = Field(..., ge=0.0, le=1000.0)
    ldl_mg_dl: float = Field(..., ge=0.0, le=500.0)
    triglycerides_mg_dl: float = Field(..., ge=0.0, le=5000.0)
    crp_mg_l: float = Field(..., ge=0.0, le=500.0)
    clinical_context: str = ""
    top_k: int = Field(default=5, ge=1, le=10)


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "service": "clinical-lab-comment-generator"}


@app.post("/generate-comment")
def generate_comment(payload: CommentRequest) -> dict:
    return pipeline.run(**payload.model_dump())
