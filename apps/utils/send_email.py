import base64
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from apps import models
from apps.utils.token import make_token
from config import settings


def __send_email_message(msg):
    with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.login(settings.SMTP_EMAIL, settings.SMTP_PASSWORD)
        server.send_message(msg)


def encode_data(pk):
    return base64.urlsafe_b64encode(str(pk).encode('utf-8'))


def decode_data(uid):
    return base64.urlsafe_b64decode(uid).decode('utf-8')


def send_verification_email(user: models.Users, host) -> None:
    token = make_token(user)
    uid = encode_data(user.id).decode('utf-8')

    message = MIMEMultipart()
    message['Subject'] = 'Activation link'
    message['From'] = settings.SMTP_EMAIL
    message['To'] = user.email
    html = f"""\
    <html>
      <body>
      <p>
      Hi {user.name} \n
      Activate your account 👇
      <h1><b>{host}{uid}/{token}</b></h1>
      </p>
    </html>
    """
    message.attach(MIMEText(html, 'html'))
    __send_email_message(message)
