# task.py
from celery import Celery
from celery.schedules import crontab
from celery.signals import before_task_publish

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import os

import time
from datetime import datetime, timedelta
import requests

app = Celery('tasks', broker='redis://127.0.0.1:6379')
app.conf.enable_utc = False
app.conf.timezone = 'Asia/Kolkata'

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(hour=17, minute=29),  # Run in the evening every day
        send_reminders.s()
    )
    # sender.add_periodic_task(
    #     crontab(day_of_month=1, hour=0, minute=0),  # Run on the first day of each month
    #     generate_and_send_monthly_report.s()
    # )
    sender.add_periodic_task(
        crontab(hour=17, minute=31),  # Run on the first day of each month
        generate_and_send_monthly_report.s()
    )

@app.task
def send_reminders():
    inactive_users = get_inactive_users()
    print("INACTIVE USER:")
    print(inactive_users)
    for user_id in inactive_users:
        print("SENDING REMINDER FOR USER ID:", user_id['id'])
        send_reminder.delay(user_id['id'])

def get_inactive_users():
    endpoint_url = 'http://127.0.0.1:5000/inactive-users'
    try:
        response = requests.get(endpoint_url)
        if response.status_code == 200:
            return response.json().get('inactive_users', [])
        else:
            print(f"Failed to fetch inactive users. Status code: {response.status_code}")
            return []
    except Exception as e:
        print(f"An error occurred while fetching inactive users: {e}")
        return []

@app.task
def send_reminder(user_id):
    url = f"http://127.0.0.1:5000/user-info/{user_id}"
    print("USER_ID", user_id)
    try:
        response = requests.get(url)
        print("RESPONSE",response)
        if response.status_code == 200:
            user = response.json()
            send_email.delay(
                sender="21f2001529@ds.study.iitm.ac.in",
                receiver=user['email'],
                subject="Please visit",
                message=f"Hello {user['username']}, please visit our app to stay updated!"
            )
        elif response.status_code == 404:
            print(f"User with ID {user_id} not found.")
        else:
            print("Error occurred:", response.text)
    except requests.exceptions.RequestException as e:
        print("Error occurred during request:", e)

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
        server.login(smtp_username, smtp_password)
        server.sendmail(sender, receiver, msg.as_string())

@app.task
def generate_and_send_monthly_report():
    month = datetime.now().strftime('%B %Y')  # Get the current month and year

# Fetch all users from the endpoint
    users_endpoint = 'http://127.0.0.1:5000/all-users'  # Update with your actual endpoint URL

    try:
        response = requests.get(users_endpoint)
        if response.status_code == 200:
            users_data = response.json().get('users', [])
        else:
            print("Failed to fetch users. Status code:", response.status_code)
            return
    except Exception as e:
        print("An error occurred while fetching users:", e)
        return

    sender_email = "21f2001529@ds.study.iitm.ac.in"

    for user in users_data:
        # Send the report via email
        recipient_email = user['email']
        subject = f"Monthly Activity Report - {month}"
        report_content = generate_monthly_report(month,user['id'])
        send_email.delay(sender_email, recipient_email, subject, report_content)

def generate_monthly_report(month,user_id):
    start_date = datetime.strptime(month, '%B %Y')
    end_date = start_date.replace(day=1, month=start_date.month % 12 + 1)

    url = f"http://127.0.0.1:5000/reports/{user_id}"
    data = {
        "start_date": start_date.strftime('%Y-%m-%d'),
        "end_date": end_date.strftime('%Y-%m-%d')
    }

    try:
        response = requests.post(url, json=data)
        if response.status_code == 200:
            report_data = response.json()
            issued_books = report_data.get('issued_books', [])
            feedbacks = report_data.get('feedbacks', [])
        else:
            print("Error occurred:", response.text)
            issued_books = []
            feedbacks = []
    except requests.exceptions.RequestException as e:
        print("Error occurred during request:", e)
        issued_books = []
        feedbacks = []

    # Format the data into HTML
    report_content = f"<html><body><h1>Monthly Activity Report - {month}</h1>"
    
    # Section for issued books
    report_content += "<h2>Issued Books</h2>"
    if issued_books:
        report_content += "<ul>"
        for issued_book in issued_books:
            report_content += f"<li>{issued_book['book_name']} - {issued_book['username']} ({issued_book['issue_date']})</li>"
        report_content += "</ul>"
    else:
        report_content += "<p>No books were issued this month.</p>"
    
    # Section for feedbacks received
    report_content += "<h2>Feedbacks Received</h2>"
    if feedbacks:
        report_content += "<ul>"
        for feedback in feedbacks:
            report_content += f"<li>{feedback['feedback_text']} - {feedback['username']} ({feedback['created_at']})</li>"
        report_content += "</ul>"
    else:
        report_content += "<p>No feedbacks were received this month.</p>"
    
    report_content += "</body></html>"

    return report_content
