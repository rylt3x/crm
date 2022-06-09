from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from importlib import reload
import smtplib
from project import settings

from email_sender.mailer import Mailer


def send_mail(msg_text: str, subj: str, receiver: str):
    mailer = Mailer(SMTP_LOGIN=settings.EMAIL_LOGIN, SMTP_PASS=settings.EMAIL_PASSWORD, SMTP_SERVICE='yandex')
    mailer.send_message([receiver], subj, msg_text)
