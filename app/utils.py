from .config import settings
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def hash(password):
    return pwd_context.hash(password)


def verify(plain_password, hash_password):
    return pwd_context.verify(plain_password, hash_password)


smtp_server = settings.smtp_server
smtp_port = settings.smtp_port
smtp_username = settings.smtp_username
smtp_password = settings.smtp_password

sender_email = settings.sender_email


def send_verification_email(user_email, verification_link, subject):

    subject = subject

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = user_email
    msg['Subject'] = subject

    html = f"""
    <html>
        <body>
            <p>Hello, please click the following link to {subject}:</p>
            <div>
            <a style="background-color: blue; color: white; text-decoration: none; padding: 10px 5px; display: inline-block"   href="{verification_link}">{subject}</a>
            </div>
        </body>
    </html>
    """
    msg.attach(MIMEText(html, 'html'))

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.sendmail(sender_email, user_email, msg.as_string())
            print("Email Sent Successfully")
    except Exception as e:
        print(f"Email sending failed:  {str(e)}")


def send_confirmation_email(user_email, link, subject):
    subject = subject
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = user_email
    msg['Subject'] = subject

    html = f"""
    <html>
        <body>
            <p>{subject}</p>
            <div >
               <a style="background-color: blue; color: white; text-decoration: none; padding: 10px 5px; display: inline-block" href="{link}">Login</a>
            </div>
        </body>
    </html>
    """
    msg.attach(MIMEText(html, 'html'))

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.sendmail(sender_email, user_email, msg.as_string())
            print("Email Sent Successfully")
    except Exception as e:
        print(f"Email sending failed:  {str(e)}")
