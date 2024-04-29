# Access Control System

## Overview
The Access Control System is a web application designed to manage access keys for users. It allows users to sign up, sign in, generate access keys, and manage their access key status.

## Features
- **User Authentication:** Users can sign up and sign in to the system securely.
- **Access Key Generation:** Upon signing in, users can generate access keys if they don't have one already.
- **Access Key Management:** Users can view details of their access keys, including creation date, expiration date, and status.
- **Revocable Access Keys:** Access keys can be revoked by the user or the administrator.
- **Email Activation:** Upon signing up, users receive an email with an activation link to verify their email address.
- **Password Reset:** Users can reset their passwords if they forget them.

## Technologies Used
- **Django:** Python-based web framework used for backend development.
- **HTML/CSS:** Frontend design and layout.
- **JavaScript:** Client-side scripting for interactive features.
- **SQLite:** Database management system used for storing user data.
- **Django Templating Language:** Used for dynamic content rendering in HTML templates.

## Setup Instructions
1. Clone the repository to your local machine.
2. Install Python (if not already installed).
3. Install Django using pip: `pip install django`.
4. Navigate to the project directory in your terminal.
5. Run the following command to start the development server: `python manage.py runserver`.
6. Access the application in your web browser at `http://localhost:8000`.

## Usage
1. Sign up for a new account if you don't have one already.
2. Sign in using your credentials.
3. Generate your access key if you don't have one.
4. Manage your access key status as needed.
5. Sign out when done.

## Contributors
- mr-kwansa [https://github.com/mr-kwansa]