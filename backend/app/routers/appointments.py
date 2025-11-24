from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/appointments", tags=["appointments"])


@router.post("/", response_model=schemas.AppointmentRead, status_code=status.HTTP_201_CREATED)
def create_appointment(payload: schemas.AppointmentCreate, db: Session = Depends(get_db)):
    caregiver = db.query(models.Caregiver).filter(models.Caregiver.id == payload.caregiver_id).first()
    if not caregiver:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Caregiver not found")

    family = db.query(models.FamilyMember).filter(models.FamilyMember.id == payload.family_id).first()
    if not family:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Family member not found")

    appointment = models.Appointment(
        caregiver_id=payload.caregiver_id,
        family_id=payload.family_id,
        appointment_date=payload.appointment_date,
        start_time=payload.start_time,
        duration_hours=payload.duration_hours,
        status=payload.status or "pending",
        notes=payload.notes,
    )
    db.add(appointment)
    db.commit()
    db.refresh(appointment)
    return appointment


@router.get("/", response_model=List[schemas.AppointmentRead])
def list_appointments(
    caregiver_id: Optional[int] = Query(default=None),
    family_id: Optional[int] = Query(default=None),
    status_filter: Optional[str] = Query(default=None),
    db: Session = Depends(get_db),
):
    query = db.query(models.Appointment)

    if caregiver_id is not None:
        query = query.filter(models.Appointment.caregiver_id == caregiver_id)
    if family_id is not None:
        query = query.filter(models.Appointment.family_id == family_id)
    if status_filter:
        query = query.filter(models.Appointment.status == status_filter)

    return query.order_by(models.Appointment.appointment_date.desc()).all()


@router.get("/{appointment_id}", response_model=schemas.AppointmentRead)
def get_appointment(appointment_id: int, db: Session = Depends(get_db)):
    appointment = db.query(models.Appointment).filter(models.Appointment.id == appointment_id).first()
    if not appointment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Appointment not found")
    return appointment


@router.patch("/{appointment_id}", response_model=schemas.AppointmentRead)
def update_appointment(appointment_id: int, payload: schemas.AppointmentUpdate, db: Session = Depends(get_db)):
    appointment = db.query(models.Appointment).filter(models.Appointment.id == appointment_id).first()
    if not appointment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Appointment not found")

    update_data = payload.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(appointment, field, value)

    db.commit()
    db.refresh(appointment)
    return appointment


@router.delete("/{appointment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_appointment(appointment_id: int, db: Session = Depends(get_db)):
    appointment = db.query(models.Appointment).filter(models.Appointment.id == appointment_id).first()
    if not appointment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Appointment not found")

    db.delete(appointment)
    db.commit()
    return None
