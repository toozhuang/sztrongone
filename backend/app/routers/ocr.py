from datetime import datetime
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlmodel import Session
from app.db import get_session
from app.models.ocr import OcrJob

router = APIRouter()

class OcrJobCreate(BaseModel):
    file_id: int
    engine: str | None = "tesseract"
    template_id: int | None = None

@router.post("/jobs")
def create_job(payload: OcrJobCreate, session: Session = Depends(get_session)):
    job = OcrJob(
        file_id=payload.file_id,
        engine=payload.engine or "tesseract",
        template_id=payload.template_id,
        status="pending",
    )
    session.add(job)
    session.commit()
    session.refresh(job)
    return {"job_id": job.id, "status": job.status}

@router.get("/jobs/{job_id}")
def get_job(job_id: int, session: Session = Depends(get_session)):
    job = session.get(OcrJob, job_id)
    if not job:
        raise HTTPException(404, "OCR job not found")
    return job

@router.post("/jobs/{job_id}/mock-complete")
def mock_complete(job_id: int, session: Session = Depends(get_session)):
    job = session.get(OcrJob, job_id)
    if not job:
        raise HTTPException(404, "OCR job not found")
    job.status = "success"
    job.parsed_json = "{}"
    job.finished_at = datetime.utcnow()
    session.add(job)
    session.commit()
    session.refresh(job)
    return {"job_id": job.id, "status": job.status}
