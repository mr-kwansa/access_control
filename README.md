# Access Control System

## Overview
The Access Control System is a web application designed to manage access keys for users. It allows users to sign up, sign in, generate access keys, and see their access key status.

## Features
- **User Authentication:** Users can sign up and sign in to the system securely.
- **Access Key Generation:** Upon signing in, users can generate access keys if they don't have one already.
- **Access Key Management:** Users can view details of their access keys, including creation date, expiration date, and status.
- **Revocable Access Keys:** Access keys can be revoked by an  administrator.
- **Email Activation:** Upon signing up, users receive an email with an activation link to verify their email address.
- **Password Reset:** Users can reset their passwords if they forget them.

## Technologies Used
- **Django:** Python-based web framework used for backend development.
- **HTML/CSS:** Frontend design and layout.
- **JavaScript:** Client-side scripting for interactive features.
- **PostgreSQL:** Database management system used for storing user data.
- **Django Templating Language:** Used for dynamic content rendering in HTML templates.

## Setup Instructions
1. Clone the repository to your local machine.
    'git clone https://github.com/your-username/access-control-system.git'

2. Install Python (if not already installed).
    'https://www.python.org/downloads/'

3. Install Django using pip: 
    `pip install django`.

4. Navigate to the project directory in your terminal.

5. Create a virtual environment by running the following 
    'python -m venv env'.

6. Activate the environmentby running the following
    'source env/bin/activate' (Macos/Liniux users)
    'env\Scripts\activate'  (Windows)

7. Run the command bellow to install any dependencies listed in the file.
    'pip install -r requirements.txt'

8. Run the following command to start the development server: 
    `python manage.py runserver`.

9. Open a web browser and go to  to view the application.
    `http://localhost:8000/`

## Usage
1. Sign up for a new account if you don't have one already.
2. Sign in using your credentials.
3. Generate your access key if you don't have one.
4. Manage your access key status as needed.
5. Sign out when done.
##
## Admin user account
-Username : admin

-Password : sysadmin@1
## Usage for Micro Focus Admin
1. Sign up for a new account if you don't have one already.
2. Sign in using your credentials.
3. You will need the super user to make yout account a staff member
4. Then you head over to the micro_focus admin panel 'micro_focus_admin/'
5. Sign out when done.

## Steps for accessing the endpoint (api) to integrate into other systems
1. Run the server and head over to 'api/micro_focus_admin/'
2. It would a json respons which you can then latter use 

## Contributors
- mr-kwansa [https://github.com/mr-kwansa]

## You can find a live version of this project at:
-[https://access-control-3rwo.onrender.com]


## Endpoints for Micro Focus Admin
-[https://access-control-3rwo.onrender.com/api/micro_focus_admin/]

-[http://127.0.0.1:8000/api/micro_focus_admin/]


## Endpoints for Micro Focus Admin with search
This can be accessed via a link in the micro focus admin page
-[http://localhost:8000/school_integration_endpoint/]


## DEBUGING

In the event of the following error....."ValueError: No support for 'b'''. We support: cockroach, mssql, mssqlms, mysql, mysql-connector, mysql2, mysqlgis, oracle, oraclegis, pgsql, postgis, postgres, postgresql, redshift, spatialite, sqlite, timescale, timescalegis"

run this comand "export DATABASE_URL=db_url"
find the db_url in the .env file


