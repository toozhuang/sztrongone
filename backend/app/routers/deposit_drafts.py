from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.db import get_session
from app.models.deposit_draft import DepositDraft, DepositDraftCreate, DepositDraftRead, DepositDraftUpdate

router = APIRouter()

@router.get("/", response_model=List[DepositDraftRead])
def list_drafts(session: Session = Depends(get_session)):
    return session.exec(select(DepositDraft)).all()

@router.post("/", response_model=DepositDraftRead)
def create_draft(payload: DepositDraftCreate, session: Session = Depends(get_session)):
    obj = DepositDraft.from_orm(payload)
    session.add(obj)
    session.commit()
    session.refresh(obj)
    return obj

@router.get("/{draft_id}", response_model=DepositDraftRead)
def get_draft(draft_id: int, session: Session = Depends(get_session)):
    obj = session.get(DepositDraft, draft_id)
    if not obj:
        raise HTTPException(404, "Draft not found")
    return obj

@router.put("/{draft_id}", response_model=DepositDraftRead)
def update_draft(draft_id: int, payload: DepositDraftUpdate, session: Session = Depends(get_session)):
    obj = session.get(DepositDraft, draft_id)
    if not obj:
        raise HTTPException(404, "Draft not found")
    data = payload.dict(exclude_unset=True)
    for k, v in data.items():
        setattr(obj, k, v)
    session.add(obj)
    session.commit()
    session.refresh(obj)
    return obj

@router.delete("/{draft_id}")
def delete_draft(draft_id: int, session: Session = Depends(get_session)):
    obj = session.get(DepositDraft, draft_id)
    if not obj:
        raise HTTPException(404, "Draft not found")
    session.delete(obj)
    session.commit()
    return {"ok": True}

@router.post("/{draft_id}/confirm")
def confirm_draft(draft_id: int, session: Session = Depends(get_session)):
    draft = session.get(DepositDraft, draft_id)
    if not draft:
        raise HTTPException(404, "Draft not found")
    if draft.status != "pending":
        raise HTTPException(400, "Draft already processed")
    
    # 验证必填字段
    if not all([draft.institution_id, draft.account_id, draft.principal, draft.start_date]):
        raise HTTPException(400, "Missing required fields")
    
    # 去重检查（简化版）
    from app.models.deposit import Deposit
    existing = session.exec(
        select(Deposit).where(
            Deposit.account_id == draft.account_id,
            Deposit.principal == draft.principal,
            Deposit.start_date == draft.start_date
        )
    ).first()
    if existing:
        raise HTTPException(409, "Duplicate deposit detected")
    
    # 创建正式记录
    from app.models.deposit import Deposit
    deposit = Deposit(
        account_id=draft.account_id,
        principal=draft.principal,
        start_date=draft.start_date,
        maturity_date=draft.maturity_date,
        rate_apy=draft.rate_apy,
        interest_method=draft.interest_method,
        compounding_freq=draft.compounding_freq,
        auto_renew=draft.auto_renew,
        notes=draft.notes
    )
    session.add(deposit)
    
    # 更新草稿状态
    draft.status = "confirmed"
    session.add(draft)
    session.commit()
    session.refresh(deposit)
    
    return {"deposit_id": deposit.id, "status": "confirmed"}

@router.post("/{draft_id}/reject")
def reject_draft(draft_id: int, session: Session = Depends(get_session)):
    draft = session.get(DepositDraft, draft_id)
    if not draft:
        raise HTTPException(404, "Draft not found")
    if draft.status != "pending":
        raise HTTPException(400, "Draft already processed")
    
    draft.status = "rejected"
    session.add(draft)
    session.commit()
    return {"status": "rejected"}
