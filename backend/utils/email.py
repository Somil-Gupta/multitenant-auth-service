import os
from dotenv import load_dotenv
import sib_api_v3_sdk # type: ignore
from sib_api_v3_sdk.rest import ApiException # type: ignore

# Load environment variables
load_dotenv()


# Brevo configuration
configuration = sib_api_v3_sdk.Configuration()
configuration.api_key['api-key'] = os.getenv("BREVO_API_KEY")

# Initialize the Brevo API client
api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))

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

def send_signup_invite_email(email: str):
    signup_link = "https://yourapp.com/invite?token=generated_token"
    content = f"""
    <h1>Welcome to Multi Tenant App</h1>
    <p>Click <a href='{signup_link}'>here</a> to complete your signup.</p>
    """
    return send_email(subject="Verify your email to complete Signup", email_to=email, content=content)


def send_password_update_email(email: str):
    content = """
    <h1>Password Change Notification</h1>
    <p>Your password has been updated successfully. If this wasn't you, please contact support immediately.</p>
    """
    return send_email(subject="Password Update Alert", email_to=email, content=content)

def send_login_alert_email(email: str):
    content = """
    <h1>New Login Alert</h1>
    <p>A new login to your account was detected. If this was not you, please secure your account.</p>
    """
    return send_email(subject="Login Alert", email_to=email, content=content)
