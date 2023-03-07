from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import six
import base64

from config import settings


def send_email(to_email: str, name: str) -> None:
    import smtplib
    message = MIMEMultipart()
    message['Subject'] = 'Registration'
    message['From'] = settings.SMTP_EMAIL
    message['To'] = to_email
    html = f"""\
    <html>
      <body>
      <p>
      Hi {name} \n
      Your verify code 👇
      <h1><b>12362517</b></h1>
      </p>
    </html>
    """
    message.attach(MIMEText(html, 'html'))
    with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.login(settings.SMTP_EMAIL, settings.SMTP_PASSWORD)
        server.send_message(message)
    print('Send EMail Message')


def make_token(user):
    text = six.text_type(user.id) + user.password + six.text_type(user.updated_at) + settings.SECRET_KEY
    token = base64.b64encode(text.encode('utf-8'))
    print(token)
    return token


def check_token():
    is_valid = True

# is_status = False
# s = '15'.encode()
#
# r = base64.urlsafe_b64encode(s)
# print(r)
#
# print(base64.urlsafe_b64decode(r).decode())
