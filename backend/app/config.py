from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    SENDGRID_API_KEY: str  = "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"
    #"ySG.iuQbzrq8QT6tuOVJZbyXZA.K9dmZfjYCsA7LwKmbNX-lUTYjyIIds3fVbOtL4OGY8Y"
    FROM_EMAIL: str = "iseul.gr@gmail.com"

    class Config:
        env_file = ".env"

settings = Settings()
#print("settings.SECRET_KEY is: ")
#print(settings.SECRET_KEY)
#print("-------------------------\n-------------------------\n\n")