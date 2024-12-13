# Personal Job Application Tracker
Author: Ghizlane Rehioui

This README file shows the steps to run this code.

## Project Goal
This project helps users manage job applications by tracking job postings, resumes, reminders, and application status.

## Steps to Run the Project
These are the steps to run the project: 
1. Clone the repository and navigate to the project directory.
2. Environment variables are defined in the `.env` file.
3. Run `docker-compose up --build` to start the backend, frontend, and database. All requirements will be installed here (see `requirements.txt` file). Another README file for React is available at `frontend/README.md`.
4. The frontend is accessible through `localhost:3000`
5. The backend is accessible through `localhost:8000` and endpoints can be tested on `localhost:8000/docs`

## Usage of the App
When the user accesses the React frontend at `localhost:3000`, they will need to **register** then use those credentials to **login**.
Once logged in, they are redirected to the **Jobs List** page which is initially empty. Then, they can click on the **Add Job** button and fill the form with the option to upload a CV/Resume/Cover letter if they want to. Once saved, the new job appears in the **Jobs List** page and in the database. The user can also create a new reminder using the **Add Reminder** page with a descriptive subject line and the time and date they wish to receive the email notification. Other functionalities include editing and deleting jobs and reminders.

### Other Notes
* Local development done on Macbook Pro M1 and my environment uses python 3.13. 
* Technologies and tools Used:
    * pgAdmin 4
    * Swagger/Postman/cURL
    * Docker
    * SendGrid and AWS S3 Dashboards