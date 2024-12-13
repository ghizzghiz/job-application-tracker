from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from typing import Optional
from datetime import date
from sqlalchemy.orm import Session
from app import crud, schemas
from app.database import SessionLocal
#from app.routes.auth import get_current_user
from app.routes.auth_get_user import get_current_user
from app.utils import upload_file_to_s3

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/jobs", response_model=schemas.JobApplication)
async def create_job(
    job_title: str = Form(...),
    company: Optional[str] = Form(None),
    location: Optional[str] = Form(None),
    application_date: Optional[date] = Form(None),
    status: Optional[str] = Form(None),
    comments: Optional[str] = Form(None),
    cv: Optional[UploadFile] = File(None),
    cover_letter: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user),
):
    cv_url = upload_file_to_s3(cv.file, cv.filename, folder="cvs") if cv else None
    cover_letter_url = upload_file_to_s3(cover_letter.file, cover_letter.filename, folder="cover_letters") if cover_letter else None

    job_data = {
        "job_title": job_title,
        "company": company,
        "location": location,
        "application_date": application_date,
        "status": status,
        "comments": comments,
        "cv": cv_url,
        "cover_letter": cover_letter_url,
    }
    return crud.create_job(db=db, job=schemas.JobApplicationCreate(**job_data), user_id=current_user.id)

@router.get("/jobs", response_model=list[schemas.JobApplication])
def list_job(
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user), 
):
    return crud.get_jobs(db=db, user_id=current_user.id)

@router.delete("/jobs/{job_id}", response_model=dict)
def delete_job(
    job_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    db_job = crud.get_job_by_id(db=db, job_id=job_id)
    if not db_job or db_job.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Job not found")
    crud.delete_job(db=db, job_id=job_id)
    return {"detail": "Job deleted"}

# Get one job by id
@router.get("/jobs/{job_id}", response_model=schemas.JobApplication)
def get_job_by_id(
    job_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user), 
):
    db_job = crud.get_job_by_id(db=db, job_id=job_id)
    if not db_job or db_job.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Job not found")
    return db_job

# Update a job
@router.patch("/jobs/{job_id}", response_model=schemas.JobApplication)
def update_job_by_id(
    job_id: int,
    updated_job: schemas.UpdatedJob,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user), 
):
    db_job = crud.update_job(db=db, job_id=job_id, updated_job=updated_job)
    if not db_job or db_job.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Job not found")
    return db_job

# Upload document using AWS S3 
@router.post("/jobs/{job_id}/upload", response_model=dict)
def upload_job_materials(
    job_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user),
):
    db_job = crud.get_job_by_id(db=db, job_id=job_id)
    if not db_job or db_job.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Job not found")

    file_url = upload_file_to_s3(file.file, file.filename)
    return {"file_url": file_url}