from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, crud, models
from app.database import SessionLocal
#from app.routes.auth import get_current_user
from app.routes.auth_get_user import get_current_user
from app.utils import send_email
import threading

router = APIRouter()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

'''@router.post("/reminders", response_model=schemas.Reminder)
def create_reminder(
    reminder: schemas.ReminderCreate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    """Create a new reminder for a job application."""
    db_reminder = crud.create_reminder(db=db, reminder=reminder, user_id=current_user.id)
    return db_reminder


@router.post("/reminders", response_model=schemas.Reminder)
def create_reminder(db: Session, reminder: schemas.ReminderCreate, user_id: int):
    # Fetch the user's email from the database
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Create the reminder in the database
    db_reminder = models.Reminder(
        reminder_description=reminder.reminder_description,
        reminder_date=reminder.reminder_date,
        owner_id=user_id,
    )
    db.add(db_reminder)
    db.commit()
    db.refresh(db_reminder)
    
    # Schedule an email notification
    threading.Thread(target=send_email, args=(user.email, db_reminder)).start()

    return db_reminder
'''

@router.post("/reminders", response_model=schemas.Reminder)
def create_reminder(
    reminder: schemas.ReminderCreate,
    db: Session = Depends(get_db),  # Inject the database session
    current_user: schemas.User = Depends(get_current_user),  # Get the authenticated user
):
    # Fetch the user's email
    user_email = current_user.email
    if not user_email:
        raise HTTPException(status_code=404, detail="User email not found")

    # Create the reminder in the database
    db_reminder = models.Reminder(
        reminder_description=reminder.reminder_description,
        reminder_date=reminder.reminder_date,
        owner_id=current_user.id,
    )
    db.add(db_reminder)
    db.commit()
    db.refresh(db_reminder)

    # Schedule an email notification
    threading.Thread(target=send_email, args=(user_email, db_reminder)).start()

    return db_reminder

@router.get("/reminders", response_model=list[schemas.Reminder])
def get_reminders(
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    """Retrieve all reminders for the authenticated user."""
    return crud.get_reminders(db=db, user_id=current_user.id)

@router.delete("/reminders/{reminder_id}", response_model=dict)
def delete_reminder(
    reminder_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    """Delete a reminder by its ID."""
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
    """Get a reminder by its ID."""
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
    """Update a reminder by its ID."""
    db_reminder = crud.update_reminder(db=db, reminder_id=reminder_id, updated_reminder=updated_reminder)
    if not db_reminder or db_reminder.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Reminder not found")
    return db_reminder