from sqlalchemy.orm import Session
from app.models import JobApplication
from app.schemas import JobApplicationCreate, UpdatedJob

def create_job(db: Session, job: JobApplicationCreate, user_id: int):
    db_job = JobApplication(**job.dict(), owner_id=user_id)
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job

def get_jobs(db: Session, user_id: int):
    return db.query(JobApplication).filter(JobApplication.owner_id == user_id).all()

def get_job_by_id(db: Session, job_id: int):
    return db.query(JobApplication).filter(JobApplication.id == job_id).first()

def delete_job(db: Session, job_id: int):
    db_job = get_job_by_id(db, job_id)
    if db_job:
        db.delete(db_job)
        db.commit()
    return db_job

def update_job(db: Session, job_id: int, updated_job: UpdatedJob):
    db_job = get_job_by_id(db, job_id)
    if not db_job:
        return None
    for field, value in updated_job.dict(exclude_unset=True).items():
        setattr(db_job, field, value)
    db.commit()
    db.refresh(db_job)
    return db_job