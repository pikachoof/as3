from datetime import date, datetime, time
from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field


class CaregiverBase(BaseModel):
    first_name: str
    last_name: str
    caregiver_type: str
    gender: Optional[str] = None
    photo_url: Optional[str] = None
    email: EmailStr
    phone: str
    city: str
    hourly_rate: float = Field(gt=0)
    bio: Optional[str] = None


class CaregiverCreate(CaregiverBase):
    password: str = Field(min_length=6)


class CaregiverUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    caregiver_type: Optional[str] = None
    gender: Optional[str] = None
    photo_url: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    city: Optional[str] = None
    hourly_rate: Optional[float] = Field(default=None, gt=0)
    bio: Optional[str] = None
    password: Optional[str] = Field(default=None, min_length=6)


class CaregiverRead(CaregiverBase):
    id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True


class FamilyMemberBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    city: str
    address: Optional[str] = None
    care_recipient_info: Optional[str] = None
    house_rules: Optional[str] = None


class FamilyMemberCreate(FamilyMemberBase):
    password: str = Field(min_length=6)


class FamilyMemberUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    city: Optional[str] = None
    address: Optional[str] = None
    care_recipient_info: Optional[str] = None
    house_rules: Optional[str] = None
    password: Optional[str] = Field(default=None, min_length=6)


class FamilyMemberRead(FamilyMemberBase):
    id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True


class JobPostBase(BaseModel):
    family_id: int
    title: str
    caregiver_type: str
    city: str
    care_recipient_age: Optional[int] = Field(default=None, ge=0)
    description: Optional[str] = None
    preferred_time_slots: List[str] = Field(default_factory=list)
    frequency: Optional[str] = None
    requirements: Optional[str] = None


class JobPostCreate(JobPostBase):
    pass


class JobPostUpdate(BaseModel):
    title: Optional[str] = None
    caregiver_type: Optional[str] = None
    city: Optional[str] = None
    care_recipient_age: Optional[int] = Field(default=None, ge=0)
    description: Optional[str] = None
    preferred_time_slots: Optional[List[str]] = None
    frequency: Optional[str] = None
    requirements: Optional[str] = None


class FamilySummary(BaseModel):
    id: int
    first_name: str
    last_name: str
    city: str

    class Config:
        orm_mode = True


class JobPostRead(JobPostBase):
    id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    family: Optional[FamilySummary]

    class Config:
        orm_mode = True


class JobApplicationBase(BaseModel):
    job_post_id: int
    caregiver_id: int
    cover_message: Optional[str] = None
    status: Optional[str] = Field(default="applied")


class JobApplicationCreate(JobApplicationBase):
    pass


class JobApplicationUpdate(BaseModel):
    cover_message: Optional[str] = None
    status: Optional[str] = None


class CaregiverSummary(BaseModel):
    id: int
    first_name: str
    last_name: str
    caregiver_type: str
    city: str

    class Config:
        orm_mode = True


class JobApplicationRead(JobApplicationBase):
    id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    caregiver: Optional[CaregiverSummary]

    class Config:
        orm_mode = True


class AppointmentBase(BaseModel):
    caregiver_id: int
    family_id: int
    appointment_date: date
    start_time: time
    duration_hours: float = Field(gt=0)
    status: Optional[str] = Field(default="pending")
    notes: Optional[str] = None


class AppointmentCreate(AppointmentBase):
    pass


class AppointmentUpdate(BaseModel):
    appointment_date: Optional[date] = None
    start_time: Optional[time] = None
    duration_hours: Optional[float] = Field(default=None, gt=0)
    status: Optional[str] = None
    notes: Optional[str] = None


class AppointmentRead(AppointmentBase):
    id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    caregiver: Optional[CaregiverSummary]
    family: Optional[FamilySummary]

    class Config:
        orm_mode = True


class MessageBase(BaseModel):
    sender_family_id: Optional[int] = None
    sender_caregiver_id: Optional[int] = None
    receiver_family_id: Optional[int] = None
    receiver_caregiver_id: Optional[int] = None
    content: str


class MessageCreate(MessageBase):
    pass


class MessageRead(MessageBase):
    id: int
    created_at: Optional[datetime]

    class Config:
        orm_mode = True
