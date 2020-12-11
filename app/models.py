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

    def custom_query(self, query, value):
        ''' custom user query. Pass through query, and value . example username:Ian '''
        return self.query.filter_by(**{query:value}).first()

    def login_attempt(self, username, password):
        query = self.custom_query('username', username)
        if (not query) or (query.password != self.hash_password(password)):
            return False
        return query

    def update_password_reset_code(self, email):
        query = self.custom_query('email', email)
        if not query:
            return False
        query.pw_reset = self.generate_password_reset()
        query.update()
        return query

    def check_pw_reset_code(self, pid):
        return self.custom_query('pw_reset', pid)

    def update_password(self, pid, password):
        query = self.custom_query('pw_reset', pid)
        query.password = self.hash_password(password)
        query.pw_reset = None
        query.update()

class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(100), nullable=False)

    def add_category(self):
        db.session.add(self)
        db.session.commit()
    
    def update_category(self):
        db.session.update(self)
        db.session.commit()
    
    def delete_category(self):
        query = self.query.filter_by(id=self.id).first()
        db.session.delete(query)
        db.session.commit()

    def custom_query(self, query, value):
        ''' custom user query. Pass through query, and value . example username:Ian '''
        return self.query.filter_by(**{query:value}).first()

    def fetch_all(self):
        return self.query.order_by(Category.id).all()

class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(5000), nullable=True)
    date_time = db.Column(db.String(300), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    category = db.Column(db.String(100), nullable=False)

    def add_post(self):
        db.session.add(self)
        db.session.commit()

    def update_post(self):
        db.session.update(self)
        db.session.commit()

    def delete_post(self):
        query = self.custom_query('id', self.id).first()
        db.session.delete(query)
        db.session.commit()

    def custom_query(self, query, value):
        ''' custom user query. Pass through query, and value . example username:Ian '''
        return self.query.filter_by(**{query:value}).first()

    def fetch_all(self):
        return self.query.order_by(Post.id).all()
