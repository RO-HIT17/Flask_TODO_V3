# To-Do List Manager

## Overview
This is a simple To-Do List Manager web application built using Flask. The application allows users to register, log in, manage their tasks, and view their task completion statistics. The app uses SQLite for data storage and SQLAlchemy as the ORM.

## Features
- **User Registration**: New users can register by providing their name, email, and password.
- **User Login**: Registered users can log in to access their personalized dashboard.
- **Task Management**: Users can add, complete, and clear tasks in their to-do list.
- **Dashboard**: Users can view the total number of tasks, completed tasks, and the completion rate.
- **Password Reset**: Users can reset their password if they forget it.
- **Task History**: Users can view their task completion history.

## Project Structure
├── app.py                  # The main application file with Flask routes
├── models.py               # The file defining the database models (User and Todo)
├── templates/              # Folder containing HTML templates
│   ├── base.html           # Base HTML template
│   ├── login.html          # Login page
│   ├── register.html       # User registration page
│   ├── forgot_password.html # Password reset page
│   ├── dashboard.html      # User dashboard
│   ├── index.html          # To-do list page
├── static/                 # Folder containing static files (CSS, JS)
│   ├── login.css           # Stylesheet for login page
│   ├── dashboard.css       # Stylesheet for dashboard page
│   ├── index.css           # Stylesheet for to-do list page
└── README.md               # This README file

## Installation

### Prerequisites
- Python 3.x
- Flask
- SQLAlchemy

### Steps
1. Clone the repository:
   git clone https://github.com/yourusername/todo-list-manager.git
   cd todo-list-manager

2. Create a virtual environment and activate it:
   python3 -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate

3. Install the dependencies:
   pip install -r requirements.txt

4. Set up the SQLite database:
   flask shell
   >>> from models import db
   >>> db.create_all()
   >>> exit()

5. Run the application:
   flask run

6. Access the application in your web browser at `http://127.0.0.1:5000/`.

## Usage

### Register
1. Navigate to the registration page.
2. Fill in your details (First Name, Last Name, Email, Password).
3. Submit the form to create a new account.

### Login
1. Go to the login page.
2. Enter your registered email and password.
3. Upon successful login, you will be redirected to your dashboard.

### Task Management
- **Add a Task**: Enter the task title in the input box and click "Add".
- **Complete a Task**: Click on the task to mark it as completed.
- **Clear Completed Tasks**: Click the "Clear Completed" button to remove all completed tasks from the list.

### Dashboard
- View statistics such as the total tasks, completed tasks, and your completion rate.

### Password Reset
- If you forget your password, click on "Forgot Password?" on the login page to reset it.

## Contributing
Contributions are welcome! Please submit a pull request or open an issue to suggest improvements.
