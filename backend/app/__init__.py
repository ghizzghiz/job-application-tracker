from fastapi import FastAPI
from .routes import auth, jobs, reminders

app = FastAPI()

# Register API routers
app.include_router(auth.router, prefix="/auth")
app.include_router(jobs.router, prefix="/jobs")
app.include_router(reminders.router, prefix="/reminders")
