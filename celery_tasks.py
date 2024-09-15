from celery import Celery
from flask_mail import Message
from app import app, mail  # Import app and mail from your main app.py

# If not already done, create a Celery instance using the make_celery function
celery = Celery(
    app.import_name,
    backend=app.config['CELERY_RESULT_BACKEND'],
    broker=app.config['CELERY_BROKER_URL']
)
celery.conf.update(app.config)

@celery.task
def send_due_date_reminder(email, task_name, due_date):
    """Send an email reminder about the due date."""
    with app.app_context():
        msg = Message('Task Due Reminder', sender='your-email@example.com', recipients=[email])
        msg.body = f'Reminder: Your task {task_name} is due on {due_date}.'
        mail.send(msg)
