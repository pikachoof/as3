from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/job-posts", tags=["job posts"])


@router.post("/", response_model=schemas.JobPostRead, status_code=status.HTTP_201_CREATED)
def create_job_post(payload: schemas.JobPostCreate, db: Session = Depends(get_db)):
    family = db.query(models.FamilyMember).filter(models.FamilyMember.id == payload.family_id).first()
    if not family:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Family member not found")

    job_post = models.JobPost(
        family_id=payload.family_id,
        title=payload.title,
        caregiver_type=payload.caregiver_type,
        city=payload.city,
        care_recipient_age=payload.care_recipient_age,
        description=payload.description,
        preferred_time_slots=payload.preferred_time_slots or [],
        frequency=payload.frequency,
        requirements=payload.requirements,
    )
    db.add(job_post)
    db.commit()
    db.refresh(job_post)
    return job_post


@router.get("/", response_model=List[schemas.JobPostRead])
def list_job_posts(
    caregiver_type: Optional[str] = Query(default=None),
    city: Optional[str] = Query(default=None),
    db: Session = Depends(get_db),
):
    query = db.query(models.JobPost)

    if caregiver_type:
        query = query.filter(models.JobPost.caregiver_type == caregiver_type)
    if city:
        query = query.filter(models.JobPost.city.ilike(f"%{city}%"))

    return query.order_by(models.JobPost.created_at.desc()).all()


@router.get("/{job_post_id}", response_model=schemas.JobPostRead)
def get_job_post(job_post_id: int, db: Session = Depends(get_db)):
    job_post = db.query(models.JobPost).filter(models.JobPost.id == job_post_id).first()
    if not job_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job post not found")
    return job_post


@router.patch("/{job_post_id}", response_model=schemas.JobPostRead)
def update_job_post(job_post_id: int, payload: schemas.JobPostUpdate, db: Session = Depends(get_db)):
    job_post = db.query(models.JobPost).filter(models.JobPost.id == job_post_id).first()
    if not job_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job post not found")

    update_data = payload.dict(exclude_unset=True)

    for field, value in update_data.items():
        setattr(job_post, field, value)

    db.commit()
    db.refresh(job_post)
    return job_post


@router.delete("/{job_post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_job_post(job_post_id: int, db: Session = Depends(get_db)):
    job_post = db.query(models.JobPost).filter(models.JobPost.id == job_post_id).first()
    if not job_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job post not found")

    db.delete(job_post)
    db.commit()
    return None
