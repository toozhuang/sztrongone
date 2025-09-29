from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select
from app.db import get_session
from sqlmodel import Session
from app.models.institution import Institution, InstitutionCreate, InstitutionRead, InstitutionUpdate

router = APIRouter()

@router.get("/", response_model=List[InstitutionRead])
def list_institutions(session: Session = Depends(get_session)):
    return session.exec(select(Institution)).all()

@router.post("/", response_model=InstitutionRead)
def create_institution(payload: InstitutionCreate, session: Session = Depends(get_session)):
    inst = Institution.from_orm(payload)
    session.add(inst)
    session.commit()
    session.refresh(inst)
    return inst

@router.get("/{inst_id}", response_model=InstitutionRead)
def get_institution(inst_id: int, session: Session = Depends(get_session)):
    inst = session.get(Institution, inst_id)
    if not inst:
        raise HTTPException(404, "Institution not found")
    return inst

@router.put("/{inst_id}", response_model=InstitutionRead)
def update_institution(inst_id: int, payload: InstitutionUpdate, session: Session = Depends(get_session)):
    inst = session.get(Institution, inst_id)
    if not inst:
        raise HTTPException(404, "Institution not found")
    data = payload.dict(exclude_unset=True)
    for k, v in data.items():
        setattr(inst, k, v)
    session.add(inst)
    session.commit()
    session.refresh(inst)
    return inst

@router.delete("/{inst_id}")
def delete_institution(inst_id: int, session: Session = Depends(get_session)):
    inst = session.get(Institution, inst_id)
    if not inst:
        raise HTTPException(404, "Institution not found")
    session.delete(inst)
    session.commit()
    return {"ok": True}
