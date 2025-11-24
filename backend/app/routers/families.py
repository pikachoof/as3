from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db
from ..utils import hash_password

router = APIRouter(prefix="/families", tags=["families"])


@router.post("/", response_model=schemas.FamilyMemberRead, status_code=status.HTTP_201_CREATED)
def create_family_member(payload: schemas.FamilyMemberCreate, db: Session = Depends(get_db)):
    existing = db.query(models.FamilyMember).filter(models.FamilyMember.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    family = models.FamilyMember(
        first_name=payload.first_name,
        last_name=payload.last_name,
        email=payload.email,
        phone=payload.phone,
        password_hash=hash_password(payload.password),
        city=payload.city,
        address=payload.address,
        care_recipient_info=payload.care_recipient_info,
        house_rules=payload.house_rules,
    )
    db.add(family)
    db.commit()
    db.refresh(family)
    return family


@router.get("/", response_model=List[schemas.FamilyMemberRead])
def list_family_members(db: Session = Depends(get_db)):
    return db.query(models.FamilyMember).order_by(models.FamilyMember.last_name).all()


@router.get("/{family_id}", response_model=schemas.FamilyMemberRead)
def get_family_member(family_id: int, db: Session = Depends(get_db)):
    family = db.query(models.FamilyMember).filter(models.FamilyMember.id == family_id).first()
    if not family:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Family member not found")
    return family


@router.patch("/{family_id}", response_model=schemas.FamilyMemberRead)
def update_family_member(family_id: int, payload: schemas.FamilyMemberUpdate, db: Session = Depends(get_db)):
    family = db.query(models.FamilyMember).filter(models.FamilyMember.id == family_id).first()
    if not family:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Family member not found")

    update_data = payload.dict(exclude_unset=True)

    if "email" in update_data:
        email_owner = (
            db.query(models.FamilyMember)
            .filter(models.FamilyMember.email == update_data["email"], models.FamilyMember.id != family_id)
            .first()
        )
        if email_owner:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already in use")

    password_value = update_data.pop("password", None)
    if password_value:
        setattr(family, "password_hash", hash_password(password_value))

    for field, value in update_data.items():
        setattr(family, field, value)

    db.commit()
    db.refresh(family)
    return family


@router.delete("/{family_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_family_member(family_id: int, db: Session = Depends(get_db)):
    family = db.query(models.FamilyMember).filter(models.FamilyMember.id == family_id).first()
    if not family:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Family member not found")

    db.delete(family)
    db.commit()
    return None
