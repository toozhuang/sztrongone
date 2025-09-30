from datetime import date
from typing import Optional
from sqlmodel import SQLModel, Field

class DepositDraftBase(SQLModel):
    ocr_job_id: int
    institution_id: Optional[int] = None
    account_id: Optional[int] = None
    principal: Optional[float] = None
    start_date: Optional[date] = None
    maturity_date: Optional[date] = None
    rate_apy: Optional[float] = None
    interest_method: str = "simple"
    compounding_freq: str = "none"
    auto_renew: bool = False
    notes: Optional[str] = None
    status: str = "pending"  # pending/confirmed/rejected
    raw_parsed: Optional[str] = None  # JSON from OCR

class DepositDraft(DepositDraftBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

class DepositDraftCreate(DepositDraftBase):
    pass

class DepositDraftRead(DepositDraftBase):
    id: int

class DepositDraftUpdate(SQLModel):
    institution_id: Optional[int] = None
    account_id: Optional[int] = None
    principal: Optional[float] = None
    start_date: Optional[date] = None
    maturity_date: Optional[date] = None
    rate_apy: Optional[float] = None
    interest_method: Optional[str] = None
    compounding_freq: Optional[str] = None
    auto_renew: Optional[bool] = None
    notes: Optional[str] = None
    status: Optional[str] = None
