from sqlalchemy import Column, Integer, String, ForeignKey, Date, DateTime, Text
from sqlalchemy.orm import relationship
from app.database import Base
from sqlalchemy.sql import func

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    jobs = relationship("JobApplication", back_populates="owner")

class JobApplication(Base):
    __tablename__ = "job_applications"
    id = Column(Integer, primary_key=True, index=True)
    job_title = Column(String, index=True)
    company = Column(String)
    location = Column(String)
    application_date = Column(Date)
    status = Column(String)
    comments = Column(Text, nullable=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="jobs")
    # CV, Resume, Cover Letter - links stored on db for AWS S3 file storage
    cv = Column(String, nullable=True)
    cover_letter = Column(String, nullable=True)

class Reminder(Base):
    __tablename__ = "reminders"

    id = Column(Integer, primary_key=True, index=True)
    reminder_description = Column(String, nullable=False)
    reminder_date = Column(DateTime, server_default=func.now())
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)