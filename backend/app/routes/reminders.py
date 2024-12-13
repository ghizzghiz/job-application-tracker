from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, crud, models
from app.database import SessionLocal
from app.routes.auth_get_user import get_current_user
from app.utils import schedule_email 
import threading

router = APIRouter()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create the reminder
@router.post("/reminders", response_model=schemas.Reminder)
def create_reminder(
    reminder: schemas.ReminderCreate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user),
):
    user_email = current_user.email
    if not user_email:
        raise HTTPException(status_code=404, detail="User email not found")

    db_reminder = models.Reminder(
        reminder_description=reminder.reminder_description,
        reminder_date=reminder.reminder_date,
        owner_id=current_user.id,
    )
    db.add(db_reminder)
    db.commit()
    db.refresh(db_reminder)

    # Schedule an email notification
    schedule_email(user_email, db_reminder)

    return db_reminder

# Retrieve all reminders for the authenticated user
@router.get("/reminders", response_model=list[schemas.Reminder])
def get_reminders(
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    return crud.get_reminders(db=db, user_id=current_user.id)

# Delete a reminder by its ID
@router.delete("/reminders/{reminder_id}", response_model=dict)
def delete_reminder(
    reminder_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    db_reminder = crud.get_reminder_by_id(db=db, reminder_id=reminder_id)
    if not db_reminder or db_reminder.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Reminder not found")
    crud.delete_reminder(db=db, reminder_id=reminder_id)
    return {"detail": "Reminder deleted"}

# Get one reminder by id
@router.get("/reminders/{reminder_id}", response_model=schemas.Reminder)
def get_reminder_by_id(
    reminder_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user), 
):
    db_reminder = crud.get_reminder_by_id(db=db, reminder_id=reminder_id)
    if not db_reminder or db_reminder.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Reminder not found")
    return db_reminder

# Update reminder
@router.patch("/reminders/{reminder_id}", response_model=schemas.Reminder)
def update_reminder_by_id(
    reminder_id: int,
    updated_reminder: schemas.UpdatedReminder,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user), 
):
    db_reminder = crud.update_reminder(db=db, reminder_id=reminder_id, updated_reminder=updated_reminder)
    if not db_reminder or db_reminder.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Reminder not found")
    return db_reminder