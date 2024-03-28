# task.py
from celery import Celery
from celery.schedules import crontab

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import os

import time
from app.models import User, Book, Request, Feedback, Section, IssuedBook
from datetime import datetime, timedelta

app = Celery('tasks', broker='redis://127.0.0.1:6379')
app.conf.enable_utc = False
app.conf.timezone = 'Asia/Kolkata'

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(hour=3, minute=39),
        send_email.s("21f2001529@ds.study.iitm.ac.in","nigaver985@ikumaru.com","Celery","This is a test message")
    )

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(hour=18, minute=0),  # Run in the evening every day
        send_reminders.s()
    )
    sender.add_periodic_task(
        crontab(day_of_month=1, hour=0, minute=0),
        generate_and_send_monthly_report.s()
    )

@app.task
def send_reminders():
    inactive_users = get_inactive_users()
    for user in inactive_users:
        send_reminder.delay(user.id)

def get_inactive_users():
    # Define the timeframe for considering a user as inactive (e.g., 24 hours)
    inactive_threshold = datetime.utcnow() - timedelta(hours=24)

    # Query the database to retrieve users who haven't visited the app within the specified timeframe
    inactive_users = User.query.filter(User.last_login < inactive_threshold).all()

    return inactive_users


@app.task
def send_reminder(user_id):
    user = User.query.get(user_id)
    sender = ""
    if user:
        receiver = user.email
        msg = MIMEMultipart()
        msg['From'] = sender
        msg['To'] = receiver
        msg['Subject'] = "Please visit"
        message = f"Hello {user.username}, please visit our app to stay updated!"
        msg.attach(MIMEText(message))

        smtp_server = 'smtp.gmail.com'
        smtp_port = 587
        smtp_username = sender
        smtp_password = 'iyupnovgffmpjjmc'

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username,smtp_password)
            server.sendmail(sender,receiver,msg.as_string())
            

@app.task
def send_email(sender, receiver, subject, message):
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = receiver
    msg['Subject'] = subject
    msg.attach(MIMEText(message))

    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_username = sender
    smtp_password = 'iyupnovgffmpjjmc'

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username,smtp_password)
        server.sendmail(sender,receiver,msg.as_string())

@app.task
def generate_and_send_monthly_report():
    # Generate the monthly report
    month = datetime.now().strftime('%B %Y')  # Get the current month and year
    report_content = generate_monthly_report(month)
    
    # Send the report via email
    sender_email = "your_email@example.com"
    recipient_email = "recipient@example.com"
    subject = f"Monthly Activity Report - {month}"
    send_email(sender_email, recipient_email, subject, report_content)

def generate_monthly_report(month):
    # Fetch data from the database for the specified month
    start_date = datetime.strptime(month, '%B %Y')
    end_date = start_date.replace(day=1, month=start_date.month % 12 + 1)
    issued_books = IssuedBook.query.filter(IssuedBook.issue_date >= start_date, IssuedBook.issue_date < end_date).all()
    feedbacks = Feedback.query.filter(Feedback.created_at >= start_date, Feedback.created_at < end_date).all()

    # Format the data into HTML
    report_content = f"<html><body><h1>Monthly Activity Report - {month}</h1>"
    
    # Section for issued books
    report_content += "<h2>Issued Books</h2>"
    if issued_books:
        report_content += "<ul>"
        for issued_book in issued_books:
            report_content += f"<li>{issued_book.book.name} - {issued_book.user.username} ({issued_book.issue_date.strftime('%Y-%m-%d')})</li>"
        report_content += "</ul>"
    else:
        report_content += "<p>No books were issued this month.</p>"
    
    # Section for feedbacks received
    report_content += "<h2>Feedbacks Received</h2>"
    if feedbacks:
        report_content += "<ul>"
        for feedback in feedbacks:
            report_content += f"<li>{feedback.feedback_text} - {feedback.user.username} ({feedback.created_at.strftime('%Y-%m-%d')})</li>"
        report_content += "</ul>"
    else:
        report_content += "<p>No feedbacks were received this month.</p>"
    
    report_content += "</body></html>"

    return report_content