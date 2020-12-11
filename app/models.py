from app.database import db
import hashlib
from hashlib import sha256
from random import choice
import string

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(100), nullable=False)
    login_attempts = db.Column(db.Integer, nullable=True)
    pw_reset = db.Column(db.String(500), nullable=True)
    
    def get_id(self):
        return self.id

    def get_role(self):
        return self.role
    
    def is_authenticated(self):
        return True

    def get_username(self):
        return self.username

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def create_user(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    @staticmethod
    def hash_password(password):
        return sha256(password.encode('utf-8')).hexdigest()

    @staticmethod
    def generate_password_reset(StringLength=200):
        generate = string.ascii_letters + string.ascii_lowercase + string.ascii_uppercase
        return ''.join(choice(generate) for i in range(StringLength))

    def check_for_admin(self):
        ''' check if admin exists. if so, return false '''
        return self.query.filter_by(role='admin').first()