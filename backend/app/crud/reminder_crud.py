from sqlalchemy.orm import Session
from app import models, schemas
from fastapi import Depends
from app.database import SessionLocal
from app.routes.auth_get_user import get_current_user

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create a new reminder
def create_reminder(db: Session, reminder: schemas.ReminderCreate, user_id: int):
    db_reminder = models.Reminder(
        reminder_description=reminder.reminder_description,
        reminder_date=reminder.reminder_date,
        owner_id=user_id,
    )
    db.add(db_reminder)
    db.commit()
    db.refresh(db_reminder)
    return db_reminder

# Retrieve all reminders for a specific user
def get_reminders(db: Session, user_id: int):
    return db.query(models.Reminder).filter(models.Reminder.owner_id == user_id).all()

# Retrieve a reminder by its ID
def get_reminder_by_id(db: Session, reminder_id: int):
    return db.query(models.Reminder).filter(models.Reminder.id == reminder_id).first()

# Delete a reminder by its ID
def delete_reminder(db: Session, reminder_id: int):
    db_reminder = get_reminder_by_id(db, reminder_id)
    if db_reminder:
        db.delete(db_reminder)
        db.commit()
    return db_reminder

# Update a Reminder by its ID
def update_reminder(db: Session, reminder_id: int, updated_reminder: schemas.UpdatedReminder):
    db_reminder = get_reminder_by_id(db, reminder_id)
    if not db_reminder:
        return None
    for field, value in updated_reminder.dict(exclude_unset=True).items():
        setattr(db_reminder, field, value)
    db.commit()
    db.refresh(db_reminder)
    return db_reminder