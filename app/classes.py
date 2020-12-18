import smtplib
from smtplib import ssl
from flask import current_app
from datetime import datetime as dt
from werkzeug.utils import secure_filename
from random import choice
import string
import os

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

class Utilities():
    ''' class full of static methods'''
    def post_timestamp():
        return dt.now().strftime("%d %B, %Y")

class Uploads():
    ''' Class to save uploads to server '''

    def __init__(self, uploaded_file, folder):
        ''' Pass through request.files & folder to save to '''
        self.uploaded_file = uploaded_file
        self.folder = folder
        
    @staticmethod
    def generate_file_id(Length=56):
        ''' rename file before saving to server '''
        generate = string.ascii_letters + string.ascii_uppercase + string.digits
        return ''.join(choice(generate) for i in range(Length))

    @staticmethod
    def check_supported_file(filename):
        ''' Check uploaded file is of supported type'''
        supported_files = ('.jpg', '.jpeg', '.png')
        return str(filename).endswith(supported_files)

    def save_upload(self):
        if not self.check_supported_file(self.uploaded_file.filename):
            return False
        
        if secure_filename(self.uploaded_file.filename) == '':
            ''' Fail safe -> Incase user tries to upload a file, and the file doesn't get submitted correctly '''
            return 'defaultPI.png'

        file_id = self.generate_file_id()
        filename = secure_filename(self.uploaded_file.filename)
        
        final_file_name = file_id + '.' + filename.split(".")[-1]
        self.uploaded_file.save(os.path.join(self.folder, final_file_name))

        return final_file_name

    def remove_upload(self, upload):
        ''' Call method once user deletes photo/product -> this will then delete it from the server '''
        os.remove(os.path.join(self.folder, upload))