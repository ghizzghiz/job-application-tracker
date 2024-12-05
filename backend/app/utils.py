from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt
from app.config import settings
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from app.config import settings

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    # Hash a plain-text password for secure storage
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    # Verify that the plain password matches the hashed password
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    # Generate a JWT access token with an expiration time
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str) -> dict:
    # Decode a JWT token to retrieve user information
    try:
        decoded_data = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return decoded_data
    except JWTError:
        return None

# Send email using SendGrid
def send_email(to_email, reminder):
    subject = reminder.reminder_description  
    content = (
        f"Hi,\n\n"
        f"Here's your reminder: {reminder.reminder_description}.\n\n"
        f"It's scheduled for {reminder.reminder_date}.\n\n"
        f"Don't forget to complete it on time!\n\n"
        f"Best regards,\n"
        f"Your Personal Job Tracker App"
    )

    message = Mail(
        from_email=settings.FROM_EMAIL,
        to_emails=to_email,
        subject=subject,
        plain_text_content=content
    )
    try:
        sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
        response = sg.send(message)
        print(f"Email sent to {to_email}. Response status: {response.status_code}")
        return response.status_code
    except Exception as e:
        print(f"Error sending email: {e}")
        return None