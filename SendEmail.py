#!/usr/bin/python
# -*- coding: utf-8 -*-

import smtplib


class SendEmail:
    def __init__(self, smtp_server, smtp_port, login, password):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.login = login
        self.password = password

    def send(self, to, subject, body):

        body = "" + body + ""

        headers = ["From: " + self.login,
                   "Subject: " + subject,
                   "To: " + to,
                   "MIME-Version: 1.0",
                   "Content-Type: text/html"]
        headers = "\r\n".join(headers)

        try:
            session = smtplib.SMTP(self.smtp_server, self.smtp_port)

            session.ehlo()
            session.starttls()
            session.ehlo
            session.login(self.login, self.password)

            session.sendmail(self.login, to, headers + "\r\n\r\n" + body)

        except:
            raise EnvironmentError('Unable to send email. Please, check your '
                                   'configuration!')

        session.quit()
