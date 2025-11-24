from sqlalchemy import JSON, Column, Date, DateTime, Float, ForeignKey, Integer, String, Text, Time
from sqlalchemy import text
from sqlalchemy.orm import relationship

from .database import Base


class Caregiver(Base):
    __tablename__ = "caregivers"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    caregiver_type = Column(String(50), nullable=False)
    gender = Column(String(50))
    photo_url = Column(String(255))
    email = Column(String(120), unique=True, nullable=False, index=True)
    phone = Column(String(50), nullable=False)
    city = Column(String(100), nullable=False)
    hourly_rate = Column(Float, nullable=False)
    bio = Column(Text)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(DateTime(timezone=True), onupdate=text("CURRENT_TIMESTAMP"))

    appointments = relationship("Appointment", back_populates="caregiver", cascade="all, delete-orphan")
    job_applications = relationship("JobApplication", back_populates="caregiver", cascade="all, delete-orphan")
    sent_messages = relationship(
        "Message",
        back_populates="sender_caregiver",
        cascade="all, delete-orphan",
        foreign_keys="Message.sender_caregiver_id",
    )
    received_messages = relationship(
        "Message",
        back_populates="receiver_caregiver",
        cascade="all, delete-orphan",
        foreign_keys="Message.receiver_caregiver_id",
    )


class FamilyMember(Base):
    __tablename__ = "family_members"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(120), unique=True, nullable=False, index=True)
    phone = Column(String(50), nullable=False)
    password_hash = Column(String(255), nullable=False)
    city = Column(String(100), nullable=False)
    address = Column(Text)
    care_recipient_info = Column(Text)
    house_rules = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(DateTime(timezone=True), onupdate=text("CURRENT_TIMESTAMP"))

    job_posts = relationship("JobPost", back_populates="family", cascade="all, delete-orphan")
    appointments = relationship("Appointment", back_populates="family", cascade="all, delete-orphan")
    sent_messages = relationship(
        "Message",
        back_populates="sender_family",
        cascade="all, delete-orphan",
        foreign_keys="Message.sender_family_id",
    )
    received_messages = relationship(
        "Message",
        back_populates="receiver_family",
        cascade="all, delete-orphan",
        foreign_keys="Message.receiver_family_id",
    )


class JobPost(Base):
    __tablename__ = "job_posts"

    id = Column(Integer, primary_key=True, index=True)
    family_id = Column(Integer, ForeignKey("family_members.id"), nullable=False)
    title = Column(String(150), nullable=False)
    caregiver_type = Column(String(50), nullable=False)
    city = Column(String(100), nullable=False)
    care_recipient_age = Column(Integer)
    description = Column(Text)
    preferred_time_slots = Column(JSON, default=list)
    frequency = Column(String(100))
    requirements = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(DateTime(timezone=True), onupdate=text("CURRENT_TIMESTAMP"))

    family = relationship("FamilyMember", back_populates="job_posts")
    applications = relationship("JobApplication", back_populates="job_post", cascade="all, delete-orphan")


class JobApplication(Base):
    __tablename__ = "job_applications"

    id = Column(Integer, primary_key=True, index=True)
    job_post_id = Column(Integer, ForeignKey("job_posts.id"), nullable=False)
    caregiver_id = Column(Integer, ForeignKey("caregivers.id"), nullable=False)
    cover_message = Column(Text)
    status = Column(String(20), default="applied", nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(DateTime(timezone=True), onupdate=text("CURRENT_TIMESTAMP"))

    job_post = relationship("JobPost", back_populates="applications")
    caregiver = relationship("Caregiver", back_populates="job_applications")


class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    caregiver_id = Column(Integer, ForeignKey("caregivers.id"), nullable=False)
    family_id = Column(Integer, ForeignKey("family_members.id"), nullable=False)
    appointment_date = Column(Date, nullable=False)
    start_time = Column(Time, nullable=False)
    duration_hours = Column(Float, nullable=False)
    status = Column(String(20), default="pending", nullable=False)
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(DateTime(timezone=True), onupdate=text("CURRENT_TIMESTAMP"))

    caregiver = relationship("Caregiver", back_populates="appointments")
    family = relationship("FamilyMember", back_populates="appointments")


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    sender_family_id = Column(Integer, ForeignKey("family_members.id"))
    sender_caregiver_id = Column(Integer, ForeignKey("caregivers.id"))
    receiver_family_id = Column(Integer, ForeignKey("family_members.id"))
    receiver_caregiver_id = Column(Integer, ForeignKey("caregivers.id"))
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=text("CURRENT_TIMESTAMP"))

    sender_family = relationship(
        "FamilyMember",
        foreign_keys=[sender_family_id],
        back_populates="sent_messages",
    )
    sender_caregiver = relationship(
        "Caregiver",
        foreign_keys=[sender_caregiver_id],
        back_populates="sent_messages",
    )
    receiver_family = relationship(
        "FamilyMember",
        foreign_keys=[receiver_family_id],
        back_populates="received_messages",
    )
    receiver_caregiver = relationship(
        "Caregiver",
        foreign_keys=[receiver_caregiver_id],
        back_populates="received_messages",
    )
