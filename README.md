
# Interview Manager API

## Overview

The **Interview Manager API** is a Django-based web service that allows for the management of interview scheduling, including user registration, login, and retrieving interview data by various criteria such as date, week, or month.

## Features

- User Registration and Login using JWT authentication.
- Schedule interviews with details like interviewee, date, time, role, and department.
- Retrieve all scheduled interviews or filter by date, week, work week (excluding weekends), or month.

## Technologies

- **Django**: The web framework used for building the application.
- **Django REST Framework**: For building the REST APIs.
- **PostgreSQL**: The database used to store user and interview data.
- **JWT Authentication**: Secure user authentication using JSON Web Tokens.

## Requirements

- Python 3.10+
- Django 4.x
- PostgreSQL
- Django REST Framework
- Django Simple JWT

## Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/your-repository/interview-manager.git
    ```

2. **Navigate to the project directory**:
    ```bash
    cd interview-manager
    ```

3. **Create a virtual environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

4. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

5. **Setup PostgreSQL Database**:
    - Make sure PostgreSQL is installed and running.
    - Create a database for the project.
    - Update `.env` to include your PostgreSQL database settings:
        ```
        DATABASE_NAME=your_database_name
        DATABASE_USER=your_database_user
        DATABASE_PASSWORD=your_password
        DATABASE_HOST=localhost
        DATABASE_PORT=5432
        ```

6. **Configure JWT in `.env`**:
    Add the following environment variables to the `.env` file for JWT configuration:
    ```
    SECRET_KEY=your_secret_key
    JWT_SECRET_KEY=your_jwt_secret_key
    JWT_ACCESS_TOKEN_LIFETIME=5  # in minutes
    JWT_REFRESH_TOKEN_LIFETIME=1  # in days
    ```

7. **Run Migrations**:
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

8. **Create a Superuser** (Optional but recommended):
    ```bash
    python manage.py createsuperuser
    ```

9. **Start the development server**:
    ```bash
    python manage.py runserver
    ```
