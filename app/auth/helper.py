from flask import Flask, jsonify
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from app import config
from app.models import db, User ,db_update



def send_password_reset_email(email, new_password):
    sender_email = config.sender_email 
    sender_password = config.sender_password 

    msg = MIMEText(f'Your new password is: {new_password}')
    msg['Subject'] = 'Password Reset'
    msg['From'] = sender_email
    msg['To'] = email

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, [email], msg.as_string())
        server.quit()
        return {'message': 'Password reset email sent successfully.'}
    except Exception as e:
        return {'error': 'Error sending password reset email', 'details': str(e)}



def is_email_exists(email):
    exists = User.query.filter_by(email=email).all()
    if not exists:
        return None
    return exists