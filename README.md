# Job Application Tracker

This project helps users manage job applications by tracking job postings, resumes, reminders, and application status.

## Setup

1. Clone the repository and navigate to the project directory.
2. Set up environment variables in the `.env` file.
3. Run `docker-compose up --build` to start the backend and database.

## Technologies Used

- FastAPI for backend
- PostgreSQL for database
- React for frontend
- Docker for containerization
- SendGrid/Twilio for notifications??????????

## Proposed Architecture
...

A backend folder
A frontend folder
A frontend folder

## Requirements
A virtual environment is initially created to have all packages and modules installed.

```python

python3 -m venv ~/tmp/job_app_env
source ~/tmp/job_app_env/bin/activate

```

We also need to check which python version is being used:
`which python3`
Output: `/opt/homebrew/bin/python3`
`python3 --version`
Output: `Python 3.13.0`

`pip3 install -r backend/requirements.txt`

`cd backend`
`alembic init alembic`



The main python libraries used are shown in the requirements.txt:
* [fastapi](): The .....
* [uvicorn]():
* [sqlalchemy]():
* [pydantic]():
* [psycopg2-binary]():
* [alembic]():


## Initial Steps
...

## API documentation

...

## Technologies Used
* pgAdmin 4
* Swagger/Postman
* Docker
* 

## Reasoning and Layers

### Backend

### Frontend

### SendGrid
pip install sendgrid
