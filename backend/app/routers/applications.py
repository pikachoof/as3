from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/applications", tags=["job applications"])


@router.post("/", response_model=schemas.JobApplicationRead, status_code=status.HTTP_201_CREATED)
def create_application(payload: schemas.JobApplicationCreate, db: Session = Depends(get_db)):
    job_post = db.query(models.JobPost).filter(models.JobPost.id == payload.job_post_id).first()
    if not job_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job post not found")

    caregiver = db.query(models.Caregiver).filter(models.Caregiver.id == payload.caregiver_id).first()
    if not caregiver:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Caregiver not found")

    existing = (
        db.query(models.JobApplication)
        .filter(
            models.JobApplication.job_post_id == payload.job_post_id,
            models.JobApplication.caregiver_id == payload.caregiver_id,
        )
        .first()
    )
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Application already exists")

    application = models.JobApplication(
        job_post_id=payload.job_post_id,
        caregiver_id=payload.caregiver_id,
        cover_message=payload.cover_message,
        status=payload.status or "applied",
    )
    db.add(application)
    db.commit()
    db.refresh(application)
    return application


@router.get("/", response_model=List[schemas.JobApplicationRead])
def list_applications(
    job_post_id: Optional[int] = Query(default=None),
    caregiver_id: Optional[int] = Query(default=None),
    db: Session = Depends(get_db),
):
    query = db.query(models.JobApplication)

    if job_post_id is not None:
        query = query.filter(models.JobApplication.job_post_id == job_post_id)
    if caregiver_id is not None:
        query = query.filter(models.JobApplication.caregiver_id == caregiver_id)

    return query.order_by(models.JobApplication.created_at.desc()).all()


@router.get("/{application_id}", response_model=schemas.JobApplicationRead)
def get_application(application_id: int, db: Session = Depends(get_db)):
    application = db.query(models.JobApplication).filter(models.JobApplication.id == application_id).first()
    if not application:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Application not found")
    return application


@router.patch("/{application_id}", response_model=schemas.JobApplicationRead)
def update_application(application_id: int, payload: schemas.JobApplicationUpdate, db: Session = Depends(get_db)):
    application = db.query(models.JobApplication).filter(models.JobApplication.id == application_id).first()
    if not application:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Application not found")

    update_data = payload.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(application, field, value)

    db.commit()
    db.refresh(application)
    return application


@router.delete("/{application_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_application(application_id: int, db: Session = Depends(get_db)):
    application = db.query(models.JobApplication).filter(models.JobApplication.id == application_id).first()
    if not application:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Application not found")

    db.delete(application)
    db.commit()
    return None
