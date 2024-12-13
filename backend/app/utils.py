from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from app.config import settings
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from botocore.exceptions import NoCredentialsError
import boto3
from apscheduler.events import EVENT_JOB_ADDED, EVENT_JOB_EXECUTED, EVENT_JOB_ERROR

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Hash a plain-text password for secure storage
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# Verify that the plain password matches the hashed password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# Generate a JWT access token with an expiration time
def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    to_encode = data.copy()
    expire = datetime.now() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

# Decode a JWT token to retrieve user information
def decode_access_token(token: str) -> dict:
    try:
        decoded_data = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return decoded_data
    except JWTError:
        return None

# Send email using SendGrid
## Initialize APScheduler
jobstores = {
    'default': SQLAlchemyJobStore(url=settings.DATABASE_URL)
}
scheduler = BackgroundScheduler(jobstores=jobstores)
scheduler.start()

def job_listener(event):
    if hasattr(event, 'exception') and event.exception:
        print(f"Job {event.job_id} failed with exception: {event.exception}")
    else:
        print(f"Job {event.job_id} executed successfully or scheduled.")

scheduler.add_listener(job_listener, EVENT_JOB_ADDED | EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)

def send_email(to_email, subject, content):
    message = Mail(
        from_email=settings.FROM_EMAIL,
        to_emails=to_email,
        subject=subject,
        plain_text_content=content,
    )
    try:
        sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
        response = sg.send(message)
        print(f"Email sent to {to_email}. Response status: {response.status_code}")
    except Exception as e:
        print(f"Error sending email: {e}")

def schedule_email(to_email, reminder):
    subject = reminder.reminder_description
    content = (
        f"Hi,\n\n"
        f"Here's your reminder: {reminder.reminder_description}.\n\n"
        f"It's scheduled for {reminder.reminder_date}.\n\n"
        f"Don't forget to complete it on time!\n\n"
        f"Best regards,\n"
        f"Your Personal Job Tracker App"
    )

    # Convert both dates to timezone-aware objects
    reminder_date = reminder.reminder_date
    if reminder_date.tzinfo is None:  # If reminder_date is naive
        reminder_date = reminder_date.replace(tzinfo=timezone.utc)

    local_now = datetime.now(timezone.utc)

    if reminder_date <= local_now:
        raise ValueError("Reminder date must be in the future.")

    scheduler.add_job(
        send_email,
        trigger='date',
        run_date=reminder_date,
        args=[to_email, subject, content],
        id=f"email_{reminder.id}",
        replace_existing=True,
    )
    print(f"Email scheduled for {reminder_date}")

# Uploads files to AWS S3
def upload_file_to_s3(file, filename, folder=""):
    if not file or not filename:
        return None
    s3 = boto3.client(
        "s3",
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_REGION,
    )
    try:
        s3_path = f"{folder}/{filename}" if folder else filename
        s3.upload_fileobj(file, settings.AWS_S3_BUCKET_NAME, s3_path)
        file_url = f"https://{settings.AWS_S3_BUCKET_NAME}.s3.amazonaws.com/{s3_path}"
        return file_url
    except NoCredentialsError:
        raise ValueError("AWS credentials not available")
    except Exception as e:
        raise ValueError(f"Failed to upload to S3: {e}")