# Flask TODO Manager

A Flask-based TODO Manager application designed to manage tasks efficiently with user authentication, task management, email reminders, and more.

## Features

### User Registration and Authentication
- **User Registration**: Allows users to register with their personal details including name, email, phone number, and password.
- **Login/Logout**: Users can log in using their email and password. Once logged in, users can manage their tasks and perform other operations. Users can also log out.
- **Forgot Password**: Users can reset their passwords using a verification code sent to their registered email.

### Task Management
- **Create Tasks**: Users can add new tasks with a title, priority level, deadline, and optional file attachment.
- **Update Tasks**: Users can update existing tasks, including changing their title, priority, deadline, and file attachment.
- **Delete Tasks**: Users can remove tasks from their list.
- **Complete Tasks**: Users can mark tasks as completed. The completion date is recorded.

### Task Filtering and Sorting
- **Filter Tasks**: Users can filter tasks by priority (e.g., High, Medium, Low) to view only tasks that match the selected priority.
- **Sort Tasks**: Users can sort tasks by title, priority, or deadline in ascending or descending order to organize their task list.

### Email Reminders
- **Automatic Reminders**: The application sends automatic email reminders for tasks that are due soon (e.g., one day before the deadline). This feature helps users stay on top of their deadlines.

### Rankings
- **User Rankings**: Users can view a leaderboard showing rankings based on the number of completed tasks. This feature encourages users to stay productive and see how they compare with others.

### File Upload
- **Attach Files**: Users can upload files (e.g., PDFs, images) related to tasks. The files are stored in the server and can be accessed through task details.

## Folder Structure

```
Flask_TODO_Manager/
│
├── app.py
├── celery_tasks.py
├── models.py
├── requirements.txt
├── README.md
├── uploads/
│   └── (Uploaded files will be stored here)
│
├── templates/
│   ├── login.html
│   ├── register.html
│   ├── forgot_password.html
│   ├── dashboard.html
│   ├── index.html
│   ├── rankings.html
│   └── (Other HTML templates)
│
└── static/
    ├── css/
    │   └── (CSS files)
    └── js/
        └── (JavaScript files)
```

## Installation

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/your-repository/Flask_TODO_Manager.git
    cd Flask_TODO_Manager
    ```

2. **Set Up a Virtual Environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Configure Redis** (For Celery):
    - Ensure Redis is running on your local machine. Configure it to listen on port 6379 or 6380 as specified in `app.py`.

5. **Set Up the Database**:
    - SQLite is used for database management. The database file (`todos.db`) will be created automatically on the first run.

6. **Run the Application**:
    ```bash
    python app.py
    ```

## Usage

### Running the Application
- Start the Flask application using the command:
    ```bash
    python app.py
    ```
- Access the application in your web browser at [http://127.0.0.1:5000](http://127.0.0.1:5000).

### User Registration and Authentication
1. **Register**:
    - Navigate to the registration page and fill out the form with your details.
2. **Login**:
    - Use the login page to enter your email and password to access the application.
3. **Forgot Password**:
    - If you forget your password, you can request a verification code to reset it.

### Task Management
1. **Add a Task**:
    - On the dashboard, use the form to create a new task. You can specify the title, priority, deadline, and attach a file.
2. **Update a Task**:
    - Navigate to the task details page and update the task information as needed.
3. **Delete a Task**:
    - Use the delete option to remove a task from the list.
4. **Complete a Task**:
    - Mark tasks as completed, which will record the completion date.

### Task Filtering and Sorting
1. **Filter Tasks**:
    - Use the filter options to view tasks based on their priority.
2. **Sort Tasks**:
    - Use the sort options to organize tasks by title, priority, or deadline.

### Email Reminders
1. **Automatic Reminders**:
    - Reminders are sent automatically for tasks that are approaching their deadline. Ensure your email settings are correct for this feature to work.

### Rankings
1. **View Rankings**:
    - Check the rankings page to see a leaderboard based on the number of completed tasks.

### File Upload
1. **Upload Files**:
    - Attach files to your tasks by selecting them during task creation or update.

## Troubleshooting

- **Redis Connection Issues**:
    Ensure Redis is running and accessible at the configured URL (`redis://localhost:6379/0` or `redis://localhost:6380/0`).

- **Email Sending Issues**:
    Verify that your email configuration is correct and that the email server allows connections from your application.

- **Database Errors**:
    Ensure the SQLite database file (`todos.db`) is accessible and not corrupted.

## Acknowledgments

- Flask for the web framework.
- Celery for task scheduling.
- Redis for task management backend.
- SQLite for the database.
