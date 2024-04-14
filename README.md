# Library Management System

## Introduction
This project is a comprehensive library management system designed to streamline the process of managing books, users, and book issuance. It provides features for administrators to monitor books, track availability, issue books to users, and revoke access if necessary.

## Installation

### Frontend
1. Navigate to the `frontend` directory.
2. Run `npm install` to install the required dependencies.
3. Run `npm run serve` to start the development server.

### Backend
1. Navigate to the `backend` directory.
2. Install the required Python packages using `pip install -r requirements.txt`.
3. Start the Celery server by following these steps:
   - Run `redis-server` (for WSL).
   - Run `celery -A tasks beat --loglevel=info` to start the Celery beat server.
   - Run `celery -A tasks beat --loglevel=info` to start the Celery worker.

## Usage
- Once both the frontend and backend servers are running, you can access the library management system through your web browser.
- Use the provided functionalities to monitor books, issue books to users, edit book details, and more.
- For administrative tasks, make sure to log in with appropriate credentials.
