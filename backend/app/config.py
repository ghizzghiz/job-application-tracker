from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    SENDGRID_API_KEY: str  = "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"
    FROM_EMAIL: str = "iseul.gr@gmail.com"

    # AWS S3 Configuration
    AWS_ACCESS_KEY_ID: str = "AKIAT7JJVGSFZW7AFOWX"
    AWS_SECRET_ACCESS_KEY: str = "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"
    AWS_S3_BUCKET_NAME: str = "personaljobtrackerbucket"
    AWS_REGION: str = "us-east-2"

    class Config:
        env_file = ".env"

settings = Settings()
#print("settings.SECRET_KEY is: ")
#print(settings.SECRET_KEY)
#print("-------------------------\n-------------------------\n\n")