from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field

class StoredFile(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    filename: str
    mime_type: str
    size_bytes: int
    sha256: str
    storage_path: str
    uploaded_at: datetime = Field(default_factory=datetime.utcnow)
