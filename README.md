#Job Board Project

This is a Job Board project built using Django, a high-level Python web framework. The project provides a platform for employers to post job vacancies and for job seekers to search and apply for those vacancies.

---

##Entities

The Job Board project consists of the following entities:

1. User:
    - 'username': The username of the user.
    - 'email': The email address of the user.
    - 'password': The password of the user.
    - 'role': The role of the user (employer or job seeker).
    Additional profile information such as name, contact details, etc.
      
2. Job (Represents a job listing posted by an employer.):
    - title: The title of the job.
    - description: A description of the job.
    - location: The location of the job.
    - company: The company associated with the job.
    - salary: The salary offered for the job.
    - created_at: The date and time when the job was created.
    - owner: The user who posted the job (Foreign Key to User).

3. Application (Represents a job application submitted by a job seeker.):
    - job: The job to which the application is submitted (Foreign Key to Job).
    - applicant: The user who submitted the application (Foreign Key to User).
    - resume: The resume attached with the application.
    - cover_letter: The cover letter attached with the application.
    - status: The status of the application (e.g., applied, under review, accepted, rejected).
    - applied_at: The date and time when the application was submitted.

4. Skill (Represents a skill that can be associated with a job or a user.):
    - name: The name of the skill.
    - description: A description of the skill.
    - proficiency_level: The proficiency level of the skill.

5. Category (Represents a category or industry to classify jobs.):
    - name: The name of the category.
    - description: A description of the category.

6. Location (Represents a geographic location associated with a job.):
    - country: The country of the location.
    - state: The state or province of the location.
    - city: The city of the location.
    - address: The address of the location.

7. Company (Represents a company or employer.):
    - name: The name of the company.
    - description: A description of the company.
    - industry: The industry to which the company belongs.
    - website: The website URL of the company.
    - logo: The logo image of the company.
---

##Features

- User Registration and Authentication: Users can create an account, log in, and log out. Authentication is required for certain actions, such as posting job vacancies or applying for jobs.
- CRUD: employers can create, update, delete vacancies.
- Searching and filtering: seekers and employers can search and filter by needed criteria.

---

##Installation

1. Clone the repository:
```
git clone https://github.com/your-username/job-board-project.git
```
2. Navigate to the project directory:
```
cd job-board
```
3. Create and activate a virtual environment (optional but recommended):
```
python3 -m venv env
source env/bin/activate
```
4. Install the project dependencies:
```
pip install -r requirements.txt
```
5. Set up the database:
```
python manage.py migrate
```
6. Create a superuser (admin account) to access the admin interface:
```
python manage.py createsuperuser
```
7. Start the development server:
```
python manage.py runserver
```
8. Open your web browser and navigate to http://localhost:8000 to access the Job Board project.

