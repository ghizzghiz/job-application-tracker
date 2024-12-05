from fastapi import FastAPI
from app.config import settings
from app.models import Base
from app.routes import auth, jobs, reminders
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.openapi.utils import get_openapi
from app.database import SessionLocal, engine

app = FastAPI()

# Enables CORS -- Cross-origin resource sharing (CORS) is a mechanism 
# that allows secure data transfers and requests between servers and browsers.
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Adjust as needed
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, OPTIONS, etc.)
    allow_headers=["*"],  # Allow all headers
)

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Job Application Tracker",
        version="1.0.0",
        description="An API for tracking job applications",
        routes=app.routes,
    )
    # Modify the security scheme
    openapi_schema["components"]["securitySchemes"]["OAuth2PasswordBearer"] = {
        "type": "http",
        "scheme": "bearer",
        "bearerFormat": "JWT",
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi


# Database setup
"""SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)"""

# Register routers
app.include_router(auth.router, tags=["auth"]) 
app.include_router(jobs.router, tags=["jobs"]) 
app.include_router(reminders.router, tags=["reminders"]) 

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to your Personal Job Application Tracker API"}

# Helps in debugging -- List all routes
@app.on_event("startup")
async def list_routes():
    for route in app.routes:
        print(f"Path: {route.path}, Name: {route.name}, Methods: {route.methods}")

# Checks http://localhost:8000/config-test to confirm all configurations are loaded correctly
@app.get("/config-test")
def config_test():
    return settings.dict()