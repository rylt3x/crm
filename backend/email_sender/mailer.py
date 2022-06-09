from . import _exceptions
from . import _utils

from datetime import datetime

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib


class Mailer:
    def __init__(self, **kwargs):
        service_name = kwargs.get('SMTP_SERVICE')
        login = kwargs.get('SMTP_LOGIN')
        app_password = kwargs.get('SMTP_PASS')

        if service_name not in _utils.get_smtp_names():
            raise _exceptions.SMTPConnectException(service_name, f'{service_name} not in {_utils.get_smtp_names()}')
        if not login:
            raise _exceptions.SMTPAuthError('Login must be provided')
        if not app_password:
            raise _exceptions.SMTPAuthError('Application password must be provided')
        if type(login) is not str:
            raise TypeError(f'SMTP_LOGIN must be {str} type')
        if type(app_password) is not str:
            raise TypeError(f'SMTP_PASS must be {str} type')

        for attr_key, attr_value in kwargs.items():
            setattr(self, attr_key, attr_value)

    def _smtp_connect(self):
        smtp_server, smtp_port = self._get_smtp_server()
        self.server = smtplib.SMTP(smtp_server, smtp_port)
        self.server.starttls()
        print(f'[{datetime.now()}] connected to {smtp_server}:{smtp_port}')
        return 'connected'

    def _smtp_auth(self):
        self.server.login(self.SMTP_LOGIN, self.SMTP_PASS)
        print(f'[{datetime.now()}] logged in')
        return 'logged in'

    def _get_smtp_server(self):
        smtp_services = _utils.get_smtp_services()
        smtp_data = smtp_services.get(self.SMTP_SERVICE)
        return tuple(smtp_data.values())

    def _smtp_disconnect(self):
        self.server.quit()
        print(f'[{datetime.now()}] disconnected')

    def _build_message(self, subject: str, mail_text: str):
        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg['From'] = self.SMTP_LOGIN
        body = MIMEMultipart('alternative')
        body.attach(MIMEText(mail_text, 'html'))
        msg.attach(body)
        return msg

    def send_message(self, receivers: list, subject: str = 'Без темы', mail_text: str = ''):
        self._smtp_connect()
        self._smtp_auth()
        if not receivers:
            raise _exceptions.SendMailError('Provide receiver parameter')
        message = self._build_message(subject, mail_text)
        self.server.sendmail(self.SMTP_LOGIN, receivers, message.as_string())
        self._smtp_disconnect()
        print(f'Message with subject {subject} sent to {", ".join(receivers)}')
        return 'message sent'
