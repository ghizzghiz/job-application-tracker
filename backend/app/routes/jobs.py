from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas
from app.database import SessionLocal
#from app.routes.auth import get_current_user
from app.routes.auth_get_user import get_current_user

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/jobs", response_model=schemas.JobApplication)
def create_job(
    job: schemas.JobApplicationCreate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user), 
):
    return crud.create_job(db=db, job=job, user_id=current_user.id)


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
    """Delete a job by its ID."""
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
    """Get a job by its ID."""
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
    """Update a job by its ID."""
    db_job = crud.update_job(db=db, job_id=job_id, updated_job=updated_job)
    if not db_job or db_job.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Job not found")
    return db_job