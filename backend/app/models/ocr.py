from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field

class OcrJob(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    file_id: int
    engine: str = "tesseract"
    template_id: Optional[int] = None
    status: str = "pending"
    parsed_json: Optional[str] = None
    error_message: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    finished_at: Optional[datetime] = None

class OcrTemplate(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    bank_code: str
    version: str = "v1"
    definition_json: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
