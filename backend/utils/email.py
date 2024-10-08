import os
from dotenv import load_dotenv
import sib_api_v3_sdk # type: ignore
from sib_api_v3_sdk.rest import ApiException # type: ignore
from domain.auth_service import AuthService
from infra.db.database import get_db
from infra.db.models import MailQueue
from celery.exceptions import MaxRetriesExceededError

import redis
from celery import Celery


celery = Celery(
    "tasks",
    broker="redis://127.0.0.1:6379/0",
    backend="redis://127.0.0.1:6379/0"
)

# Load environment variables
load_dotenv()

# Brevo configuration
configuration = sib_api_v3_sdk.Configuration()
configuration.api_key['api-key'] = os.getenv("BREVO_API_KEY")

# Initialize the Brevo API client
api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))

def get_fresh_db_session():
    return next(get_db())

@celery.task(bind=True, max_retries=3, default_retry_delay=60)  # max_retries limits to 3 retries, retry every 60 seconds
def process_email(self, email_to: str, subject: str, content: str):
    db = get_fresh_db_session()
    try:
        send_email(subject=subject, email_to=email_to, content=content)
        mail_entry = db.query(MailQueue).filter(MailQueue.message_id == email_to).first()
        if mail_entry:
            mail_entry.status = "sent"
            db.commit()
    except Exception as exc:
        # On failure, retry the task
        try:
            mail_entry = db.query(MailQueue).filter(MailQueue.message_id == email_to).first()
            if mail_entry:
                mail_entry.status = "failed"
                db.commit()
            # Retry the task
            raise self.retry(exc=exc)
        except MaxRetriesExceededError:
            # Handle case where retries are exhausted
            mail_entry.status = "failed"
            db.commit()
    finally:
        db.close()


def queue_email(subject: str, email_to: str, content: str, user_id: int):
    db = get_fresh_db_session()
    try:
        mail_entry = MailQueue(message_id=email_to, status="queued", user_id=user_id)
        db.add(mail_entry)
        db.commit()
        db.refresh(mail_entry)
        process_email.delay(subject=subject, email_to=email_to, content=content)
    finally:
        db.close()

# Helper function to send emails
def send_email(subject: str, email_to: str, content: str):
    email_data = sib_api_v3_sdk.SendSmtpEmail(
        to=[{"email": email_to}],
        sender={"email": "somil2760@gmail.com", "name": "Multitenant Auth Service"},
        subject=subject,
        html_content=content
    )
    try:
        api_instance.send_transac_email(email_data)
        return {"message": "Email sent successfully!"}
    except ApiException as e:
        return {"error": f"Exception when sending email: {e}"}


def send_signup_invite_email(email: str, password: str | None = None):
    db = get_fresh_db_session()
    try:
        user = db.query(MailQueue).filter(MailQueue.message_id == email).first()
        if not user:
            return {"error": "User not found"}
        
        generated_token = AuthService(db).create_refresh_token({"sub": email})
        signup_link = f"http://localhost:8020/invite-verify?token={generated_token}"
        content = f"""
        <h1>Welcome to Multi Tenant App</h1>
        <p>Click <a href='{signup_link}'>here</a> to complete your signup.</p>
        """
        if password is not None:
            content += f"""
            <p>Your autogenerated password is {password}. Please change it for better security</p>
        """
        queue_email(subject="Verify your email to complete Signup", email_to=email, content=content, user_id=user.id)
    finally:
        db.close()


def send_org_invite_email(email: str, organization: str):
    db = get_fresh_db_session()
    try:
        user = db.query(MailQueue).filter(MailQueue.message_id == email).first()
        if not user:
            return {"error": "User not found"}
        
        content = f"""
        <h1>Welcome to Multi Tenant App</h1>
        <p>You have been invited to organization {organization}.</p>
        <p>If it's your first time using Multitenant App, verify your email through the link received in a separate email.</p>
        """
        queue_email(subject="Organization Invitation", email_to=email, content=content, user_id=user.id)
    finally:
        db.close()


def send_password_update_email(email: str):
    db = get_fresh_db_session()
    try:
        user = db.query(MailQueue).filter(MailQueue.message_id == email).first()
        if not user:
            return {"error": "User not found"}
        
        content = """
        <h1>Password Change Notification</h1>
        <p>Your password has been updated successfully. If this wasn't you, please contact support immediately.</p>
        """
        queue_email(subject="Password Update Alert", email_to=email, content=content, user_id=user.id)
    finally:
        db.close()


def send_login_alert_email(email: str):
    db = get_fresh_db_session()
    try:
        user = db.query(MailQueue).filter(MailQueue.message_id == email).first()
        if not user:
            return {"error": "User not found"}
        
        content = """
        <h1>New Login Alert</h1>
        <p>A new login to your account was detected. If this was not you, please secure your account.</p>
        """
        queue_email(subject="Login Alert", email_to=email, content=content, user_id=user.id)
    finally:
        db.close()