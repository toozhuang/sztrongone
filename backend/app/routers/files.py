import hashlib
from pathlib import Path
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlmodel import Session
from app.db import get_session
from app.models.file import StoredFile

UPLOAD_DIR = Path("backend/data/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

router = APIRouter()

@router.post("/upload")
async def upload_file(f: UploadFile = File(...), session: Session = Depends(get_session)):
    if f.content_type not in {"image/png", "image/jpeg", "application/pdf"}:
        raise HTTPException(400, "Unsupported file type")
    content = await f.read()
    sha = hashlib.sha256(content).hexdigest()
    dest = UPLOAD_DIR / sha
    with open(dest, "wb") as out:
        out.write(content)
    record = StoredFile(
        filename=f.filename,
        mime_type=f.content_type or "application/octet-stream",
        size_bytes=len(content),
        sha256=sha,
        storage_path=str(dest),
    )
    session.add(record)
    session.commit()
    session.refresh(record)
    return {"file_id": record.id, "sha256": sha}
