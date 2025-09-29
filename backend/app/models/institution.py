from typing import Optional
from sqlmodel import SQLModel, Field

class InstitutionBase(SQLModel):
    name: str
    type: str = "bank"
    metadata_json: Optional[str] = None

class Institution(InstitutionBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

class InstitutionCreate(InstitutionBase):
    pass

class InstitutionRead(InstitutionBase):
    id: int

class InstitutionUpdate(SQLModel):
    name: Optional[str] = None
    type: Optional[str] = None
    metadata_json: Optional[str] = None
