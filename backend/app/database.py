from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Load the DATABASE_URL from environment variables
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set")

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Create a configured "SessionLocal" class for session handling
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for defining models
Base = declarative_base()