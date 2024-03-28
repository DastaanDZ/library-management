import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import os

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

send_email("21f2001529@ds.study.iitm.ac.in","nigaver985@ikumaru.com","Test subject","This is a test message")
