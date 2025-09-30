import json
from datetime import datetime
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlmodel import Session
from app.db import get_session
from app.models.ocr import OcrJob
from app.models.file import StoredFile
from app.models.deposit_draft import DepositDraft
from app.services.ocr_exec import run_ocr

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

@router.post("/jobs/{job_id}/run")
def run_job(job_id: int, session: Session = Depends(get_session)):
    job = session.get(OcrJob, job_id)
    if not job:
        raise HTTPException(404, "OCR job not found")
    file = session.get(StoredFile, job.file_id)
    if not file:
        raise HTTPException(404, "File not found")
    try:
        result = run_ocr(file.storage_path)
        job.status = "success"
        job.parsed_json = json.dumps(result, ensure_ascii=False)
    except Exception as e:
        job.status = "failed"
        job.error_message = str(e)
    job.finished_at = datetime.utcnow()
    session.add(job)
    session.commit()
    session.refresh(job)
    return {"job_id": job.id, "status": job.status, "parsed": job.parsed_json}

@router.post("/jobs/{job_id}/create-draft")
def create_draft_from_ocr(job_id: int, session: Session = Depends(get_session)):
    job = session.get(OcrJob, job_id)
    if not job:
        raise HTTPException(404, "OCR job not found")
    if job.status != "success":
        raise HTTPException(400, "OCR job not completed successfully")
    
    # 解析OCR结果
    parsed_data = json.loads(job.parsed_json or "{}")
    
    # 创建草稿
    draft = DepositDraft(
        ocr_job_id=job_id,
        principal=float(parsed_data.get("principal_guess", 0)) if parsed_data.get("principal_guess") else None,
        rate_apy=float(parsed_data.get("rate_apy_guess", 0)) if parsed_data.get("rate_apy_guess") else None,
        raw_parsed=job.parsed_json,
        status="pending"
    )
    session.add(draft)
    session.commit()
    session.refresh(draft)
    
    return {"draft_id": draft.id, "status": "created"}
