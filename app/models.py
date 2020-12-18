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
    description = db.Column(db.String(300), nullable=True)
    category_name = db.Column(db.String(100), nullable=False)
    slug = db.Column(db.String(300), nullable=False)
    count = db.Column(db.Integer, nullable=True, default='0')

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
    content = db.Column(db.TEXT(5000), nullable=True)
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
        query = self.custom_query('id', self.id)
        if not query:
            return False
        db.session.delete(query)
        db.session.commit()
        return True

    def custom_query(self, query, value):
        ''' custom user query. Pass through query, and value . example username:Ian '''
        return self.query.filter_by(**{query:value}).first()

    def fetch_all(self):
        return self.query.order_by(Post.id).all()

class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    book_title = db.Column(db.String(400), nullable=False)
    book_price = db.Column(db.String(100), nullable=True)
    book_category = db.Column(db.String(300), nullable=True)
    book_description = db.Column(db.String(3000), nullable=True)
    ## Change book cat once categories have been created
    slug = db.Column(db.String(200), nullable=False)
    referral_link = db.Column(db.String(500), nullable=False)
    images = db.relationship('Image', backref='book')

    def add_book(self):
        db.session.add(self)
        db.session.commit()
        return self.id

    def delete_book(self):
        db.session.delete(self)
        db.session.commit()
        
    def update_book(self):
       db.session.commit(self)
        
    def custom_query(self, query, value):
        ''' custom user query. Pass through query, and value . example username:Ian '''
        return self.query.filter_by(**{query:value}).first()

class Image(db.Model):
    __tablename__ = 'images'
    id = db.Column(db.Integer, primary_key=True)
    img = db.Column(db.String(300), nullable=False)
    img_old_name = db.Column(db.String(300), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)

    def custom_query(self, query, value):
        ''' custom user query. Pass through query, and value . example username:Ian '''
        return self.query.filter_by(**{query:value}).first()

    def add_image(self):
        db.session.add(self)
        db.session.commit()

    def delete_image(self):
        query = self.query.filter_by(id=self.id)
        db.session.delete(query)
        db.session.commit()