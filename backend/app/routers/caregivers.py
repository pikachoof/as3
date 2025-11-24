from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db
from ..utils import hash_password

router = APIRouter(prefix="/caregivers", tags=["caregivers"])


@router.post("/", response_model=schemas.CaregiverRead, status_code=status.HTTP_201_CREATED)
def create_caregiver(payload: schemas.CaregiverCreate, db: Session = Depends(get_db)):
    existing = db.query(models.Caregiver).filter(models.Caregiver.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    caregiver = models.Caregiver(
        first_name=payload.first_name,
        last_name=payload.last_name,
        caregiver_type=payload.caregiver_type,
        gender=payload.gender,
        photo_url=payload.photo_url,
        email=payload.email,
        phone=payload.phone,
        city=payload.city,
        hourly_rate=payload.hourly_rate,
        bio=payload.bio,
        password_hash=hash_password(payload.password),
    )
    db.add(caregiver)
    db.commit()
    db.refresh(caregiver)
    return caregiver


@router.get("/", response_model=list[schemas.CaregiverRead])
def list_caregivers(
    caregiver_type: Optional[str] = Query(default=None),
    city: Optional[str] = Query(default=None),
    min_rate: Optional[float] = Query(default=None, ge=0),
    max_rate: Optional[float] = Query(default=None, ge=0),
    db: Session = Depends(get_db),
):
    query = db.query(models.Caregiver)

    if caregiver_type:
        query = query.filter(models.Caregiver.caregiver_type == caregiver_type)
    if city:
        query = query.filter(models.Caregiver.city.ilike(f"%{city}%"))
    if min_rate is not None:
        query = query.filter(models.Caregiver.hourly_rate >= min_rate)
    if max_rate is not None:
        query = query.filter(models.Caregiver.hourly_rate <= max_rate)

    return query.order_by(models.Caregiver.last_name, models.Caregiver.first_name).all()


@router.get("/{caregiver_id}", response_model=schemas.CaregiverRead)
def get_caregiver(caregiver_id: int, db: Session = Depends(get_db)):
    caregiver = db.query(models.Caregiver).filter(models.Caregiver.id == caregiver_id).first()
    if not caregiver:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Caregiver not found")
    return caregiver


@router.patch("/{caregiver_id}", response_model=schemas.CaregiverRead)
def update_caregiver(caregiver_id: int, payload: schemas.CaregiverUpdate, db: Session = Depends(get_db)):
    caregiver = db.query(models.Caregiver).filter(models.Caregiver.id == caregiver_id).first()
    if not caregiver:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Caregiver not found")

    update_data = payload.dict(exclude_unset=True)

    if "email" in update_data:
        email_owner = (
            db.query(models.Caregiver)
            .filter(models.Caregiver.email == update_data["email"], models.Caregiver.id != caregiver_id)
            .first()
        )
        if email_owner:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already in use")

    password_value = update_data.pop("password", None)
    if password_value:
        setattr(caregiver, "password_hash", hash_password(password_value))

    for field, value in update_data.items():
        setattr(caregiver, field, value)

    db.commit()
    db.refresh(caregiver)
    return caregiver


@router.delete("/{caregiver_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_caregiver(caregiver_id: int, db: Session = Depends(get_db)):
    caregiver = db.query(models.Caregiver).filter(models.Caregiver.id == caregiver_id).first()
    if not caregiver:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Caregiver not found")

    db.delete(caregiver)
    db.commit()
    return None
