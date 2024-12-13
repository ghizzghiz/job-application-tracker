from pydantic import BaseModel, EmailStr
from typing import Optional, Literal
from datetime import date, datetime

##############################
# USER AUTHENTICATION DETAILS
##############################

# Schema for user creation
class UserCreate(BaseModel):
    email: EmailStr
    password: str

# Schema for user login
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# Schema for user output
class User(BaseModel):
    id: int
    email: EmailStr

    class Config:
        from_attributes = True

##############################
# LOGIN RESPONSE MODEL
##############################
class LoginReturns(BaseModel):
    access_token: str
    token_type: str

##############################
# JOB APPLICATION DETAILS 
##############################

# Base schema for job applications
class JobApplicationBase(BaseModel):
    job_title: str
    company: Optional[str] = None
    location: Optional[str] = None
    application_date: Optional[date] = None
    status: Optional[Literal["Applied", "Interview Scheduled", "Offer Received", "Rejected"]] = None
    comments: Optional[str] = None
    cv: Optional[str] = None
    cover_letter: Optional[str] = None

# Schema for creating a new job application
class JobApplicationCreate(JobApplicationBase):
    pass

# Schema for reading a job application (includes the ID and owner_id)
class JobApplication(JobApplicationBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True

class UpdatedJob(BaseModel): 
    # not using JobApplicationBase inheritence b/c otherwise makes all mandatory
    job_title: Optional[str] = None
    company: Optional[str] = None
    location: Optional[str] = None
    application_date: Optional[date] = None
    status: Optional[Literal["Applied", "Interview Scheduled", "Offer Received", "Rejected"]] = None
    comments: Optional[str] = None
    cv: Optional[str] = None
    cover_letter: Optional[str] = None

    class Config:
        from_attributes = True

##############################
# REMINDER 
##############################
class ReminderBase(BaseModel):
    reminder_description: str
    reminder_date: datetime 

class ReminderCreate(ReminderBase):
    pass

class Reminder(ReminderBase):
    id: int
    owner_id: int

    class Config:
        #orm_mode = True
        from_attributes = True

class DeletedReminder(BaseModel):
    detail: str

class UpdatedReminder(BaseModel):
    reminder_description: Optional[str] = None
    reminder_date: Optional[datetime] = None

    class Config:
        from_attributes = True
