from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import or_
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/messages", tags=["messages"])


@router.post("/", response_model=schemas.MessageRead, status_code=status.HTTP_201_CREATED)
def send_message(payload: schemas.MessageCreate, db: Session = Depends(get_db)):
    if payload.sender_family_id is None and payload.sender_caregiver_id is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Sender is required")
    if payload.receiver_family_id is None and payload.receiver_caregiver_id is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Receiver is required")

    if payload.sender_family_id is not None:
        family = db.query(models.FamilyMember).filter(models.FamilyMember.id == payload.sender_family_id).first()
        if not family:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sender family not found")
    if payload.sender_caregiver_id is not None:
        caregiver = db.query(models.Caregiver).filter(models.Caregiver.id == payload.sender_caregiver_id).first()
        if not caregiver:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sender caregiver not found")

    if payload.receiver_family_id is not None:
        family = db.query(models.FamilyMember).filter(models.FamilyMember.id == payload.receiver_family_id).first()
        if not family:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Receiver family not found")
    if payload.receiver_caregiver_id is not None:
        caregiver = db.query(models.Caregiver).filter(models.Caregiver.id == payload.receiver_caregiver_id).first()
        if not caregiver:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Receiver caregiver not found")

    message = models.Message(
        sender_family_id=payload.sender_family_id,
        sender_caregiver_id=payload.sender_caregiver_id,
        receiver_family_id=payload.receiver_family_id,
        receiver_caregiver_id=payload.receiver_caregiver_id,
        content=payload.content,
    )
    db.add(message)
    db.commit()
    db.refresh(message)
    return message


@router.get("/", response_model=List[schemas.MessageRead])
def list_messages(
    family_id: Optional[int] = Query(default=None),
    caregiver_id: Optional[int] = Query(default=None),
    db: Session = Depends(get_db),
):
    query = db.query(models.Message)

    if family_id is not None:
        query = query.filter(
            or_(
                models.Message.sender_family_id == family_id,
                models.Message.receiver_family_id == family_id,
            )
        )
    if caregiver_id is not None:
        query = query.filter(
            or_(
                models.Message.sender_caregiver_id == caregiver_id,
                models.Message.receiver_caregiver_id == caregiver_id,
            )
        )

    return query.order_by(models.Message.created_at.asc()).all()
