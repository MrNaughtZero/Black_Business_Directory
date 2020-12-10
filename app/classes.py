import smtplib
from smtplib import ssl
from flask import current_app

class Emails():
    ''' Class for sending emails. User Registration, New Business, Forgotten Password, Unauthorised Admin Attempts, Account Lockout '''
    def __init__(self, email_to):
        self.email_to = email_to

    def smtp_information(send_to, message_content):
        try:
            server_ssl = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            smtp_user = current_app.config['SMTP_USER']
            smtp_pass = current_app.config['SMTP_PASS']
            server_ssl.login(smtp_user, smtp_pass)
            server_ssl.sendmail(smtp_user, send_to, message_content)
            server_ssl.close()
        except Exception as e:
            with open('logging/email-log.txt', 'a') as email_log:
                email_log.write(f'{e}\n')
            return False

    def admin_registration(self):
        send_to = self.email
        subject = 'Mahali - Admin Registered'
        body = 'New Admin Registration. Please use http://127.0.0.1:5000/auth/login to login.'
        message_content = f'subject: {subject}\n\n{body}'
        
        emailInformation(send_to, message_content)
