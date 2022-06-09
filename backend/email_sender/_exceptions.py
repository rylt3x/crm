class SMTPConnectException(Exception):
    def __init__(self, smtp_service_name:str, message):
        self.service_name = smtp_service_name
        self.message = message
        super(SMTPConnectException, self).__init__(self.message)

    def __str__(self):
        return f'{self.service_name} not allowed.'


class SMTPAuthError(Exception):
    pass


class SendMailError(Exception):
    pass